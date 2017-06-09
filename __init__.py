from camera import *
from shapedetector import *


cameras = [Camera('USB Cam', 1)]

for cam in cameras:
    cv2.namedWindow(cam.name)

while True:
    for cam in cameras:
        frame = cam.snap()

        frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        frame_blurred = cv2.GaussianBlur(frame_gray, (5, 5), 0)
        frame_bilateral = cv2.bilateralFilter(frame_blurred, 5, 175, 175)
        frame_edges = cv2.Canny(frame_bilateral, 100, 200)

        _, frame_contours, _ = cv2.findContours(frame_edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        for contour in frame_contours:

            shape = ShapeDetector.detect(contour)

            if isinstance(shape, ellipsedetector.Ellipse):
                (x, y), (min_a, max_a), angle = shape.shape
                ellipse = shape.shape
                cv2.ellipse(frame, ellipse, (0, 255, 0), 3)
                cv2.drawContours(frame, [contour], -1, (0, 0, 255), 2)
                cv2.circle(frame, (int(x), int(y)), int(max_a / 2), (255, 0, 0), 2)

        cv2.imshow(cam.name, frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

for cam in cameras:
    cam.cap.release()
cv2.destroyAllWindows()
