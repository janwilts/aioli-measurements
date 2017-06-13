import cv2


class Frame:
    def __init__(self, frame):
        self._frame = frame

    @property
    def frame(self):
        return self._frame

    def contours(self):
        _, frame_contours, _ = cv2.findContours(self._frame, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        return frame_contours
