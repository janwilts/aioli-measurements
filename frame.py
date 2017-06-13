from shapedetector import *


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
