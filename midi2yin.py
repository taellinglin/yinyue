def number_to_note(number):
    notes = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
    octave = number // 12 - 1
    note = notes[number % 12]
    return note + str(octave)

import mido
import argparse

def midi_to_yin(input_file, output_file):
    mid = mido.MidiFile(input_file)
    
    yin_data = []

    for i, track in enumerate(mid.tracks):
        yin_lines = [f'@piano_{i}']  # Default to a separate pseudo-instrument for each track

        note_on_time = {}
        note_on_velocity = {}
        for msg in track:
            if msg.type == 'note_on':
                note_on_time[msg.note] = msg.time
                note_on_velocity[msg.note] = msg.velocity
            elif msg.type == 'note_off' and msg.note in note_on_time:
                duration = msg.time - note_on_time[msg.note]
                note = number_to_note(msg.note)
                velocity = note_on_velocity[msg.note]
                yin_lines.append(f'{note} D{duration} V{velocity}')
                del note_on_time[msg.note]
                del note_on_velocity[msg.note]
        
        yin_data.append('\n'.join(yin_lines))

    with open(output_file, 'w') as f:
        for instrument_data in yin_data:
            f.write(f'{instrument_data}\n\n')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('input_file', help="The .mid file to convert")
    parser.add_argument('-o', '--output_file', help="The .yin file to output", default="output.yin")
    args = parser.parse_args()

    midi_to_yin(args.input_file, args.output_file)

if __name__ == "__main__":
    main()
