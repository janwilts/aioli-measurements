from shapedetector import *
import numpy as np


class Frame:
    def __init__(self, frame):
        self._frame = frame

    @property
    def frame(self):
        return self._frame

    def contours(self, frame=None):
        """ Returns contours of the frame, either with own variable or externally supplied. """

        frame_type = self._frame
        if frame is not None:
            frame_type = frame

        _, frame_contours, _ = cv2.findContours(frame_type, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        return frame_contours

    def find_reference(self, reference_size_mm):
        """ Finds the reference object in the frame with the supplied size of the reference and frame """

        contours = self.contours(self._frame)

        if len(contours) < 1:
            return False, False

        reference = max(contours, key=cv2.contourArea)

        shape = ShapeDetector.detect(reference[0])

        if isinstance(shape, ellipsedetector.Ellipse):
            _, (min_a, max_a), _ = ellipsedetector.detect(reference)
            return reference_size_mm / max_a, max_a - min_a
        else:
            return False, False

    def remove_straights(self, user_frame=None, min_line_length=0, max_line_gap=0, draw_length=100):
        user_frame = cv2.GaussianBlur(user_frame, (5, 5), 0)
        gray = cv2.cvtColor(user_frame, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(gray, 50, 150, apertureSize=3)
        lines = cv2.HoughLinesP(edges, 1, np.pi / 180, 100, min_line_length, max_line_gap)
        if lines is not None:
            for line in lines:
                for x1, y1, x2, y2 in line:
                    x = (x1 + x2) / 2
                    y = (y1 + y2) / 2
                    tanyx = np.arctan((y2 - y1) / (x2 - x1))
                    x1 = int(x + draw_length * np.cos(tanyx))
                    y1 = int(y + draw_length * np.sin(tanyx))
                    x2 = int(x - draw_length * np.cos(tanyx))
                    y2 = int(y - draw_length * np.sin(tanyx))
                    cv2.line(edges, (x1, y1), (x2, y2), (0, 255, 0), 5)
        return edges