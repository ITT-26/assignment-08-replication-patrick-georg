import sounddevice as sd
from guitar_controls.guitar_input import GuitarInput
import pynput


def choose_input_device():
    # print info about audio devices
    print("Available input devices:\n")
    devices = sd.query_devices()

    input_devices = []
    for i, dev in enumerate(devices):
        if dev["max_input_channels"] > 0:
            print(f"{i}: {dev['name']}")
            input_devices.append(i)

    # let user select audio device
    input_device = int(input("\nSelect input device: "))
    return input_device


class GuitarController:
    def __init__(self, device_index):
        self.device_index = device_index

        # create a keyboard controller
        self.keyboard = pynput.keyboard.Controller()

        # guitar input object with strike callback
        self.guitar = None

        # running state
        self.running = False

        # dummy actions for each note -> print the note and what key or what functionality it would trigger
        self.note_actions = {
            "G3": lambda: (print("G3: ARROW UP"), self.simulate_key_press(pynput.keyboard.Key.up)),
            "F#3": lambda: (print("F#3: PAGE UP"), self.simulate_key_press(pynput.keyboard.Key.page_up)),
            "E4": lambda: (print("E4: ARROW DOWN"), self.simulate_key_press(pynput.keyboard.Key.down)),
            "D#4": lambda: (print("D#4: PAGE DOWN"), self.simulate_key_press(pynput.keyboard.Key.page_down)),
            "B3": lambda: (print("B3: BACK"), self.simulate_key_press(pynput.keyboard.Key.esc)),
            "C4": lambda: (print("C4: ENTER"), self.simulate_key_press(pynput.keyboard.Key.enter)),
            "D4": lambda: (print("D4: LOCK"), self.simulate_key_press(pynput.keyboard.Key.alt_l)),
        }

    def start(self):
        # don't start if already running
        if self.running:
            return

        # guitar input object with strike callback
        self.guitar = GuitarInput(
            device_index=self.device_index,
            on_strike=self.on_strike,
        )
        self.guitar.stream.start()

        # running is true
        self.running = True
        print("Controller Started.")

    def stop(self):
        # cant stop if not running
        if not self.running:
            return

        # stop and close the guitar input stream
        if self.guitar is not None:
            self.guitar.stream.stop()
            self.guitar.stream.close()
            self.guitar = None

        # not running anymore
        self.running = False
        print("Controller Stopped.")

    def update(self):
        # update guitar input if running
        if self.running and self.guitar is not None:
            self.guitar.update()

    def simulate_key_press(self, key):
        # press and release the key
        self.keyboard.tap(key)

    # callback for string strike event
    def on_strike(self, freq, note):
        # get action from NOTE_ACTIONS dictionary
        action = self.note_actions.get(note)

        # do action
        if action is not None:
            action()

        # print no action for note
        else:
            print(f"No action for: {note} ({freq:.2f} Hz)")


# main function -> just testing for the moment
if __name__ == "__main__":
    # get device
    device_index = choose_input_device()

    controller = GuitarController(device_index=device_index)
    controller.start()

    try:
        while True:
            controller.update()
    except KeyboardInterrupt:
        controller.stop()