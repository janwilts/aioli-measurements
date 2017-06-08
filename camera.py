import cv2


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
