# Constants for the main window

WIDTH = 1280
HEIGHT = 720

CAPTION = "Guitar Input"

BACKGROUND_COLOR = (50, 50, 75)

# Height of the bottom panel in pixels
BOTTOM_PANEL_HEIGHT = 206

# Ratio between top right and top left panels
TOP_RIGHT_RATIO = 0.5


# states for main window
STATES = ["main_menu", "preset_select", "metronome", "tuner"]


# Dict for images on right panel
RIGHT_IMAGE_DICT = {
    "main_menu": "assets/top_right/music-note.png",
    "preset_select": "assets/top_right/amplifier.png",
    "metronome": "assets/top_right/metronome-tick.png",
    "tuner": "assets/top_right/diapason-tuner.png",
}


# Dict for images on bottom panel
BOTTOM_PANEL_IMAGE_DICT = {
    "left": {
        "main_menu": "assets/bottom/fretboard_left_main.png",
        "preset_select": "assets/bottom/fretboard_left_preset.png",
        "metronome": "assets/bottom/fretboard_left_metronome.png",
        "tuner": "assets/bottom/fretboard_left_tuner.png",
        "locked": "assets/bottom/fretboard_left_locked.png",
    },
    "right": {
        "main_menu": "assets/bottom/fretboard_right_main.png",
        "preset_select": "assets/bottom/fretboard_right_preset.png",
        "metronome": "assets/bottom/fretboard_right_metronome.png",
        "tuner": "assets/bottom/fretboard_right_tuner.png",
        "locked": "assets/bottom/fretboard_right_locked.png",
    },
}

RIGHT_IMAGE_BOX_SIZE = 300
