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

cameras = [Camera('USB Cam', 1, 'top-down')]


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
        straights = crop.remove_straights()

        _, straights_contours, _ = cv2.findContours(straights.frame, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        for contour in straights_contours:
            contour_shape = ShapeDetector.detect(contour)

            if isinstance(contour_shape, ellipsedetector.Ellipse):
                (x, y), (min_a, max_a), angle = contour_shape.shape
                cv2.ellipse(crop.frame, contour_shape.shape, (0, 255, 0), 3)
                cv2.drawContours(crop.frame, [contour], -1, (0, 0, 255), 2)
                cv2.circle(crop.frame, (int(x), int(y)), int(max_a / 2), (255, 0, 0), 2)

        cv2.imshow('crop', crop.frame)
        cv2.imshow('test', straights.frame)
        cv2.imshow(cam.name, image.frame)


if __name__ == '__main__':
    for cam in cameras:
        cv2.namedWindow(cam.name)

    cv2.namedWindow('crop')
    cv2.namedWindow('test')

    while True:
        main()
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    for cam in cameras:
        cam.cap.release()
        cv2.destroyAllWindows()
