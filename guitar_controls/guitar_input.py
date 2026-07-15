import math
import time
from collections import deque

import numpy as np
import sounddevice as sd

from guitar_controls.guitar_input_constants import *

# note names
NOTE_NAMES = ["C", "C#", "D", "D#", "E", "F",
              "F#", "G", "G#", "A", "A#", "B"]


# parabolic interpolation for peak refinement (suggested by ai to make note detection more accurate)
def parabolic_interpolation(y, x):
    if x <= 0 or x >= len(y) - 1:
        return float(x)

    denom = y[x - 1] - 2 * y[x] + y[x + 1]
    if abs(denom) < 1e-12:
        return float(x)

    return x + 0.5 * (y[x - 1] - y[x + 1]) / denom


class GuitarInput:
    def __init__(
        self,
        device_index=None,
        on_pitch=None,
        on_strike=None,
    ):
        # sample rate and block size
        self.sample_rate = SAMPLE_RATE
        self.block_size = BLOCK_SIZE

        # minimum and maximum frequency for pitch detection
        self.fmin = FMIN
        self.fmax = FMAX

        # confidence threshold for pitch detection
        self.confidence_threshold = CONFIDENCE_THRESHOLD

        # threshold for silence
        self.silence_threshold = SILENCE_THRESHOLD

        # threshold for detecting a new stroke
        self.stroke_threshold = STROKE_THRESHOLD

        # jump factor for detecting a new stroke while string is still vibrating -> but players should just mute the string
        self.jump_factor = JUMP_FACTOR

        # debounce time for detecting a new stroke
        self.debounce_seconds = DEBOUNCE_SECONDS

        # strike delay after detecting a new stroke before reporting the pitch
        self.strike_delay_seconds = STRIKE_DELAY_SECONDS

        # timeout for detecting a new stroke after the last stroke
        self.strike_timeout_seconds = STRIKE_TIMEOUT_SECONDS

        # callbacks for pitch and strike events
        self.on_pitch = on_pitch
        self.on_strike = on_strike

        # history of recent audio levels for stroke detection
        self.level_history = deque(maxlen=6)

        # state variables for stroke detection
        self.pending_strike = False

        # time when the current strike started
        self.strike_started_at = 0.0
        self.last_strike_time = -999.0

        # set up audio input stream
        self.stream = sd.InputStream(
            device=device_index,
            channels=1,
            samplerate=self.sample_rate,
            blocksize=self.block_size,
            dtype="float32",
        )

    @staticmethod
    # convert frequency to note name
    def freq_to_note(freq):
        midi = int(round(69 + 12 * math.log2(freq / 440.0)))
        note_name = NOTE_NAMES[midi % 12]
        octave = (midi // 12) - 1
        return f"{note_name}{octave}"

    @staticmethod
    # convert frequency to note name, and cents difference from exact note frequency -> for tuner later
    def freq_to_cents(freq):
        midi = int(round(69 + 12 * math.log2(freq / 440.0)))
        note_name = NOTE_NAMES[midi % 12]
        octave = (midi // 12) - 1
        note_freq = 440.0 * (2 ** ((midi - 69) / 12))
        cents = 1200.0 * math.log2(freq / note_freq)
        return f"{note_name}{octave}", note_freq, cents

    # detect the pitch
    def detect_pitch(self, signal):

        # convert signal to float64 and remove DC offset
        x = signal.astype(np.float64)
        x = x - np.mean(x)

        # if the signal is too quiet, return None
        if np.max(np.abs(x)) < 1e-4:
            return None, 0.0

        # hanning window to reduce spectral leakage (I used it in assignment 2 as well so I hope it helps here too)
        x = x * np.hanning(len(x))

        # autocorrelation method for pitch detection
        autocorrelation = np.correlate(x, x, mode="full")
        autocorrelation = autocorrelation[len(autocorrelation) // 2:]

        # find peak in autocorrelation in the thresholds
        lag_min = int(self.sample_rate / self.fmax)
        lag_max = int(self.sample_rate / self.fmin)

        # check for index bounds and return None if invalid
        if lag_max >= len(autocorrelation):
            lag_max = len(autocorrelation) - 1
        if lag_min >= lag_max:
            return None, 0.0

        # region of the note peak
        region = autocorrelation[lag_min:lag_max]

        # index of peak in the region
        peak_idx = lag_min + int(np.argmax(region))

        # parabolic interpolation for peak refinement
        peak_refined = parabolic_interpolation(autocorrelation, peak_idx)

        # to fix out of bounds error, clamp the peak_refined to be within the valid range of autocorrelation indices
        peak_refined = max(
            1.0, min(float(len(autocorrelation) - 1), peak_refined))

        # no valid peak found, return None
        peak_index = int(round(peak_refined))
        if peak_index < 0 or peak_index >= len(autocorrelation):
            return None, 0.0

        # calculate frequency
        freq = self.sample_rate / peak_refined

        # confidence of the detected pitch based on the autocorrelation value at the peak
        confidence = float(
            autocorrelation[peak_index] / (autocorrelation[0] + 1e-12))
        return freq, confidence

    # update method to read audio data, detect pitch, and handle strike events
    def update(self):

        # read audio data from stream
        indata, overflowed = self.stream.read(self.block_size)
        if overflowed:
            return

        # audio data
        mono = indata[:, 0]

        # calculate RMS level of the audio signal
        level = float(np.sqrt(np.mean(mono.astype(np.float64) ** 2)))
        now = time.time()

        # level to level history for strike detection
        self.level_history.append(level)

        # if the level is below the silence threshold -> no strike detection, return early
        if level < self.silence_threshold:
            return

        # last minimum level in the history for strike detection
        recent_min = min(self.level_history)

        # new strike if the level is above the stroke_threshold and level is more than recent_min * jump_factor and debounce time has passed since last strike
        is_new_strike = (
            level >= self.stroke_threshold
            and level > recent_min * self.jump_factor
            and (now - self.last_strike_time) >= self.debounce_seconds
        )

        # if new strike
        if is_new_strike:

            # strike is pending
            self.pending_strike = True

            # strike started now
            self.strike_started_at = now

            # last strike time is now
            self.last_strike_time = now

            # level history cleared because its a new strike
            self.level_history.clear()

        # detect pitch
        freq, confidence = self.detect_pitch(mono)

        # frequency is valid and confidence is above threshold
        if freq is not None and confidence >= self.confidence_threshold:

            # convert frequency to note name
            note = self.freq_to_note(freq)

            # if pitch callback exists
            if self.on_pitch is not None:
                # do pitch callback with every information
                self.on_pitch(freq, note, confidence)

            # strike event pending
            if self.pending_strike:
                # strike delay time has passed since strike started -> note should be stable enough to report
                if (now - self.strike_started_at) >= self.strike_delay_seconds:

                    # if strike callback exists
                    if self.on_strike is not None:
                        # do strike callback with frequency and note
                        self.on_strike(freq, note)

                    # no strike pending anymore
                    self.pending_strike = False

        # if strike event is pending
        if self.pending_strike:
            # if strike timeout has passed since strike started
            if (now - self.strike_started_at) > self.strike_timeout_seconds:
                # no strike pending anymore
                self.pending_strike = False
