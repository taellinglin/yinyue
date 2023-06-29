import ply.lex as lex

# Define the list of token names
tokens = (
    'TITLE',
    'AUTHOR',
    'EFFECT',
    'LABEL',
    'VALUE',
)

# Define the regular expressions for each token
t_TITLE = r'Title:'
t_AUTHOR = r'Author:'
t_EFFECT = r'Effect:'
t_LABEL = r'Label:'
t_VALUE = r'Value:'
t_UNICODE = r'[\p{L}\p{N}\p{P}]+'

# Define ignored characters (whitespace and tabs)
t_ignore = ' \t'


def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


def t_error(t):
    print(f"Lexer Error: Unexpected character '{t.value[0]}'")
    t.lexer.skip(1)


# Build the lexer
lexer = lex.lex()
