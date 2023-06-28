from sf2utils.sf2parse import Sf2File
from pprint import pprint
import sys
import os


def extract_samples(sf2_file, output_folder):
    with open(sf2_file, 'rb') as file:
        sf2 = Sf2File(file)

        # Create the output folder if it doesn't exist
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        # Extract and save the sample data
        for index, sample in enumerate(sf2.samples):
            sample_data = sample.raw_sample_data
            sample_name = sample.name

            # Generate a unique file name for the sample
            sample_filename = f"sample_{index + 1}_{sample_name}.wav"
            sample_filepath = os.path.join(output_folder, sample_filename)

            with open(sample_filepath, 'wb') as sample_file:
                sample_file.write(sample_data)

            print(f"Sample {index + 1}: {sample_filename}")



def generate_yue_file(sf2_file, output_yue_file):
    with open(sf2_file, 'rb') as file:
        sf2 = Sf2File(file)

        # Generate the instrument definitions
        instrument_definitions = []
        for index, instrument in enumerate(sf2.instruments):
            instrument_name = instrument.name
            instrument_definitions.append(f"INSTRUMENT: {index + 1} - {instrument_name}")

        # Write the instrument definitions to the output .yue file
        with open(output_yue_file, 'w') as yue_file:
            yue_file.write('\n'.join(instrument_definitions))

        print(f"YUE file generated: {output_yue_file}")


def print_sf2_info(sf2_file):
    try:
        with open(sf2_file, 'rb') as f:
            sf2 = Sf2File(f)
    except FileNotFoundError:
        raise FileNotFoundError('Error in reading file. Make sure the path is correct and is an sf2 file.')

    print("\n\033[1;32mInfo from file:\033[0m")
    pprint(sf2.info)
    print(f'\n\033[1;32mSample offset (bytes):\033[0m {sf2.sample_offset}')
    print("\n\033[1;32mPresets:\033[0m")
    print("\033[0;36mMore options: \033[0m\n-presets (list preset data)\n-samples (list sample data)")

    if '-presets' in sys.argv:
        print("\n\033[1;32mPresets:\033[0m")
        pprint(sf2.presets)
    if '-samples' in sys.argv:
        print("\n\033[1;32mSamples:\033[0m")
        pprint(sf2.samples)


# Usage
if len(sys.argv) < 2:
    print("Please provide the .sf2 file as an argument.")
else:
    sf2_file = sys.argv[1]
    output_folder = sys.argv[2] if len(sys.argv) > 2 else 'samples'
    output_yue_file = sys.argv[3] if len(sys.argv) > 3 else 'output.yue'

    # Extract samples
    extract_samples(sf2_file, output_folder)

    # Generate .yue file
    generate_yue_file(sf2_file, output_yue_file)

    # Print SF2 file info
    print_sf2_info(sf2_file)
