import numpy as np
import scipy.io.wavfile as wav
import scipy.signal
import sounddevice as sd
import scipy.signal

class SubtractiveSynthesizer:
    def __init__(self, instrument_file):
        self.load_instrument(instrument_file)
        self.lfo = None
        self.panning_lfo = None
        self.sample_rate = 192000
        self.channel_volumes = {}  # Dictionary to store channel volumes
        self.channel_panning = {}  # Dictionary to store channel panning values

    def load_instrument(self, instrument_file):
        # Load and parse the instrument file to extract parameters
        # Here, you would implement the logic to read and parse the .instrument file
        # and store the relevant parameters, such as waveform type, filter type, ADSR values, etc.
        # For simplicity, let's assume we have the following parameters:
        # Define the oscillator types you want to use
        self.oscillator_types = ["sine", "triangle", "sawtooth", "square"]
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
    def generate_oscillator(self, osc_type, frequency, t):
            if osc_type == "sine":
                return np.sin(2 * np.pi * frequency * t)
            elif osc_type == "triangle":
                return scipy.signal.sawtooth(2 * np.pi * frequency * t, 0.5)
            elif osc_type == "sawtooth":
                return scipy.signal.sawtooth(2 * np.pi * frequency * t)
            elif osc_type == "square":
                return scipy.signal.square(2 * np.pi * frequency * t)
            elif osc_type == "noise":
                return np.random.uniform(-1, 1, len(t))
            else:
                raise ValueError(f"Invalid oscillator type: {osc_type}")
            
    def calculate_envelope(self, duration, velocity):
        """
        Calculate the amplitude envelope of the signal.
        This is a placeholder and should be replaced with actual envelope calculations.
        """
        num_samples = int(self.sample_rate * duration)
        envelope = np.ones(num_samples)  # Replace with actual calculation
        envelope = envelope * velocity / 127.0  # Scale by velocity
        return envelope

    def generate_waveform(self, frequency, duration, velocity):
        # Generate the waveform for the given frequency and duration
        num_samples = int(self.sample_rate * duration)
        t = np.arange(num_samples) / self.sample_rate
                # Print variables for debugging
        print(f"Frequency: {frequency}")
        print(f"Duration: {duration}")
        print(f"Velocity: {velocity}")
        # Generate the oscillators
        oscillators = [
            self.generate_oscillator(osc_type, frequency, t)
            for osc_type in self.oscillator_types
        ]

        # Apply ADSR envelope
        envelope = self.apply_adsr_envelope(duration)

        # Apply velocity scaling
        scaled_envelope = envelope * velocity
        scaled_envelope = self.calculate_envelope(duration, velocity)

        # Apply panning
        pan_l, pan_r = self.calculate_panning(scaled_envelope)

        # Adjust the shape of panning arrays to match the waveform
        #pan_l = np.expand_dims(pan_l, axis=1)
        #pan_r = np.expand_dims(pan_r, axis=1)

        # Combine the oscillators, envelope, velocity, and panning
        scaled_envelope_l = scaled_envelope * pan_l
        scaled_envelope_r = scaled_envelope * pan_r
        waveform = np.sum(oscillators, axis=0)[:, None] * np.stack((scaled_envelope_l, scaled_envelope_r), axis=1)

        return waveform

    
    def calculate_panning(self, scaled_envelope):
        # Panning method implementation. This is a simple example.
        # More complex panning algorithms may require additional parameters and calculations.

        panning_value = 0.5  # Assuming equal panning for left and right channels, you can adjust this as needed.

        # Applying panning using the sine law of panning.
        pan_l = scaled_envelope * np.sqrt(panning_value) 
        pan_r = scaled_envelope * np.sqrt(1-panning_value)

        return pan_l, pan_r

    def apply_adsr_envelope(self, duration):
        sample_rate = 192000
        num_samples = int(sample_rate * duration)
        t = np.linspace(0, duration, num_samples, False)

        envelope = np.zeros(num_samples)

        attack_samples = int(self.attack_time * sample_rate)
        decay_samples = int(self.decay_time * sample_rate)
        release_samples = int(self.release_time * sample_rate)

        print(f"Attack samples: {attack_samples}")
        print(f"Decay samples: {decay_samples}")
        print(f"Release samples: {release_samples}")

        attack_segment = np.linspace(0, 1, attack_samples)
        decay_segment = np.linspace(1, self.sustain_level, decay_samples, endpoint=False)
        release_segment = np.linspace(self.sustain_level, 0, release_samples, endpoint=False)

        print(f"Attack segment shape: {attack_segment.shape}")
        print(f"Decay segment shape: {decay_segment.shape}")
        print(f"Release segment shape: {release_segment.shape}")

        envelope[:attack_samples] = attack_segment

        if decay_samples > 0:
            num_decay_repeats = int(np.ceil(num_samples / decay_samples))
            decay_segment_repeat = np.tile(decay_segment, num_decay_repeats)[:num_samples]
            print(f"Decay segment repeat shape: {decay_segment_repeat.shape}")
            print(f"Decay segment repeat length: {len(decay_segment_repeat)}")

            envelope[attack_samples:attack_samples + decay_samples] = decay_segment_repeat[:decay_samples]

        print(f"Envelope shape: {envelope.shape}")
        print(f"Assigned envelope segment shape: {envelope[attack_samples:attack_samples + decay_samples].shape}")

        if release_samples > 0:
            envelope[-release_samples:] = release_segment

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

        chunk_duration = 1  # Adjust the chunk duration as needed
        chunk_samples = int(chunk_duration * 192000)
        num_chunks = int(duration / chunk_duration)

        print(f"Generating waveform. F: {frequency}, D: {duration}, V: {velocity}")

        for i in range(num_chunks):
            t = np.linspace(0, chunk_duration, chunk_samples, False)
            waveform = self.generate_waveform(frequency, chunk_duration, velocity)

            # Play the audio chunk in real-time using sounddevice
            print(f"Playing audio chunk {i+1}/{num_chunks}...")
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
