import keyboard
import cv2
import numpy as np
from PIL import ImageGrab, ImageTk, Image
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
    
    # convert to rgb
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # we get the map from the frame
    map_gta = frame[500:600, 15:160]

    # we crop the frame to remove the top bar
    frame = frame[150:500, 3:]

    # resize the frame
    frame = cv2.resize(frame, (300, 225))


    return frame, map_gta


# variable to keep track if the script is running
running = False

def capturing_script():
    # change this to the name of the window
    window_name='Grand Theft Auto V'
    
    # search for the first window with name of gta
    window = gw.getWindowsWithTitle(window_name)[0]

    # activate the window
    window.activate()
    
    # creating dataframe to store the data
    if(os.path.exists('./data.csv')):
        # if file exists, load it
        df = pd.read_csv('./data.csv')
    else:
        # if file doesn't exist, create data frame
        df = pd.DataFrame(columns=['image_id', 'q', 'z', 's', 'd', 'zq', 'zd', 'sq', 'sd'])

    # list of dictionaries to make it faster to append to the dataframe
    data = []


    # loop of capturing frames with corresponding key pressed
    kc.start()

    while running:
        t1 = time.time()
        # get keys pressed
        keys = kc.get_keys()
        
        # get frame
        frame, map_gta = capture_frame(window)
        
        # keep only cars that are close to the car
        # cars_distances = [car for car in cars_distances if car[1] < 100]
        
        im_id=int(time.time() * 1000)
        
        if(os.path.exists('./tempScreenShots') == False):
            os.mkdir('./tempScreenShots')

        cv2.imwrite('./tempScreenShots/'+str(im_id)+'.png', frame)
        cv2.imwrite('./tempScreenShots/'+str(im_id)+'_map.png', map_gta)
        
        # append to the list of dictionaries
        temp = {}
        if(keys.count(1) <= 1):
            temp = {'image_id': im_id, 'q': keys[0], 'z': keys[1], 's': keys[2], 'd': keys[3], 'zq': 0, 'zd': 0, 'sq': 0, 'sd': 0}

        elif(keys.count(1) == 2):
            # if keys are z and q
            if(keys[0] == 1 and keys[1] == 1):
                temp = {'image_id': im_id, 'q': 0, 'z': 0, 's': 0, 'd': 0, 'zq': 1, 'zd': 0, 'sq': 0, 'sd': 0}
            # if keys are z and d
            elif(keys[1] == 1 and keys[3] == 1):
                temp = {'image_id': im_id, 'q': 0, 'z': 0, 's': 0, 'd': 0, 'zq': 0, 'zd': 1, 'sq': 0, 'sd': 0}
            # if keys are s and q
            elif(keys[0] == 1 and keys[2] == 1):
                temp = {'image_id': im_id, 'q': 0, 'z': 0, 's': 0, 'd': 0, 'zq': 0, 'zd': 0, 'sq': 1, 'sd': 0}
            # if keys are s and d
            elif(keys[2] == 1 and keys[3] == 1):
                temp = {'image_id': im_id, 'q': 0, 'z': 0, 's': 0, 'd': 0, 'zq': 0, 'zd': 0, 'sq': 0, 'sd': 1}
        else:
            temp = {'image_id': im_id, 'q': 0, 'z': 0, 's': 0, 'd': 0, 'zq': 0, 'zd': 0, 'sq': 0, 'sd': 0}

        data.append(temp)

        # print the fps
        print(f'FPS: {1/(time.time() - t1)}')

    kc.stop()

    print("Capturing finished")
    
    # promopt user if he wants to save the data
    save = tk.messagebox.askyesno('Save data', 'Do you want to save the data?')
    
    # if yes, save the data
    if(save):
        # append the data to the dataframe
        tempDf = pd.DataFrame(data, columns=['image_id', 'q', 'z', 's', 'd', 'zq', 'zd', 'sq', 'sd'])
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

    img_path = os.path.join(os.path.dirname(__file__), 'gtaVSelfDrivingCarBG.ico')
    root.wm_iconbitmap(img_path)


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


