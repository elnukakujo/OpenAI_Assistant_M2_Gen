grammar ClassDiagram;

// Entry point for parsing
classDiagram: (enumerations classes relationships)?;

enumerations: 'Enumerations:' (enumeration)+;
enumeration: STRING '(' literals ')';
literals: STRING (',' STRING)*;

classes: 'Classes:' (classDefinition)+;
classDefinition: ('abstract')? STRING '(' (attributes)? ')';
attributes: attribute (',' attribute)*;
attribute: ('const')? attributeType ('[]')? STRING ('=' (STRING | NUM))?;

relationships: 'Relationships:' (composition | inheritance | association)*;
composition: mul STRING 'contain' mul STRING;
inheritance: STRING 'inherit' STRING;
association: mul STRING 'associate' mul STRING;

mul: '(*)' | '('NUM')' | '('NUM '..' ('*' | NUM)')';
attributeType: STRING;

STRING: [a-zA-Z0-9_]+;
NUM: [0-9]+;
WS: [ \t\r\n]+ -> skip; // Ignore whitespace