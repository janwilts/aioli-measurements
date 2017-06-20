from shapedetector import *
import numpy as np


class Frame:
    def __init__(self, frame):
        self._frame = frame

    @property
    def frame(self):
        return self._frame

    def subtract(self, subtracting):
        return Frame(self._frame - subtracting.frame)

    def thresh_contours(self):
        _, thresh = cv2.threshold(self._frame, 127, 255, 0)
        _, contours, _ = cv2.findContours(thresh, 1, 2)
        return contours
