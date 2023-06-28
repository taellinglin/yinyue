import sys
import os
import mido
from ply import lex, yacc

# Lexer tokens
tokens = (
    'START_TIME',
    'END_TIME',
    'VELOCITY',
    'CHORD',
    'PANNING',
    'CUTOFF',
    'RESONANCE',
    'PITCH_BEND',
    'CHANNEL_VOLUME',
    'CHANNEL_PANNING',
    'FLOAT',
    'INT',
)

# Lexer rules
t_START_TIME = r'start_time'
t_END_TIME = r'end_time'
t_VELOCITY = r'velocity'
t_CHORD = r'chord'
t_PANNING = r'panning'
t_CUTOFF = r'cutoff'
t_RESONANCE = r'resonance'
t_PITCH_BEND = r'pitch_bend'
t_CHANNEL_VOLUME = r'channel_volume'
t_CHANNEL_PANNING = r'channel_panning'
t_FLOAT = r'\d+\.\d+'
t_INT = r'\d+'

t_ignore = ' \t\n'

def t_error(t):
    print(f"Illegal character '{t.value[0]}'")
    t.lexer.skip(1)

# Parser rules
def p_track(p):
    '''track : parameter track
             | empty'''

def p_parameter(p):
    '''parameter : START_TIME time_value
                 | END_TIME time_value
                 | VELOCITY velocity_value
                 | CHORD chord_value
                 | PANNING panning_value
                 | CUTOFF cutoff_value
                 | RESONANCE resonance_value
                 | PITCH_BEND pitch_bend_value
                 | CHANNEL_VOLUME volume_value
                 | CHANNEL_PANNING panning_value'''

def p_time_value(p):
    '''time_value : FLOAT'''
    p[0] = p[1]

def p_velocity_value(p):
    '''velocity_value : INT'''
    p[0] = p[1]

def p_chord_value(p):
    '''chord_value : INT'''
    p[0] = p[1]

def p_panning_value(p):
    '''panning_value : INT'''
    p[0] = p[1]

def p_cutoff_value(p):
    '''cutoff_value : INT'''
    p[0] = p[1]

def p_resonance_value(p):
    '''resonance_value : INT'''
    p[0] = p[1]

def p_pitch_bend_value(p):
    '''pitch_bend_value : INT'''
    p[0] = p[1]

def p_volume_value(p):
    '''volume_value : INT'''
    p[0] = p[1]

def p_empty(p):
    '''empty :'''
    pass

# Build lexer and parser
lexer = lex.lex()
parser = yacc.yacc()

# Function to convert MIDI ticks to seconds
def ticks_to_seconds(ticks, ticks_per_beat, tempo):
    return ticks * tempo / (ticks_per_beat * 1000000)

# Function to parse MIDI data and generate the .yin file
def parse_midi_to_yin(midi_file_path, output_file_path=None):
    # Load the MIDI file
    midi = mido.MidiFile(midi_file_path)

    # Constants
    ticks_per_beat = midi.ticks_per_beat
    tempo = 500000  # Default tempo (microseconds per beat)

    # Trackers data
    trackers_data = {}

    # Iterate over all tracks in the MIDI file
    for track in midi.tracks:
        current_tick = 0
        current_time = 0
        current_channel = 0

        for message in track:
            current_tick += message.time
            current_time = ticks_to_seconds(current_tick, ticks_per_beat, tempo)

            # Set tempo if necessary
            if message.type == 'set_tempo':
                tempo = message.tempo

            # Track channel events
            elif message.type == 'control_change':
                # Handle channel volume changes
                if message.control == 7:
                    trackers_data.setdefault(current_channel, {}).update({'channel_volume': message.value})
                # Handle channel panning changes
                elif message.control == 10:
                    trackers_data.setdefault(current_channel, {}).update({'channel_panning': message.value})

            # Track note events
            elif message.type == 'note_on':
                # Handle note off events
                if message.velocity == 0:
                    note_dict = trackers_data.setdefault(current_channel, {}).get(message.note, {})
                    if not isinstance(note_dict, dict):
                        note_dict = {}
                    note_dict.update({'end_time': current_time})
                    trackers_data[current_channel][message.note] = note_dict
                # Handle note on events
                else:
                    note_dict = trackers_data.setdefault(current_channel, {}).get(message.note, {})
                    if not isinstance(note_dict, dict):
                        note_dict = {}
                    note_dict.update({'start_time': current_time, 'velocity': message.velocity})
                    trackers_data[current_channel][message.note] = note_dict




    # Generate output file name if not provided
    if not output_file_path:
        output_file_name = os.path.splitext(midi_file_path)[0] + '.yin'
        output_file_path = output_file_name

    # Generate .yin file
    with open(output_file_path, 'w') as f:
        for channel, channel_data in trackers_data.items():
            f.write(f'C{channel}:\n')
            for note, note_data in channel_data.items():
                f.write(f'N{note}: ')
                if isinstance(note_data, dict):
                    parameter_strings = []
                    for parameter, value in note_data.items():
                        if parameter == 'start_time':
                            symbol = 'S'
                        elif parameter == 'velocity':
                            symbol = 'V'
                        elif parameter == 'channel_panning':
                            symbol = 'P'
                        elif parameter == 'channel_volume':
                            symbol = 'Vo'
                        parameter_strings.append(f'{symbol}: {value}')
                    f.write(', '.join(parameter_strings) + '\n')
                else:
                    f.write(f'{note_data}\n')



# Command-line arguments handling
if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Usage: python midi2yin.py <input_file.mid> [output_file.yin]')
    else:
        input_file_path = sys.argv[1]
        output_file_path = sys.argv[2] if len(sys.argv) >= 3 else None
        parse_midi_to_yin(input_file_path, output_file_path)
