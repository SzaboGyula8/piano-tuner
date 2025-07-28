import numpy as np
from scipy.interpolate import PchipInterpolator
import sys

NOTE_NAMES = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'Bb', 'H']

def midi_to_name(midi_num):
    octave = (midi_num // 12) - 1
    name = NOTE_NAMES[midi_num % 12]
    return f"{name}{octave}"

def cent_to_ratio(cent):
    return 2 ** (cent / 1200)

def load_cent_file(path):
    with open(path, 'r') as f:
        return [cent_to_ratio(float(line.strip())) for line in f if line.strip()]

def generate_stretch_function(stretch_ratios):
    midi_points = [21, 24, 36, 48, 60, 72, 84, 96, 108]  # A0, C1–C8
    interpolator = PchipInterpolator(midi_points, stretch_ratios, extrapolate=True)
    return interpolator

def generate_frequency_table(a4_freq, stretch_ratios, temper_ratios, output_path="output_freqs.txt"):
    stretch_func = generate_stretch_function(stretch_ratios)

    with open(output_path, 'w') as f_out:
        for midi in range(7, 109):  # G-1 (7) to C8 (108)
            note = midi_to_name(midi)
            base_freq = a4_freq * 2 ** ((midi - 69) / 12)
            stretch_factor = stretch_func(midi)
            temper_factor = temper_ratios[midi % 12]
            final_freq = base_freq * stretch_factor * temper_factor
            f_out.write(f"{note}\t{final_freq:.6f}\n")

    print(f"Ready: {output_path}")

# === Execution ===
if __name__ == "__main__":
    print("Initializing... Please wait a few seconds.\n")
    if len(sys.argv) >= 2:
        try:
            a4_freq = float(sys.argv[1])
        except ValueError:
            print("Frequency format error. Example: python generate_freq_table.py 435.0")
            sys.exit(1)
    else:
        a4_freq = 440.0  # default if not provided

    stretch_ratios = load_cent_file("stretch_cex.txt")
    temper_ratios = load_cent_file("temper_cex.txt")
    generate_frequency_table(a4_freq, stretch_ratios, temper_ratios)
