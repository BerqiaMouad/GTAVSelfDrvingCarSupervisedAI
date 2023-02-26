import keyboard
import cv2
import numpy as np
from PIL import ImageGrab
import pygetwindow as gw
import time
import pandas as pd
import tkinter as tk
import customtkinter as ctk
import threading
import os.path
import shutil
from keys_capture import KeyCapture


# new key capture object 
kc = KeyCapture()


# Get frame from game window
def capture_frame(window):
    # make screenshot of the window
    screenshot = ImageGrab.grab(bbox=(window.left, window.top, window.left + window.width, window.top + window.height))
    
    # convert to numpy array
    frame = np.array(screenshot)
    
    # convert to BGR
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    return frame


# variable to keep track if the script is running
running = False

def capturing_script():
    # change this to the name of the window
    window_name='Grand Theft Auto V'
    
    # search for the first window with name of trackmania
    window = gw.getWindowsWithTitle(window_name)[0]

    # activate the window
    window.activate()
    
    # creating dataframe to store the data
    if(os.path.exists('./data.csv')):
        # if file exists, load it
        df = pd.read_csv('./data.csv')
    else:
        # if file doesn't exist, create data frame
        df = pd.DataFrame(columns=['image_id', 'q', 'z', 's', 'd', 'no_key'])

    # list of dictionaries to make it faster to append to the dataframe
    data = []


    # loop of capturing frames with corresponding key pressed
    kc.start()

    while running:
        # get keys pressed
        keys = kc.get_keys()
        
        # get frame
        frame = capture_frame(window)
        
        # keep only cars that are close to the car
        # cars_distances = [car for car in cars_distances if car[1] < 100]
        
        im_id=int(time.time() * 1000)
        
        if(os.path.exists('./tempScreenShots') == False):
            os.mkdir('./tempScreenShots')

        cv2.imwrite('./tempScreenShots/'+str(im_id)+'.png', frame)
        
        # append to the list of dictionaries
        temp = {'image_id': im_id, 'q': keys[0], 'z': keys[1], 's': keys[2], 'd': keys[3], 'no_key': (1 if keys[0] == keys[1] == keys[2] == keys[3] == 0 else 0)}
        data.append(temp)

    kc.stop()

    print("Capturing finished")
    
    # promopt user if he wants to save the data
    save = tk.messagebox.askyesno('Save data', 'Do you want to save the data?')
    
    # if yes, save the data
    if(save):
        # append the data to the dataframe
        tempDf = pd.DataFrame(data, columns=['image_id', 'q', 'z', 's', 'd', 'no_key'])
        df = pd.concat([df, tempDf], ignore_index=True)
        
        # save the data
        df.to_csv('./data.csv', index=False)
        if(os.path.exists('./screenShots') == False):
            os.mkdir('./screenShots')
        for file in os.listdir('./tempScreenShots'):
            shutil.move('./tempScreenShots/'+file, './screenShots/'+file)
        os.rmdir('./tempScreenShots')
        tk.messagebox.showinfo('Data saved', 'Data saved')

    # if no, delete the data
    else:
        tk.messagebox.showinfo('Data not saved', 'Data not saved')
        for file in os.listdir('./tempScreenShots'):
            os.remove('./tempScreenShots/'+file)
        
        # delete the tempScreenShots folder
        os.rmdir('./tempScreenShots')


# function to start the capturing script
def start_capturing():
    global running
    running = True
    print("Capturing started...")
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
    ctk.set_appearance_mode('dark')
    ctk.set_default_color_theme("blue")

    root=ctk.CTk()
    root.title("Capture Data")
    root.geometry("500x500")
    root.resizable(False, False)

    # label to help user know what is the key to start
    label = ctk.CTkLabel(root, text="Press 'F8' to start capturing.", font=('Ubuntu', 17))
    label.pack(pady=20, padx=20)
    label.place(relx=0.5, y=100, anchor=tk.CENTER)
    
    # label to help user know what is the key to stop capturing
    label = ctk.CTkLabel(root, text="Press 'F9' to stop capturing.", font=('Ubuntu', 15))
    label.pack(pady=20, padx=20)
    label.place(relx=0.5, y=150, anchor=tk.CENTER)

    # creating a button to start capturing
    start_button = ctk.CTkButton(root, text="Start Capturing", width=170, height=50, font=('Ubuntu', 20), corner_radius=25, command=start_capturing)
    start_button.pack(pady=20, padx=20)
    start_button.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

    # adding F2 key to stop capturing
    keyboard.add_hotkey('F9', stop_capturing)

    # adding F1 key to start capturing
    keyboard.add_hotkey('F8', start_capturing)

    root.mainloop()


