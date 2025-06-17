# tuner_utils.py

import numpy as np
from constants import freq_to_note_name, NOTE_NAMES

A4_FREQ = 440.0  # Standard pitch

def freq_to_midi_number(freq):
    # Convert frequency to the closest MIDI number.
    return int(round(12 * np.log2(freq / A4_FREQ) + 69))

def midi_number_to_freq(midi_number):
    # Convert MIDI number back to frequency.
    return A4_FREQ * (2 ** ((midi_number - 69) / 12))

def get_pitch_difference(target_freq, played_freq):
#    Return semitone and cent difference between played and target.
    if played_freq <= 0:
        return None, None

    target_midi = 12 * np.log2(target_freq / A4_FREQ) + 69
    played_midi = 12 * np.log2(played_freq / A4_FREQ) + 69

    semitone_diff = round(played_midi - target_midi)
    cent_diff = int((played_midi - target_midi) * 100)

    return semitone_diff, cent_diff

def is_pitch_close(target_freq, played_freq, threshold_cents=50):
    # Returns True if within threshold_cents of target_freq.
    _, cents = get_pitch_difference(target_freq, played_freq)
    return abs(cents) <= threshold_cents

