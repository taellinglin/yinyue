import os
import tkinter as tk
from tkinter import ttk
import mido

PATCHES_DIR = './patches'

class SynthesizerGUI:
    def __init__(self, synthesizer):
        self.synthesizer = synthesizer
        self.available_patches = self.get_available_patches()
        self.current_patch_index = 0

        self.root = tk.Tk()
        self.root.title('SignalSynth')
        self.root.geometry('800x600')

        # Configure the style for the window
        style = ttk.Style()
        style.theme_use('alt')
        style.configure('.', background='black', foreground='white')
        style.configure('TButton', background='black', foreground='white')
        style.configure('TLabel', background='black', foreground='white')
        style.configure('TCheckbutton', background='black', foreground='white')
        style.configure('TScale', background='black', foreground='white')

        # Create the patch selection controls
        self.create_patch_controls()

        # Create a frame to hold the parameter controls
        self.parameter_frame = ttk.Frame(self.root)
        self.parameter_frame.pack(pady=10)

        # Create knobs and labels for parameters
        self.parameter_knobs = {}
        self.parameter_labels = {}
        self.create_parameter_knobs()

        # Connect to MIDI keyboard
        self.midi_input = mido.open_input()
        self.midi_input.callback = self.handle_midi_message
        self.create_piano_keys()
        self.root.mainloop()

    def note_to_midi(self, note):
        # Note names to MIDI note numbers mapping
        note_map = {
            'C': 60,
            'C#': 61,
            'Db': 61,
            'D': 62,
            'D#': 63,
            'Eb': 63,
            'E': 64,
            'F': 65,
            'F#': 66,
            'Gb': 66,
            'G': 67,
            'G#': 68,
            'Ab': 68,
            'A': 69,
            'A#': 70,
            'Bb': 70,
            'B': 71
        }

        # Extract the note name and octave
        note_parts = note.split('-')
        note_name = note_parts[0]
        octave = int(note_parts[1])

        # Calculate the MIDI note number
        midi_note = note_map[note_name] + octave * 12

        return midi_note

    def create_piano_keys(self):
        # Create a frame to hold the piano keys
        piano_frame = ttk.Frame(self.root)
        piano_frame.pack(pady=10)

        # Define the keys and their corresponding MIDI note numbers
        keys = [('C', 60), ('D', 62), ('E', 64), ('F', 65), ('G', 67), ('A', 69), ('B', 71)]

        # Create buttons for each key
        for key_name, note in keys:
            key_button = ttk.Button(piano_frame, text=key_name, command=lambda n=note: self.play_note_on_midi(n))
            key_button.pack(side='left', padx=2)

    def play_note_on_midi(self, note):
        try:
            velocity = 100
            self.synthesizer.play_note(0, note, velocity)
        except ValueError:
            print("Invalid note format:", note)

    def get_available_patches(self):
        # Get a list of available .instrument files in the patches directory
        patches = []
        for filename in os.listdir(PATCHES_DIR):
            if filename.endswith('.instrument'):
                patches.append(filename)
        return patches

    def load_patch(self, patch_index):
        # Load the selected patch from the available_patches list
        if patch_index >= 0 and patch_index < len(self.available_patches):
            patch_file = os.path.join(PATCHES_DIR, self.available_patches[patch_index])
            self.synthesizer.load_instrument(patch_file)

    def select_previous_patch(self):
        # Select the previous patch
        self.current_patch_index -= 1
        if self.current_patch_index < 0:
            self.current_patch_index = len(self.available_patches) - 1
        self.load_patch(self.current_patch_index)

    def select_next_patch(self):
        # Select the next patch
        self.current_patch_index += 1
        if self.current_patch_index >= len(self.available_patches):
            self.current_patch_index = 0
        self.load_patch(self.current_patch_index)

    def update_parameter(self, value, parameter):
        # Update the parameter value in the synthesizer
        self.synthesizer.set_parameter(parameter, value)

    def create_patch_controls(self):
        # Create the patch selection controls
        patch_frame = ttk.Frame(self.root)
        patch_frame.pack()

        # Create the patch selection label
        patch_label = ttk.Label(patch_frame, text='Patch:')
        patch_label.pack(side='left')

        # Create the patch selection combobox
        patch_combobox = ttk.Combobox(patch_frame, values=self.available_patches, state='readonly', width=20)
        patch_combobox.current(self.current_patch_index)
        patch_combobox.bind('<<ComboboxSelected>>', lambda event: self.load_patch(patch_combobox.current()))
        patch_combobox.pack(side='left')

        # Create the previous patch button
        previous_patch_button = ttk.Button(patch_frame, text='◀', command=self.select_previous_patch)
        previous_patch_button.pack(side='left')

        # Create the next patch button
        next_patch_button = ttk.Button(patch_frame, text='▶', command=self.select_next_patch)
        next_patch_button.pack(side='left')

    def create_parameter_knobs(self):
        # Create knobs and labels for parameters
        for param in self.synthesizer.params:
            # Create a frame for each parameter
            param_frame = ttk.Frame(self.parameter_frame)
            param_frame.pack(side='top', pady=5)

            # Create a label for the parameter
            label = ttk.Label(param_frame, text=param)
            label.pack(side='left', padx=5)
            self.parameter_labels[param] = label

            # Create a knob for the parameter
            knob = ttk.Scale(param_frame, from_=0, to=100, orient='horizontal',
                             command=lambda v, p=param: self.update_parameter(v, p))
            knob.pack(side='left', padx=5)
            value = self.synthesizer.get_parameter(param)
            if isinstance(value, (int, float)):
                knob.set(float(value))
            else:
                knob.set(0.0)

    def handle_midi_message(self, message):
        if message.type == 'note_on':
            velocity = message.velocity / 127.0
            self.synthesizer.play_note(message.note, velocity)
            # Play the note on MIDI as well
            self.play_note_on_midi(self.note_to_midi(mido.note_number_to_name(message.note)))
        elif message.type == 'note_off':
            self.synthesizer.stop_note(message.note)


# Example usage
from subsynth import SubtractiveSynthesizer

# Create an instance of the SubtractiveSynthesizer
synthesizer = SubtractiveSynthesizer('default.instrument')

# Create the GUI using the synthesizer instance
gui = SynthesizerGUI(synthesizer)