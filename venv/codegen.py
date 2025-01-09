from parser import parse
from lexer import tokenize

def generate_python(ast_node, indent_level=0):
    indent = "    " * indent_level
    lines = []

    if isinstance(ast_node, type(None)):
        return ""

    if ast_node.__class__.__name__ == "ProgramNode":
        for stmt in ast_node.statements:
            lines.append(generate_python(stmt, indent_level))
    
    elif ast_node.__class__.__name__ == "SetNode":
        # SET x TO 10 -> x = 10
        lines.append(f"{indent}{ast_node.var_name} = {ast_node.value}")
    
    elif ast_node.__class__.__name__ == "IfNode":
        # if x < 5:
        cond_var, cond_op, cond_val = ast_node.condition
        python_op = {"LESS": "<", "GREATER": ">", "EQUAL": "=="}[cond_op]
        lines.append(f"{indent}if {cond_var} {python_op} {cond_val}:")
        # Then block
        for stmt in ast_node.then_block:
            lines.append(generate_python(stmt, indent_level+1))
        lines.append(f"{indent}else:")
        # Else block
        for stmt in ast_node.else_block:
            lines.append(generate_python(stmt, indent_level+1))

    elif ast_node.__class__.__name__ == "PrintNode":
        # PRINT x -> print(x)
        expr = ast_node.expression
        if isinstance(expr, int):
            lines.append(f"{indent}print({expr})")
        else:
            lines.append(f"{indent}print({expr})")

    return "\n".join(lines)

if __name__ == "__main__":
    code_sample = """BEGIN
SET x TO 10
IF x < 5 THEN
  PRINT x
ELSE
  PRINT 0
ENDIF
END
"""
    tokens = tokenize(code_sample)
    ast = parse(tokens)
    python_code = generate_python(ast)
    print("Generated Python code:\n")
    print(python_code)
    
    # Optionally, you can write this to a .py file:
    with open("output.py", "w") as f:
        f.write(python_code)
    print("\nPython code written to output.py")
