import numpy as np
from crop import *
from camera import Camera
from shapedetector import *

# Constants
REQUIRED_WIDTH = 370
TRAY_SIZE = 50
REFERENCE_COLOR_LOW = [0, 0, 0]
REFERENCE_COLOR_UP = [0, 0, 0]
REFERENCE_SIZE_MM = 100

cameras = [Camera('USB Cam', 1)]


def main():
    """ Main, function, entry point """
    for camera in cameras:
        frame_edges = camera.snap_canny(snap=True)

        subtracted_edges = frame_edges.subtract(camera.reference)
        contours = subtracted_edges.thresh_contours()

        for contour in contours:
            contour_area = cv2.contourArea(contour)
            if contour_area > 5:
                print contour_area

        cv2.imshow('edges', frame_edges.frame)
        cv2.imshow('subtracted', subtracted_edges.frame)
        cv2.imshow('reference', cam.reference.frame)


if __name__ == '__main__':
    for cam in cameras:
        cv2.namedWindow(cam.name)
        cam.calibrate(5)

    while True:
        main()
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    for cam in cameras:
        cam.cap.release()
        cv2.destroyAllWindows()
