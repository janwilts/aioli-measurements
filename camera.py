import cv2
import numpy as np


class Camera:
    def __init__(self, name, cap):
        self._name = name
        self._cap = cv2.VideoCapture(cap)

    @property
    def name(self):
        return self._name

    @property
    def cap(self):
        return self._cap

    def snap(self):
        _, frame = self._cap.read()
        return frame

    def snap_canny(self, image=None, snap=False):
        if snap:
            image = self.snap()

        image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        image_blurred = cv2.GaussianBlur(image_gray, (5, 5), 0)
        image_bilateral = cv2.bilateralFilter(image_blurred, 5, 175, 175)
        image_edges = cv2.Canny(image_bilateral, 100, 200)

        return image_edges

    def snap_color(self, lower, upper):
        frame = self.snap()
        frame_hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        lower_color = np.array(lower)
        upper_color = np.array(upper)

        frame_mask = cv2.inRange(frame_hsv, lower_color, upper_color)

        return frame_mask
