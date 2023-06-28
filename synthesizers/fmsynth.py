import numpy as np
import sounddevice as sd

class FMSynth:
    def __init__(self, sample_rate=44100):
        self.sample_rate = sample_rate
        self.tremolo_frequency = 6.0

    def create_note(self, frequency, duration, velocity):
        # Create time array
        t = np.linspace(0, duration, int(self.sample_rate * duration), False)

        # Adjust decay_rate based on the duration
        decay_rate = 1.0 / duration

        # Create audio components
        carrier = np.sin(frequency * t * 2 * np.pi)
        modulator = np.sin(self.tremolo_frequency * t * 2 * np.pi)
        envelope = np.exp(-decay_rate * t)

        # Combine components to make final audio wave
        audio_wave = velocity * envelope * (carrier + carrier * modulator)

        return audio_wave

    def play_chord(self, notes):
        # Get the maximum duration to size the audio_wave correctly
        max_duration = max(note['duration'] for note in notes)

        # Initialize audio_wave to have the correct size
        audio_wave = np.zeros(int(self.sample_rate * max_duration))

        # Add the note for each frequency to audio_wave
        for note in notes:
            note_wave = self.create_note(note['frequency'], note['duration'], note['velocity'])
            audio_wave[:len(note_wave)] += note_wave

        # Make sure audio_wave is within -1 to 1 to prevent clipping
        audio_wave *= 1.0 / np.max(np.abs(audio_wave))

        # Play the sound
        sd.play(audio_wave, self.sample_rate)

        # Wait for the sound to finish playing
        sd.wait()
