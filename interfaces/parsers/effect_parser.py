import ply.yacc as yacc
from lexer import tokens

# Define the grammar rules
def p_effect(p):
    '''effect : TITLE title_value AUTHOR author_value effect_name param_list'''

    # Access the parsed data structure
    p[0] = {'title': p[2], 'author': p[4], 'effect_name': p[5], 'params': p[6]}


def p_title_value(p):
    '''title_value : UNICODE'''

    # Store the title value
    p[0] = p[1]


def p_author_value(p):
    '''author_value : UNICODE'''

    # Store the author value
    p[0] = p[1]


def p_effect_name(p):
    '''effect_name : EFFECT UNICODE'''

    # Store the effect name
    p[0] = p[2]


def p_param_list(p):
    '''param_list : param
                  | param_list param'''

    # Build a dictionary of parameters
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[2]]


def p_param(p):
    '''param : LABEL UNICODE VALUE UNICODE'''

    # Build a dictionary representing a parameter
    p[0] = {'label': p[2], 'value': p[4]}


def p_error(p):
    if p:
        print(f"Parser Error: Unexpected token '{p.value}' at line {p.lineno}")
    else:
        print("Parser Error: Unexpected end of input")


# Build the parser
parser = yacc.yacc()
