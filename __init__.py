from camera import *
from shapedetector import *


cameras = [Camera('USB Cam', 1)]

for cam in cameras:
    cv2.namedWindow(cam.name)

while True:
    for cam in cameras:
        _, frame = cam.cap.read()

        frame_bilateral = cv2.bilateralFilter(frame, 5, 175, 175)
        frame_edges = cv2.Canny(frame_bilateral, 75, 200)

        _, frame_contours, _ = cv2.findContours(frame_edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        for contour in frame_contours:
            M = cv2.moments(contour)

            if M['m00'] == 0:
                M['m00'] = 1

            cX = int(M['m10'] / M['m00'])
            cY = int(M['m01'] / M['m00'])

            shape = ShapeDetector.detect(contour)

            if shape.name == 'circle':
                cv2.drawContours(frame, [contour], -1, (0, 255, 0), 2)
                cv2.circle(frame, (cX, cY), 7, (255, 255, 255), -1)
                cv2.putText(frame, shape.name, (cX, cY), cv2.QT_FONT_BLACK, 1, (255, 255, 255), 2)

            cv2.imshow(cam.name, frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

for cam in cameras:
    cam.cap.release()

cv2.destroyAllWindows()

