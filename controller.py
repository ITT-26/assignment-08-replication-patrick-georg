import sounddevice as sd
from guitar_input import GuitarInput
import pynput


def choose_input_device():
    # print info about audio devices
    print("Available input devices:\n")
    devices = sd.query_devices()

    input_devices = []
    for i, dev in enumerate(devices):
        if dev['max_input_channels'] > 0:
            print(f"{i}: {dev['name']}")
            input_devices.append(i)

    # let user select audio device
    input_device = int(input("\nSelect input device: "))
    return input_device


# dummy actions for each note -> print the note and what key or what functionality it would trigger
NOTE_ACTIONS = {
    "G3": lambda: (print("G3: ARROW UP"), simulate_key_press(pynput.keyboard.Key.up)),
    "F#3": lambda: (print("F#3: PAGE UP"), simulate_key_press(pynput.keyboard.Key.page_up)),
    "E4": lambda: (print("E4: ARROW DOWN"), simulate_key_press(pynput.keyboard.Key.down)),
    "D#4": lambda: (print("D#4: PAGE DOWN"), simulate_key_press(pynput.keyboard.Key.page_down)),
    "B3": lambda: (print("B3: BACK"), simulate_key_press(pynput.keyboard.Key.backspace)),
    "C4": lambda: (print("C4: ENTER"), simulate_key_press(pynput.keyboard.Key.enter)),
    # lock should lock away these actions -> with a keyboard input it should be reversable -> dont want to trigger something while playing
    "D4": lambda: (print("D4: LOCK"))
}


def simulate_key_press(key):
    # create a keyboard controller
    keyboard = pynput.keyboard.Controller()

    # press and release the key
    keyboard.tap(key)


# callback for string strike event
def on_strike(freq, note):
    # get action from NOTE_ACTIONS dictionary
    action = NOTE_ACTIONS.get(note)

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

    # guitar input object with strike callback
    guitar = GuitarInput(device_index=device_index, on_strike=on_strike)

    print("Controller Started -> Ctrl+C to stop.")
    with guitar.stream:
        try:
            while True:
                guitar.update()
        except KeyboardInterrupt:
            print("Controller Stopped.")
