import numpy as np
from scipy.signal import fftconvolve
from sf2_loader import Sf2


class AdditiveSynthesizer:
    def __init__(self, sf2_file):
        self.sf2_file = sf2_file
        self.patches = {}
        self.polyphony = 4  # Number of simultaneous notes

        # Load samples from SF2 file
        self.load_samples()

    def load_samples(self):
        sf2 = Sf2()
        sf2.load(self.sf2_file)
        for sample_name, sample_data in sf2.sample_data.items():
            self.patches[sample_name] = sample_data

    def generate_patch(self, sample_name, frequencies, amplitudes):
        sample_data = self.patches.get(sample_name)
        if sample_data is None:
            raise ValueError("Sample '{}' not found.".format(sample_name))

        # Normalize amplitudes
        amplitudes = amplitudes / np.max(amplitudes)

        # Initialize the patch
        patch = np.zeros_like(sample_data, dtype=np.float32)

        # Generate additive components
        for freq, amp in zip(frequencies, amplitudes):
            t = np.arange(len(sample_data)) / sample_data.sample_rate
            component = np.sin(2 * np.pi * freq * t)
            patch += amp * component

        # Normalize the patch
        patch /= np.max(patch)

        return patch

    def play_notes(self, sample_name, notes, durations):
        if len(notes) != len(durations):
            raise ValueError("The number of notes and durations must be the same.")

        patch = self.patches.get(sample_name)
        if patch is None:
            raise ValueError("Sample '{}' not found.".format(sample_name))

        # Calculate the total length of the output signal
        total_duration = np.sum(durations)
        total_samples = int(total_duration * patch.sample_rate)

        # Initialize the output signal
        output = np.zeros(total_samples, dtype=np.float32)

        # Iterate over the notes
        for note, duration in zip(notes, durations):
            freq = 440 * (2 ** ((note - 69) / 12))
            t = np.arange(int(duration * patch.sample_rate)) / patch.sample_rate
            component = np.sin(2 * np.pi * freq * t)
            output[:len(component)] += component
            output = np.clip(output, -1.0, 1.0)

        return output


# Example usage
sf2_file = 'Super_Nintendo.sf2'
synth = AdditiveSynthesizer(sf2_file)

# Generate a patch
frequencies = [440, 660, 880]
amplitudes = [1.0, 0.5, 0.3]
patch = synth.generate_patch('sample_name', frequencies, amplitudes)

# Play some notes
notes = [60, 64, 67]  # C4, E4, G4
durations = [1.0, 0.8, 0.6]  # Seconds
output = synth.play_notes('sample_name', notes, durations)
