import numpy as np
from shapedetector import *
from frame import Frame


class FrameProcessor:
    def __init__(self, angle_smoothing_length):
        self._reference = None
        self._reference_canny = None
        self._angle_smoothing_array = []
        for i in xrange(angle_smoothing_length):
            self._angle_smoothing_array.append(None)

    @property
    def reference(self):
        if self._reference is not None:
            return Frame(self._reference)

    @property
    def reference_canny(self):
        if self._reference_canny is not None:
            return self._reference_canny

    @property
    def angle_smoothing_array(self):
        return self._angle_smoothing_array

    @classmethod
    def frame_canny(cls, frame):
        """ Creates a canny (outline) image using the snap method """

        image_blurred = cv2.GaussianBlur(frame, (5, 5), 0)
        image_gray = cv2.cvtColor(image_blurred, cv2.COLOR_BGR2GRAY)
        image_edges = cv2.Canny(image_gray, 50, 150, apertureSize=3)
        return Frame(image_edges)

    def get_calibration_frame(self, angle_array, frame):

        rotation_angle = frame.get_rotation()
        if 15 > rotation_angle > -15:
            if angle_array[0] is not None:
                angle_array.append(rotation_angle)
            else:
                angle_array[0] = rotation_angle
            self.insert_angle(self._angle_smoothing_array, rotation_angle, -15, 15)
        return Frame(frame), angle_array

    def frame_rotation(self, crop_pixels, frame):
        """ Snaps a rotated image, by using some external frame-methods """

        rotation_angle = frame.get_rotation()
        angle_array = self.insert_angle(self._angle_smoothing_array, rotation_angle, -15, 15)
        self._angle_smoothing_array = angle_array
        smoothed_angle, _ = self.smooth_angle(angle_array, 1.5)

        rotated_frame = frame.rotate_frame(smoothed_angle)
        height, width = rotated_frame.shape
        rotated_frame_crop = rotated_frame.frame[crop_pixels:height - crop_pixels, crop_pixels:width - crop_pixels]
        return Frame(rotated_frame_crop), smoothed_angle

    @classmethod
    def insert_angle(cls, array, new_angle, min_angle, max_angle):

        if max_angle > new_angle > min_angle:
            array.append(new_angle)
            array.remove(array[0])
        return array

    @classmethod
    def smooth_angle(cls, array, difference_threshold):
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

    def calibrate(self, amount_of_frames, frame):
        """ Calibrates the camera by snapping x amount of images and rotating them according to the smoothed angle """

        calibration_frames = []
        angle_array = [None]
        for i in xrange(0, amount_of_frames, 1):
            frame, angle_array = self.get_calibration_frame(angle_array, frame)
            calibration_frames.append(frame.frame)

        smoothed_angle, group_size = self.smooth_angle(angle_array, 1.5)
        if group_size < len(angle_array) - 1:
            return False

        total_frame = None
        for i in xrange(0, amount_of_frames, 1):
            calibration_frames[i] = calibration_frames[i].rotate_frame(smoothed_angle)
            canny = self.frame_canny(calibration_frames[i].frame)

            if i > 0:
                total_frame += canny.frame
            else:
                total_frame = canny.frame

        self._reference_canny = Frame(total_frame)
        self._reference = Frame(calibration_frames[amount_of_frames - 1].frame)
        return self._reference.frame, self._reference_canny
