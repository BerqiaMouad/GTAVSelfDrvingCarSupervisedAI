import time
from pynput import keyboard


class KeyCapture:
    def __init__(self):
        self.keys = set()
        self.listener = None

    def on_press(self, key):
        # check if key is F8
        if key == keyboard.Key.f8:
            # ignore it
            return 
        try:
            self.keys.add(key.char)
        except AttributeError:
            self.keys.add(key)

    def on_release(self, key):
        # check if key is F8
        if key == keyboard.Key.f8:
            # ignore it
            return
        try:
            self.keys.remove(key.char)
        except AttributeError:
            self.keys.remove(key)

    def start(self):
        self.listener = keyboard.Listener(on_press=self.on_press, on_release=self.on_release)
        self.listener.start()

    def stop(self):
        if self.listener is not None:
            self.listener.stop()

    def get_keys(self):
        return [(1 if 'q' in self.keys else 0), (1 if 'z' in self.keys else 0), (1 if 's' in self.keys else 0), (1 if 'd' in self.keys else 0)]

