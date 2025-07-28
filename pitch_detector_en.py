import numpy as np
import sounddevice as sd
import time

# == Configuration ==
INPUT_FREQ_FILE = "output_freqs.txt"
SAMPLE_RATE = 11025
FRAME_DURATION = 0.75  # seconds
THRESHOLD_DB = -50     # minimum signal level in dB
ZERO_PAD_FACTOR = 8    # padding multiplier (improves resolution)

# == Load frequency table ==
def load_freq_table(path):
    freq_map = {}
    with open(path, 'r') as f:
        for line in f:
            parts = line.strip().split()
            if len(parts) != 2:
                continue
            note, freq = parts
            freq_map[note] = float(freq)
    return freq_map

# == Find nearest note ==
def find_closest_note(freq, freq_table):
    if freq is None:
        return None, None, None

    min_note = None
    min_diff = float('inf')

    for note, target_freq in freq_table.items():
        if target_freq <= 0:
            continue

    for note, target_freq in freq_table.items():
        if target_freq <= 0 or freq <= 0 or not np.isfinite(freq):
            continue
        cents = 1200 * np.log2(freq / target_freq)
        if abs(cents) < abs(min_diff):
            min_diff = cents
            min_note = note

    if min_note is None:
        return None, None, None

    return min_note, freq_table[min_note], min_diff

# == Peak interpolation ==
def parabolic_interpolation(spectrum, peak_idx):
    if 1 <= peak_idx < len(spectrum) - 1:
        alpha = spectrum[peak_idx - 1]
        beta = spectrum[peak_idx]
        gamma = spectrum[peak_idx + 1]
        p = 0.5 * (alpha - gamma) / (alpha - 2 * beta + gamma)
        return peak_idx + p
    else:
        return peak_idx

# == Low-pass filtering ==
def low_pass_filter(data, cutoff_freq, sample_rate):
    from numpy.fft import rfft, irfft, rfftfreq

    spectrum = rfft(data)
    freqs = rfftfreq(len(data), 1 / sample_rate)
    spectrum[freqs > cutoff_freq] = 0
    filtered = irfft(spectrum)
    return filtered

# == Pitch detection ==
def detect_pitch(data, sample_rate):
    fmin = 24     #~G0
    fmax = 5000   #~E8

    cutoff = 1500
    data = low_pass_filter(data, cutoff, sample_rate)

    window = np.hanning(len(data))
    data = data * window
    data = data - np.mean(data)

    corr = np.correlate(data, data, mode='full')
    corr = corr[len(corr) // 2:]

    n_padded = len(corr) * ZERO_PAD_FACTOR
    corr_padded = np.zeros(n_padded)
    corr_padded[:len(corr)] = corr

    lag_min = int(sample_rate / fmax)
    lag_max = int(sample_rate / fmin)
    if lag_max >= len(corr):
        lag_max = len(corr) - 1

    corr_peak_region = corr_padded[lag_min:lag_max * ZERO_PAD_FACTOR]

    if len(corr_peak_region) == 0:
        return None

    peak_idx = np.argmax(corr_peak_region) + lag_min

    if corr_padded[peak_idx] < 1e-6:
        return None

    peak_idx_interp = parabolic_interpolation(corr_padded, peak_idx)

    pitch_freq = sample_rate / peak_idx_interp
    return pitch_freq

# == Main ==
def main():
    # Use command-line argument if provided
    if len(sys.argv) > 1:
        freq_file = sys.argv[1]
    else:
        freq_file = INPUT_FREQ_FILE

    freq_table = load_freq_table(freq_file)
    print(f"Starting pitch detector using '{freq_file}'... (press Ctrl+C to stop)\n")

    try:
        while True:
            samples = int(SAMPLE_RATE * FRAME_DURATION)
            recording = sd.rec(samples, samplerate=SAMPLE_RATE, channels=1, dtype='float64')
            sd.wait()

            data = recording[:, 0]
            freq = detect_pitch(data, SAMPLE_RATE)

            if freq is None:
                print("No usable sound detected.")
            else:
                note, target_freq, diff_cents = find_closest_note(freq, freq_table)
                if note is None:
                    print("No matching note found in frequency table.")
                else:
                    print(f"{note} ({target_freq:.2f} Hz) | detected: {freq:.2f} Hz | deviation: {diff_cents:+.1f} cent")

            time.sleep(0.05)

    except KeyboardInterrupt:
        print("\nExiting.")

if __name__ == "__main__":
    print("Initializing... Please wait a few seconds.\n", flush=True)
    main()
