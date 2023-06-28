from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label


def get_content():
    arrangement_layout = BoxLayout(orientation='vertical')
    arrangement_layout.add_widget(Label(text='Arrangement Tab Content'))
    return arrangement_layout
