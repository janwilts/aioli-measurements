import math
from crop import crop_rotated_image
from frame import Frame
import numpy as np
from shapedetector import *


class Camera:
    def __init__(self, name, cap, angle_smoothing_length, status=False):
        self._name = name
        self._cap = cv2.VideoCapture(cap)
        self._status = status
        self._reference = None
        self._reference_canny = None
        self._angle_smoothing_array = []
        for i in xrange(0, angle_smoothing_length, 1):
            self._angle_smoothing_array.append(None)
        self._cap.set(3, 1080)
        self._cap.set(4, 1080)

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

    def snap_calibration_frame(self, angle_array):
        frame = self.snap()
        rotation_angle = frame.get_rotation()
        if 15 > rotation_angle > -15:
            if angle_array[0] is not None:
                angle_array.append(rotation_angle)
            else:
                angle_array[0] = rotation_angle
            self.insert_angle(self._angle_smoothing_array, rotation_angle, -15, 15)
        return Frame(frame), angle_array

    def snap_rotation(self, crop_pixels, frame=None):
        """ Snaps a rotated image, by using some external frame-methods """

        if frame is None:
            frame = self.snap()

        rotation_angle = frame.get_rotation()
        angle_array = self.insert_angle(self._angle_smoothing_array, rotation_angle, -15, 15)
        self._angle_smoothing_array = angle_array
        smoothed_angle, _ = self.smooth_angle(angle_array, 1.5)

        rotated_frame = frame.rotate_frame(smoothed_angle)
        height, width = rotated_frame.shape
        rotated_frame_crop = rotated_frame.frame[crop_pixels:height - crop_pixels, crop_pixels:width - crop_pixels]
        return Frame(rotated_frame_crop), smoothed_angle

    def insert_angle(self, array, new_angle, min_angle, max_angle):
        if max_angle > new_angle > min_angle:
            array.append(new_angle)
            array.remove(array[0])
        return array

    def smooth_angle(self, array, difference_threshold):
        """  """
        groups = [[]]
        for i in xrange(1, len(array)):
            if array[0] is None:
                array = array[1:]
            else:
                groups = [[array[0]]]
                break
        for x in xrange(1, len(array)):
            for y in xrange(0, len(groups)):
                if array[x] is not None:
                    if np.mean(groups[y]) - difference_threshold < array[x] < np.mean(groups[y]) + difference_threshold:
                        groups[y].append(array[x])
                    else:
                        groups.append([array[x]])
        group_size = 0
        smoothed_angle = 0
        for group in groups:
            if len(group) > (len(array) / 2):
                smoothed_angle = np.mean(group)
                group_size = len(group)
            elif len(group) > group_size:
                group_size = len(group)
        if group_size < (len(array) / 2):
            print 'WARNING: Rotation measurements are spread too much'
            smoothed_angle = array[len(array)-1]
        return smoothed_angle, group_size

    def calibrate(self, amount_of_frames):
        """ Calibrates the camera by snapping x amount of images and rotating them according to the smoothed angle """
        calibration_frames = []
        angle_array = [None]
        for i in xrange(0, amount_of_frames, 1):
            frame, angle_array = self.snap_calibration_frame(angle_array)
            calibration_frames.append(frame.frame)

        smoothed_angle, group_size = self.smooth_angle(angle_array, 1.5)
        if group_size < len(angle_array) - 1:
            return False

        total_frame = None
        for i in xrange(0, amount_of_frames, 1):
            calibration_frames[i] = calibration_frames[i].rotate_frame(smoothed_angle)
            canny = self.snap_canny(calibration_frames[i].frame)

            if i > 0:
                total_frame += canny.frame
            else:
                total_frame = canny.frame

        self._reference_canny = Frame(total_frame)
        self._reference = Frame(calibration_frames[amount_of_frames - 1].frame)
        return True
