import numpy as np
import scipy.io.wavfile as wav
import scipy.signal
import sounddevice as sd
import ply.lex as lex
import ply.yacc as yacc

tokens = (
    'OSCILLATOR',
    'COLON',
    'IDENTIFIER',
    'VALUE',
    'LABEL',
)

def t_OSCILLATOR(t):
    r'振荡器[0-9]*:'
    return t

def t_COLON(t):
    r':'
    return t

def t_IDENTIFIER(t):
    r'[^\s:]+'
    return t

def t_VALUE(t):
    r'".*"'
    t.value = t.value.strip('"')
    return t

def t_LABEL(t):
    r'[^\s:]+'
    return t

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

t_ignore = ' \t'  # Ignore spaces and tabs

def t_error(t):
    print(f"Illegal character '{t.value[0]}'")
    t.lexer.skip(1)

lexer = lex.lex()

def p_instrument(p):
    '''instrument : label COLON instrument_body'''
    p[0] = {'title': p[1], 'body': p[3]}

def p_label(p):
    '''label : LABEL'''
    p[0] = p[1]

def p_instrument_body(p):
    '''instrument_body : parameter_list oscillator_list'''
    p[0] = {'parameters': p[1], 'oscillators': p[2]}

def p_parameter_list(p):
    '''parameter_list : parameter parameter_list
                      | empty'''
    if len(p) > 2:
        p[0] = [p[1]] + p[2]
    else:
        p[0] = []

def p_parameter(p):
    '''parameter : label COLON value'''
    p[0] = {p[1]: p[3]}

def p_oscillator_list(p):
    '''oscillator_list : oscillator oscillator_list
                       | empty'''
    if len(p) > 2:
        p[0] = [p[1]] + p[2]
    else:
        p[0] = []

def p_oscillator(p):
    '''oscillator : OSCILLATOR oscillator_body'''
    p[0] = {'type': p[1], 'body': p[2]}

def p_oscillator_body(p):
    '''oscillator_body : parameter_list'''
    p[0] = p[1]

def p_value(p):
    '''value : VALUE'''
    p[0] = p[1]

def p_empty(p):
    '''empty :'''
    pass

def p_error(p):
    print(f"Syntax error at token {p.type}, line {p.lineno}, position {p.lexpos}")

parser = yacc.yacc()

