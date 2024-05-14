import re

# Token types
TOKEN_NUMBER = 'NUMBER'
TOKEN_PLUS = 'PLUS'
TOKEN_MINUS = 'MINUS'
TOKEN_MUL = 'MUL'
TOKEN_DIV = 'DIV'
TOKEN_LPAREN = 'LPAREN'
TOKEN_RPAREN = 'RPAREN'
TOKEN_EOF = 'EOF'
TOKEN_INVALID = 'INVALID'

# Token specifications
token_specification = [
    (TOKEN_NUMBER,  r'\d+(\.\d*)?'),  # Integer or decimal number
    (TOKEN_PLUS,    r'\+'),           # Addition operator
    (TOKEN_MINUS,   r'-'),            # Subtraction operator
    (TOKEN_MUL,     r'\*'),           # Multiplication operator
    (TOKEN_DIV,     r'/'),            # Division operator
    (TOKEN_LPAREN,  r'\('),           # Left parenthesis
    (TOKEN_RPAREN,  r'\)'),           # Right parenthesis
    ('SKIP',        r'[ \t]+'),       # Skip spaces and tabs
    (TOKEN_INVALID, r'.'),            # Any other character
]

# Compile the regular expressions into a scanner
token_regex = '|'.join('(?P<%s>%s)' % pair for pair in token_specification)
scanner = re.compile(token_regex)

# Token class
class Token:
    def __init__(self, type_, value):
        self.type = type_
        self.value = value

    def __repr__(self):
        return f'Token({self.type}, {self.value})'

# Function to tokenize input string
def tokenize(code):
    tokens = []
    for match in scanner.finditer(code):
        kind = match.lastgroup
        value = match.group()
        if kind == 'SKIP':
            continue
        elif kind == TOKEN_INVALID:
            raise RuntimeError(f'{value!r} unexpected')
        else:
            tokens.append(Token(kind, value))
    tokens.append(Token(TOKEN_EOF, 'EOF'))
    return tokens

# AST Node types
AST_NUMBER = 'NUMBER'
AST_BINOP = 'BINOP'

# AST Node class
class ASTNode:
    def __init__(self, type_, value=None, left=None, right=None):
        self.type = type_
        self.value = value
        self.left = left
        self.right = right

    def __repr__(self):
        return f'ASTNode({self.type}, {self.value}, {self.left}, {self.right})'

# Parser class
class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current_token = None
        self.pos = -1
        self.next_token()

    def next_token(self):
        self.pos += 1
        if self.pos < len(self.tokens):
            self.current_token = self.tokens[self.pos]
        else:
            self.current_token = Token(TOKEN_EOF, 'EOF')

    def expect(self, token_type):
        if self.current_token.type == token_type:
            self.next_token()
        else:
            raise SyntaxError(f"Expected {token_type}, got {self.current_token.type}")

    def parse(self):
        return self.expr()

    def expr(self):
        node = self.term()
        while self.current_token.type in (TOKEN_PLUS, TOKEN_MINUS):
            token = self.current_token
            self.next_token()
            node = ASTNode(AST_BINOP, token.value, node, self.term())
        return node

    def term(self):
        node = self.factor()
        while self.current_token.type in (TOKEN_MUL, TOKEN_DIV):
            token = self.current_token
            self.next_token()
            node = ASTNode(AST_BINOP, token.value, node, self.factor())
        return node

    def factor(self):
        token = self.current_token
        if token.type == TOKEN_NUMBER:
            self.next_token()
            return ASTNode(AST_NUMBER, token.value)
        elif token.type == TOKEN_LPAREN:
            self.next_token()
            node = self.expr()
            self.expect(TOKEN_RPAREN)
            return node
        else:
            raise SyntaxError(f"Unexpected token: {token.type}")

# IR Code Generator class
class IRCodeGenerator:
    def __init__(self):
        self.temp_count = 0

    def new_temp(self):
        temp_name = f't{self.temp_count}'
        self.temp_count += 1
        return temp_name

    def generate(self, node):
        if node.type == AST_NUMBER:
            temp = self.new_temp()
            print(f'{temp} = {node.value}')
            return temp
        elif node.type == AST_BINOP:
            left_temp = self.generate(node.left)
            right_temp = self.generate(node.right)
            temp = self.new_temp()
            print(f'{temp} = {left_temp} {node.value} {right_temp}')
            return temp

if __name__ == '__main__':
    # Read input from standard input
    input_code = input("Enter expression: ")

    # Tokenize input
    tokens = tokenize(input_code)

    # Parse the tokens
    parser = Parser(tokens)
    ast = parser.parse()

    # Generate IR code
    ir_generator = IRCodeGenerator()
    ir_generator.generate(ast)


#$ python ir_generator.py
#Enter expression: 3 + 5 * (10 - 4)
#t0 = 3
#t1 = 10
#t2 = 4
#t3 = t1 - t2
#t4 = 5
#t5 = t4 * t3
#t6 = t0 + t5
