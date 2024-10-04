import re

# Define tokens
tokens = [
    ('LET', r'let'),
    ('PRINT', r'print'),
    ('NUMBER', r'\d+'),
    ('IDENTIFIER', r'[a-zA-Z_]\w*'),
    ('EQUALS', r'='),
    ('PLUS', r'\+'),
    ('MINUS', r'-'),
    ('TIMES', r'\*'),
    ('DIVIDE', r'/'),
    ('LPAREN', r'\('),
    ('RPAREN', r'\)'),
    ('STRING', r'"[^"]*"'),
    ('WHITESPACE', r'\s+'),
]

# Lexer
def tokenize(code):
    pos = 0
    tokens_list = []
    while pos < len(code):
        match = None
        for token_expr in tokens:
            tag, pattern = token_expr
            regex = re.compile(pattern)
            match = regex.match(code, pos)
            if match:
                text = match.group(0)
                if tag != 'WHITESPACE':
                    token = (tag, text)
                    tokens_list.append(token)
                break
        if not match:
            raise SyntaxError(f'Illegal character: {code[pos]}')
        else:
            pos = match.end(0)
    return tokens_list

# AST Nodes
class ASTNode:
    pass

class BinOp(ASTNode):
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right

class Number(ASTNode):
    def __init__(self, value):
        self.value = value

class String(ASTNode):
    def __init__(self, value):
        self.value = value

class Var(ASTNode):
    def __init__(self, name):
        self.name = name

class Assign(ASTNode):
    def __init__(self, name, value):
        self.name = name
        self.value = value

class Print(ASTNode):
    def __init__(self, expr):
        self.expr = expr

# Parser
def parse(tokens):
    def parse_expression(index):
        left, index = parse_term(index)
        while index < len(tokens) and tokens[index][0] in ('PLUS', 'MINUS'):
            op = tokens[index][0]
            index += 1
            right, index = parse_term(index)
            left = BinOp(left, op, right)
        return left, index

    def parse_term(index):
        left, index = parse_factor(index)
        while index < len(tokens) and tokens[index][0] in ('TIMES', 'DIVIDE'):
            op = tokens[index][0]
            index += 1
            right, index = parse_factor(index)
            left = BinOp(left, op, right)
        return left, index

    def parse_factor(index):
        token = tokens[index]
        if token[0] == 'NUMBER':
            index += 1
            return Number(int(token[1])), index
        elif token[0] == 'STRING':
            index += 1
            return String(token[1][1:-1]), index  # Remove quotes
        elif token[0] == 'IDENTIFIER':
            index += 1
            return Var(token[1]), index
        elif token[0] == 'LPAREN':
            index += 1
            expr, index = parse_expression(index)
            if tokens[index][0] != 'RPAREN':
                raise SyntaxError('Expected )')
            index += 1
            return expr, index
        else:
            raise SyntaxError('Expected number, string, or (')

    def parse_statement(index):
        token = tokens[index]
        print(f"Parsing statement at index {index}: {token}")  # Debugging output
        if token[0] == 'LET':
            index += 1
            if tokens[index][0] != 'IDENTIFIER':
                raise SyntaxError('Expected variable name')
            var_name = tokens[index][1]
            index += 1
            if tokens[index][0] != 'EQUALS':
                raise SyntaxError('Expected =')
            index += 1
            expr, index = parse_expression(index)
            return Assign(var_name, expr), index
        elif token[0] == 'PRINT':
            index += 1
            expr, index = parse_expression(index)
            return Print(expr), index
        else:
            raise SyntaxError(f'Expected let or print, but got {token[0]}')

    statements = []
    index = 0
    while index < len(tokens):
        stmt, index = parse_statement(index)
        statements.append(stmt)
    return statements

# Interpreter
class Interpreter:
    def __init__(self):
        self.variables = {}

    def evaluate(self, node):
        if isinstance(node, Number):
            return node.value
        elif isinstance(node, String):
            return node.value
        elif isinstance(node, Var):
            if node.name in self.variables:
                return self.variables[node.name]
            else:
                raise NameError(f'Variable {node.name} not defined')
        elif isinstance(node, BinOp):
            left_val = self.evaluate(node.left)
            right_val = self.evaluate(node.right)
            if node.op == 'PLUS':
                if isinstance(left_val, str) or isinstance(right_val, str):
                    return str(left_val) + str(right_val)
                return left_val + right_val
            elif node.op == 'MINUS':
                return left_val - right_val
            elif node.op == 'TIMES':
                return left_val * right_val
            elif node.op == 'DIVIDE':
                return left_val / right_val

    def execute(self, statements):
        for stmt in statements:
            if isinstance(stmt, Assign):
                value = self.evaluate(stmt.value)
                self.variables[stmt.name] = value
            elif isinstance(stmt, Print):
                value = self.evaluate(stmt.expr)
                print(value)

# Read LiteScript code from a file
with open(r'code.ls', 'r') as file:
    code = file.read()

tokens = tokenize(code)
print(f"Tokens: {tokens}")  # Debugging outputclear
statements = parse(tokens)
interpreter = Interpreter()
interpreter.execute(statements)