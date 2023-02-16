import time
from pynput import keyboard


class KeyCapture:
    def __init__(self):
        self.keys = []

    def on_press(self, key):
        try:
            self.keys.append(key.char)
        except AttributeError:
            self.keys.append(key.name)

    def on_release(self, key):
        try:
            self.keys.remove(key.char)
        except AttributeError:
            self.keys.remove(key.name)

    def start(self):
        listener = keyboard.Listener(on_press=self.on_press, on_release=self.on_release)
        listener.start()

    def get_keys(self):
        return [(1 if 'q' in self.keys else 0), (1 if 'z' in self.keys else 0), (1 if 's' in self.keys else 0), (1 if 'd' in self.keys else 0)]
