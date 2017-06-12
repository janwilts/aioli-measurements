from camera import Camera
from shapedetector import *
from shapeprocessor import *


REQUIRED_WIDTH = 370
REFERENCE_OBJ_COLOR = ([], [])

cameras = [Camera('USB Cam', 1)]


def main():
    for cam in cameras:
        frame = cam.snap()

        frame_processed = cam.snap_canny(frame)

        _, frame_contours, _ = cv2.findContours(frame_processed, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        for contour in frame_contours:

            shape = ShapeDetector.detect(contour)

            if isinstance(shape, ellipsedetector.Ellipse):
                (x, y), (min_a, max_a), angle = shape.shape
                cv2.ellipse(frame, shape.shape, (0, 255, 0), 3)
                cv2.drawContours(frame, [contour], -1, (0, 0, 255), 2)
                cv2.circle(frame, (int(x), int(y)), int(max_a / 2), (255, 0, 0), 2)

                sp = ShapeProcessor(max_a)
                sp.compare_shape(REQUIRED_WIDTH)

        cv2.imshow(cam.name, frame)
        cv2.imshow(cam.name + 'color', cam.snap_color([100, 80, 80], [140, 120, 120]))


if __name__ == '__main__':
    for cam in cameras:
        cv2.namedWindow(cam.name)

    while True:
        main()
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    for cam in cameras:
        cam.cap.release()
        cv2.destroyAllWindows()
