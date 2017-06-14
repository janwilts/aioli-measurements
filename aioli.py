import numpy as np
from camera import Camera
from frame import Frame
from shapedetector import *
from shapeprocessor import *


REQUIRED_WIDTH = 370
REFERENCE_SIZE_MM = 100
REFERENCE_COLOR_LOWER = [0, 0, 0]
REFERENCE_COLOR_UPPER = [0, 0, 0]

cameras = [Camera('USB Cam', 1)]

# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
# cv2.namedWindow("controls", 0)
#
# markLowRed = 28
# markLowGreen = 145
# markLowBlue = 54
# markUppRed = 90
# markUppGreen = 208
# markUppBlue = 176
#
# def setGreenr(x):
#     global markLowRed
#     markLowRed = x
# def setGreeng(x):
#     global markLowGreen
#     markLowGreen = x
# def setGreenb(x):
#     global markLowBlue
#     markLowBlue = x
# def setGreenR(x):
#     global markUppRed
#     markUppRed = x
# def setGreenG(x):
#     global markUppGreen
#     markUppGreen = x
# def setGreenB(x):
#     global markUppBlue
#     markUppBlue = x

# # create trackbar
# cv2.createTrackbar('g: r', "controls", 0, 255, setGreenr)
# cv2.createTrackbar('g: g', "controls", 0, 255, setGreeng)
# cv2.createTrackbar('g: b', "controls", 0, 255, setGreenb)
# cv2.createTrackbar('g: R', "controls", 0, 255, setGreenR)
# cv2.createTrackbar('g: G', "controls", 0, 255, setGreenG)
# cv2.createTrackbar('g: B', "controls", 0, 255, setGreenB)
# # set trackbar position
# cv2.setTrackbarPos('g: r', "controls", markLowRed)
# cv2.setTrackbarPos('g: g', "controls", markLowGreen)
# cv2.setTrackbarPos('g: b', "controls", markLowBlue)
# cv2.setTrackbarPos('g: R', "controls", markUppRed)
# cv2.setTrackbarPos('g: G', "controls", markUppGreen)
# cv2.setTrackbarPos('g: B', "controls", markUppBlue)
# # =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-


lowest_line = None
highest_line = None
crop = None

def main():
    # Loop through cameras
    for cam in cameras:
        image = Frame(cam.snap())

        # Get the difference between ellipse and circle on reference
        reference = Frame(cam.snap_color(REFERENCE_COLOR_LOWER, REFERENCE_COLOR_UPPER))
        reference_px_mm, reference_diff = reference.find_reference(REFERENCE_SIZE_MM)

        # Snap a frame ad process it, then find the contours
        processed = Frame(cam.snap_canny(image.frame))
        lines = cv2.HoughLinesP(processed.frame, 1, np.pi / 180, 20)

        if lines is None:
            # If the outer frame is not found
            cv2.imshow(cam.name, image.frame)
            continue

        global highest_line
        global lowest_line
        global crop

        height, width, _ = image.frame.shape

        if crop is None:
            crop = image.frame

        if highest_line is None and lowest_line is None:
            highest_line = [0, height / 2, width, height / 2]
            lowest_line = highest_line

        for x1, y1, x2, y2 in lines[0]:
            line = [0, y1, width, y2]
            center = (y1 + y2) / 2

            if lowest_line[1] > y1 and lowest_line[3] > y2:
                lowest_line = line
                crop = image.frame[center:, 0:]
                cv2.imshow('crop', crop)
            elif highest_line[1] < y1 and highest_line[3] < y2:
                print 'lower'
                highest_line = line
                crop = image.frame[:center, 0:]
                cv2.imshow('crop', crop)



            cv2.line(image.frame, (0, y1), (width, y2), (0, 0, 255), 2)

        cv2.imshow(cam.name, image.frame)
        # cv2.imshow(cam.name + 'color', cam.snap_color([markLowBlue, markLowGreen, markLowRed], [markUppBlue, markUppGreen, markUppRed]))


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
