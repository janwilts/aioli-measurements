import cv2


class Ellipse:
    def __init__(self, x, y, min_a, max_a, angle):
        self.x = x
        self.y = y
        self.min_a = min_a
        self.max_a = max_a
        self.angle = angle

    @property
    def shape(self):
        return (self.x, self.y), (self.min_a, self.max_a), self.angle


def detect(contour):
    (x, y), (min_a, max_a), angle = cv2.fitEllipse(contour)
    ellipse = None
    if max_a / min_a > .2:
        ellipse = Ellipse(x, y, min_a, max_a, angle)
    return ellipse