class SubtractiveSynthesizer:
    def __init__(self, instrument_file):
        self.instrument = self.load_instrument(instrument_file)
        self.oscillator_types = ['sine', 'triangle', 'sawtooth', 'square', 'noise' ]
        self.params = self.get_parameters()
        print(self.params)
        print(self.instrument)
        print(self.instrument.get('振荡器'))
        print(f"Oscillator Types: {self.oscillator_types}")
        self.sample_rate = 192000
        self.attack_time = 0.1
        self.sustain_level = 0.5
        self.decay_time = 0.5
        self.release_time = 0.2
        self.channel_panning = [0.5,0.5]
        self.channel_volumes = [0.5,0.5]
        self.current_notes = []

    def load_instrument(self, instrument_file):
        with open(instrument_file, 'r', encoding='utf-8') as f:
            instrument_data = f.read()

        lexer.input(instrument_data)
        tokens = []
        for token in lexer:
            if token is None:
                break
            tokens.append(token)

        return self.parse_instrument(instrument_file)







    def parse_instrument(self, instrument_file):
        with open(instrument_file, 'r', encoding='utf-8') as file:
            data = file.read()

        lexer = lex.lex()
        lexer.input(data)
        tokens = list(lexer)

        instrument = {}
        current_section = instrument
        stack = []

        for token in tokens:
            if token.type == 'SECTION_HEADER':
                section_name = token.value.strip(':')
                current_section[section_name] = {}
                stack.append(current_section)
                current_section = current_section[section_name]
            elif token.type == 'KEY':
                key = token.value.strip(':')
                current_section[key] = None
            elif token.type == 'VALUE':
                value = token.value
                if isinstance(current_section, list):
                    current_section.append(value)
                else:
                    current_section[key] = value
            elif token.type == 'INDENT':
                pass
            elif token.type == 'DEDENT':
                stack.pop()
                current_section = stack[-1]

        return instrument



    def get_parameters(self):
        params = []

        for oscillator in self.instrument.get('oscillators', []):
            params.append(oscillator.get('waveform_type', ''))

        return params



        # Additional parameters and settings for your synthesizer can be included here
    def generate_oscillator(self, osc_type, frequency, t):
            print("Generating oscillator:", osc_type, frequency)
            print(f"Oscillator types: {self.oscillator_types}")

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
        sample_rate = 192000
        num_samples = int(sample_rate * duration)
        t = np.linspace(0, duration, num_samples, False)

        envelope = np.zeros(num_samples)

        attack_samples = int(self.attack_time * sample_rate)
        decay_samples = int(self.decay_time * sample_rate)
        release_samples = int(self.release_time * sample_rate)

        attack_segment = np.linspace(0, 1, attack_samples)
        decay_segment = np.linspace(1, self.sustain_level, decay_samples, endpoint=False)
        release_segment = np.linspace(self.sustain_level, 0, release_samples, endpoint=False)

        envelope[:attack_samples] = attack_segment

        if decay_samples > 0:
            num_decay_repeats = int(np.ceil(num_samples / decay_samples))
            decay_segment_repeat = np.tile(decay_segment, num_decay_repeats)[:num_samples]
            envelope[attack_samples:attack_samples + decay_samples] = decay_segment_repeat[:decay_samples]

        if release_samples > 0:
            envelope[-release_samples:] = release_segment

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
        print(f"Oscillators: {oscillators}")
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
        print(f"np.sum(oscillators, axis=0).shape: {np.sum(oscillators, axis=0).shape}")
        print(f"scaled_envelope_l.shape: {scaled_envelope_l.shape}")
        print(f"scaled_envelope_r.shape {scaled_envelope_r.shape}")
        print(f"np.stack((scaled_envelope_l, scaled_envelope_r), axis=1).shape {np.stack((scaled_envelope_l, scaled_envelope_r), axis=1).shape}")
        oscillators = np.array(oscillators)
        print(f"Oscillators: {oscillators}")
        print(f"Oscillator Shape: {oscillators.shape}")
        oscillators_sum = np.sum(oscillators, axis=0)
        envelope_stack = np.stack((scaled_envelope_l, scaled_envelope_r), axis=-1)
        waveform = np.column_stack((oscillators_sum * envelope_stack[:, 0], oscillators_sum * envelope_stack[:, 1]))


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
        cutoff_frequency = 4000  # Adjust the cutoff frequency as needed
        order = 2  # Adjust the filter order as needed

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
        sample_rate = 192000
        lfo = np.zeros_like(t)
        lfo[:int(self.lfo_attack_time * sample_rate)] = np.linspace(0, self.lfo_amplitude, int(self.lfo_attack_time * sample_rate))
        lfo[int(self.lfo_attack_time * sample_rate):] = self.lfo_amplitude * np.sin(2 * np.pi * self.lfo_frequency * t[int(self.lfo_attack_time * sample_rate):])

        return lfo

    def apply_panning_lfo(self, t):
        sample_rate = 192000
        panning_lfo = np.zeros_like(t)
        panning_lfo[:int(self.panning_attack_time * sample_rate)] = np.linspace(0, self.panning_amplitude, int(self.panning_attack_time * sample_rate))
        if self.panning_waveform == "sine":
            panning_lfo[int(self.panning_attack_time * sample_rate):] = self.panning_amplitude * np.sin(2 * np.pi * self.panning_frequency * t[int(self.panning_attack_time * sample_rate):])
        elif self.panning_waveform == "triangle":
            panning_lfo[int(self.panning_attack_time * sample_rate):] = self.panning_amplitude * scipy.signal.sawtooth(2 * np.pi * self.panning_frequency * t[int(self.panning_attack_time * sample_rate):], 0.5)
        elif self.panning_waveform == "sawtooth":
            panning_lfo[int(self.panning_attack_time * sample_rate):] = self.panning_amplitude * scipy.signal.sawtooth(2 * np.pi * self.panning_frequency * t[int(self.panning_attack_time * sample_rate):])
        elif self.panning_waveform == "square":
            panning_lfo[int(self.panning_attack_time * sample_rate):] = self.panning_amplitude * scipy.signal.square(2 * np.pi * self.panning_frequency * t[int(self.panning_attack_time * sample_rate):])
        else:
            raise ValueError(f"Invalid panning LFO waveform: {self.panning_waveform}")

        return panning_lfo


    def play_note(self, channel, note, velocity):
        # Generate the waveform for the given note parameters
        frequency = self.calculate_frequency(note)
        duration = 1  # Adjust the duration as needed

        chunk_duration = 1  # Adjust the chunk duration as needed
        chunk_samples = int(chunk_duration * 192000)
        num_chunks = int(duration / chunk_duration)

        print(f"Generating waveform. F: {frequency}, D: {duration}, V: {velocity}")

        for i in range(num_chunks):
            t = np.linspace(0, chunk_duration, chunk_samples, False)
            waveform = self.generate_waveform(frequency, chunk_duration, velocity)
            self.current_notes.append(note)
            # Play the audio chunk in real-time using sounddevice
            print(f"Playing audio chunk {i+1}/{num_chunks}...")
            sd.play(waveform, samplerate=192000, blocking=True)

        print("Audio playback complete.")

    def stop_note(self, note):
        self.current_notes.remove(note)

    def set_channel_volume(self, channel, volume):
        # Set the volume for the given channel
        self.channel_volumes[channel] = volume

    def set_channel_panning(self, channel, panning):
        # Set the panning value for the given channel
        self.channel_panning[channel] = panning

    def calculate_frequency(self, note):
        # Calculate the frequency for a given note based on A4 = 440 Hz
        a4_frequency = 440.0  # Frequency of A4 note
        return a4_frequency * (2 ** ((note - 69) / 12))
    def set_parameter(self, parameter, value):
        setattr(self, parameter, value)
    def get_parameter(self, parameter):
        # Get the value of the specified parameter
        value = self.instrument
        for param in parameter.split('.'):
            value = value.get(param)
            if value is None:
                break
        return value
    
    def set_attack_time(self, attack_time):
        # Set the attack time in seconds
        self.attack_time = attack_time

    def get_attack_time(self):
        # Get the attack time in seconds
        return self.attack_time