import ply.yacc as yacc
from lexer import tokens

# Define the grammar rules
def p_clip(p):
    '''clip : note_list'''

    # Access the parsed data structure
    p[0] = p[1]

def p_note_list(p):
    '''note_list : note
                 | note_list note'''

    # Build a list of notes
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[2]]

def p_note(p):
    '''note : NOTE PARAM_VALUE PARAM_VALUE PARAM_VALUE'''

    # Build a dictionary representing a note
    p[0] = {'type': 'note', 'note': p[1], 'velocity': p[2], 'duration': p[3], 'channel': p[4]}

def p_control_change(p):
    '''control_change : CONTROL_CHANGE PARAM_VALUE PARAM_VALUE PARAM_VALUE'''

    # Build a dictionary representing a control change event
    p[0] = {'type': 'control_change', 'controller': p[1], 'value': p[2], 'channel': p[3]}

def p_program_change(p):
    '''program_change : PROGRAM_CHANGE PARAM_VALUE PARAM_VALUE'''

    # Build a dictionary representing a program change event
    p[0] = {'type': 'program_change', 'program': p[1], 'channel': p[2]}

def p_pitch_bend(p):
    '''pitch_bend : PITCH_BEND PARAM_VALUE PARAM_VALUE PARAM_VALUE'''

    # Build a dictionary representing a pitch bend event
    p[0] = {'type': 'pitch_bend', 'value': p[1], 'channel': p[2]}

def p_error(p):
    if p:
        print(f"Parser Error: Unexpected token '{p.value}' at line {p.lineno}")
    else:
        print("Parser Error: Unexpected end of input")

# Build the parser
parser = yacc.yacc()
