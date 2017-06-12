import cv2


class Ellipse:
    def __init__(self, x, y, min_a, max_a, angle):
        self.x = int(x)
        self.y = int(y)
        self.min_a = int(min_a)
        self.max_a = int(max_a)
        self.angle = int(angle)

    @property
    def shape(self):
        return (self.x, self.y), (self.min_a, self.max_a), self.angle


def detect(contour):
    (x, y), (min_a, max_a), angle = cv2.fitEllipse(contour)
    ellipse = Ellipse(x, y, min_a, max_a, angle)
    return ellipse
