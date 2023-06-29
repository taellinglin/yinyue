from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.filechooser import FileChooserListView
from kivy.uix.slider import Slider
from kivy.uix.togglebutton import ToggleButton
import numpy as np
import sounddevice as sd
import scipy.io.wavfile as wavfile

class WaveSynthGUI(BoxLayout):
    def __init__(self, **kwargs):
        super(WaveSynthGUI, self).__init__(**kwargs)

        self.synthesizer = WavetableSynthesizer()

        # Create the file chooser
        self.file_chooser = FileChooserListView()
        self.file_chooser.bind(selection=self.load_waveform)

        # Create the waveform label
        self.waveform_label = Label(text="Waveform: Not Loaded")

        # Create the frequency slider
        self.frequency_slider = Slider(min=0, max=20000, value=self.synthesizer.frequency)
        self.frequency_slider.bind(value=self.update_frequency)

        # Create the duration slider
        self.duration_slider = Slider(min=0, max=10, value=self.synthesizer.duration)
        self.duration_slider.bind(value=self.update_duration)

        # Create the play button
        self.play_button = ToggleButton(text='Play', on_press=self.toggle_playback)

        # Create the load button
        self.load_button = Button(text='Load Waveform', on_release=self.open_file_chooser)

        # Add the widgets to the layout
        self.add_widget(self.file_chooser)
        self.add_widget(self.waveform_label)
        self.add_widget(Label(text="Frequency"))
        self.add_widget(self.frequency_slider)
        self.add_widget(Label(text="Duration"))
        self.add_widget(self.duration_slider)
        self.add_widget(self.play_button)
        self.add_widget(self.load_button)

    def load_waveform(self, instance, value):
        if value:
            waveform_path = value[0]
            self.synthesizer.load_waveform_from_file(waveform_path)
            self.waveform_label.text = f"Waveform: {waveform_path}"
    
    def open_file_chooser(self, instance):
        self.file_chooser.path = '.'
        self.file_chooser.selection = []

    def update_frequency(self, instance, value):
        self.synthesizer.frequency = value

    def update_duration(self, instance, value):
        self.synthesizer.duration = value

    def toggle_playback(self, instance):
        if instance.state == "down":
            self.synthesizer.play()
        else:
            sd.stop()


class WaveSynthApp(App):
    def build(self):
        return WaveSynthGUI()


if __name__ == "__main__":
    WaveSynthApp().run()
