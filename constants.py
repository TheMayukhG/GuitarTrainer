# constants.py

import numpy as np

# Standard guitar string tuning (low E to high E) in Hz
STANDARD_TUNING = {
    "E2": 82.41,
    "A2": 110.00,
    "D3": 146.83,
    "G3": 196.00,
    "B3": 246.94,
    "E4": 329.63
}

# All note names across octaves
NOTE_NAMES = ['C', 'C#', 'D', 'D#', 'E', 'F',
              'F#', 'G', 'G#', 'A', 'A#', 'B']

def freq_to_note_name(freq):
    """Convert frequency to closest note name and octave."""
    if freq <= 0:
        return None, None

    note_num = 12 * np.log2(freq / 440.0) + 69
    note_index = int(round(note_num)) % 12
    octave = int(round(note_num)) // 12 - 1
    name = NOTE_NAMES[note_index]
    return f"{name}{octave}", round(note_num)
