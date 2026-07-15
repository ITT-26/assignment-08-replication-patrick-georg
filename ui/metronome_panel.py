import os
import time
import winsound

import pyglet
from pyglet import shapes
from pyglet import gl

from ui.main_window_constants import *


# will appear on top left
class MetronomePanel:
    def __init__(self, bpm=120):

        # rectangle for the panel
        self.rect = (0, 0, 0, 0)

        # start bpm
        self.bpm = bpm

        # if the metronome is running or not
        self.running = False

        # time until the next flash (in seconds)
        self.flash_until = 0.0

        # control images
        base_dir = os.path.dirname(os.path.abspath(__file__))
        self.image_paths = {
            "up": os.path.join(base_dir, "assets", "controls", "chevron-up-bg.png"),
            "down": os.path.join(base_dir, "assets", "controls", "chevron-down-bg.png"),
            "double_up": os.path.join(base_dir, "assets", "controls", "chevron-double-up-bg.png"),
            "double_down": os.path.join(base_dir, "assets", "controls", "chevron-double-down-bg.png"),
            "enter": os.path.join(base_dir, "assets", "controls", "keyboard-return-bg.png"),
        }
        self.images = self.load_control_images()

        # values for the metronome sound
        self.click_length_s = 0.05
        self.next_sound_allowed_at = 0.0
        self.sound_path = os.path.join(base_dir, "assets", "sound", "beep.wav")


    # loads control images from the specified paths and returns a dictionary of loaded images
    def load_control_images(self):
        # make dict for images
        images = {}
        # get the base directory of the image
        for name, full_path in self.image_paths.items():
            # load image and store it in dict
            try:
                images[name] = pyglet.image.load(full_path)
            except Exception:
                images[name] = None
        return images

    # sets the rectangle for the metronome panel
    def set_rect(self, rect):
        self.rect = rect

    # change the bpm
    def change_bpm(self, delta):
        # changes the bpm value with min and max (30-300)
        self.bpm = max(30, min(300, self.bpm + delta))
        # if it is running, restart the metronome to apply the new bpm
        if self.running:
            self.stop()
            self.start()

    # starts the metronome
    def start(self):
        # don't start if already running
        if self.running:
            return
        # set interval for the metronome ticks based on bpm
        pyglet.clock.schedule_interval(self.tick, 60.0 / self.bpm)
        self.running = True

    # stops the metronome
    def stop(self):
        # cant stop if not running
        if not self.running:
            return
        
        # stop the metronome ticks
        pyglet.clock.unschedule(self.tick)
        self.running = False

    # start if not running, stop if running
    def toggle(self):
        if self.running:
            self.stop()
        else:
            self.start()

    # called every metronome tick
    def tick(self, dt):
        now = time.perf_counter()
        if now < self.next_sound_allowed_at:
            return
        self.next_sound_allowed_at = now + self.click_length_s

        winsound.PlaySound(
            self.sound_path,
            winsound.SND_FILENAME | winsound.SND_ASYNC | winsound.SND_NODEFAULT,
        )

    # helper method to draw a text label
    def draw_label(self, text, x, y, size=14, color=(255, 255, 255, 255), anchor_x="left"):
        pyglet.text.Label(
            text,
            x=x,
            y=y,
            font_size=size,
            color=color,
            anchor_x=anchor_x,
            anchor_y="center",
        ).draw()

    # helper method to draw an image and text next to it
    def draw_icon_and_text(self, image_name, text, x, y):

        # get image
        image = self.images.get(image_name)

        # for transparency in images
        gl.glEnable(gl.GL_BLEND)
        gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)

        # draw image and text
        if image is not None:
            image.blit(x, y, width=20, height=20)
        self.draw_label(text, x + 28, y + 10, size=14)

    # draw the metronome panel
    def draw(self):

        # position and size of the panel
        x, y, w, h = self.rect

        # background rectangle
        shapes.Rectangle(x, y, w, h, color=BACKGROUND_COLOR).draw()

        # draw labels
        self.draw_label("Metronome", x + 20, y + h - 40, size=16)
        self.draw_label(f"{self.bpm} BPM", x + 20, y + h - 110, size=32)

        # draw controls
        controls_y = y + h - 190
        self.draw_icon_and_text("up", "+1", x + 20, controls_y)
        self.draw_icon_and_text("down", "-1", x + 20, controls_y - 35)
        self.draw_icon_and_text("double_up", "+5", x + 20, controls_y - 70)
        self.draw_icon_and_text("double_down", "-5", x + 20, controls_y - 105)
        self.draw_icon_and_text("enter", "start/stop", x + 20, controls_y - 140)

        # circle for the metronom flash
        circle_x = x + w - 110
        circle_y = y + h - 120


        # set the color of the circle based on whether it is running or not
        color = (80, 200, 120) if self.running else (80, 80, 80)

        # draw circle
        shapes.Circle(circle_x, circle_y, 28, color=color).draw()