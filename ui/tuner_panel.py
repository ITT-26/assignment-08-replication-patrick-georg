import pyglet
from pyglet import shapes
from ui.main_window_constants import *

from guitar_controls.guitar_input import GuitarInput


class TunerPanel:
    def __init__(self, device_index=None):

        # background
        self.rect = (0, 0, 0, 0)

        # device
        self.device_index = device_index

        # guitar input object
        self.guitar = None

        # running state
        self.running = False

        # note display
        self.note = "--"

        # shows too low, too high or in tune
        self.status = "waiting"

        # color for status text -> changes depending on status
        self.status_color = (180, 180, 180)

    # background
    def set_rect(self, rect):
        self.rect = rect

    # starts the tuner
    def start(self):

        # don't start if already running
        if self.running:
            return

        # make guitar input object and start the stream
        self.guitar = GuitarInput(
            device_index=self.device_index,
            on_pitch=self.on_pitch,
        )
        self.guitar.stream.start()

        # refresh the tuner panel at 20 FPS
        pyglet.clock.schedule_interval(self.update, 1 / 20)

        # running is true
        self.running = True

    # stops the tuner
    def stop(self):

        # cant stop if not running
        if not self.running:
            return

        # unschedule the update function
        pyglet.clock.unschedule(self.update)

        # stop and close the guitar input stream
        if self.guitar is not None:
            self.guitar.stream.stop()
            self.guitar.stream.close()
            self.guitar = None

        # not running anymore
        self.running = False

    # tuning method based on old code
    def on_pitch(self, freq, note, confidence):
        _, _, cents = GuitarInput.freq_to_cents(freq)
        self.note = note

        # cent margin for when its considered in tune
        if abs(cents) <= 5:
            self.status = "in tune"
            self.status_color = (80, 200, 120)
        
        # out of margin and positive cents -> too high
        elif cents > 0:
            self.status = "too high"
            self.status_color = (220, 120, 80)
        
        # out of margin and negative cents -> too low
        else:
            self.status = "too low"
            self.status_color = (220, 120, 80)

    # update function called by pyglet clock
    def update(self, dt):
        # get guitar input update
        if self.guitar is not None:
            self.guitar.update()

    # draw label
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

    def draw(self):

        # rectangle for background
        x, y, w, h = self.rect

        shapes.Rectangle(x, y, w, h, color=BACKGROUND_COLOR).draw()

        # tuner label
        self.draw_label("Tuner", x + 20, y + h - 40, size=16)

        # note label
        self.draw_label(self.note, x + 20, y + h - 110, size=34)

        # status label
        self.draw_label(self.status, x + 20, y + h - 170, size=20, color=(*self.status_color, 255))