from lexer import tokenize
from anytree import Node, RenderTree
from ast_nodes import ProgramNode, SetNode, IfNode, PrintNode

def parse(tokens):
    i = 0

    def advance():
        nonlocal i
        token = tokens[i]
        i += 1
        return token

    def match(expected_type):
        token = advance()
        if token[0] != expected_type:
            raise ValueError(f"Expected token type {expected_type}, but got {token[0]}")
        return token

    def parse_program():
        statements = []
        while i < len(tokens):
            token = tokens[i]
            if token[0] == "BEGIN":
                advance()
            elif token[0] == "END":
                advance()
                break
            elif token[0] == "SET":
                statements.append(parse_set())
            elif token[0] == "IF":
                statements.append(parse_if())
            elif token[0] == "PRINT":
                statements.append(parse_print())
            else:
                raise ValueError(f"Unexpected token: {token}")
        return ProgramNode(statements)

    def parse_set():
        match("SET")
        var_token = match("IDENT")
        match("TO")
        value_token = match("NUMBER")
        return SetNode(var_name=var_token[1], value=int(value_token[1]))

    def parse_if():
        match("IF")
        var_token = match("IDENT")
        op_token = advance()
        if op_token[0] not in ("LESS", "GREATER", "EQUAL"):
            raise ValueError(f"Invalid operator '{op_token[1]}' in condition")
        num_token = match("NUMBER")
        condition = (var_token[1], op_token[0], int(num_token[1]))
        match("THEN")
        then_block = []
        while tokens[i][0] != "ELSE" and tokens[i][0] != "ENDIF":
            then_block.append(parse_statement())
        else_block = []
        if tokens[i][0] == "ELSE":
            advance()
            while tokens[i][0] != "ENDIF":
                else_block.append(parse_statement())
        match("ENDIF")
        return IfNode(condition=condition, then_block=then_block, else_block=else_block)

    def parse_print():
        match("PRINT")
        next_tok = advance()
        if next_tok[0] == "IDENT":
            return PrintNode(next_tok[1])
        elif next_tok[0] == "NUMBER":
            return PrintNode(int(next_tok[1]))
        else:
            raise ValueError(f"Invalid token in PRINT: {next_tok}")

    def parse_statement():
        token = tokens[i]
        if token[0] == "SET":
            return parse_set()
        elif token[0] == "IF":
            return parse_if()
        elif token[0] == "PRINT":
            return parse_print()
        else:
            raise ValueError(f"Unexpected token: {token}")

    root = parse_program()
    if i != len(tokens):
        raise ValueError("Extra tokens after valid program.")
    return root

def ast_to_tree(ast):
    def create_node(ast_node, parent=None):
        if isinstance(ast_node, ProgramNode):
            node = Node("Program", parent=parent)
            for stmt in ast_node.statements:
                create_node(stmt, node)
        elif isinstance(ast_node, SetNode):
            node = Node(f"Set({ast_node.var_name} = {ast_node.value})", parent=parent)
        elif isinstance(ast_node, IfNode):
            node = Node("If", parent=parent)
            condition_node = Node(f"Condition({ast_node.condition})", parent=node)
            then_node = Node("Then", parent=node)
            for stmt in ast_node.then_block:
                create_node(stmt, then_node)
            if ast_node.else_block:
                else_node = Node("Else", parent=node)
                for stmt in ast_node.else_block:
                    create_node(stmt, else_node)
        elif isinstance(ast_node, PrintNode):
            node = Node(f"Print({ast_node.expression})", parent=parent)
        else:
            raise ValueError(f"Unknown AST node type: {type(ast_node)}")
        return node

    root_node = create_node(ast)
    return root_node

def render_tree(tree):
    return "\n".join([f"{pre}{node.name}" for pre, _, node in RenderTree(tree)])