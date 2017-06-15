import numpy as np
from frame import Frame
from shapedetector import *


class Camera:
    def __init__(self, name, cap, orientation):
        self._name = name
        self._cap = cv2.VideoCapture(cap)
        self._orientation = orientation

    @property
    def name(self):
        return self._name

    @property
    def cap(self):
        return self._cap

    @property
    def orientation(self):
        return self._orientation

    def snap(self):
        _, frame = self._cap.read()
        return frame

    def calibrate(self, reference_color_lower, reference_color_upper, reference_size_mm):
        """ Calibrates the camera by finding the reference object and returning its size in pixels """

        reference = Frame(self.snap_color(reference_color_lower, reference_color_upper))
        reference_px_mm, reference_diff = reference.find_reference(reference_size_mm)
        return reference_px_mm, reference_diff

    def snap_canny(self, image=None, snap=False):
        """ Creates a canny (outline) image using the snap method """

        if snap:
            image = self.snap()

        image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        image_blurred = cv2.GaussianBlur(image_gray, (5, 5), 0)
        image_bilateral = cv2.bilateralFilter(image_blurred, 5, 175, 175)
        image_edges = cv2.Canny(image_bilateral, 100, 200)
        image_edge_blur = cv2.GaussianBlur(image_edges, (5, 5), 0)
        return image_edge_blur

    def snap_color(self, lower, upper):
        """ Creates a color-filtered image based on the supplied RGB colors """

        frame = self.snap()

        lower_color = np.array(lower)
        upper_color = np.array(upper)

        frame_mask = cv2.inRange(frame, lower_color, upper_color)
        return frame_mask
