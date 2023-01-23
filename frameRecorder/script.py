import keyboard
import cv2
import numpy as np
import pyautogui
import pygetwindow as gw
import time
import pandas as pd


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


if __name__ == '__main__':
    window_name='Google Chrome'
    
    # search for the first window with name of trackmania
    window = gw.getWindowsWithTitle(window_name)[0]

    # activate the window
    window.activate()
    
    # creating dataframe to store the data
    df = pd.DataFrame(columns=['image_id', 'key_pressed'])

    # loop of capturing frames with corresponding key pressed
    while True:
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
        df = df.append({'image_id': im_id, 'q': q, 'z': z, 's': s, 'd': d, 'No Key': no_key}, ignore_index=True)
        df.to_csv('./data.csv', index=False)



        
