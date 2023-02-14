import time
from pynput import keyboard

keys = []

def on_press(key):
    global keys
    try:
        keys.append(key.char)
    except AttributeError:
        keys.append(key.name)

def on_release(key):
    global keys
    try:
        keys.remove(key.char)
    except AttributeError:
        keys.remove(key.name)

# Start keyboard listener in a separate thread
listener = keyboard.Listener(on_press=on_press, on_release=on_release)
listener.start()

# Print the "temp" dictionary every second
while True:
    a, w, s, d = 0, 0, 0, 0
    if 'a' in keys:
        a = 1
    if 'w' in keys:
        w = 1
    if 's' in keys:
        s = 1
    if 'd' in keys:
        d = 1
    temp = {'a': a, 'w': w, 's': s, 'd': d}
    print(temp)
    time.sleep(0.1)
