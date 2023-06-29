from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty

class SettingsInterface(BoxLayout):
    sample_rate_input = ObjectProperty(None)
    midi_in_toggle = ObjectProperty(None)
    midi_in_port_input = ObjectProperty(None)
    midi_out_toggle = ObjectProperty(None)
    midi_out_port_input = ObjectProperty(None)

class SettingsApp(App):
    def build(self):
        return SettingsInterface()


if __name__ == "__main__":
    SettingsApp().run()