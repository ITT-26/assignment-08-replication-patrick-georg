# Constants for the main window

WIDTH = 1280
HEIGHT = 720

CAPTION = "Guitar Input"

BACKGROUND_COLOR = (50, 50, 75)

# Height of the bottom panel in pixels
BOTTOM_PANEL_HEIGHT = 206

# Ratio between top right and top left panels
TOP_RIGHT_RATIO = 0.5

STATES = ["main_menu", "preset_select", "metronome", "tuner"]


RIGHT_IMAGE_DICT = {
    "main_menu": "assets/top_right/music-note.png",
    "preset_select": "assets/top_right/amplifier.png",
    "metronome": "assets/top_right/metronome-tick.png",
    "tuner": "assets/top_right/diapason-tuner.png",
}

RIGHT_IMAGE_BOX_SIZE = 300