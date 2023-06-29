import numpy as np
import sounddevice as sd

class WavetableSynthesizer:
    def __init__(self, sample_rate=44100):
        self._sample_rate = sample_rate
        self._waveform = None
        self._frequency = 440
        self._duration = 1

    @property
    def sample_rate(self):
        return self._sample_rate

    @sample_rate.setter
    def sample_rate(self, value):
        self._sample_rate = value

    @property
    def waveform(self):
        return self._waveform

    def load_waveform(self, waveform):
        self._waveform = waveform

    @property
    def frequency(self):
        return self._frequency

    @frequency.setter
    def frequency(self, value):
        self._frequency = value

    @property
    def duration(self):
        return self._duration

    @duration.setter
    def duration(self, value):
        self._duration = value

    def play(self):
        if self._waveform is None:
            raise ValueError("Waveform not loaded. Please load a waveform.")

        t = np.linspace(0, self._duration, int(self._duration * self._sample_rate), endpoint=False)
        phase = self._frequency * t % 1  # Phase increment for each sample
        indices = np.floor(phase * len(self._waveform)).astype(int)
        output = self._waveform[indices]

        sd.play(output, samplerate=self._sample_rate)
        sd.wait()

    def generate_waveform(self):
        if self._waveform is None:
            raise ValueError("Waveform not loaded. Please load a waveform.")

        t = np.linspace(0, self._duration, int(self._duration * self._sample_rate), endpoint=False)
        phase = self._frequency * t % 1  # Phase increment for each sample
        indices = np.floor(phase * len(self._waveform)).astype(int)
        output = self._waveform[indices]

        return output

# Example usage
if __name__ == "__main__":
    # Create a WavetableSynthesizer instance
    synthesizer = WavetableSynthesizer(sample_rate=44100)

    # Load a waveform (e.g., a sine wave)
    waveform = np.sin(2 * np.pi * np.linspace(0, 1, int(synthesizer.sample_rate)))

    # Load the waveform into the synthesizer
    synthesizer.load_waveform(waveform)

    # Set frequency and duration
    synthesizer.frequency = 440
    synthesizer.duration = 1

    # Play the note
    synthesizer.play()
