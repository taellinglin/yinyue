import ply.lex as lex

# Define the list of token names
tokens = (
    'NOTE',
    'CONTROL_CHANGE',
    'PROGRAM_CHANGE',
    'PITCH_BEND',
    'PARAM_VALUE',
    'NEWLINE',
)

# Define the regular expressions for each token
t_NOTE = r'Note [A-Ga-g][#b]?[0-9]+'
t_CONTROL_CHANGE = r'Control [0-9]+ [0-9]+'
t_PROGRAM_CHANGE = r'Program [0-9]+'
t_PITCH_BEND = r'PitchBend [0-9]+'
t_PARAM_VALUE = r'[^\n]+'
t_NEWLINE = r'\n'

# Define ignored characters (whitespace and tabs)
t_ignore = ' \t'

# Define error handling rule
def t_error(t):
    print(f"Lexer Error: Unexpected character '{t.value[0]}'")
    t.lexer.skip(1)

# Build the lexer
lexer = lex.lex()
