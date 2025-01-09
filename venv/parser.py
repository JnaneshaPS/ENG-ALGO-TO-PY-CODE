from lexer import tokenize

class ASTNode:
    pass

class ProgramNode(ASTNode):
    def __init__(self, statements):
        self.statements = statements

    def __repr__(self):
        return f"ProgramNode(statements={self.statements})"

class SetNode(ASTNode):
    def __init__(self, var_name, value):
        self.var_name = var_name
        self.value = value

    def __repr__(self):
        return f"SetNode(var_name={self.var_name}, value={self.value})"

class IfNode(ASTNode):
    def __init__(self, condition, then_block, else_block):
        self.condition = condition
        self.then_block = then_block
        self.else_block = else_block

    def __repr__(self):
        return f"IfNode(condition={self.condition}, then_block={self.then_block}, else_block={self.else_block})"

class PrintNode(ASTNode):
    def __init__(self, expression):
        self.expression = expression

    def __repr__(self):
        return f"PrintNode(expression={self.expression})"

def parse(tokens):
    i = 0

    def peek():
        if i < len(tokens):
            return tokens[i]
        return None

    def advance():
        nonlocal i
        i += 1
        return tokens[i - 1]

    def match(expected_type):
        token = peek()
        if token is None:
            raise ValueError(f"Expected {expected_type} but got end of input")
        if token[0] != expected_type:
            raise ValueError(f"Expected {expected_type} but got {token[0]} ({token[1]})")
        return advance()

    def parse_program():
        match("BEGIN")
        stmts = parse_statement_list()
        match("END")
        return ProgramNode(stmts)

    def parse_statement_list():
        statement_list = []
        while True:
            token = peek()
            if token is None or token[0] in ("END", "ENDIF", "ELSE"):  # Stop on END, ENDIF, or ELSE
                break
            if token[0] in ("SET", "IF", "PRINT"):
                statement_list.append(parse_statement())
            else:
                raise ValueError(f"Unexpected token {token[0]} ({token[1]}) in statement list")
        return statement_list

    def parse_statement():
        token = peek()
        if token[0] == "SET":
            return parse_set()
        elif token[0] == "IF":
            return parse_if()
        elif token[0] == "PRINT":
            return parse_print()
        else:
            raise ValueError(f"Unexpected token {token} in statement")

    def parse_set():
        match("SET")
        var_token = match("IDENT")
        match("TO")
        num_token = match("NUMBER")
        return SetNode(var_token[1], int(num_token[1]))

    def parse_if():
        match("IF")
        condition = parse_condition()
        match("THEN")
        then_block = parse_statement_list()
        match("ELSE")
        else_block = parse_statement_list()
        match("ENDIF")  # Explicitly match ENDIF
        return IfNode(condition, then_block, else_block)

    def parse_condition():
        var_token = match("IDENT")
        op_token = advance()
        if op_token[0] not in ("LESS", "GREATER", "EQUAL"):
            raise ValueError(f"Invalid operator '{op_token[1]}' in condition")
        num_token = match("NUMBER")
        return (var_token[1], op_token[0], int(num_token[1]))

    def parse_print():
        match("PRINT")
        next_tok = advance()
        if next_tok[0] == "IDENT":
            return PrintNode(next_tok[1])
        elif next_tok[0] == "NUMBER":
            return PrintNode(int(next_tok[1]))
        else:
            raise ValueError(f"Invalid token in PRINT: {next_tok}")

    root = parse_program()
    if i != len(tokens):
        raise ValueError("Extra tokens after valid program.")
    return root
