from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.slider import Slider
from kivy.uix.switch import Switch
from kivy.uix.spinner import Spinner
from kivy.uix.widget import Widget
from kivy.uix.button import Button


class DrumSynthGUI(BoxLayout):
    def __init__(self, synthesizer, **kwargs):
        super(DrumSynthGUI, self).__init__(**kwargs)
        self.synthesizer = synthesizer

        # Create labels and knobs for each parameter
        self.create_parameter_widgets()

        # Add parameter widgets to the layout
        self.add_parameter_widgets()

    def create_parameter_widgets(self):
        self.param_widgets = {}

        # Envelope Parameters
        self.create_label_widget('Envelope Parameters')
        self.create_knob_widget('Attack', 'envelope_attack', 0.01, 0.1)
        self.create_knob_widget('Decay', 'envelope_decay', 0.1, 0.5)
        self.create_knob_widget('Sustain', 'envelope_sustain', 0.6, 1.0)
        self.create_knob_widget('Release', 'envelope_release', 0.1, 0.5)

        # Drum Parameters
        self.create_label_widget('Drum Parameters')
        self.create_spinner_widget('Impact', 'impact', ['mallet', 'hand', 'brush', 'scrape', 'roll', 'pad'])
        self.create_spinner_widget('Tension', 'tension', ['loose', 'medium', 'tight'])
        self.create_spinner_widget('Material', 'material', ['wood', 'steel', 'skin', 'rubber', 'plastic'])
        self.create_spinner_widget('Size', 'size', ['small', 'medium', 'large'])

    def create_label_widget(self, text):
        label = Label(text=text)
        self.add_widget(label)

    def create_knob_widget(self, label_text, param_name, min_value, max_value):
        knob_label = Label(text=label_text)
        knob = Slider(min=min_value, max=max_value, value=self.synthesizer.__getattribute__(param_name))
        knob.bind(value=lambda instance, value, param_name=param_name: self.on_knob_change(param_name, value))
        self.param_widgets[param_name] = knob

        knob_layout = BoxLayout(orientation='vertical')
        knob_layout.add_widget(knob_label)
        knob_layout.add_widget(knob)

        self.add_widget(knob_layout)

    def create_spinner_widget(self, label_text, param_name, values):
        spinner_label = Label(text=label_text)
        spinner = Spinner(text=self.synthesizer.__getattribute__(param_name), values=values)
        spinner.bind(text=lambda instance, value, param_name=param_name: self.on_spinner_change(param_name, value))
        self.param_widgets[param_name] = spinner

        spinner_layout = BoxLayout(orientation='vertical')
        spinner_layout.add_widget(spinner_label)
        spinner_layout.add_widget(spinner)

        self.add_widget(spinner_layout)

    def add_parameter_widgets(self):
        for param_widget in self.param_widgets.values():
            self.add_widget(param_widget)

    def on_knob_change(self, param_name, value):
        self.synthesizer.__setattr__(param_name, value)

    def on_spinner_change(self, param_name, value):
        self.synthesizer.__setattr__(param_name, value)
