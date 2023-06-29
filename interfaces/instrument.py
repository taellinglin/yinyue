from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.carousel import Carousel
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.graphics import Color, Rectangle


class InstrumentInterface(BoxLayout):
    def __init__(self, **kwargs):
        super(InstrumentInterface, self).__init__(**kwargs)

    def select_synth(self, synth_name):
        # Remove existing instrument panels
        self.carousel.clear_widgets()

        # Create and add the selected synthesizer's GUI panel
        if synth_name == 'SubSynth':
            self.carousel.add_widget(SubSynthGUI())
        elif synth_name == 'AddSynth':
            self.carousel.add_widget(AddSynthGUI())
        elif synth_name == 'StringSynth':
            self.carousel.add_widget(StringSynthGUI())
        elif synth_name == 'DrumSynth':
            self.carousel.add_widget(DrumSynthGUI())
        elif synth_name == 'WaveSynth':
            self.carousel.add_widget(WaveSynthGUI())
        elif synth_name == 'ModSynth':
            self.carousel.add_widget(ModSynthGUI())
        elif synth_name == 'SingSynth':
            self.carousel.add_widget(SingSynthGUI())


def get_content(self, synthesizer=None):
    instrument_layout = InstrumentInterface()

    return instrument_layout


class InstrumentInterfaceApp(App):
    def build(self):
        return get_content()


if __name__ == "__main__":
    InstrumentInterfaceApp().run()
