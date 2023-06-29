import ply.lex as lex

# Define the list of token names
tokens = (
    'SYNTH',
    'PARAM_NAME',
    'PARAM_VALUE',
    'TITLE',
    'AUTHOR',
)

# Define the regular expressions for each token
t_SYNTH = r'Synth:'
t_PARAM_NAME = r'[^\n:]+'
t_PARAM_VALUE = r'[^\n:]+'
t_TITLE = r'Title:'
t_AUTHOR = r'Author:'

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
