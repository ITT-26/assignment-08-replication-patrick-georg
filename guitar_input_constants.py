# Values for guitar input

# Sample rate (same as for the audio interface)
SAMPLE_RATE = 48000

# Block size (number of samples per block)
BLOCK_SIZE = 4096

# Minimum and maximum frequency for pitch detection (in Hz)
FMIN = 60.0
FMAX = 500.0

# Confidence threshold for pitch detection (0.0 to 1.0)
CONFIDENCE_THRESHOLD = 0.08

# Silence threshold for detecting a new stroke (0.0 to 1.0)
SILENCE_THRESHOLD = 0.005

# Stroke threshold for detecting a new stroke (0.0 to 1.0)
STROKE_THRESHOLD = 0.015

# Jump factor for detecting a new stroke while string is still vibrating -> lower value -> more sensitive to new strokes
JUMP_FACTOR = 2.5

# Debounce time for detecting a new stroke (in seconds)
DEBOUNCE_SECONDS = 0.18

# strike delay time after detecting a new stroke before reporting the pitch (in seconds)
STRIKE_DELAY_SECONDS = 0.08

# strike timeout for detecting a new stroke after the last stroke (in seconds)
STRIKE_TIMEOUT_SECONDS = 0.35