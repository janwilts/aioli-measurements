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

    @property
    def binary(self, inv=False):
        thresh = cv2.THRESH_BINARY
        if inv:
            thresh = cv2.THRESH_BINARY_INV
        _, output = cv2.threshold(self._frame, 127, 255, thresh)
        return Frame(output)

    def get_rotation(self):
        """ looks in the most left and most right rows of the frame, finds the first edges and calculates the angle """
        _, width = self.shape
        width -= 1

        frame_gray = cv2.cvtColor(self._frame, cv2.COLOR_BGR2GRAY)
        frame_edges = cv2.Canny(frame_gray, 50, 150, 0)

        top_left = 0
        top_right = 0
        count = 0.0
        for x in frame_edges:
            if x[0] == 255 and top_left == 0:
                top_left = count
                if top_right > 0:
                    break
            if x[width] == 255 and top_right == 0:
                top_right = count
                if top_left > 0:
                    break
            count += 1

        return math.degrees(math.atan2(top_right - top_left, width+1))


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
