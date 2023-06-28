from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.graphics import Color, Rectangle
from kivy.clock import Clock
import random
import colorsys

class ColorfulButton(Button):
    def __init__(self, note, octave, synthesizer, **kwargs):
        super().__init__(**kwargs)
        self.note = note
        self.octave = octave
        self.synthesizer = synthesizer
        self.draw_background()

    def draw_background(self):
        hue = random.random()
        saturation = 1  # Adjust the saturation value as needed
        value = 1.6  # Adjust the value/brightness value as needed
        r, g, b = colorsys.hsv_to_rgb(hue, saturation, value)
        self.background_color = (r, g, b, 1)


    def play_note(self):
        note_value = self.note_to_int(self.note) + self.octave * 12
        midi_note = note_value + 60  # Adjust the MIDI note offset as needed
        self.synthesizer.play_note(0, midi_note, 100)

    def note_to_int(self, note):
        note_dict = {'C': 0, 'C#': 1, 'D': 2, 'D#': 3, 'E': 4, 'F': 5, 'F#': 6, 'G': 7, 'G#': 8, 'A': 9, 'A#': 10, 'B': 11}
        return note_dict[note]


def get_content(synthesizer=None):
    performance_layout = BoxLayout(orientation='vertical')

    def update_bg_rect(instance, value):
        performance_layout.bg_rect.pos = performance_layout.pos
        performance_layout.bg_rect.size = performance_layout.size

    performance_layout.update_bg_rect = update_bg_rect

    # Create a black background
    with performance_layout.canvas.before:
        Color(0, 0, 0, 1)  # Set color to black
        performance_layout.bg_rect = Rectangle(pos=performance_layout.pos, size=performance_layout.size)

    performance_layout.bind(pos=performance_layout.update_bg_rect, size=performance_layout.update_bg_rect)

    if synthesizer:
        print("Synthesizer Passed...")

    grid_layout = GridLayout(cols=12, rows=12, spacing=4, size_hint=(1, 1))
    buttons = []
    num_octaves = 12
    notes = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']

    # Create buttons for each note and octave
    for octave in range(0, num_octaves):
        for note in notes:
            button = ColorfulButton(note=note, octave=octave, synthesizer=synthesizer, size_hint=(1 / 12, 1 / 12))
            button.bind(on_press=lambda btn: btn.play_note())
            buttons.append(button)
            grid_layout.add_widget(button)

    performance_layout.add_widget(grid_layout)

    def update_colors(*args):
        for button in buttons:
            button.draw_background()

    # Schedule color update every second
    Clock.schedule_interval(update_colors, 1)

    return performance_layout



