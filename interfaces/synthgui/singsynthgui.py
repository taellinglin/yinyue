from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.switch import Switch
from kivy.uix.slider import Slider
from kivy.garden.knob import Knob


class SingSynthGUI(BoxLayout):
    def __init__(self, synthesizer, **kwargs):
        super(SingSynthGUI, self).__init__(**kwargs)
        self.orientation = "vertical"
        self.synthesizer = synthesizer

        # Create controls for phenomes
        phenomes_label = Label(text="Phenomes")
        self.add_widget(phenomes_label)
        for phenome in self.synthesizer.get_phenomes():
            knob = Knob(min=0, max=10, value=phenome)
            knob.bind(value=self.update_phenome)
            self.add_widget(knob)

        # Create control for legato
        legato_label = Label(text="Legato")
        self.add_widget(legato_label)
        legato_switch = Switch(active=self.synthesizer.get_legato())
        legato_switch.bind(active=self.update_legato)
        self.add_widget(legato_switch)

    def update_phenome(self, knob, value):
        # Update the phenome value in the synthesizer
        index = self.children.index(knob) - 1  # Subtract 1 to account for the label
        self.synthesizer.set_phenome(index, value)

    def update_legato(self, switch, active):
        # Update the legato mode in the synthesizer
        self.synthesizer.set_legato(active)
