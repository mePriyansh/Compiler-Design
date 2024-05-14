import re
import sys

# Define token types and their corresponding regular expressions
token_specification = [
    ('NUMBER',  r'\d+(\.\d*)?'),  # Integer or decimal number
    ('PLUS',    r'\+'),           # Addition operator
    ('MINUS',   r'-'),            # Subtraction operator
    ('MUL',     r'\*'),           # Multiplication operator
    ('DIV',     r'/'),            # Division operator
    ('LPAREN',  r'\('),           # Left parenthesis
    ('RPAREN',  r'\)'),           # Right parenthesis
    ('SKIP',    r'[ \t]+'),       # Skip spaces and tabs
    ('MISMATCH',r'.'),            # Any other character
]

# Compile the regular expressions into a scanner
token_regex = '|'.join('(?P<%s>%s)' % pair for pair in token_specification)
scanner = re.compile(token_regex)

# Token IDs
token_ids = {name: idx for idx, (name, _) in enumerate(token_specification)}

def tokenize(code):
    for match in scanner.finditer(code):
        kind = match.lastgroup
        value = match.group()
        if kind == 'SKIP':
            continue
        elif kind == 'MISMATCH':
            raise RuntimeError(f'{value!r} unexpected')
        yield (kind, value)

# Parser implementation
class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current_token = None
        self.next_token()

    def next_token(self):
        try:
            self.current_token = next(self.tokens)
        except StopIteration:
            self.current_token = None

    def expect(self, token_type):
        if self.current_token and self.current_token[0] == token_type:
            self.next_token()
        else:
            raise SyntaxError(f"Expected {token_type}, got {self.current_token}")

    def parse(self):
        return self.expr()

    def expr(self):
        node = self.term()
        while self.current_token and self.current_token[0] in ('PLUS', 'MINUS'):
            token = self.current_token
            self.next_token()
            node = (token[0], node, self.term())
        return node

    def term(self):
        node = self.factor()
        while self.current_token and self.current_token[0] in ('MUL', 'DIV'):
            token = self.current_token
            self.next_token()
            node = (token[0], node, self.factor())
        return node

    def factor(self):
        token = self.current_token
        if token[0] == 'NUMBER':
            self.next_token()
            return ('NUMBER', token[1])
        elif token[0] == 'LPAREN':
            self.next_token()
            node = self.expr()
            self.expect('RPAREN')
            return node
        else:
            raise SyntaxError(f"Unexpected token: {token}")

if __name__ == '__main__':
    # Read input from standard input
    input_code = sys.stdin.read()

    # Tokenize input
    tokens = tokenize(input_code)

    # Parse the tokens
    parser = Parser(tokens)
    parse_tree = parser.parse()

    # Print the parse tree
    print(parse_tree)


#$ echo "3 + 5 * (10 - 4)" | python parser.py
#('PLUS', ('NUMBER', '3'), ('MUL', ('NUMBER', '5'), ('MINUS', ('NUMBER', '10'), ('NUMBER', '4'))))

