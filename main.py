import ply.lex as lex
import ply.yacc as yacc
import argparse
import sys

# Tokens
tokens = (
    'NOTE',
    'INSTRUMENT',
    'TEMPO',
    'DURATION',
    'VELOCITY',
)

# Lexer rules
def t_NOTE(t):
    r'[A-G][#b]?-?[0-9]+'
    return t


def t_INSTRUMENT(t):
    r'@[A-Za-z_][A-Za-z_0-9]*'
    return t

def t_TEMPO(t):
    r'T\d+'
    return t

def t_DURATION(t):
    r'D\d+'
    return t
    
def t_error(t):
    print("Illegal character '%s'" % t.value[0], file=sys.stderr)
    t.lexer.skip(1)


def t_VELOCITY(t):
    r'V\d+'
    return t

t_ignore = ' \t\n'

# Parser rules
def p_statements(p):
    '''statements : statement
                  | statements statement'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[2]]

def p_statement(p):
    '''statement : note_statement
                 | instrument_statement
                 | tempo_statement
                 | duration_statement
                 | velocity_statement'''
    p[0] = p[1]

def p_note_statement(p):
    'note_statement : NOTE DURATION VELOCITY'
    p[0] = ('note', p[1], int(p[2][1:]), int(p[3][1:]))

def p_instrument_statement(p):
    'instrument_statement : INSTRUMENT'
    p[0] = ('instrument', p[1])

def p_tempo_statement(p):
    'tempo_statement : TEMPO'
    p[0] = ('tempo', int(p[1][1:]))

def p_duration_statement(p):
    'duration_statement : DURATION'
    p[0] = ('duration', int(p[1][1:]))

def p_velocity_statement(p):
    'velocity_statement : VELOCITY'
    p[0] = ('velocity', int(p[1][1:]))

def p_error(p):
    if p:
        print("Syntax error at '%s'" % p.value, file=sys.stderr)
    else:
        print("Syntax error at EOF", file=sys.stderr)


lexer =lex.lex()

parser = yacc.yacc()

def parse_program(program):
    return parser.parse(program, lexer=lexer)

def parse_file(input_filename, output_filename):
    with open(input_filename, 'r') as file:
        program = file.read()
    parsed_program = parse_program(program)
    with open(output_filename, 'w') as file:
        file.write(str(parsed_program))

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('input_file', help="The .yin file to parse")
    parser.add_argument('-o', '--output_file', help="The .yue file to output", default="output.yue")
    args = parser.parse_args()

    parse_file(args.input_file, args.output_file)

if __name__ == "__main__":
    main()
