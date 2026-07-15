import json
import os

import pyglet
from pyglet import shapes
from pyglet import gl

from ui.main_window_constants import *


# will appear on top left
class PresetPanel:
    def __init__(self, presets_path="all_presets.json", on_select=None):

        # rectangle for the panel
        self.rect = (0, 0, 0, 0)

        # callback function to call when a preset is selected
        self.on_select = on_select

        # load presets from json
        self.preset_items = self.load_presets(presets_path)

        # index of currently selected preset
        self.selected_index = 0
        # index of the top visible preset in the list
        self.top_index = 0
        # how many presets are visible at once in the list
        self.visible_count = 7

        # paths for control images
        base_dir = os.path.dirname(os.path.abspath(__file__))
        self.image_paths = {
            "up": os.path.join(base_dir, "assets", "controls", "chevron-up-bg.png"),
            "down": os.path.join(base_dir, "assets", "controls", "chevron-down-bg.png"),
            "enter": os.path.join(base_dir, "assets", "controls", "keyboard-return-bg.png"),
            "escape": os.path.join(base_dir, "assets", "controls", "keyboard-esc-bg.png"),
        }
        self.images = self.load_control_images()

    # sets the rectangle for the preset panel
    def set_rect(self, rect):
        self.rect = rect

    # gets presets from json file
    def load_presets(self, path):

        # check if the file exists
        if not os.path.exists(path):
            return []
        # read the json file and return the list of presets
        try:
            with open(path, "r", encoding="utf-8") as file:
                data = json.load(file)
            return data.get("presets", [])
        except Exception:
            return []

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

    # handles user input while in preset selection mode
    def handle_input(self, symbol):

        # check if there are presets
        if not self.preset_items:
            return None

        # up and down controls
        if symbol == pyglet.window.key.UP:
            self.selected_index = (
                self.selected_index - 1) % len(self.preset_items)

        elif symbol == pyglet.window.key.DOWN:
            self.selected_index = (
                self.selected_index + 1) % len(self.preset_items)

        # select control
        elif symbol == pyglet.window.key.ENTER:
            # get selected preset name
            selected_preset = self.preset_items[self.selected_index]
            if self.on_select is not None:
                # callback function with the selected preset
                self.on_select(selected_preset)
            return selected_preset

        # scroll
        self.update_scroll()

    # scrolls the list
    def update_scroll(self):
        # checks if selected index is smaller than the top index
        if self.selected_index < self.top_index:
            # change top index to selected index
            self.top_index = self.selected_index
        # checks if selected index is larger than the bottom visible index
        elif self.selected_index >= self.top_index + self.visible_count:
            # change top index to show the selected index at the bottom
            self.top_index = self.selected_index - self.visible_count + 1

    # helper method to draw a text label
    def draw_label(self, text, x, y, font_size=14, color=(255, 255, 255, 255), anchor_x="left"):
        pyglet.text.Label(
            text,
            x=x,
            y=y,
            font_size=font_size,
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
        self.draw_label(text, x + 28, y + 10, font_size=12)

    # draw the preset panel
    def draw(self):

        # position and size of the panel
        x, y, w, h = self.rect

        # draw background rectangle
        shapes.Rectangle(x, y, w, h, color=BACKGROUND_COLOR).draw()

        # draw label
        self.draw_label("Preset Select", x + 20, y + h - 40, font_size=16)

        # draw controls
        controls_y = y + h - 95
        self.draw_icon_and_text("up", "Select", x + 20, controls_y)
        self.draw_icon_and_text("down", "Select", x + 20, controls_y - 30)
        self.draw_icon_and_text("enter", "Load", x + 20, controls_y - 60)
        self.draw_icon_and_text(
            "escape", "Return to menu", x + 20, controls_y - 90)

        # error message if no presets are found
        if not self.preset_items:
            self.draw_label(
                "No presets found",
                x + 20,
                y + h - 210,
                font_size=12,
                color=(220, 180, 180, 255),
            )
            return

        # preset list position and row size
        list_start_y = y + h - 230
        row_h = 30

        # start at the top index
        start = self.top_index

        # end at the top index + visible count, but not exceeding the number of presets
        end = min(start + self.visible_count, len(self.preset_items))

        # draw each visible preset in the list
        for row, preset_index in enumerate(range(start, end)):

            # current y position for this row
            row_y = list_start_y - row * row_h

            # check if this preset is selected
            is_selected = preset_index == self.selected_index

            # background rectangle for selected preset
            if is_selected:
                shapes.Rectangle(
                    x + 16,
                    row_y - 14,
                    w - 32,
                    24,
                    color=(90, 90, 120),
                ).draw()

            # draw the preset name
            self.draw_label(
                self.preset_items[preset_index],
                x + 28,
                row_y,
                font_size=12,
            )

        # info text at the bottom to show the current selected index and total number of presets
        info_text = f"{self.selected_index + 1}/{len(self.preset_items)}"
        self.draw_label(
            info_text,
            x + w - 20,
            y + 20,
            font_size=11,
            anchor_x="right",
            color=(180, 180, 180, 255),
        )
