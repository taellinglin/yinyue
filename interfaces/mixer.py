from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label


class Channel(BoxLayout):
    def __init__(self, channel_name, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "vertical"
        self.channel_name = channel_name
        self.add_widget(Label(text=channel_name))
        self.effects_rack = GridLayout(cols=1, spacing=10)
        self.add_widget(self.effects_rack)

    def add_effect(self, effect_name):
        effect_label = Label(text=effect_name)
        self.effects_rack.add_widget(effect_label)


class MixerInterface(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "horizontal"
        self.channels = GridLayout(cols=1, size_hint=(0.7, 1))
        self.effects = GridLayout(cols=1, size_hint=(0.3, 1))
        self.add_widget(self.channels)
        self.add_widget(self.effects)

    def add_channel(self, channel_name):
        channel = Channel(channel_name)
        self.channels.add_widget(channel)

    def add_effect_to_channel(self, channel_name, effect_name):
        for channel in self.channels.children:
            if channel.channel_name == channel_name:
                channel.add_effect(effect_name)
                break

    def add_effect(self, effect_name):
        effect_label = Label(text=effect_name)
        self.effects.add_widget(effect_label)


class MixerApp(App):
    def build(self):
        mixer = MixerInterface()
        mixer.add_channel("Channel 1")
        mixer.add_channel("Channel 2")
        mixer.add_effect_to_channel("Channel 1", "Reverb")
        mixer.add_effect_to_channel("Channel 1", "Delay")
        mixer.add_effect_to_channel("Channel 2", "Compression")
        mixer.add_effect("Master EQ")
        mixer.add_effect("Limiter")
        return mixer


if __name__ == "__main__":
    MixerApp().run()
