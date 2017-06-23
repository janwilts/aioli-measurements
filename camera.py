import math
from crop import crop_rotated_image
from frame import Frame
from shapedetector import *


class Camera:
    def __init__(self, name, cap, status=False):
        self._name = name
        self._cap = cv2.VideoCapture(cap)
        self._status = status
        self._reference = None
        self._reference_canny = None

    @property
    def name(self):
        return self._name

    @property
    def cap(self):
        return self._cap

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, value):
        self._status = value

    @property
    def reference(self):
        if self._reference is not None:
            return self._reference

    @property
    def reference_canny(self):
        if self._reference_canny is not None:
            return self._reference_canny

    @property
    def angle_smoothing_array(self):
        return self._angle_smoothing_array

    def status(self):
        test_frame = self.snap()
        if test_frame.frame is None:
            return False
        return True

    def snap(self):
        _, frame = self._cap.read()
        return Frame(frame)

    def snap_canny(self, frame=None):
        """ Creates a canny (outline) image using the snap method """

        if frame is None:
            frame = self.snap().frame

        image_blurred = cv2.GaussianBlur(frame, (5, 5), 0)
        image_gray = cv2.cvtColor(image_blurred, cv2.COLOR_BGR2GRAY)
        image_edges = cv2.Canny(image_gray, 50, 150, apertureSize=3)
        return Frame(image_edges)

    def snap_rotation(self, crop_pixels, frame=None):
        """ Snaps a rotated image, by using some external frame-methods """

        if frame is None:
            frame = self.snap()

        rotation_angle = frame.get_rotation()
        rotated_frame = frame.rotate_frame(rotation_angle)

        height, width = rotated_frame.shape
        rotated_frame_crop = rotated_frame.frame[crop_pixels:height - 2*crop_pixels, crop_pixels:width - 2*crop_pixels]
        return Frame(rotated_frame_crop), rotation_angle

    def calibrate(self, amount_of_frames):
        """ Calibrates the camera by snapping 5 images and summing them """

        reference, angle = self.snap_rotation(0)
        reference_height, reference_width = reference.shape
        radians = math.radians(angle)
        crop_rotated_image(radians, reference_height, reference_width)

        self._reference = reference

        total_frame = None
        for i in xrange(0, amount_of_frames, 1):
            canny = self.snap_canny(self._reference.frame)
            if i > 0:
                total_frame += canny.frame
            else:
                total_frame = canny.frame

        self._reference_canny = Frame(total_frame)
