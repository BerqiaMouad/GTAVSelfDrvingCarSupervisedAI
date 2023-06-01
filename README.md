# **GTAVSDC: GTA V Self Driving Car**

<p>
The goal of this project is to create an AI agent that can navigate the streets of Los
Santos, the fictional city in GTA 5, while following a predetermi-ned route.
</p>
<p>
The main challenge of this project is to develop an AI agent that can generalize well
to new situations and environments, beyond the specific scenarios it has been trained
on. In addition, it is important to ensure that the AI agent operates safely and does not
cause harm to pedestrians or other vehicles.
</p>



## **Table of content**
+ [Introduction](#introduction)
+ [Features](#features)
+ [Installation](#installation)
+ [Usage](#usage)
+ [Contributing](#contributing)


## **Introduction**
<p>
In recent years, self-driving cars have become a hot topic in the world of technology
and transportation. The idea of vehicles that can operate autonomously, without human
intervention, has captured the imaginations of many engineers and researchers around
the globe. As a result, numerous companies and organizations are working on developing
this technology to make it a reality.
</p>
<p>
One way to test and develop self-driving car algorithms is through simulation. Video
game environments, such as Grand Theft Auto V (GTA 5), provide an opportunity to
create a realistic simulation for autonomous driving. In this project, we explore the use
of supervised AI to control a self-driving car in GTA 5.
</p>

## **Features**

### **Lane Detection**
<p>
Our AI agent uses lane detection to determine the direction of the road and to stay in the correct lane. We use OpenCV with the Cany mask to find the lanes.
</p>

### **Following a Route**
<p>
Our AI agent uses another CNN to detect the route and follow it. We use a CNN to detect the route. This model is not an independent model, it is a part of the main model. The main model uses the output of this model to determine the direction of the road and to stay in the correct lane.
</p>

### **Features to be added**
+ Object detection
+ Traffic lights detection

## **Installation**

To install the project, you need to install the following dependencies:
+ [Python 3.6](https://www.python.org/downloads/release/python-360/)
+ [Tensorflow 1.14](https://www.tensorflow.org/install/pip)
+ [OpenCV 4.1.1](https://pypi.org/project/opencv-python/)
+ [Numpy 1.16.4](https://pypi.org/project/numpy/)
+ [Pillow 6.1.0](https://pypi.org/project/Pillow/)
+ [PyAutoGUI 0.9.48](https://pypi.org/project/PyAutoGUI/)
+ [PyGetWindow 0.0.5](https://pypi.org/project/PyGetWindow/)
+ [Tkinter 8.6]
+ [Custom Tkinter 0.3](https://pypi.org/project/customtkinter/0.3/) 
+ [Pynput 1.7.6](https://pypi.org/project/pynput/)

Then Clone the repo using the following command:
```bash
git clone --recurse-submodules git@github.com:BerqiaMouad/GTAVSelfDrvingCarSupervisedAI.git 
```

## **Usage**

To run the project, you need to go to the project directory and then go the AI directory and run the Drive.py file using the following command:
```bash
python Drive.py
```
Wait for the model to be loaded, you will see a message in the terminal indicating that the model is loaded. Then press F8 to start the AI agent. To stop the AI agent, press F9.

## **Contributing**

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

