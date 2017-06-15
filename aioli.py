import numpy as np
from crop import crop_image
from camera import Camera
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
        image = camera.snap()
        reference_px_mm, reference_diff = camera.calibrate(REFERENCE_COLOR_LOW, REFERENCE_COLOR_UP, REFERENCE_SIZE_MM)

        # Snap a frame ad process it, then find the contours
        processed = camera.snap_canny(image.frame)
        lines = cv2.HoughLinesP(processed.frame, 1, np.pi / 180, 400)

        if lines is None:
            # TODO: Gui error here
            cv2.imshow(cam.name, image.frame)
            continue

        # Return the cropped frame
        crop = crop_image(image, lines, TRAY_SIZE)

        cv2.imshow('crop', crop.frame)
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
