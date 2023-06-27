import ply.lex as lex
import ply.yacc as yacc
from midiutil.MidiFile import MIDIFile
import argparse
import tempfile
import os
import subprocess
import sys

class YinPlayer:
    tokens = (
        'NOTE',
        'INSTRUMENT',
        'TEMPO',
        'DURATION',
        'VELOCITY',
    )

    def t_NOTE(t):
        r'[A-G][#b]?[0-9]+'
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

    def t_VELOCITY(t):
        r'V\d+'
        return t

    t_ignore = ' \t\n'

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
        p[0] = ('instrument', p[1][1:])

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
        print("Syntax error in input!", file=sys.stderr)

    lexer = lex.lex()
    parser = yacc.yacc()

    def __init__(self, soundfont):
        self.soundfont = soundfont

    def parse_program(self, program):
        return self.parser.parse(program, lexer=self.lexer)

    def convert_to_midi(self, parsed_program):
        mf = MIDIFile(1)
        track = 0
        time = 0
        mf.addTrackName(track, time, "Sample Track")
        mf.addTempo(track, time, 120)

        for command in parsed_program:
            if command[0] == 'note':
                channel = 0
                pitch = command[1]
                time = command[2]
                duration = command[3]
                volume = 100
                mf.addNote(track, channel, pitch, time, duration, volume)

        temp = tempfile.NamedTemporaryFile(delete=False)
        mf.writeFile(temp)
        temp.close()
        return temp.name

    def play_midi(self, midi_file):
        command = ['fluidsynth', '-i', self.soundfont, midi_file]
        subprocess.run(command, check=True)
        os.remove(midi_file)

    def play(self, input_file):
        with open(input_file, 'r') as file:
            program = file.read()
        parsed_program = self.parse_program(program)
        midi_file = self.convert_to_midi(parsed_program)
        self.play_midi(midi_file)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('input_file', help="The .yin file to parse")
    parser.add_argument('-s', '--soundfont', help="The GM sf2 file", required=True)
    args = parser.parse_args()

    player = YinPlayer(args.soundfont)
    player.play(args.input_file)
