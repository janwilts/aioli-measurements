from frame import Frame
from shapedetector import *


class Camera:
    def __init__(self, name, cap, status=False):
        self._name = name
        self._cap = cv2.VideoCapture(cap)
        self._status = status
        self._reference = None

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

    def snap_canny(self, image=None, snap=False):
        """ Creates a canny (outline) image using the snap method """

        if snap:
            image = self.snap().frame

        image_blurred = cv2.GaussianBlur(image, (5, 5), 0)
        image_gray = cv2.cvtColor(image_blurred, cv2.COLOR_BGR2GRAY)
        image_edges = cv2.Canny(image_gray, 50, 150, apertureSize=3)
        return Frame(image_edges)

    def snap_rotation(self, crop_pixels):
        frame = self.snap()
        rotation_angle = frame.get_rotation()
        rotated_frame = frame.rotate_frame(rotation_angle)

        height, width = rotated_frame.shape
        rotated_frame_crop = rotated_frame.frame[crop_pixels:height - 2*crop_pixels, crop_pixels:width - 2*crop_pixels]
        return Frame(rotated_frame_crop)


    def calibrate(self, amount_of_frames):
        """ Calibrates the camera by snapping 5 images and summing them """
        self._reference = self.snap_rotation(0)

        total_frame = None
        for i in xrange(0, amount_of_frames, 1):
            image = self.snap_canny(snap=True)
            if i > 0:
                total_frame += image.frame
            else:
                total_frame = image.frame
        self._reference_canny = Frame(total_frame)
