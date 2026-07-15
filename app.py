import pyglet
from ui.setup_window import SetupWindow
from ui.main_window import MainWindow


# launch app method
def launch_app():

    # state for main window
    state = {"main_window": None}

    # callback for when setup is confirmed
    def on_setup_confirm(device_index, handedness):

        # MainWindow with selected options
        state["main_window"] = MainWindow(
            device_index=device_index,
            handedness=handedness,
        )

    # start setup window with callback
    SetupWindow(on_setup_confirm)
    pyglet.app.run()


if __name__ == "__main__":
    launch_app()
