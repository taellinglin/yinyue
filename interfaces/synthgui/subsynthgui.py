# synth_gui.py

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.slider import Slider
from kivy.garden.knob import Knob



class SubSynthGUI(BoxLayout):
    def __init__(self, **kwargs):
        super(SubSynthGUI, self).__init__(**kwargs)

        # Create Envelope sliders
        envelope_label = Label(text="Envelope Settings")
        envelope_attack = Knob(min=0, max=1, value=0.5)
        envelope_decay = Knob(min=0, max=1, value=0.5)
        envelope_sustain = Knob(min=0, max=1, value=0.5)
        envelope_release = Knob(min=0, max=1, value=0.5)

        # Create LFO sliders
        lfo_label = Label(text="LFO Settings")
        lfo_frequency = Knob(min=0, max=10, value=5)
        lfo_depth = Knob(min=0, max=1, value=0.5)

        # Add widgets to the layout
        self.add_widget(envelope_label)
        self.add_widget(envelope_attack)
        self.add_widget(envelope_decay)
        self.add_widget(envelope_sustain)
        self.add_widget(envelope_release)
        self.add_widget(lfo_label)
        self.add_widget(lfo_frequency)
        self.add_widget(lfo_depth)
