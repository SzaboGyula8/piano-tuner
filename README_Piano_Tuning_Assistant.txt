Piano Tuning Assistant – Project Overview
=========================================

This is a two-part piano tuning toolset designed for accurate and efficient
acoustic piano tuning. The tools are implemented in Python, and run either
in a Python environment or as Windows-compatible executable files (EXE).

------------------------------------------------------------
PROJECT PURPOSE
------------------------------------------------------------

Many piano tuning apps are limited by fixed temperaments and smartphone UI
constraints. This project provides an alternative that:

- Works with custom temperaments and stretch tunings.
- Is fully transparent and editable by the user.
- Runs comfortably on laptops, with stable detection and clear output.
- Can be integrated into a personal tuning workflow.

------------------------------------------------------------
COMPONENTS
------------------------------------------------------------

The project consists of two main components:

1. Frequency Table Generator  
   ---------------------------
   This script calculates the full 88-key frequency table based on:

   - A user-defined **stretch curve** (9 values: A0, C1–C8).
   - A **temperament pattern** (12 values in cents).
   - A specified **A4 base frequency** (e.g. 440.0 Hz).

   Output: A simple text file listing all pitch names and corresponding frequencies.

2. Real-Time Pitch Detector  
   ---------------------------
   This script uses your microphone to analyze input sound in real-time.
   It matches the detected dominant frequency to the closest note from
   the frequency table and shows the difference in **cents** (±).

   Input: A frequency table file (output from component 1).  
   Output: Console messages, one line every 0.75s.

------------------------------------------------------------
WORKFLOW
------------------------------------------------------------

1. Create the `temperament.txt` and `stretch.txt` files.
2. Run the generator script to produce `output_freqs.txt`.
3. Use the pitch detector to tune each key using your ears + visual guidance.
4. Optionally, rename and store multiple tuning tables for different purposes.
   You can specify the filename as a command-line argument to the tuning tool.

   Example:

       python pitch_detector_en.py my_tuning_table.txt

If no argument is given, the program uses `output_freqs.txt` by default.

------------------------------------------------------------
FILE STRUCTURE
------------------------------------------------------------

- `generate_freq_table.py`         ← Frequency table generator (Python)
- `pitch_detector_en.py`           ← Real-time pitch detection (Python)
- `output_freqs.txt`               ← Generated frequency table
- `temperament.txt`                ← 12-tone temperament description
- `stretch.txt`                    ← 9-point stretch curve
- `README_freqgen.txt`             ← Readme for the generator
- `README_detector.txt`            ← Readme for the pitch detector
- `README.txt` or MAIN_README.txt  ← This file

Executable versions of the `.py` scripts may also be included:

- `generate_freq_table.exe`
- `pitch_detector_en.exe`

These require no Python installation and run directly under Windows.

------------------------------------------------------------
SYSTEM REQUIREMENTS
------------------------------------------------------------

- Python 3.8+ (only needed for source-based usage)
- Dependencies: numpy, scipy, sounddevice

For EXE usage: Windows 10+ (x64)

------------------------------------------------------------
LICENSE
------------------------------------------------------------

MIT License — Free to use, modify, and share.

------------------------------------------------------------
TARGET USERS
------------------------------------------------------------

- Piano tuners who prefer using a **laptop over a phone**.
- Tuners interested in **non-equal** or historical temperaments.
- Users who want **fine control** over stretch tuning.
- Anyone needing a **simple and stable** frequency-based tuner.

