import math
import numpy as np
from crop import crop_image
from shapedetector import *


class Frame:
    def __init__(self, frame):
        self._frame = frame

    @property
    def frame(self):
        return self._frame

    @property
    def shape(self):
        height, width, _ = self._frame.shape
        return height, width

    def get_rotation(self):
        height, width = self.shape

        frame_gray = cv2.cvtColor(self._frame, cv2.COLOR_BGR2GRAY)
        frame_edges = cv2.Canny(frame_gray, 50, 150, 0)
        frame_blurred_edges = cv2.GaussianBlur(frame_edges, (5, 5), 0)
        frame_lines = cv2.HoughLinesP(frame_blurred_edges, 1, np.pi / 100, 150, 50, 10)

        top_left, top_right = crop_image(frame_lines, height, width)

        if top_left and top_right:
            return math.degrees(math.atan2(float(top_right[1] - top_left[1]), float(top_right[0] - top_left[0])))

        else:
            return 0

    def rotate_frame(self, degrees):
        """ Rotates an image using a rotation matrix, arguments: degrees to rotate """

        height, width = self.shape
        center_point = (width / 2, height / 2)
        rotation_matrix = cv2.getRotationMatrix2D(center_point, degrees, 1.0)
        rotated_image = cv2.warpAffine(self._frame, rotation_matrix, (width, height))
        return Frame(rotated_image)

    def subtract(self, subtracting):
        return Frame(self._frame - subtracting)

    def thresh_contours(self):
        _, thresh = cv2.threshold(self._frame, 127, 255, 0)
        _, contours, _ = cv2.findContours(thresh, 1, 2)
        return contours
