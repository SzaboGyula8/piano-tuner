Frequency Table Generator for Custom Tuning
===========================================

This script creates a pitch frequency table combining pitch stretch and 
non-equal temperament, both defined via input files in cents.

Files:
------

- generate_freq_table.py     # This script
- stretch_cex.txt            # Stretch values in cents (one per pitch range)
- temper_cex.txt             # Temperament values in cents (12 values, one octave)
- output_freqs.txt           # Output: one line per note with tuned frequency

How It Works:
-------------

- A4 base frequency (default: 435.0 Hz) can be overridden via command line.
- `stretch_cex.txt` is interpolated across the keyboard range using PCHIP.
- `temper_cex.txt` is repeated for each octave.
- Final frequency is calculated as:

    final_freq = base_freq * stretch_factor * temperament_factor

  where:
    - base_freq = A4 * 2^((midi - 69) / 12)
    - stretch_factor = interpolated ratio from stretch_cex.txt
    - temperament_factor = ratio from temper_cex.txt

Input Format:
-------------

- `stretch_cex.txt`:
    A list of values in cents, one per fixed MIDI point:
    (A0, C1, C2, C3, C4, C5, C6, C7, C8)

- `temper_cex.txt`:
    Exactly 12 lines, one per chromatic pitch class from C to B (H in German),
    repeating across octaves.

Usage:
------

  python generate_freq_table.py 434.0

  # If no parameter is given, defaults to 435.0 Hz.

Output:
-------

- Writes to `output_freqs.txt` with the format:

    C3     130.787654
    C#3    138.526342
    D3     146.813023
    ...
    C8     4186.009045

Dependencies:
-------------

- numpy
- scipy

Install with:

  pip install numpy scipy

License:
--------

MIT or Public Domain – use freely for education, research, or tuning tools.
