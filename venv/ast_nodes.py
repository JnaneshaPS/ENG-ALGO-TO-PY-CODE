class ProgramNode:
    def __init__(self, statements):
        self.statements = statements

class SetNode:
    def __init__(self, var_name, value):
        self.var_name = var_name
        self.value = value

class IfNode:
    def __init__(self, condition, then_block, else_block):
        self.condition = condition
        self.then_block = then_block
        self.else_block = else_block

class PrintNode:
    def __init__(self, expression):
        self.expression = expression