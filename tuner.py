import sounddevice as sd
from guitar_controls.guitar_input import GuitarInput


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


# callback for pitch detection event
def on_pitch(freq, note, confidence):

    # convert frequency to cents
    _, _, cents = GuitarInput.freq_to_cents(freq)

    # simple check if the note is in tune -> TODO: fix string issue
    direction = "fine  " if abs(cents) < 5 else (
        "too high " if cents > 0 else "too low ")
    print(
        f"Note: {note:3s} | {freq:7.2f} Hz | {cents:+.1f} cent | {direction}", end="\r")


# main function -> just testing for the moment
if __name__ == "__main__":

    # get device
    device_index = choose_input_device()

    # guitar input object with pitch callback
    guitar = GuitarInput(device_index=device_index, on_pitch=on_pitch)


    # loop
    print("Play a string -> Ctrl+C to stop")
    with guitar.stream:
        try:
            while True:
                guitar.update()
        except KeyboardInterrupt:
            print("Stopped.")
