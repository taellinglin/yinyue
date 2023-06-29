from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label


class Clip(Button):
    def __init__(self, clip_type, **kwargs):
        super().__init__(**kwargs)
        self.clip_type = clip_type
        self.text = f"{clip_type} Clip"


class TimelineChannel(GridLayout):
    def __init__(self, channel_name, **kwargs):
        super().__init__(**kwargs)
        self.cols = 1
        self.channel_name = channel_name
        self.add_widget(Label(text=channel_name))

    def add_clip(self, clip_type):
        clip = Clip(clip_type)
        self.add_widget(clip)


class ArrangeInterface(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "vertical"
        self.timeline = GridLayout(cols=1, size_hint=(1, 1))
        self.add_widget(self.timeline)

    def add_channel(self, channel_name):
        channel = TimelineChannel(channel_name)
        self.timeline.add_widget(channel)

    def add_clip_to_channel(self, channel_name, clip_type):
        for channel in self.timeline.children:
            if channel.channel_name == channel_name:
                channel.add_clip(clip_type)
                break


class ArrangeApp(App):
    def build(self):
        arrange_interface = ArrangeInterface()
        arrange_interface.add_channel("Channel 1")
        arrange_interface.add_channel("Channel 2")
        arrange_interface.add_clip_to_channel("Channel 1", "Audio")
        arrange_interface.add_clip_to_channel("Channel 1", "MIDI")
        arrange_interface.add_clip_to_channel("Channel 2", "MIDI")
        return arrange_interface


if __name__ == "__main__":
    ArrangeApp().run()
