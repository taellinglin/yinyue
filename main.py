from kivy.app import App
from kivy.lang import Builder
from kivy.factory import Factory

from interfaces.perform import PerformInterface
from interfaces.arrange import ArrangeInterface
from interfaces.mixer import MixerInterface
from interfaces.compose import ComposeInterface
from interfaces.instrument import InstrumentInterface
from interfaces.settings import SettingsInterface

from synthesizers.addsynth import AdditiveSynthesizer
from synthesizers.subsynth import SubtractiveSynthesizer
from synthesizers.modsynth import ModulationSynthesizer
from synthesizers.wavesynth import WavetableSynthesizer
from synthesizers.stringsynth import StringedSynthesizer
from synthesizers.singsynth import SingingSynthesizer
from synthesizers.drumsynth import DrummingSynthesizer

class YinYue(App):
    
    def build(self):
        Factory.register('SettingsInterface', cls=SettingsInterface)
        Factory.register('InstrumentInterface', cls=InstrumentInterface)
        Factory.register('ComposeInterface', cls=ComposeInterface)
        Factory.register('MixerInterface', cls=MixerInterface)
        Factory.register('ArrangeInterface', cls=ArrangeInterface)
        Factory.register('PerformInterface', cls=PerformInterface)
        self.subsynth = SubtractiveSynthesizer('./patches/SubSynth/default.instrument')
        self.addsynth = AdditiveSynthesizer()
        self.modsynth = ModulationSynthesizer('./patches/ModSynth/default.instrument')
        self.addsynth = WavetableSynthesizer('./patches/WaveSynth/default.instrument')
        self.stringsynth = StringedSynthesizer('./patches/SingSynth/default.instrument')
        self.singsynth = SingingSynthesizer('./patches/SingSynth/default.instrument')
        self.drumsynth = DrummingSynthesizer('./patches/DrumSynth/default.instrument')
        Builder.load_file('interfaces/settingsinterface.kv')
        Builder.load_file('interfaces/instrumentinterface.kv')
        Builder.load_file('interfaces/composeinterface.kv')
        Builder.load_file('interfaces/mixerinterface.kv')
        Builder.load_file('interfaces/arrangeinterface.kv')
        Builder.load_file('interfaces/performinterface.kv')
        return Builder.load_file('main.kv')

if __name__ == '__main__':
    YinYue().run()
