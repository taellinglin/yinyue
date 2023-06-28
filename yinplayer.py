import sys
from ply import lex
import subsynth

# Create subsynth instance
synth = subsynth.SubtractiveSynthesizer("default.instrument")

# Define tokens
tokens = (
    'CHANNEL',
    'NOTE',
    'START_TIME',
    'VELOCITY',
    'PANNING',
    'VOLUME',
    'ILLEGAL',
)

# Regular expressions for tokens
def t_CHANNEL(t):
    r'C\d+:'
    t.value = int(t.value[1:-1])  # Extract the channel number
    return t

def t_NOTE(t):
    r'N\d+:'
    t.value = int(t.value[1:-1])  # Extract the note number
    return t

def t_START_TIME(t):
    r'S:\s*\d+(\.\d+)?'
    t.value = float(t.value[2:])  # Extract the start time
    return t

def t_VELOCITY(t):
    r'V:\s*\d+'
    t.value = int(t.value[2:])  # Extract the velocity
    return t

def t_PANNING(t):
    r'P:\s*\d+'
    t.value = int(t.value[2:])  # Extract the panning value
    return t

def t_VOLUME(t):
    r'V:\s*(\d+(\.\d+)?(?:,\s*V:\s*\d+(\.\d+)?)*)'
    values = t.value[2:].split(',')
    t.value = [float(v.strip()) for v in values]
    return t

def t_ILLEGAL(t):
    r'[^ \t\n]+'
    print(f"Illegal character '{t.value}'")
    t.lexer.skip(1)

# Error handling rule
def t_error(t):
    print(f"Illegal character '{t.value[0]}'")
    t.lexer.skip(1)

t_ignore = ' \t\n,'

# Build lexer
lexer = lex.lex()

def parse_yin(yin_file_path, synth):
    # Read the file
    with open(yin_file_path, 'r') as f:
        yin_file_contents = f.readlines()

    # Process the lines
    for line in yin_file_contents:
        line = line.strip()

        if line.startswith('C') and line[1].isdigit():
            # Extract the channel number
            current_channel = int(line[1:-1])
            print(f"Current channel: {current_channel}")
        elif line.startswith(('Nchannel_panning', 'Nchannel_volume')):
            # Extract the channel panning or volume
            parts = line.split(':')
            channel_parameter = parts[0]
            value = int(parts[1].strip())
            if channel_parameter == 'Nchannel_panning':
                print(f"Channel panning: {value}")
                synth.set_channel_panning(current_channel, value)
            elif channel_parameter == 'Nchannel_volume':
                print(f"Channel volume: {value}")
                synth.set_channel_volume(current_channel, value)
        elif line.startswith('N'):
            # Extract the note number
            print("Extracting Note Number...")
            current_note = int(line[1:line.index(':')])  # Get the integer note number before the ':'

            print("Extracting Note Parameters...")
            # Extract the note parameters (start time, velocity)
            note_params = line[line.index(':')+1:].split(', ')

            start_time = None
            velocities = []
            for param in note_params:
                if param.startswith('S:'):
                    print("Extracting start time")
                    start_time = float(param[2:].strip())  # Extract the start time
                    print(f"Start time: {start_time}")
                elif param.startswith('V:'):
                    print("Appending Velocities")
                    velocities.append(int(float(param[2:].strip())))  # Extract the velocity
                    print(f"Velocities: {velocities}")

            # Ensure start_time and velocity are not None before playing note
            if start_time is not None and velocities:
                for velocity in velocities:
                    print(f"Playing note with velocity: {velocity}")
                    synth.play_note(current_channel, current_note, velocity)
        elif line:
            # Skip unexpected lines
            continue





if __name__ == '__main__':
    if len(sys.argv) < 3:
        print('Usage: python yin2midi.py <input_file.yin> <instrument_file.instrument>')
    else:
        input_file_path = sys.argv[1]
        instrument_file_path = sys.argv[2]

        # Create subsynth instance with the instrument file
        synth = subsynth.SubtractiveSynthesizer(instrument_file_path)

        parse_yin(input_file_path, synth)
