from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.slider import Slider
from kivy.uix.image import Image

class AddSynthGUI(BoxLayout):
    def __init__(self, **kwargs):
        super(AddSynthGUI, self).__init__(**kwargs)
        self.orientation = 'vertical'
        self.create_chorus_group()
        self.create_reverb_group()
        self.create_partials_group()

    def create_chorus_group(self):
        chorus_group = BoxLayout(orientation='vertical', size_hint=(1, None), height=200)
        chorus_label = Label(text='Chorus Parameters', size_hint=(1, 0.2))
        chorus_group.add_widget(chorus_label)
        chorus_params = ['Phase Offset', 'Rate', 'Depth', 'Mix']
        for param in chorus_params:
            chorus_group.add_widget(Slider(min=0, max=1, value=0.5, size_hint=(1, None), height=40, value_track=True))
        self.add_widget(chorus_group)

    def create_reverb_group(self):
        reverb_group = BoxLayout(orientation='vertical', size_hint=(1, None), height=200)
        reverb_label = Label(text='Reverb Parameters', size_hint=(1, 0.2))
        reverb_group.add_widget(reverb_label)
        reverb_params = ['Decay', 'Impact', 'Tone', 'Size', 'Mix']
        for param in reverb_params:
            reverb_group.add_widget(Slider(min=0, max=1, value=0.5, size_hint=(1, None), height=40, value_track=True))
        self.add_widget(reverb_group)

    def create_partials_group(self):
        partials_group = BoxLayout(orientation='vertical', size_hint=(1, None), height=200)
        partials_label = Label(text='Partials', size_hint=(1, 0.2))
        partials_group.add_widget(partials_label)
        partials_wavetable = Image(source='partials.png')
        partials_group.add_widget(partials_wavetable)
        self.add_widget(partials_group)

    def get_content(self):
        return self

class AddSynthApp(App):
    def build(self):
        return AddSynthGUI()

if __name__ == '__main__':
    AddSynthApp().run()
