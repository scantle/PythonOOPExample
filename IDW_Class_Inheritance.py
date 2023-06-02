"""
Example of Inverse Distance Weighting (IDW) as part of a class
"""
import numpy as np

# -------------------------------------------------------------------------------------------------------------------- #
# Functions
# -------------------------------------------------------------------------------------------------------------------- #

class Point(object):
    def __init__(self, x, y, value=None):
        """ Initiate Object, assign values to object attributes"""
        self.x = x
        self.y = y
        self.v = value

    def distance(self, other):
        return ((self.x - other.x) ** 2 + (self.y - other.y) ** 2) ** 0.5

    def __sub__(self, other):
        if type(other) is Point:
            return self.distance(other)
        elif hasattr(other, '__iter__'):
            return np.array([self.distance(item) for item in other])
        else:
            raise TypeError("Can only subtract Point instances")

# -------------------------------------------------------------------------------------------------------------------- #

class Interpolate(object):
    def __init__(self, data: list):
        self.data = data

    def _calc_method(self, p):
        """ Default: closest value"""
        imin = np.argmin(p - self.data)
        return self.data[imin].v

    def calc(self, p: Point):
        return self._calc_method(p)

# -------------------------------------------------------------------------------------------------------------------- #

class IDW(Interpolate):
    def __init__(self, data: list, n=2):
        super().__init__(data)
        self.n = 2

    # Static method! Doesn't rely on anything in the object
    @staticmethod
    def _calc_weight(p1: Point, p2: Point, n: float):
        """ Calculate inverse distance weight given (x1,y1) and (x2,y2) and power value n"""
        return 1/((p1-p2)**n)

    # OVERRIDE BASE CLASS METHOD!!
    def _calc_method(self, p: Point):
        """ Inverse Distance weighted interpolation to point (px, py)
        :param p: Interpolation point
        :param n: Power value (usually 2)
        :return: interpolated value at point (px, py)
        """
        weights = self._calc_weight(p, self.data, self.n)
        values = [item.v for item in self.data]
        return np.dot(weights, values)/weights.sum()

# -------------------------------------------------------------------------------------------------------------------- #
# Main
# -------------------------------------------------------------------------------------------------------------------- #
data_coords = np.meshgrid(np.arange(0, 10.0), np.arange(0, 10.0))
points = []
for x, y in zip(data_coords[0].flatten(), data_coords[1].flatten()):
    points.append(Point(x, y, value=np.sqrt(x**2.85 + y**2)))

# Setup point we're interpolating to
p = Point(x=5.5, y=5.5)

# Base method
interp = Interpolate(points)
interp.calc(p=p)

interp = IDW(points)
interp.calc(p=p)