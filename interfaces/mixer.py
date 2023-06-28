from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label


def get_content():
    mixer_layout = BoxLayout(orientation='vertical')
    mixer_layout.add_widget(Label(text='Mixer Tab Content'))
    return mixer_layout
