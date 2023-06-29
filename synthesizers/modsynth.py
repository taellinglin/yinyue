import numpy as np
import sounddevice as sd

class ModulationSynthesizer:
    def __init__(self, sample_rate=192000):
        self.sample_rate = sample_rate
        self.notes = []
        self.modulation_index = 1.0
        self.carrier_frequency = 440.0
        self.modulator_frequency = 440.0
        self.detuning = 0.0
        self.attack_time = 0.1
        self.release_time = 0.1
        self.amplitude = 0.8
        self.polyphony = True

    def set_notes(self, notes):
        self.notes = notes

    def set_modulation_index(self, modulation_index):
        self.modulation_index = modulation_index

    def set_carrier_frequency(self, carrier_frequency):
        self.carrier_frequency = carrier_frequency

    def set_modulator_frequency(self, modulator_frequency):
        self.modulator_frequency = modulator_frequency

    def set_detuning(self, detuning):
        self.detuning = detuning

    def set_attack_time(self, attack_time):
        self.attack_time = attack_time

    def set_release_time(self, release_time):
        self.release_time = release_time

    def set_amplitude(self, amplitude):
        self.amplitude = amplitude

    def set_polyphony(self, polyphony):
        self.polyphony = polyphony

    def get_notes(self):
        return self.notes

    def get_modulation_index(self):
        return self.modulation_index

    def get_carrier_frequency(self):
        return self.carrier_frequency

    def get_modulator_frequency(self):
        return self.modulator_frequency

    def get_detuning(self):
        return self.detuning

    def get_attack_time(self):
        return self.attack_time

    def get_release_time(self):
        return self.release_time

    def get_amplitude(self):
        return self.amplitude

    def get_polyphony(self):
        return self.polyphony

    def play(self):
        if self.polyphony:
            # If polyphony is enabled, play multiple notes simultaneously
            frames = self.generate_polyphonic_frames()
        else:
            # If polyphony is disabled, play notes one at a time
            frames = self.generate_monophonic_frames()

        sd.play(frames, samplerate=self.sample_rate)

    def generate_monophonic_frames(self):
        total_frames = int(self.sample_rate * sum(self.notes))
        frames = np.zeros(total_frames)

        phase = 0.0
        time = 0.0
        for note in self.notes:
            duration = self.sample_rate * note
            note_frames = np.zeros(duration)

            modulator = np.sin(2 * np.pi * self.modulator_frequency * np.arange(duration) / self.sample_rate)
            carrier = np.sin(2 * np.pi * (self.carrier_frequency + self.detuning) * np.arange(duration) / self.sample_rate + self.modulation_index * modulator)

            envelope = self.generate_envelope(duration)
            note_frames = envelope * carrier

            frames[time:time + duration] += note_frames
            time += duration

        return frames

    def generate_polyphonic_frames(self):
        total_frames = int(self.sample_rate * max(self.notes))
        frames = np.zeros(total_frames)

        for note in self.notes:
            duration = self.sample_rate * note
            note_frames = np.zeros(duration)

            modulator = np.sin(2 * np.pi * self.modulator_frequency * np.arange(duration) / self.sample_rate)
            carrier = np.sin(2 * np.pi * (self.carrier_frequency + self.detuning) * np.arange(duration) / self.sample_rate + self.modulation_index * modulator)

            envelope = self.generate_envelope(duration)
            note_frames = envelope * carrier

            frames[:duration] += note_frames

        return frames

    def generate_envelope(self, duration):
        envelope = np.ones(duration)
        attack_frames = int(self.sample_rate * self.attack_time)
        release_frames = int(self.sample_rate * self.release_time)

        if attack_frames + release_frames < duration:
            envelope[:attack_frames] = np.linspace(0, 1, attack_frames)
            envelope[-release_frames:] = np.linspace(1, 0, release_frames)

        return envelope
