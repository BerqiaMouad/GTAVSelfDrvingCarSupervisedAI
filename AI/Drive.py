import tensorflow as tf
import numpy as np
import cv2
from PIL import ImageGrab
import pygetwindow as gw
import keyboard
from pynput.keyboard import Key, Controller
import time


# function to capture frame and preprocess it
def capture_frame(gta_window):

    screenshot = ImageGrab.grab(bbox=(gta_window.left, gta_window.top, gta_window.left + gta_window.width, gta_window.top + gta_window.height))

    screenshot = np.array(screenshot)

    frame = cv2.cvtColor(screenshot, cv2.COLOR_BGR2RGB)

    frame = frame[150:500, 3:]

    frame = cv2.resize(frame, (300, 225))

    frame = frame / 255.0

    frame = np.array(frame)

    return frame


# function to hold the key
def hold_key(key, KB):
    if(key == 'z'):
        return

    KB.press(key)
    time.sleep(0.2)
    KB.release(key)


# global variable to start or stop game
running = False


# function to start
def start_game():
    global running
    running = True

# function to stop
def stop_game():
    global running
    running = False




if __name__ == "__main__":
    
    keyboard.add_hotkey('F8', start_game)
    
    print("Loading model...")
    model = tf.keras.models.load_model('./model_2_0_0.h5')
    print("Model loaded !")
    
    while not running:
        continue

    print("Starting...")
    print("3")
    time.sleep(1)
    print("2")
    time.sleep(1)
    print("1")
    time.sleep(1)


    # getting the window
    gta = 'Grand Theft Auto V'

    gta_window = gw.getWindowsWithTitle(gta)[0]

    gta_window.activate()

    KB = Controller()
    
    keyboard.add_hotkey('F9', stop_game)

    while running:
        KB.press('z')
        frame = capture_frame(gta_window)

        # predict the keys to be pressed
        prediction = model.predict(np.array([frame]))

        # send the keys to gta window, get the one with highest probability
        keys = ['q', 'z', 's', 'd', 'zq', 'zd', 'sq', 'sd']

        key = keys[np.argmax(prediction)]

        # get the indice of the key
        indice = keys.index(key)

        press = True

        if press:
            print()
            print(f"Key : {key}")
            print()
            if(len(key) == 1):
                hold_key(key, KB)
            else:
                hold_key(key[0], KB)
                hold_key(key[1], KB)

        KB.release('z')

        
    KB.release('z')
    
    print("Stopping...")

