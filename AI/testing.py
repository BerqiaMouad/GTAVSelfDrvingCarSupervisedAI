import numpy as np
import cv2 as cv
import matplotlib.pyplot as plt
import pandas as pd
import torch
from models.experimental import attempt_load
from utils.general import non_max_suppression, xyxy2xywh
from utils.torch_utils import time_synchronized
from PIL import ImageGrab, ImageTk, Image
import pygetwindow as gw
import time

# check device cpu of gpu
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
if torch.cuda.is_available():
    torch.cuda.empty_cache()

# Load model
model = attempt_load('yolov7.pt', map_location=device)

# Set parameters
if(device == 'cuda'):
    model.half()

img_size = (128, 128);
conf_thres = 0.25

if(device == 'cuda'):
    model(torch.zeros(1, 3, img_size).to(device).type_as(next(model.parameters())))

# function to detect object 
def detect_objects_per_frame(frame):
    # Resize image
    img = cv.resize(frame, img_size, img_size)
    img = img.transpose(2, 0, 1)  # HWC to CHW
    img = torch.from_numpy(img).to(device).float()
    img = img.half() if device == 'cuda' else img.float()  # uint8 to fp16/32
    img /= 255.0

    # Detect objects
    t1 = time_synchronized()
    with torch.no_grad():
        pred = model(img.unsqueeze(0), augment = False)[0]
    pred = non_max_suppression(pred, conf_thres, agnostic = False)
    t2 = time_synchronized()
    
    img = img.detach()
    del img

    # Process detections
    objs = {}
    for i, det in enumerate(pred):
        # Rescale detection coordinates
        if det is not None and len(det):

            # getting the x, y coordinates with the width and height and drawing the boxes
            for *xyxy, conf, cls in reversed(det):
                temp_tensor = torch.tensor(xyxy).view(1, 4)
                x, y, w, h = xyxy2xywh(temp_tensor).squeeze(0)
                xx, yy, ww, hh = (x / img_size[0]) * frame.shape[1], (y / img_size[1]) * frame.shape[0], (w / img_size[0]) * frame.shape[1], (h / img_size[1]) * frame.shape[0]
                
                # freeing memory occupied by the tensor
                temp_tensor = temp_tensor.detach()
                del temp_tensor
                torch.cuda.empty_cache()

                label = f'{model.names[int(cls)]} {conf:.2f}'
                objs[label] = [xx, yy, ww, hh]
                cv.rectangle(frame, (int(xx - ww / 2), int(yy - hh / 2)), (int(xx - ww / 2 + ww), int(yy - hh / 2 + hh)), (255, 255, 0), 2)
                cv.putText(frame, label, (int(xx - ww / 2), int(yy - h / 2) - 10), cv.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 0), 1)
    

    return (objs, frame, t1, t2)


# Get frame from game window
def capture_frame(window):
    # make screenshot of the window
    screenshot = ImageGrab.grab(bbox=(window.left, window.top, window.left + window.width, window.top + window.height))
    
    # convert to numpy array
    frame = np.array(screenshot)
    
    # convert to BGR
    frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)

    return frame



if __name__ == '__main__':
    
    window_name = "Grand Theft Auto V"

    # search for the first window with name of gta 5
    window = gw.getWindowsWithTitle(window_name)[0]

    # activate the window
    window.activate()

    while(True):
        tt1 = time_synchronized()
        # get the frame
        frame = capture_frame(window)

        # crop the frame
        frame = frame[50:490, :]

        # detect the objects
        objs, frame, t1, t2 = detect_objects_per_frame(frame)
    
        # print the time
        print(f"Detection Time: {t2 - t1} s |", end=" ")


        # show the frame
        cv.imshow(window_name, frame)

        # wait for 1ms
        if cv.waitKey(1) == ord('q'):
            break

        tt2 = time_synchronized()

        print(f'FPS: {1 / (tt2 - tt1)}')


    
