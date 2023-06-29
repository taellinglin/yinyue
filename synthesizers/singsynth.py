import numpy as np
import sounddevice as sd

class SingingSynthesizer:
    def __init__(self, sample_rate=44100):
        self.sample_rate = sample_rate
        self.phenomes = []
        self.legato = False

    def set_phenomes(self, phenomes):
        self.phenomes = phenomes

    def set_legato(self, legato):
        self.legato = legato

    def get_phenomes(self):
        return self.phenomes

    def get_legato(self):
        return self.legato

    def generate_frames(self):
        total_frames = int(self.sample_rate * sum(self.phenomes))
        frames = np.zeros(total_frames)

        time = 0.0
        for phenome in self.phenomes:
            duration = self.sample_rate * phenome
            phenome_frames = np.zeros(duration)

            # Perform physical modeling synthesis for the phenome (vocal sounds)
            frequency = self.get_phenome_frequency(phenome)
            synthesized_frames = self.physical_modeling_synthesis(frequency, duration)

            phenome_frames += synthesized_frames

            frames[int(time):int(time + duration)] += phenome_frames

            if self.legato:
                time += duration
            else:
                time = 0.0

        return frames

    def get_phenome_frequency(self, phenome):
        # Calculate the frequency for the given phenome
        # You can use a mapping or formula to determine the frequency based on the phenome
        frequency = ...  # Calculate the frequency based on the phenome
        return frequency

    def physical_modeling_synthesis(self, frequency, duration):
        # Implement your physical modeling synthesis algorithm here
        # Generate the synthesized frames for the given frequency and duration
        # You can use techniques such as Karplus-Strong, waveguide synthesis, or other physical modeling approaches
        synthesized_frames = ...  # Generate the synthesized frames using physical modeling synthesis
        return synthesized_frames

    def play(self):
        frames = self.generate_frames()
        sd.play(frames, samplerate=self.sample_rate)
