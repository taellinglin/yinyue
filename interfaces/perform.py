from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.graphics import Color, Rectangle
from kivy.clock import Clock
import random
import colorsys


class ColorfulButton(Button):
    def __init__(self, note, octave, synthesizer, stream, **kwargs):
        super().__init__(**kwargs)
        self.note = note
        self.octave = octave
        self.synthesizer = synthesizer
        self.stream = stream
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


class PerformInterface(BoxLayout):
    def __init__(self, synthesizer=None, stream=None, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.synthesizer = synthesizer
        self.stream = stream
        self.bg_rect = Rectangle(pos=self.pos, size=self.size)
        self.update_bg_rect()
        self.create_content()
        self.schedule_color_update()

    def update_bg_rect(self, *args):
        if self.bg_rect:
            self.bg_rect.pos = self.pos
            self.bg_rect.size = self.size

    def create_content(self):
        with self.canvas.before:
            Color(0, 0, 0, 1)  # Set color to black
            self.bg_rect = Rectangle(pos=self.pos, size=self.size)

        self.bind(pos=self.update_bg_rect, size=self.update_bg_rect)

        if self.synthesizer:
            print("Synthesizer Passed...")

        grid_layout = GridLayout(cols=12, rows=12, spacing=4, size_hint=(1, 1))
        buttons = []
        num_octaves = 12
        notes = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']

        for octave in range(-4, num_octaves - 4):
            for note in notes:
                button = ColorfulButton(note=note, octave=octave, synthesizer=self.synthesizer, stream=self.stream,
                                        size_hint=(1 / 12, 1 / 12))
                button.bind(on_press=lambda btn: btn.play_note())
                buttons.append(button)
                grid_layout.add_widget(button)

        self.add_widget(grid_layout)

    def update_colors(self, *args):
        for button in self.buttons:
            button.draw_background()

    def schedule_color_update(self):
        self.buttons = self.walk(restrict=True, loopback=True)
        Clock.schedule_interval(self.update_colors, 1)


def get_content(synthesizer=None, stream=None):
    return PerformInterface(synthesizer=synthesizer, stream=stream)
