import numpy as np
from crop import crop
from camera import Camera
from frame import Frame
from shapeprocessor import *

# Constants
REQUIRED_WIDTH = 370
TRAY_SIZE = 50
REFERENCE_COLOR_LOW = [0, 0, 0]
REFERENCE_COLOR_UP = [0, 0, 0]
REFERENCE_SIZE_MM = 100

cameras = [Camera('USB Cam', 1, 'top')]


def main():
    """ Main, function, entry point """
    for camera in cameras:
        image = Frame(camera.snap())
        reference_px_mm, reference_diff = camera.calibrate(REFERENCE_COLOR_LOW, REFERENCE_COLOR_UP, REFERENCE_SIZE_MM)

        # Snap a frame ad process it, then find the contours
        processed = Frame(camera.snap_canny(image.frame))
        lines = cv2.HoughLinesP(processed.frame, 1, np.pi / 180, 20)

        if lines is None:
            # TODO: Gui error here
            cv2.imshow(cam.name, image.frame)
            continue

        # Return the cropped frame
        frame_crop = crop(image, lines, TRAY_SIZE)

        cv2.imshow('crop', frame_crop)
        cv2.imshow(cam.name, image.frame)

if __name__ == '__main__':
    for cam in cameras:
        cv2.namedWindow(cam.name)

    cv2.namedWindow('crop')

    while True:
        main()
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    for cam in cameras:
        cam.cap.release()
        cv2.destroyAllWindows()
