import cv2
import shape
import ellipsedetector


class ShapeDetector:
    def __init__(self):
        pass

    @classmethod
    def detect(cls, contour):
        perimeter = cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, 0.01 * perimeter, True)
        area = cv2.contourArea(contour)

        if len(approx) == 3:
            return shape.TRIANGLE

        elif len(approx) == 4:
            return shape.RECTANGLE

        elif len(approx) == 5:
            return shape.PENTAGON

        elif len(approx) == 6:
            return shape.HEXAGON

        elif len(approx) > 6 & len(approx) < 25 & int(area > 200):
            ellipse = ellipsedetector.detect(contour)

            if ellipse is None:
                return shape.CIRCLE
            else:
                return ellipse

        else:
            return shape.UNDEFINED
