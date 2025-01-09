from lexer import tokenize
from parser import parse

# Define your pseudocode
code_sample = """BEGIN
SET x TO 10
IF x < 5 THEN
  PRINT x
ELSE
  PRINT 0
ENDIF
END"""

# Tokenize and parse
tokens = tokenize(code_sample)
print("Tokens:", tokens)

ast = parse(tokens)
print("Parsed AST:", ast)
