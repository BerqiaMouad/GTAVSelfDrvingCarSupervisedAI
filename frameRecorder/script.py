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


# Get key pressed
def capture_key_pressed():
    if(keyboard.is_pressed('q')):
        return 'q'
    elif(keyboard.is_pressed('z')):
        return 'z'
    elif(keyboard.is_pressed('s')):
        return 's'
    elif(keyboard.is_pressed('d')):
        return 'd'
    else:
        return 'no_key'

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
    window_name='Google Chrome'
    
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
    while running:
        key = capture_key_pressed()
        
        frame = capture_frame(window)
        
        im_id=int(time.time() * 1000)
        
        if(os.path.exists('./tempScreenShots') == False):
            os.mkdir('./tempScreenShots')

        cv2.imwrite('./tempScreenShots/'+str(im_id)+'.png', frame)
        
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
        temp = {'image_id': im_id, 'q': q, 'z': z, 's': s, 'd': d, 'no_key': no_key}
        data.append(temp)
    
    
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


# function to stop the capturing script
def start_capturing():
    global running
    running = True
    print("Capturing started...")
    capturing_script_sep_thread()

# function to stop the capturing script
def stop_capturing():
    global running
    running = False
    print("Capturing stopped")

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
    
    # creating a button to start capturing
    start_button = ctk.CTkButton(root, text="Start Capturing", width=170, height=50, font=('Ubuntu', 20), corner_radius=25, command=start_capturing)
    start_button.pack(pady=20, padx=20)
    start_button.place(relx=0.5, rely=0.3, anchor=tk.CENTER)

    # creating a button to stop capturing
    stop_button = ctk.CTkButton(root, text="Stop Capturing", width=170, height=50, font=('Ubuntu', 20), corner_radius=25, command=stop_capturing)
    stop_button.pack(pady=20, padx=20)
    stop_button.place(relx=0.5, rely=0.5, anchor=tk.CENTER)


    root.mainloop()

