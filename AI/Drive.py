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

    map_gta = screenshot[500:600, 15:160]

    frame = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)
    frame = cv2.Canny(frame, threshold1=120, threshold2=220)
    frame = frame[100: , :]
    lanes = np.zeros((frame.shape[0], frame.shape[1], 3), dtype=np.uint8)
    lanes[:, :, 0] = frame
    lanes[:, :, 1] = frame
    lanes[:, :, 2] = frame

    lines = cv2.HoughLinesP(frame, rho=1, theta=np.pi/90, threshold=70, minLineLength=20, maxLineGap=50)

    if lines is not None:
        for line in lines:
            x1, y1, x2, y2 = line[0]
            cv2.line(lanes, (x1, y1), (x2, y2), (0, 255, 0), 5)

    lanes = cv2.resize(lanes, (200, 66))
    
    frame = lanes

    frame = frame.astype('float32') / 255.0
    map_gta = map_gta.astype('float32') / 255.0

    frame = np.array(frame)
    map_gta = np.array(map_gta)

    return frame, map_gta


# function to hold the key
def hold_key(key, KB):
    KB.press(key)

def release_key(key, KB):
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
    model = tf.keras.models.load_model('./final_model_v1_8_0.h5')
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


    pressed = []

    while running:
        frame, map_frame = capture_frame(gta_window)

        frame = np.expand_dims(frame, axis=0)
        map_frame = np.expand_dims(map_frame, axis=0)

        # predict the keys to be pressed
        prediction = model.predict([frame, map_frame])


        prediction_turn = [prediction[0][0] + prediction[0][4], prediction[0][3] + prediction[0][5]]
        prediction_accelerate = [prediction[0][1] + prediction[0][4] + prediction[0][5], prediction[0][2] + prediction[0][6] + prediction[0][7]]

        # send the keys to gta window, get the one with highest probability
        keys_turn = ['q', 'd']
        keys_accelerate = ['z', 's']

        key_turn = keys_turn[np.argmax(prediction_turn)]
        key_accelerate = keys_accelerate[np.argmax(prediction_accelerate)]

        indice_turn = np.argmax(prediction_turn)
        indice_accelerate = np.argmax(prediction_accelerate)

        press = True
        
        start = time.time()

        if press:
            print()
            print(f"Key : {key_turn} => {prediction_turn[indice_turn]}")
            print(f"Key : {key_accelerate} => {prediction_accelerate[indice_accelerate]}")
            print()
            
            to_press = []


            if(time.time() - start > 1):
                start = time.time()
                continue
            
            if prediction_turn[indice_turn] >= 0.25:
                to_press.append(key_turn)
            
            if prediction_accelerate[indice_accelerate] >= 0.5:
                to_press.append(key_accelerate)

            to_release = []
            for i in pressed:
                if i not in to_press:
                    release_key(i, KB)
                    to_release.append(i)


            for i in to_release:
                if i in pressed:
                    pressed.remove(i)

            for i in to_press:
                if i not in pressed:
                    hold_key(i, KB)
                    pressed.append(i)


    print("Stopping...")

