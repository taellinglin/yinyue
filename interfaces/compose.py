from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label


def get_content():
    composition_layout = BoxLayout(orientation='vertical')
    composition_layout.add_widget(Label(text='Composition Tab Content'))
    return composition_layout
