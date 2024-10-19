import sys
from antlr4 import *
from ClassDiagramLexer import ClassDiagramLexer
from ClassDiagramParser import ClassDiagramParser

def generate_xmi(parsed_data):
    xmi = """<?xml version="1.0" encoding="UTF-8"?>
<XMI xmi.version="2.1" xmlns:UML="http://www.omg.org/spec/UML/20090901">
    <UML:Model name="ClassDiagram" visibility="public">
"""

    enumerations, classes, relationships = parsed_data
    
    for enum in enumerations:
        xmi += f"        <UML:Enumeration name=\"{enum[0]}\">\n"
        for literal in enum[1]:
            xmi += f"            <UML:Literal name=\"{literal}\"/>\n"
        xmi += "        </UML:Enumeration>\n"
    
    for class_def in classes:
        class_name, attributes, is_abstract = class_def
        if is_abstract:
            xmi += f"        <UML:Class name=\"{class_name}\" visibility=\"abstract\">\n"
        else:
            xmi += f"        <UML:Class name=\"{class_name}\" visibility=\"public\">\n"
        for attr in attributes:
            attr_type = attr[0] if attr[0] else "undefined"
            xmi += f"            <UML:Attribute name=\"{attr[1]}\" type=\"{attr_type}\"/>\n"
        xmi += "        </UML:Class>\n"

    for rel in relationships:
        if len(rel) == 4 and isinstance(rel, tuple):  # Adjusted for Composition and Association
            xmi += f"        <UML:Association>\n"
            xmi += f"            <UML:End type=\"{rel[1]}\" multiplicity=\"{rel[0]}\"/>\n"
            xmi += f"            <UML:End type=\"{rel[3]}\" multiplicity=\"{rel[2]}\"/>\n"
            xmi += "        </UML:Association>\n"
        elif len(rel) == 3 and rel[1] == 'inherit':  # Inheritance
            xmi += f"        <UML:Generalization general=\"{rel[2]}\" specific=\"{rel[0]}\"/>\n"
        else:
            print(f"Warning: Unexpected relationship format: {rel}")  # This can help you debug further

    xmi += """    </UML:Model>
</XMI>"""
    return xmi

def main(input_file, output_file):
    input_stream = FileStream(input_file)
    lexer = ClassDiagramLexer(input_stream)
    token_stream = CommonTokenStream(lexer)
    parser = ClassDiagramParser(token_stream)

    tree = parser.classDiagram()  # Start parsing from the classDiagram rule

    # Extract enumerations, classes, and relationships
    enumerations = []
    classes = []
    relationships = []

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
                is_abstract = cls.getChild(0).getText() == 'abstract'
                if cls.attributes():
                    for attr in cls.attributes().attribute():
                        attr_type = attr.attributeType().getText() if attr.attributeType() else None  # Ensure this is correct
                        # Accessing the STRING tokens; assuming there can be multiple STRING tokens
                        attr_names = [s.getText().strip('"') for s in attr.STRING()]
                        # Assuming you want to handle the first attribute name or all
                        for attr_name in attr_names:
                            attributes.append((attr_type, attr_name))
                classes.append((class_name, attributes, is_abstract))

        elif isinstance(child, ClassDiagramParser.RelationshipsContext):
            for rel in child.children:
                if isinstance(rel, ClassDiagramParser.CompositionContext):
                    # Ensure both ends of the composition relationship are captured
                    relationships.append((rel.mul(0).getText(), rel.STRING(0).getText(), rel.mul(1).getText(), rel.STRING(1).getText()))  # Add class2
                elif isinstance(rel, ClassDiagramParser.InheritanceContext):
                    relationships.append((rel.STRING(0).getText(), 'inherit', rel.STRING(1).getText()))  # Correct as it is
                elif isinstance(rel, ClassDiagramParser.AssociationContext):
                    # Ensure you access both classes and their multiplicities
                    relationships.append((rel.mul(0).getText(), rel.STRING(0).getText(), rel.mul(1).getText(), rel.STRING(1).getText()))  # Add class2

    xmi_output = generate_xmi((enumerations, classes, relationships))

    with open(output_file, 'w') as f:
        f.write(xmi_output)

if __name__ == "__main__":
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    main(input_file, output_file)
