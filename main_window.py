import os
import pyglet
from pyglet import shapes
from pyglet import gl
from pyglet.window import key

from guitar_rig_preset_selector import GuitarRigPresetSelector
from tuner_panel import TunerPanel
from metronome_panel import MetronomePanel
from preset_panel import PresetPanel

from controller import GuitarController

from main_window_constants import *


class MainWindow(pyglet.window.Window):
    def __init__(self, device_index=None, handedness="right"):

        # for transparency
        gl.glEnable(gl.GL_BLEND)
        gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)

        # handness for controller visualization
        self.handedness = handedness

        # device index
        self.device_index = device_index

        # for selecting presets
        self.selector = GuitarRigPresetSelector()

        # Guitar controller
        self.controller = GuitarController(device_index=device_index)

        # left panels
        self.tuner_panel = TunerPanel(device_index=device_index)
        self.metronome_panel = MetronomePanel(bpm=120)
        self.preset_panel = PresetPanel(on_select=self.on_preset_selected)

        # padding and gap for layout
        self.padding = 12
        self.gap = 10

        # layout parameters for placing the screens
        self.bottom_height = BOTTOM_PANEL_HEIGHT
        self.top_right_ratio = TOP_RIGHT_RATIO

        # rectangles for the panels
        self.bottom_rect = (0, 0, 0, 0)
        self.top_left_rect = (0, 0, 0, 0)
        self.top_right_rect = (0, 0, 0, 0)

        # current screen state
        self.current_screen = "main_menu"

        # options for main menu and selected index
        self.menu_items = ["Presets", "Metronome"]
        self.selected_index = 0

        # flag if guitar controller is locked
        self.locked = False

        # images for the right panel depending on current screen
        self.right_image_paths = RIGHT_IMAGE_DICT
        self.right_images = {}
        self.load_right_images()

        # super this late because it crashes otherwise (some pyglet issue with the setup window)
        super().__init__(WIDTH, HEIGHT, caption=CAPTION, resizable=False)

        # update layout and start the controller
        self.update_layout(self.width, self.height)
        self.controller.start()

    # callback for when a preset is selected
    def on_preset_selected(self, selected_preset):
        self.selector.select_preset_by_name(selected_preset)
        print("Selected preset:", selected_preset)

    # loads the images for right panel
    def load_right_images(self):

        # dict for images
        self.right_images = {}

        # directory of the current file
        base_dir = os.path.dirname(os.path.abspath(__file__))

        # go through each screen state and corresponding image path
        for screen, rel_path in self.right_image_paths.items():

            # get the full path of the image
            full_path = os.path.join(base_dir, rel_path)

            # error message if the image is missing
            if not os.path.exists(full_path):
                self.right_images[screen] = None
                print(f"Image missing for {screen}: {full_path}")
                continue

            # try to load the image and store it in the dict
            try:
                self.right_images[screen] = pyglet.image.load(full_path)
                print(f"Loaded {screen}: {full_path}")
            # print error message if it failed
            except Exception as error:
                self.right_images[screen] = None
                print(f"Failed loading {screen}: {full_path} -> {error}")

    # updating the layout
    def update_layout(self, width, height):

        # bottom panel rectangle
        bottom_h = self.bottom_height
        self.bottom_rect = (0, 0, width, bottom_h)

        # y position is bottom height + gap
        top_y = bottom_h + self.gap

        # height is the height of the window minus the top y position minus the padding
        top_h = max(0, height - top_y - self.padding)

        # top x is the padding
        top_x = self.padding

        # width of the top panel is the width of the window minus 2 * padding
        top_w = max(0, width - 2 * self.padding)

        # right and left width based on the ratio and gap
        right_w = int(top_w * self.top_right_ratio)
        left_w = max(0, top_w - right_w - self.gap)

        # rectangles for the top left and top right panels
        self.top_left_rect = (top_x, top_y, left_w, top_h)
        self.top_right_rect = (top_x + left_w + self.gap,
                               top_y, right_w, top_h)

        # set the rectangles for the panels (top left)
        self.tuner_panel.set_rect(self.top_left_rect)
        self.metronome_panel.set_rect(self.top_left_rect)
        self.preset_panel.set_rect(self.top_left_rect)

    # handling inputs
    def on_key_press(self, symbol, modifiers):

        # if locked only space can unlock inputs
        if self.locked:
            if symbol == key.SPACE:
                self.locked = False
            return

        # key for locking inputs -> guitar controller shouldnt do stuff while playing songs
        if symbol == key.LALT:
            self.locked = True
            return

        # handle inputs based on the current screen
        if self.current_screen == "main_menu":
            self.handle_main_menu_input(symbol)
        elif self.current_screen == "preset_select":
            self.preset_panel.handle_input(symbol)
            if symbol == key.ESCAPE:
                self.current_screen = "main_menu"
        elif self.current_screen == "metronome":
            self.handle_metronome_input(symbol)
        elif self.current_screen == "tuner":
            self.handle_tuner_input(symbol)

    # handle main menu controls
    def handle_main_menu_input(self, symbol):

        # up and down to navigate the menu
        if symbol == key.UP:
            self.selected_index = (
                self.selected_index - 1) % len(self.menu_items)
        elif symbol == key.DOWN:
            self.selected_index = (
                self.selected_index + 1) % len(self.menu_items)

        # enter to select a menu item and switch to the corresponding screen
        elif symbol == key.ENTER:
            selected_item = self.menu_items[self.selected_index]
            if selected_item == "Presets":
                self.current_screen = "preset_select"
            elif selected_item == "Metronome":
                self.current_screen = "metronome"

        # space to switch to the tuner screen -> no guitar input for tuner because it would not work if out of tune
        elif symbol == key.SPACE:
            self.current_screen = "tuner"
            self.tuner_panel.start()

    # handle metronome controls
    def handle_metronome_input(self, symbol):

        # escape to return to main menu (and stop)
        if symbol == key.ESCAPE:
            self.metronome_panel.stop()
            self.current_screen = "main_menu"

        # control bpm
        elif symbol == key.UP:
            self.metronome_panel.change_bpm(1)
        elif symbol == key.DOWN:
            self.metronome_panel.change_bpm(-1)
        elif symbol == key.PAGEUP:
            self.metronome_panel.change_bpm(5)
        elif symbol == key.PAGEDOWN:
            self.metronome_panel.change_bpm(-5)

        # toggle metronome start/stop with enter
        elif symbol == key.ENTER:
            self.metronome_panel.toggle()

    # handle tuner controls
    def handle_tuner_input(self, symbol):
        # escape or space to return to main menu (and stop)
        if symbol == key.SPACE or symbol == key.ESCAPE:
            self.tuner_panel.stop()
            self.current_screen = "main_menu"

    # helper for drawing a text label
    def draw_label(
        self,
        text,
        x,
        y,
        font_size=14,
        color=(255, 255, 255, 255),
        anchor_x="left",
        anchor_y="center",
        italic=False,
    ):
        pyglet.text.Label(
            text,
            x=x,
            y=y,
            font_size=font_size,
            italic=italic,
            anchor_x=anchor_x,
            anchor_y=anchor_y,
            color=color,
        ).draw()

    # helper for drawing a rectangle background for a panel
    def draw_panel_background(self, rect, color):
        x, y, width, height = rect
        shapes.Rectangle(x, y, width, height, color=color).draw()

    # draws bottom panel: TODO show correct image based on handedness and screen state
    def draw_bottom_panel(self):
        self.draw_panel_background(self.bottom_rect, BACKGROUND_COLOR)
        image_path = "assets/bottom/fretboard_left_handed_scaled.png"
        image = pyglet.image.load(image_path)
        x, y, w, h = self.bottom_rect
        image.blit(x, y, width=w, height=h)

    # helper for drawing an image fitted into a rectangle (for right panel)
    def draw_image_fit_rect(self, image, rect):

        # get the rectangle dimensions
        x, y, w, h = rect

        # no image
        if image is None:
            return

        # target width and height for the image to fit into the rectangle
        target_w = RIGHT_IMAGE_BOX_SIZE
        target_h = RIGHT_IMAGE_BOX_SIZE

        # scale image to fit into the rectangle while maintaining aspect ratio
        scale = min(target_w / image.width, target_h / image.height)

        # calculate the width and height of the image after scaling
        draw_w = int(image.width * scale)
        draw_h = int(image.height * scale)

        # position
        draw_x = x + (w - draw_w) // 2
        draw_y = y + (h - draw_h) // 2

        # show image
        image.blit(draw_x, draw_y, width=draw_w, height=draw_h)

    # draw right panel
    def draw_right_panel(self):

        # draw background rectangle for the right panel
        self.draw_panel_background(self.top_right_rect, BACKGROUND_COLOR)

        # get current image
        image = self.right_images.get(self.current_screen)

        # draw the image fitted into the right panel rectangle
        if image is not None:

            # just to be sure
            gl.glEnable(gl.GL_BLEND)
            gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)

            self.draw_image_fit_rect(image, self.top_right_rect)

    # draw main menu on the left panel
    def draw_main_menu_left(self):

        # draw background rectangle for the left panel
        self.draw_panel_background(self.top_left_rect, BACKGROUND_COLOR)

        # dimensions of the left panel rectangle
        x, y, width, height = self.top_left_rect

        # label for the main menu
        self.draw_label("Main Menu", x + 20, y + height - 40, font_size=16)

        # start y position for the menu items and row height
        start_y = y + height - 95
        row_h = 44

        # go through menu items
        for index, item in enumerate(self.menu_items):

            # current y position for this menu item
            row_y = start_y - index * row_h

            # is this menu item selected
            is_selected = index == self.selected_index

            # draw a background rectangle for the selected menu item
            if is_selected:
                shapes.Rectangle(
                    x + 16,
                    row_y - 18,
                    width - 32,
                    32,
                    color=(90, 90, 120),
                ).draw()

            # draw the menu item text
            self.draw_label(item, x + 28, row_y, font_size=14)

        # label for tuner shortcut at the bottom of the menu
        self.draw_label(
            "press SPACE for tuner",
            x + 28,
            start_y - len(self.menu_items) * row_h - 10,
            font_size=12,
            color=(180, 180, 180, 255),
            italic=True,
        )

    # call metronome draw
    def draw_metronome_left(self):
        self.metronome_panel.draw()

    # call tuner draw and set the rectangle for the tuner panel
    def draw_tuner_left(self):
        self.tuner_panel.set_rect(self.top_left_rect)
        self.tuner_panel.draw()

    # on draw loop
    def on_draw(self):

        # update controller only if it's not locked or not in tuner mode
        if not self.locked and not self.current_screen == "tuner":
            self.controller.update()

        # clear windwo
        self.clear()

        # draw bottom panel
        self.draw_bottom_panel()

        # draw the left panel depending on the current screen state
        if self.current_screen == "main_menu":
            self.draw_main_menu_left()
        elif self.current_screen == "preset_select":
            self.preset_panel.draw()
        elif self.current_screen == "metronome":
            self.draw_metronome_left()
        elif self.current_screen == "tuner":
            self.draw_tuner_left()

        # draw the right panel
        self.draw_right_panel()


# was used for testing
if __name__ == "__main__":
    window = MainWindow()
    pyglet.app.run()
