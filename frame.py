import math
import cv2


class Frame:
    def __init__(self, frame):
        """ Constructor """
        self._frame = frame

    @property
    def frame(self):
        """ The main frame, numpy array """
        return self._frame

    @property
    def shape(self):
        """ Returns the shape of the frame, width and height """
        height, width, _ = self._frame.shape
        return height, width

    def binary(self, min_thresh, max_thresh, inv=False):
        """ Returns a binary image from frame """
        thresh = cv2.THRESH_BINARY
        if inv:
            thresh = cv2.THRESH_BINARY_INV
        _, output = cv2.threshold(self._frame, min_thresh, max_thresh, thresh)
        return output

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

    # Unused code from the marker detection

    # -----------------------------------------------------------------------------------------------------------------
    # def get_marker_pos(self, min_val, line_range, line_tresh, skip_edge_pixels=5):
    #     height, width = self._frame.shape
    #     frame_edges = self._frame
    #
    #     xpos = 0
    #     ypos = 0
    #     for row in frame_edges[:height/2]:
    #         if row[0] > min_val or row[width-1]:
    #             x = xpos
    #             y = skip_edge_pixels
    #             for col in row[:width/2]:
    #                 count_values = []
    #                 for z in xrange(line_range):
    #                     if frame_edges[x-z][y] > min_val:
    #                         count_values.append(True)
    #                 if len(count_values) > line_tresh:
    #                     ypos = y
    #                     break
    #                 y += 1
    #         if ypos > 0:
    #             return (xpos, ypos)
    #         xpos += 1
    #     return (xpos, ypos)
    # -----------------------------------------------------------------------------------------------------------------

    def subtract(self, subtracting):
        """ Subtract a frame from current frame """
        return Frame(self._frame - subtracting)

    def thresh_contours(self):
        """ Returns the contours within the frame """
        _, thresh = cv2.threshold(self._frame, 127, 255, 0)
        _, contours, _ = cv2.findContours(thresh, 1, 2)
        return contours
