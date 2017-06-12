from camera import Camera
from frame import Frame
from shapedetector import *
from shapeprocessor import *


REQUIRED_WIDTH = 370
REFERENCE_COLOR_LOWER = [0, 0, 0]
REFERENCE_COLOR_UPPER = [0, 0, 0]

cameras = [Camera('USB Cam', 1)]

# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
cv2.namedWindow("controls", 0)

markLowRed = 28
markLowGreen = 145
markLowBlue = 54
markUppRed = 90
markUppGreen = 208
markUppBlue = 176

def setGreenr(x):
    global markLowRed
    markLowRed = x
def setGreeng(x):
    global markLowGreen
    markLowGreen = x
def setGreenb(x):
    global markLowBlue
    markLowBlue = x
def setGreenR(x):
    global markUppRed
    markUppRed = x
def setGreenG(x):
    global markUppGreen
    markUppGreen = x
def setGreenB(x):
    global markUppBlue
    markUppBlue = x

# create trackbar
cv2.createTrackbar('g: r', "controls", 0, 255, setGreenr)
cv2.createTrackbar('g: g', "controls", 0, 255, setGreeng)
cv2.createTrackbar('g: b', "controls", 0, 255, setGreenb)
cv2.createTrackbar('g: R', "controls", 0, 255, setGreenR)
cv2.createTrackbar('g: G', "controls", 0, 255, setGreenG)
cv2.createTrackbar('g: B', "controls", 0, 255, setGreenB)
# set trackbar position
cv2.setTrackbarPos('g: r', "controls", markLowRed)
cv2.setTrackbarPos('g: g', "controls", markLowGreen)
cv2.setTrackbarPos('g: b', "controls", markLowBlue)
cv2.setTrackbarPos('g: R', "controls", markUppRed)
cv2.setTrackbarPos('g: G', "controls", markUppGreen)
cv2.setTrackbarPos('g: B', "controls", markUppBlue)
# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-


def main():
    # Loop through cameras
    for cam in cameras:
        image = Frame(cam.snap())

        # Get the difference between ellipse and circle on reference
        reference = Frame(cam.snap_color(REFERENCE_COLOR_LOWER, REFERENCE_COLOR_UPPER))
        reference_px_mm, reference_diff = cam.find_reference(reference.frame, 100)

        # Snap a frame ad process it, then find the contours
        processed = Frame(cam.snap_canny(image.frame))
        contours = processed.contours()

        if contours > 2:
            pass

        for contour in contours:

            shape = ShapeDetector.detect(contour)

            if isinstance(shape, ellipsedetector.Ellipse):
                (x, y), (min_a, max_a), angle = shape.shape
                cv2.ellipse(image.frame, shape.shape, (0, 255, 0), 3)
                cv2.drawContours(image.frame, [contour], -1, (0, 0, 255), 2)
                cv2.circle(image.frame, (int(x), int(y)), int(max_a / 2), (255, 0, 0), 2)

                sp = ShapeProcessor(max_a)
                sp.compare_shape(REQUIRED_WIDTH)

        cv2.imshow(cam.name, image.frame)
        cv2.imshow(cam.name + 'color', cam.snap_color([markLowBlue, markLowGreen, markLowRed], [markUppBlue, markUppGreen, markUppRed]))


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
