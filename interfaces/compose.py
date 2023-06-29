from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.slider import Slider
from kivy.uix.scrollview import ScrollView


class NoteButton(Button):
    def __init__(self, note, **kwargs):
        super().__init__(**kwargs)
        self.note = note


class ComposeInterface(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "vertical"

        # Create piano keys
        piano_layout = GridLayout(cols=1, spacing=2)
        for note in reversed(range(21, 109)):  # MIDI note numbers for piano keys
            button = NoteButton(note=note, text=str(note), size_hint_y=None, height=30)
            piano_layout.add_widget(button)
        piano_scroll = ScrollView(size_hint=(1, 0.8))
        piano_scroll.add_widget(piano_layout)
        self.add_widget(piano_scroll)

        # Create note grid
        note_grid = GridLayout(cols=32, spacing=2, size_hint=(1, None))
        note_grid.bind(minimum_height=note_grid.setter("height"))

        for _ in range(128):
            note_button = Button(background_color=(0, 0, 1, 1))
            note_grid.add_widget(note_button)

        note_scroll = ScrollView(size_hint=(1, 0.2))
        note_scroll.add_widget(note_grid)
        self.add_widget(note_scroll)

        # Create parameter panel
        parameter_panel = GridLayout(cols=3, size_hint=(1, None), height=100, padding=(10, 10))
        parameter_panel.bind(minimum_height=parameter_panel.setter("height"))

        parameter_panel.add_widget(Label(text="Velocity"))
        velocity_slider = Slider(min=0, max=127, value=64)
        parameter_panel.add_widget(velocity_slider)

        parameter_panel.add_widget(Label(text="Panning"))
        panning_slider = Slider(min=-1, max=1, value=0)
        parameter_panel.add_widget(panning_slider)

        self.add_widget(parameter_panel)


class ComposeApp(App):
    def build(self):
        return PianoRoll()


if __name__ == "__main__":
    ComposeApp().run()
