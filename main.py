from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelHeader
from kivy.core.text import LabelBase
import os
import sys
sys.path.insert(1, './interfaces')
sys.path.insert(2, './synthesizers')
sys.path.insert(3, './utils')
import perform
import arrange
import mixer
import compose
from subsynth import SubtractiveSynthesizer

class YinYue(App):
    def build(self):
        # Set the custom font for Chinese characters
        LabelBase.register(name='ZCoolXiaoWei', fn_regular='./fonts/ZCOOLXiaoWei-Regular.ttf')
        self.synthesizer = SubtractiveSynthesizer('./patches/pad.instrument')
        # Main layout
        main_layout = BoxLayout(orientation='vertical')

        # Content area with tabs
        content = TabbedPanel(do_default_tab=False)

        # Load tab content from separate files
        tabs = [
            {'title': '履行', 'content': 'perform.py'},
            {'title': '安排', 'content': 'arrange.py'},
            {'title': '混合器', 'content': 'mixer.py'},
            {'title': '撰写', 'content': 'compose.py'},
            {'title': '设置', 'content': 'settings.py'}
        ]

        for tab in tabs:
            header = TabbedPanelHeader(text=tab['title'], font_name='ZCoolXiaoWei' )
            content_module = __import__(tab['content'].split('.')[0])
            content_layout = content_module.get_content(self.synthesizer) if content_module.__name__ == 'perform' else content_module.get_content()



            # Call get_content() function from content module
            header.content = content_layout
            content.add_widget(header)

        # Add content to main layout
        main_layout.add_widget(content)

        return main_layout


if __name__ == '__main__':
    YinYue().run()
