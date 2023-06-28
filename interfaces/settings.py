from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.checkbox import CheckBox
from kivy.uix.slider import Slider

def get_content():
    settings_layout = BoxLayout(orientation='vertical')

    # Settings label
    settings_label = Label(text='Settings', font_name='ZCoolXiaoWei')
    settings_layout.add_widget(settings_label)

    # MIDI Input Devices
    input_devices_label = Label(text='MIDI Input Devices', font_name='ZCoolXiaoWei')
    settings_layout.add_widget(input_devices_label)
    
    # List of input devices
    input_devices = ['Input Device 1', 'Input Device 2', 'Input Device 3']  # Replace with your actual input devices
    for device in input_devices:
        device_layout = BoxLayout(orientation='horizontal')
        
        # Checkbox to enable/disable the device
        device_checkbox = CheckBox(active=True)
        device_layout.add_widget(device_checkbox)
        
        # Device name
        device_label = Label(text=device)
        device_layout.add_widget(device_label)
        
        settings_layout.add_widget(device_layout)

    # MIDI Output Devices
    output_devices_label = Label(text='MIDI Output Devices', font_name='ZCoolXiaoWei')
    settings_layout.add_widget(output_devices_label)
    
    # List of output devices
    output_devices = ['Output Device 1', 'Output Device 2', 'Output Device 3']  # Replace with your actual output devices
    for device in output_devices:
        device_layout = BoxLayout(orientation='horizontal')
        
        # Checkbox to enable/disable the device
        device_checkbox = CheckBox(active=True)
        device_layout.add_widget(device_checkbox)
        
        # Device name
        device_label = Label(text=device)
        device_layout.add_widget(device_label)
        
        settings_layout.add_widget(device_layout)
        
    # Port Number Slider
    port_slider_label = Label(text='Port Number')
    settings_layout.add_widget(port_slider_label)
    
    port_slider = Slider(min=0, max=16, value=1)
    settings_layout.add_widget(port_slider)

    # Tempo Slider
    tempo_slider_label = Label(text='Tempo')
    settings_layout.add_widget(tempo_slider_label)
    
    tempo_slider = Slider(min=0, max=200, value=120)
    settings_layout.add_widget(tempo_slider)

    return settings_layout
