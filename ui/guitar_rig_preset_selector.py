import pyautogui
import pygetwindow as gw
import pyperclip
from pywinauto.keyboard import send_keys


# Base Window dimensions (where coordinates are based on)
WINDOW_WIDTH = 1456
WINDOW_HEIGHT = 819

# Coordinates for search field
SEARCH_FIELD_X = 252
SEARCH_FIELD_Y = 155

# Relative coordinates for search field
SEARCH_FIELD_REL_X = SEARCH_FIELD_X / WINDOW_WIDTH
SEARCH_FIELD_REL_Y = SEARCH_FIELD_Y / WINDOW_HEIGHT

# Coordinates for first search result
SELECT_RESULT_X = 148
SELECT_RESULT_Y = 440

# Relative coordinates for first search result
SELECT_RESULT_REL_X = SELECT_RESULT_X / WINDOW_WIDTH
SELECT_RESULT_REL_Y = SELECT_RESULT_Y / WINDOW_HEIGHT


class GuitarRigPresetSelector:

    # get the window upon loading
    def __init__(self):
        self.window = self.find_gr7_window()

    # find the Guitar Rig 7 window
    def find_gr7_window(self):
        for w in gw.getAllWindows():
            if "guitar rig 7" in (w.title or "").lower():
                return w
        return None

    # focussing the window
    def focus_gr7(self):
        if not self.window:
            return False, "Guitar Rig 7 not found."
        try:
            if self.window.isMinimized:
                self.window.restore()
            self.window.activate()
        except Exception:
            pass
        return True, None

    # minimizing the window
    def minimize_gr7(self):
        self.window = self.find_gr7_window()
        if not self.window:
            return False, "Guitar Rig 7 not found."
        try:
            self.window.minimize()
            return True, None
        except Exception as error:
            return False, str(error)

    # actual thing we want to do: select a preset by name
    def select_preset_by_name(self, name):

        # find the window again in case something changed
        self.window = self.find_gr7_window()
        if not self.window:
            return False, "Guitar Rig 7 not found."

        # Focus the window
        success, error = self.focus_gr7()
        if not success:
            return False, error

        # Dynamically scale to current window size
        search_x = int(self.window.left +
                       self.window.width * SEARCH_FIELD_REL_X)
        search_y = int(self.window.top +
                       self.window.height * SEARCH_FIELD_REL_Y)

        select_x = int(self.window.left +
                       self.window.width * SELECT_RESULT_REL_X)
        select_y = int(self.window.top + self.window.height *
                       SELECT_RESULT_REL_Y)

        # Click on the search field and type the preset name
        pyautogui.click(search_x, search_y)
        pyperclip.copy(name)
        send_keys('^v')

        # Click on the first search result
        pyautogui.click(select_x, select_y)
        pyautogui.click(select_x, select_y)

        # minimize the window to focus back on the previous window
        self.minimize_gr7()


# test selecting Rock Seeker preset
if __name__ == "__main__":
    selector = GuitarRigPresetSelector()
    preset_name = "Rock Seeker"
    selector.select_preset_by_name(preset_name)
