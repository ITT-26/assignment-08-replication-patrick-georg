import pyglet
import sounddevice as sd
from pyglet import shapes

from ui.main_window_constants import *


class SetupWindow(pyglet.window.Window):

    # Colors
    BG = BACKGROUND_COLOR
    BTN = (70, 70, 95)
    BTN_ACTIVE = (120, 110, 70)
    BTN_START = (80, 140, 100)
    DEVICE_BOX = (85, 85, 115)

    # max length of text
    MAX_DEVICE_TEXT_LEN = 60

    def __init__(self, on_confirm):

        # window dimensions and title
        super().__init__(680, 360, caption="Setup", resizable=False)

        # callback for confirming selection
        self.on_confirm = on_confirm

        # load available input devices
        self.devices = self.load_devices()
        self.device_pos = 0
        self.hand = "right"

        # dictionary of button rectangle
        self.buttons = {
            "prev": (40, 190, 50, 45),
            "next": (590, 190, 50, 45),
            "left": (80, 70, 120, 45),
            "right": (220, 70, 120, 45),
            "start": (500, 40, 140, 55),
        }

    # load available input devices
    def load_devices(self):
        try:
            devices = [
                (i, d.get("name", f"Input {i}"))
                for i, d in enumerate(sd.query_devices())
                if d.get("max_input_channels", 0) > 0
            ]
            return devices or [(None, "No input device")]
        except Exception as err:
            print("Device query failed:", err)
            return [(None, "No input device")]

    # cap the text to a certain length and add dots if it exceeds that length
    def cap_text(self, text, max_len):
        if len(text) <= max_len:
            return text
        if max_len <= 3:
            return text[:max_len]
        return text[: max_len - 3] + "..."

    # check if a point is inside a rectangle
    def inside(self, x, y, rect):
        rx, ry, rw, rh = rect
        return rx <= x <= rx + rw and ry <= y <= ry + rh

    # draw button helper
    def draw_button(self, rect, text, color, font_size=12):
        x, y, w, h = rect
        shapes.Rectangle(x, y, w, h, color=color).draw()
        pyglet.text.Label(
            text,
            x=x + w // 2,
            y=y + h // 2,
            font_size=font_size,
            anchor_x="center",
            anchor_y="center",
        ).draw()

    # handle mouse press events
    def on_mouse_press(self, x, y, button, modifiers):

        # previous button clicked -> move to previous device
        if self.inside(x, y, self.buttons["prev"]):
            self.device_pos = (self.device_pos - 1) % len(self.devices)
            return

        # next button clicked -> move to next device
        if self.inside(x, y, self.buttons["next"]):
            self.device_pos = (self.device_pos + 1) % len(self.devices)
            return

        # left hand button clicked
        if self.inside(x, y, self.buttons["left"]):
            self.hand = "left"
            return

        # right hand button clicked
        if self.inside(x, y, self.buttons["right"]):
            self.hand = "right"
            return

        # start button clicked -> close window and call callback with selected options
        if self.inside(x, y, self.buttons["start"]):
            device_index = self.devices[self.device_pos][0]
            if device_index is None:
                print("No usable input device.")
                return
            self.on_confirm(device_index, self.hand)
            self.close()

    # on draw loop
    def on_draw(self):

        # clear window
        self.clear()

        # draw background
        shapes.Rectangle(0, 0, self.width, self.height, color=self.BG).draw()

        # draw title
        pyglet.text.Label("Setup", x=20, y=330, font_size=18).draw()

        # device selection
        self.draw_button((110, 190, 460, 45), "", self.DEVICE_BOX)
        idx, name = self.devices[self.device_pos]
        name = self.cap_text(name, self.MAX_DEVICE_TEXT_LEN)
        device_text = f"[{idx}] {name}" if idx is not None else name

        # device text label
        pyglet.text.Label(
            device_text,
            x=340,
            y=212,
            font_size=11,
            anchor_x="center",
            anchor_y="center",
        ).draw()

        # previous and next buttons
        self.draw_button(self.buttons["prev"], "<", self.BTN)
        self.draw_button(self.buttons["next"], ">", self.BTN)

        # buttons for left and right handedness (Color change based on selection)
        left_color = self.BTN_ACTIVE if self.hand == "left" else self.BTN
        right_color = self.BTN_ACTIVE if self.hand == "right" else self.BTN
        self.draw_button(self.buttons["left"], "LEFTHANDED", left_color)
        self.draw_button(self.buttons["right"], "RIGHTHANDED", right_color)

        # start button
        self.draw_button(self.buttons["start"], "START", self.BTN_START)


# testing
def demo_confirm(device_index, handedness):
    print("Device:", device_index, "Hand:", handedness)


if __name__ == "__main__":
    SetupWindow(demo_confirm)
    pyglet.app.run()
