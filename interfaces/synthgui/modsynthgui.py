from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.slider import Slider
from kivy.garden.knob import Knob


class ModSynthGUI(BoxLayout):
    def __init__(self, synthesizer, **kwargs):
        super(ModSynthGUI, self).__init__(**kwargs)
        self.synthesizer = synthesizer

        # Create labels and knobs for the parameters
        labels = ['调制指数', '载波频率', '调制器频率', '音程', '攻击时间', '释放时间', '音量']
        getters = [self.synthesizer.get_modulation_index, self.synthesizer.get_carrier_frequency,
                   self.synthesizer.get_modulator_frequency, self.synthesizer.get_detuning,
                   self.synthesizer.get_attack_time, self.synthesizer.get_release_time, self.synthesizer.get_amplitude]
        setters = [self.synthesizer.set_modulation_index, self.synthesizer.set_carrier_frequency,
                   self.synthesizer.set_modulator_frequency, self.synthesizer.set_detuning,
                   self.synthesizer.set_attack_time, self.synthesizer.set_release_time, self.synthesizer.set_amplitude]

        for label, getter, setter in zip(labels, getters, setters):
            self.add_widget(Label(text=label))
            knob = Knob(min=-1, max=1, value=getter(), step=0.01)
            knob.bind(on_release=partial(self.update_parameter, setter, knob))
            self.add_widget(knob)

        # Create play button
        play_button = Button(text='播放', size_hint=(None, None), size=(100, 50))
        play_button.bind(on_release=self.play_synthesizer)
        self.add_widget(play_button)

    def update_parameter(self, setter, knob, *args):
        value = knob.value
        setter(value)

    def play_synthesizer(self, *args):
        self.synthesizer.play()
