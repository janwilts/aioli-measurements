class Shape:
    def __init__(self, name, sides):
        self._name = name
        self._sides = sides

    @property
    def name(self):
        return self._name

    @property
    def sides(self):
        return self._sides

UNDEFINED = Shape('undefined', 0)
TRIANGLE = Shape('triangle', 3)
RECTANGLE = Shape('rectangle', 4)
PENTAGON = Shape('pentagon', 5)
HEXAGON = Shape('hexagon', 6)
CIRCLE = Shape('circle', -1)
ELLIPSE = Shape('ellipse', -1)
