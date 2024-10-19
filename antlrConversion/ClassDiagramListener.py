# Generated from ClassDiagram.g4 by ANTLR 4.13.2
from antlr4 import *
if "." in __name__:
    from .ClassDiagramParser import ClassDiagramParser
else:
    from ClassDiagramParser import ClassDiagramParser

# This class defines a complete listener for a parse tree produced by ClassDiagramParser.
class ClassDiagramListener(ParseTreeListener):

    # Enter a parse tree produced by ClassDiagramParser#classDiagram.
    def enterClassDiagram(self, ctx:ClassDiagramParser.ClassDiagramContext):
        pass

    # Exit a parse tree produced by ClassDiagramParser#classDiagram.
    def exitClassDiagram(self, ctx:ClassDiagramParser.ClassDiagramContext):
        pass


    # Enter a parse tree produced by ClassDiagramParser#enumerations.
    def enterEnumerations(self, ctx:ClassDiagramParser.EnumerationsContext):
        pass

    # Exit a parse tree produced by ClassDiagramParser#enumerations.
    def exitEnumerations(self, ctx:ClassDiagramParser.EnumerationsContext):
        pass


    # Enter a parse tree produced by ClassDiagramParser#enumeration.
    def enterEnumeration(self, ctx:ClassDiagramParser.EnumerationContext):
        pass

    # Exit a parse tree produced by ClassDiagramParser#enumeration.
    def exitEnumeration(self, ctx:ClassDiagramParser.EnumerationContext):
        pass


    # Enter a parse tree produced by ClassDiagramParser#literals.
    def enterLiterals(self, ctx:ClassDiagramParser.LiteralsContext):
        pass

    # Exit a parse tree produced by ClassDiagramParser#literals.
    def exitLiterals(self, ctx:ClassDiagramParser.LiteralsContext):
        pass


    # Enter a parse tree produced by ClassDiagramParser#classes.
    def enterClasses(self, ctx:ClassDiagramParser.ClassesContext):
        pass

    # Exit a parse tree produced by ClassDiagramParser#classes.
    def exitClasses(self, ctx:ClassDiagramParser.ClassesContext):
        pass


    # Enter a parse tree produced by ClassDiagramParser#classDefinition.
    def enterClassDefinition(self, ctx:ClassDiagramParser.ClassDefinitionContext):
        pass

    # Exit a parse tree produced by ClassDiagramParser#classDefinition.
    def exitClassDefinition(self, ctx:ClassDiagramParser.ClassDefinitionContext):
        pass


    # Enter a parse tree produced by ClassDiagramParser#attributes.
    def enterAttributes(self, ctx:ClassDiagramParser.AttributesContext):
        pass

    # Exit a parse tree produced by ClassDiagramParser#attributes.
    def exitAttributes(self, ctx:ClassDiagramParser.AttributesContext):
        pass


    # Enter a parse tree produced by ClassDiagramParser#attribute.
    def enterAttribute(self, ctx:ClassDiagramParser.AttributeContext):
        pass

    # Exit a parse tree produced by ClassDiagramParser#attribute.
    def exitAttribute(self, ctx:ClassDiagramParser.AttributeContext):
        pass


    # Enter a parse tree produced by ClassDiagramParser#relationships.
    def enterRelationships(self, ctx:ClassDiagramParser.RelationshipsContext):
        pass

    # Exit a parse tree produced by ClassDiagramParser#relationships.
    def exitRelationships(self, ctx:ClassDiagramParser.RelationshipsContext):
        pass


    # Enter a parse tree produced by ClassDiagramParser#composition.
    def enterComposition(self, ctx:ClassDiagramParser.CompositionContext):
        pass

    # Exit a parse tree produced by ClassDiagramParser#composition.
    def exitComposition(self, ctx:ClassDiagramParser.CompositionContext):
        pass


    # Enter a parse tree produced by ClassDiagramParser#inheritance.
    def enterInheritance(self, ctx:ClassDiagramParser.InheritanceContext):
        pass

    # Exit a parse tree produced by ClassDiagramParser#inheritance.
    def exitInheritance(self, ctx:ClassDiagramParser.InheritanceContext):
        pass


    # Enter a parse tree produced by ClassDiagramParser#association.
    def enterAssociation(self, ctx:ClassDiagramParser.AssociationContext):
        pass

    # Exit a parse tree produced by ClassDiagramParser#association.
    def exitAssociation(self, ctx:ClassDiagramParser.AssociationContext):
        pass


    # Enter a parse tree produced by ClassDiagramParser#mul.
    def enterMul(self, ctx:ClassDiagramParser.MulContext):
        pass

    # Exit a parse tree produced by ClassDiagramParser#mul.
    def exitMul(self, ctx:ClassDiagramParser.MulContext):
        pass


    # Enter a parse tree produced by ClassDiagramParser#attributeType.
    def enterAttributeType(self, ctx:ClassDiagramParser.AttributeTypeContext):
        pass

    # Exit a parse tree produced by ClassDiagramParser#attributeType.
    def exitAttributeType(self, ctx:ClassDiagramParser.AttributeTypeContext):
        pass



del ClassDiagramParser