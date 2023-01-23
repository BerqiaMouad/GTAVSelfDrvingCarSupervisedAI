import keyboard
import cv2
import numpy as np
import pyautogui
import pygetwindow as gw
import time
import pandas as pd
import tkinter as tk
import customtkinter as ctk
import threading

# Get key pressed
def capture_key_pressed():
    key = keyboard.read_key()
    return key

# Get frame from game window
def capture_frame(window):
    # make screenshot of the window
    screenshot = pyautogui.screenshot(region=(window.left, window.top, window.width, window.height))
    
    # convert to numpy array
    frame = np.array(screenshot)
    
    # convert to BGR
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    return frame


# variable to keep track if the script is running
running = False

def capturing_script():
    window_name='Trackmania'
    
    # search for the first window with name of trackmania
    window = gw.getWindowsWithTitle(window_name)[0]

    # activate the window
    window.activate()
    
    # creating dataframe to store the data
    df = pd.DataFrame(columns=['image_id', 'q', 'z', 's', 'd', 'no_key'])

    # loop of capturing frames with corresponding key pressed
    while running:
        key = capture_key_pressed()
        frame = capture_frame(window)
        im_id=int(time.time() * 1000)
        cv2.imwrite('./screenshots/'+str(im_id)+'.png', frame)
        
        q=False
        z=False
        s=False
        d=False
        no_key=False

        # check if key pressed is one of the keys we want to capture
        if(key == 'q'):
            q=True
        elif(key=='z'):
            z=True
        elif(key=='s'):
            s=True
        elif(key=='d'):
            d=True
        else:
            q=False
            z=False
            s=False
            d=False
            no_key=True
        df = df.append({'image_id': im_id, 'q': q, 'z': z, 's': s, 'd': d, 'no_key': no_key}, ignore_index=True)
        df.to_csv('./data.csv', index=False)

# function to stop the capturing script
def start_capturing():
    global running
    running = True
    capturing_script_sep_thread()

# function to stop the capturing script
def stop_capturing():
    global running
    running = False

# function to make a seprate thread for capturing script
def capturing_script_sep_thread():
    t = threading.Thread(target=capturing_script)
    t.start()

if __name__ == '__main__':
    root=tk.Tk()
    root.title("Capture Data")
    root.geometry("500x500")
    root.resizable(False, False)
    root.configure(background='dark slate gray')
    
    # creating a button to start capturing
    start_button = tk.Button(root, text="Start Capturing", command=start_capturing)
    start_button.pack(pady=10, padx=10)

    # creating a button to stop capturing
    stop_button = tk.Button(root, text="Stop Capturing", command=stop_capturing)
    stop_button.pack(pady=10, padx=10)


    root.mainloop()

        
