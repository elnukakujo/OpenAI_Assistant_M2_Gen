grammar ClassDiagram;

// Entry point for parsing
classDiagram: (enumerations classes relationships)?;

enumerations: 'Enumerations:' (enumeration)+;
enumeration: STRING '(' literals ')';
literals: STRING (',' STRING)*;

classes: 'Classes:' (classDefinition)+;
classDefinition: ('abstract')? STRING '(' (attributes)? (relationships)? ')';
attributes: attribute (',' attribute)*;
attribute: ('const')? attributeType ('[]')? STRING (('=' (STRING | NUM))?); // Allow optional assignment for attributes

relationships: (composition | inheritance | association) (',' (composition | inheritance | association))*;

composition: 'contain' mul STRING;
inheritance: 'inherit' mul STRING;
association: 'associate' mul STRING;

mul: '(*)' | '(' NUM ')' | '(' NUM '..' ('*' | NUM) ')';
attributeType: STRING;

STRING: [a-zA-Z_][a-zA-Z0-9_]*; // Adjusted to ensure it starts with a letter
NUM: [0-9]+;
WS: [ \t\r\n]+ -> skip; // Ignore whitespace