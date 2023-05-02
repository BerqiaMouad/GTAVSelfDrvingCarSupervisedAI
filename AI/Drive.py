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

    screenshot = ImageGrab.grab(bbox=(gta_window.left, gta_window.top, gta_window.left + 800, gta_window.top + 600))

    screenshot = np.array(screenshot)

    frame = cv2.cvtColor(screenshot, cv2.COLOR_BGR2RGB)

    map_gta = frame[500:600, 15:160]

    frame = frame[150:500, 3:]

    frame = cv2.resize(frame, (200, 150))

    frame = frame / 255.0
    map_gta = map_gta / 255.0

    frame = np.array(frame)
    map_gta = np.array(map_gta)

    return frame, map_gta


# function to hold the key
def hold_key(key, KB):
    KB.press(key)
    if(key == 'z'):
        time.sleep(0.4)
    else:
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
    model = tf.keras.models.load_model('./final_model_v1_0_0.h5')
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
        frame, map_frame = capture_frame(gta_window)

        frame = np.expand_dims(frame, axis=0)
        map_frame = np.expand_dims(map_frame, axis=0)

        # predict the keys to be pressed
        prediction = model.predict([frame, map_frame])

        prediction_turn = [prediction[0][0], prediction[0][3]]
        prediction_accelerate = [prediction[0][1], prediction[0][2]]

        # send the keys to gta window, get the one with highest probability
        keys_turn = ['q', 'd']
        keys_accelerate = ['z', 's']

        key_turn = keys_turn[np.argmax(prediction_turn)]
        key_accelerate = keys_accelerate[np.argmax(prediction_accelerate)]

        indice_turn = np.argmax(prediction_turn)
        indice_accelerate = np.argmax(prediction_accelerate)

        press = True

        if press:
            print()
            print(f"Key : ", end='')
            print(key_turn, end='')
            print(" ", end='')
            print(key_accelerate)
            print()

            hold_key(key_turn, KB)
            
            if prediction_accelerate[indice_accelerate] > 0.25:
                hold_key(key_accelerate, KB)

    print("Stopping...")

