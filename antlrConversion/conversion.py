import sys
from antlr4 import *
from antlrConversion.ClassDiagramLexer import ClassDiagramLexer
from antlrConversion.ClassDiagramParser import ClassDiagramParser
import pandas as pd

def generate_xmi(parsed_data):
    xmi = """<?xml version="1.0" encoding="UTF-8"?>
<ecore:EPackage xmi:version="2.0" xmlns:xmi="http://www.omg.org/XMI" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    xmlns:ecore="http://www.eclipse.org/emf/2002/Ecore" name="ClassDiagram" nsURI="http://www.example.com/ClassDiagram"
    nsPrefix="ClassDiagram">\n"""

    enumerations, classes = parsed_data

    # Enumerations
    for enum in enumerations:
        xmi += f'  <eClassifiers xsi:type="ecore:EEnum" name="{enum[0]}">\n'
        for literal in enum[1]:
            xmi += f'    <eLiterals name="{literal}"/>\n'
        xmi += "  </eClassifiers>\n"

    # Classes and attributes
    for class_def in classes:
        class_name, attributes, is_abstract = class_def
        xmi += f'  <eClassifiers xsi:type="ecore:EClass" name="{class_name}"'
        if is_abstract:
            xmi += ' abstract="true">\n'
        else:
            xmi += '>\n'

        # Attributes as EStructuralFeatures
        for attr in attributes:
            print(attr)
            if attr[0] in ['composition', 'inheritance', 'association']:
                if attr[0]=='composition':
                    rel = attr[1]
                    mul = rel[0] if rel[0] !='(*)' else '(-1)'
                    containing = rel[1]
                    xmi += f'    <eStructuralFeatures xsi:type="ecore:EReference" name="{containing}" '
                    if len(mul) >=5:
                        lower, higher = mul.split('..')
                        higher = higher if higher !='*)' else '-1)'
                        xmi += f'eType="#//{containing}" containment="true" lowerBound="{lower[1:]}" upperBound="{higher[:-1]}"/>\n'
                    else:
                        print(mul[1:-1])
                        xmi += f'eType="#//{containing}" containment="true" upperBound="{mul[1:-1]}"/>\n'
                if attr[0]=='inheritance':
                    xmi += f'    <eSuperTypes href="#//{attr[1]}"/>\n'
                if attr[0]=='association':
                    rel = attr[1]
                    mul = rel[0] if rel[0] !='(*)' else '(-1)'
                    to = rel[1]
                    xmi += f'    <eStructuralFeatures xsi:type="ecore:EReference" name="{to}" '
                    if len(mul) >=5:
                        lower, higher = mul.split('..')
                        higher = higher if higher !='*)' else '-1)'
                        xmi += f'eType="#//{to}" containment="false" lowerBound="{lower[1:]}" upperBound="{higher[:-1]}"/>\n'
                    else:
                        xmi += f'eType="#//{to}" containment="false" upperBound="{mul[1:-1]}"/>\n'
                
            else:
                attr_type = attr[0] if attr[0] else "EString"  # Default to EString if type is missing
                attr_name = attr[1]
                is_const = attr[2]
                default_value = attr[3]
                
                # Correct handling of attribute naming and default values
                xmi += f'    <eStructuralFeatures xsi:type="ecore:EAttribute" name="{attr_name}" '
                if attr_type == "string" or attr_type== "int" or attr_type== "boolean":
                    xmi += f'eType="ecore:EDataType http://www.eclipse.org/emf/2002/Ecore#//E{attr_type.capitalize()}"'
                else:
                    xmi += f'eType="#//{attr_type.capitalize()}"'
                
                # Handle constants and default values
                if is_const:
                    xmi += ' changeable="false"'
                if default_value is not None:
                    xmi += f' defaultValueLiteral="{default_value}"'
                xmi += '/>\n'

        xmi += "  </eClassifiers>\n"

    xmi += "</ecore:EPackage>"
    return xmi


def conversion(input_ebnf):
    input_stream = InputStream(input_ebnf)
    lexer = ClassDiagramLexer(input_stream)
    token_stream = CommonTokenStream(lexer)
    parser = ClassDiagramParser(token_stream)

    tree = parser.classDiagram()  # Start parsing from the classDiagram rule

    # Extract enumerations, classes, and relationships
    enumerations = []
    classes = []

    for child in tree.children:
        if isinstance(child, ClassDiagramParser.EnumerationsContext):
            for enum in child.enumeration():
                enum_name = enum.STRING().getText().strip('"')
                literals = [lit.getText().strip('"') for lit in enum.literals().STRING()]
                enumerations.append((enum_name, literals))

        elif isinstance(child, ClassDiagramParser.ClassesContext):
            for cls in child.classDefinition():
                class_name = cls.STRING().getText().strip('"')
                attributes = []
                is_abstract = cls.getChild(0).getText() == 'abstract' if cls.getChild(0) else False
                
                # Extract attributes
                if cls.attributes():
                    for attr in cls.attributes().attribute():
                        attr_type = attr.attributeType().getText() if attr.attributeType() else None
                        attr_names = [s.getText().strip('"') for s in attr.STRING()]
                        
                        # Handle constant and default values
                        is_const = 'const' in attr.getText()
                        default_value = None
                        if '=' in attr.getText():
                            default_value = attr.getText().split('=')[1].strip()
                        
                        # Append attribute details
                        for attr_name in attr_names:
                            attributes.append((attr_type, attr_name, is_const, default_value))

                # Extract relationships as attributes
                if cls.relationships():
                    for rel in cls.relationships().children:
                        if isinstance(rel, ClassDiagramParser.CompositionContext):
                            # Composition relationships
                            attributes.append((
                                'composition',  # Relationship type
                                (
                                    rel.mul().getText(),  # Multiplicity to
                                    rel.STRING().getText()# Target class
                                )   
                            ))
                        elif isinstance(rel, ClassDiagramParser.InheritanceContext):
                            attributes.append((
                                'inheritance',  # Relationship type
                                (
                                    rel.STRING().getText()# Target class
                                )   
                            ))
                        elif isinstance(rel, ClassDiagramParser.AssociationContext):
                            # Association relationships
                            attributes.append((
                                'association',  # Relationship type
                                (
                                    rel.mul().getText(),  # Multiplicity to
                                    rel.STRING().getText()# Target class
                                )   
                            ))
                classes.append((class_name, attributes, is_abstract))

    return generate_xmi((enumerations, classes))

def csv_convertion():
    df = pd.read_csv("data/input_output_GPT.csv")
        
    # Create a new column "test" and apply the conversion function to each row in the "Prompt" column
    df['OutputXMI'] = df['Output'].apply(conversion)
    df['Expected_OutputXMI'] = df['Expected_Output'].apply(conversion)

    # Save the updated dataframe to a new CSV file
    df.to_csv("data/input_output_GPT.csv", index=False)