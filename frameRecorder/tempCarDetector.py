import cv2
import pandas as pd

class CarDetector:
    def __init__(self, image):
        self.image = image
        self.image_copy = image.copy()
        self.gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        self.blurred = cv2.GaussianBlur(self.gray, (5, 5), 0)
        self.car_classifier = cv2.CascadeClassifier('./cars.xml')
        self.cars = self.car_classifier.detectMultiScale(self.blurred, 1.1, 3)
        self.real_width = 6
        self.pixel_width = self.cars[0][2]
        self.focal_length = (self.pixel_width * 100) / self.real_width
        self.distances = []

    def get_distance(self):
        for (x, y, w, h) in self.cars:
            distance = (self.focal_length * self.real_width) / w
            self.distances.append(distance)
        return self.distances

