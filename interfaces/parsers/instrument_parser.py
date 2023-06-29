import ply.yacc as yacc
from lexer import tokens

# Define the grammar rules
def p_instrument(p):
    '''instrument : TITLE title_value AUTHOR author_value synth_list'''

    # Access the parsed data structure
    p[0] = {'title': p[2], 'author': p[4], 'synths': p[5]}


def p_title_value(p):
    '''title_value : PARAM_VALUE'''

    # Store the title value
    p[0] = p[1]


def p_author_value(p):
    '''author_value : PARAM_VALUE'''

    # Store the author value
    p[0] = p[1]


def p_synth_list(p):
    '''synth_list : synth
                  | synth_list synth'''

    # Build a list of synthesizers
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[2]]


def p_synth(p):
    '''synth : SYNTH synth_name synth_params'''

    # Build a dictionary representing a synthesizer
    p[0] = {'synth_name': p[2], 'params': p[3]}


def p_synth_name(p):
    '''synth_name : PARAM_VALUE'''

    # Store the synthesizer name
    p[0] = p[1]


def p_synth_params(p):
    '''synth_params : param_list'''

    # Access the parsed data structure
    p[0] = p[1]


def p_param_list(p):
    '''param_list : param
                  | param_list param'''

    # Build a dictionary of parameters
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[2]]


def p_param(p):
    '''param : PARAM_NAME PARAM_VALUE'''

    # Build a dictionary representing a parameter
    p[0] = {'param_name': p[1], 'param_value': p[2]}


def p_error(p):
    if p:
        print(f"Parser Error: Unexpected token '{p.value}' at line {p.lineno}")
    else:
        print("Parser Error: Unexpected end of input")


# Build the parser
parser = yacc.yacc()
