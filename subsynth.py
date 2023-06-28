import numpy as np
import scipy.io.wavfile as wav
import scipy.signal
import sounddevice as sd

class SubtractiveSynthesizer:
    def __init__(self, instrument_file):
        self.load_instrument(instrument_file)
        self.lfo = None
        self.panning_lfo = None
        self.channel_volumes = {}  # Dictionary to store channel volumes
        self.channel_panning = {}  # Dictionary to store channel panning values

    def load_instrument(self, instrument_file):
        # Load and parse the instrument file to extract parameters
        # Here, you would implement the logic to read and parse the .instrument file
        # and store the relevant parameters, such as waveform type, filter type, ADSR values, etc.
        # For simplicity, let's assume we have the following parameters:

        self.waveform_type = "sine"  # Options: "sine", "triangle", "sawtooth", "square", "noise"
        self.filter_type = "lowpass"  # Options: "lowpass", "highpass", "bandpass", "bandreject"
        self.attack_time = 0.1
        self.decay_time = 0.2
        self.sustain_level = 0.6
        self.release_time = 0.3
        self.lfo_attack_time = 0.1
        self.lfo_amplitude = 0.5
        self.lfo_speed = 2.0
        self.lfo_waveform = "sine"  # Options: "sine", "triangle", "sawtooth", "square"
        self.panning_lfo_attack_time = 0.1
        self.panning_lfo_amplitude = 0.5
        self.panning_lfo_speed = 2.0
        self.panning_lfo_waveform = "sine"  # Options: "sine", "triangle", "sawtooth", "square"

        # Additional parameters and settings for your synthesizer can be included here

    def generate_waveform(self, frequency, duration, velocity):
        # Generate the base waveform
        sample_rate = 192000  # Sample rate (adjust if needed)
        num_samples = int(sample_rate * duration)
        t = np.linspace(0, duration, num_samples, False)

        # Create the oscillators (assuming four oscillators)
        oscillators = []
        for _ in range(4):
            if self.waveform_type == "sine":
                oscillator = np.sin(2 * np.pi * frequency * t)
            elif self.waveform_type == "triangle":
                oscillator = np.abs(scipy.signal.sawtooth(2 * np.pi * frequency * t, 0.5))
            elif self.waveform_type == "sawtooth":
                oscillator = scipy.signal.sawtooth(2 * np.pi * frequency * t)
            elif self.waveform_type == "square":
                oscillator = scipy.signal.square(2 * np.pi * frequency * t)
            elif self.waveform_type == "noise":
                oscillator = np.random.uniform(-1, 1, num_samples)
            else:
                raise ValueError(f"Invalid waveform type: {self.waveform_type}")

            oscillators.append(oscillator)

        # Apply panning and velocity with LFO
        pan = self.apply_panning_lfo(t)
        pan_l = np.sqrt(0.5 * (1 - pan))
        pan_r = np.sqrt(0.5 * (1 + pan))
        waveform = np.sum(oscillators) * velocity * np.column_stack((pan_l, pan_r))

        # Apply the ADSR envelope
        envelope = self.apply_adsr_envelope(t)
        waveform *= envelope[:, np.newaxis]

        # Apply the filter
        filtered_waveform = self.apply_filter(waveform)

        return filtered_waveform

    def apply_adsr_envelope(self, t):
        # Generate the ADSR envelope
        sample_rate = 192000
        num_samples = len(t)

        envelope = np.zeros_like(t)
        envelope[:int(self.attack_time * sample_rate)] = np.linspace(0, 1, int(self.attack_time * sample_rate))
        envelope[int(self.attack_time * sample_rate):int((self.attack_time + self.decay_time) * sample_rate)] = \
            np.linspace(1, self.sustain_level, int(self.decay_time * sample_rate))
        envelope[int((self.attack_time + self.decay_time) * sample_rate):-int(self.release_time * sample_rate)] = \
            self.sustain_level
        envelope[-int(self.release_time * sample_rate):] = \
            np.linspace(self.sustain_level, 0, int(self.release_time * sample_rate))

        return envelope

    def apply_filter(self, waveform):
        # Apply the desired filter type
        cutoff_frequency = 8000  # Adjust the cutoff frequency as needed
        order = 4  # Adjust the filter order as needed

        if self.filter_type == "lowpass":
            b, a = scipy.signal.butter(order, cutoff_frequency, btype="lowpass", fs=192000, analog=False, output="ba")
        elif self.filter_type == "highpass":
            b, a = scipy.signal.butter(order, cutoff_frequency, btype="highpass", fs=192000, analog=False, output="ba")
        elif self.filter_type == "bandpass":
            b, a = scipy.signal.butter(order, [cutoff_frequency - 1000, cutoff_frequency + 1000], btype="bandpass",
                                       fs=192000, analog=False, output="ba")
        elif self.filter_type == "bandreject":
            b, a = scipy.signal.butter(order, [cutoff_frequency - 1000, cutoff_frequency + 1000], btype="bandstop",
                                       fs=192000, analog=False, output="ba")
        else:
            raise ValueError(f"Invalid filter type: {self.filter_type}")

        filtered_waveform = scipy.signal.lfilter(b, a, waveform, axis=0)

        return filtered_waveform

    def apply_lfo(self, t):
        # Apply the LFO modulation
        sample_rate = 192000
        lfo = np.zeros_like(t)
        lfo[:int(self.lfo_attack_time * sample_rate)] = np.linspace(0, self.lfo_amplitude,
                                                                     int(self.lfo_attack_time * sample_rate))
        lfo[int(self.lfo_attack_time * sample_rate):] = self.lfo_amplitude * np.sin(
            2 * np.pi * self.lfo_speed * t[int(self.lfo_attack_time * sample_rate):])

        return lfo

    def apply_panning_lfo(self, t):
        # Apply the panning LFO modulation
        sample_rate = 192000
        panning_lfo = np.zeros_like(t)
        panning_lfo[:int(self.panning_lfo_attack_time * sample_rate)] = np.linspace(0, self.panning_lfo_amplitude,
                                                                                     int(
                                                                                         self.panning_lfo_attack_time * sample_rate))
        if self.panning_lfo_waveform == "sine":
            panning_lfo[int(self.panning_lfo_attack_time * sample_rate):] = self.panning_lfo_amplitude * np.sin(
                2 * np.pi * self.panning_lfo_speed * t[
                                                      int(self.panning_lfo_attack_time * sample_rate):])
        elif self.panning_lfo_waveform == "triangle":
            panning_lfo[int(self.panning_lfo_attack_time * sample_rate):] = self.panning_lfo_amplitude * scipy.signal.sawtooth(
                2 * np.pi * self.panning_lfo_speed * t[
                                                      int(self.panning_lfo_attack_time * sample_rate):],
                0.5)
        elif self.panning_lfo_waveform == "sawtooth":
            panning_lfo[int(self.panning_lfo_attack_time * sample_rate):] = self.panning_lfo_amplitude * scipy.signal.sawtooth(
                2 * np.pi * self.panning_lfo_speed * t[
                                                      int(self.panning_lfo_attack_time * sample_rate):])
        elif self.panning_lfo_waveform == "square":
            panning_lfo[int(self.panning_lfo_attack_time * sample_rate):] = self.panning_lfo_amplitude * scipy.signal.square(
                2 * np.pi * self.panning_lfo_speed * t[
                                                      int(self.panning_lfo_attack_time * sample_rate):])
        else:
            raise ValueError(f"Invalid panning LFO waveform: {self.panning_lfo_waveform}")

        return panning_lfo

    def play_note(self, channel, note, velocity):
        # Generate the waveform for the given note parameters
        frequency = self.calculate_frequency(note)
        duration = 1.0  # Adjust the duration as needed

        waveform = self.generate_waveform(frequency, duration, velocity)
        print("Generated waveform.")

        # Save the waveform as a WAV file
        print("Writing WAV file...")
        wav.write('subsynth_output.wav', 192000, waveform)
        print("Wrote WAV file.")

        # Play the audio in real-time using sounddevice
        print("Playing audio...")
        sd.play(waveform, samplerate=192000, blocking=True)
        print("Audio playback complete.")


    def set_channel_volume(self, channel, volume):
        # Set the volume for the given channel
        self.channel_volumes[channel] = volume

    def set_channel_panning(self, channel, panning):
        # Set the panning value for the given channel
        self.channel_panning[channel] = panning

    def calculate_frequency(self, note):
        # Calculate the frequency for a given MIDI note number
        a4_frequency = 440.0  # Frequency of A4 note
        return (a4_frequency / 32) * (2 ** ((note - 9) / 12))
