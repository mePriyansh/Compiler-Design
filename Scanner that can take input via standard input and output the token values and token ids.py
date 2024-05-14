import re
import sys

# Define token types and their corresponding regular expressions
token_specification = [
    ('NUMBER', r'\d+(\.\d*)?'),  # Integer or decimal number
    ('IDENT',  r'[A-Za-z]+'),    # Identifiers
    ('OP',     r'[+\-*/]'),      # Arithmetic operators
    ('NEWLINE', r'\n'),          # Line endings
    ('SKIP',   r'[ \t]+'),       # Skip over spaces and tabs
    ('MISMATCH', r'.'),          # Any other character
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
        if kind == 'NEWLINE':
            continue
        elif kind == 'SKIP':
            continue
        elif kind == 'MISMATCH':
            raise RuntimeError(f'{value!r} unexpected')
        yield (value, token_ids[kind])

if __name__ == '__main__':
    # Read input from standard input
    input_code = sys.stdin.read()

    # Tokenize input and print tokens with their IDs
    for value, token_id in tokenize(input_code):
        print(f'Token: {value}, Token ID: {token_id}')


#Usage
#$ echo "x = 10 + 20" | python scanner.py
#Token: x, Token ID: 1
#Token: =, Token ID: 2
#Token: 10, Token ID: 0
#Token: +, Token ID: 2
#Token: 20, Token ID: 0

