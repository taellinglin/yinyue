from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.slider import Slider
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.dropdown import DropDown


class StringSynthGUI(BoxLayout):
    def __init__(self, **kwargs):
        super(StringSynthGUI, self).__init__(**kwargs)

        self.orientation = 'vertical'

        # Create parameter labels
        driver_label = Label(text='Driver:')
        body_material_label = Label(text='Body Material:')
        body_dimensions_label = Label(text='Body Dimensions:')
        body_acoustics_label = Label(text='Body Acoustics:')
        string_material_label = Label(text='String Material:')
        string_tension_label = Label(text='String Tension:')
        fretless_label = Label(text='Fretless:')

        # Create parameter selectors and switches
        self.driver_dropdown = DropDown()
        drivers = ['pluck', 'strum', 'slap', 'tap', 'bowed', 'struck']
        for driver in drivers:
            button = ToggleButton(text=driver, group='driver', state='down')
            self.driver_dropdown.add_widget(button)
        self.driver_button = ToggleButton(text='pluck', group='driver', state='down')
        self.driver_button.bind(on_release=self.driver_dropdown.open)

        self.body_material_dropdown = DropDown()
        body_materials = ['wood', 'metal', 'plastic']
        for material in body_materials:
            button = ToggleButton(text=material, group='body_material', state='down')
            self.body_material_dropdown.add_widget(button)
        self.body_material_button = ToggleButton(text='wood', group='body_material', state='down')
        self.body_material_button.bind(on_release=self.body_material_dropdown.open)

        self.body_dimensions_slider = Slider(min=0, max=100, value=50)
        self.body_acoustics_slider = Slider(min=0, max=100, value=50)

        self.string_material_dropdown = DropDown()
        string_materials = ['steel', 'nylon', 'gut']
        for material in string_materials:
            button = ToggleButton(text=material, group='string_material', state='down')
            self.string_material_dropdown.add_widget(button)
        self.string_material_button = ToggleButton(text='steel', group='string_material', state='down')
        self.string_material_button.bind(on_release=self.string_material_dropdown.open)

        self.string_tension_dropdown = DropDown()
        string_tensions = ['standard', 'low', 'high']
        for tension in string_tensions:
            button = ToggleButton(text=tension, group='string_tension', state='down')
            self.string_tension_dropdown.add_widget(button)
        self.string_tension_button = ToggleButton(text='standard', group='string_tension', state='down')
        self.string_tension_button.bind(on_release=self.string_tension_dropdown.open)

        self.fretless_switch = ToggleButton(text='Off', group='fretless', state='normal')

        # Add widgets to the layout
        self.add_widget(driver_label)
        self.add_widget(self.driver_button)
        self.add_widget(body_material_label)
        self.add_widget(self.body_material_button)
        self.add_widget(body_dimensions_label)
        self.add_widget(self.body_dimensions_slider)
        self.add_widget(body_acoustics_label)
        self.add_widget(self.body_acoustics_slider)
        self.add_widget(string_material_label)
        self.add_widget(self.string_material_button)
        self.add_widget(string_tension_label)
        self.add_widget(self.string_tension_button)
        self.add_widget(fretless_label)
        self.add_widget(self.fretless_switch)

    def get_params(self):
        params = {}
        params['driver'] = self.driver_button.text
        params['body_material'] = self.body_material_button.text
        params['body_dimensions'] = self.body_dimensions_slider.value
        params['body_acoustics'] = self.body_acoustics_slider.value
        params['string_material'] = self.string_material_button.text
        params['string_tension'] = self.string_tension_button.text
        params['fretless'] = self.fretless_switch.state == 'down'
        return params
