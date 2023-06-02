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

    # Static method! Doesn't rely on anything in the object
    @staticmethod
    def _calc_weight(p1: Point, p2: Point, n: float):
        """ Calculate inverse distance weight given (x1,y1) and (x2,y2) and power value n"""
        return 1/((p1-p2)**n)

    # Private method! Can't be seen by the user
    def _idw(self, p: Point, n: float=2):
        """ Inverse Distance weighted interpolation to point (px, py)
        :param p: Interpolation point
        :param n: Power value (usually 2)
        :return: interpolated value at point (px, py)
        """
        weights = self._calc_weight(p, self.data, n)
        values = [item.v for item in self.data]
        return np.dot(weights, values)/weights.sum()

    def calc(self, p: Point, method="IDW"):
        match method:
            case "IDW":
                ans = self._idw(p)
            case _:
                raise ValueError("That ain't right.")
        return ans

# -------------------------------------------------------------------------------------------------------------------- #
# Main
# -------------------------------------------------------------------------------------------------------------------- #

# Test point subtraction
p1 = Point(5.5, 5.5)
p2 = Point(0.0, 0.0)
print(f"Distance between points: {p1 - p2}")

# Fails:
p1 - 5.5

# -------------------------------------------------------------------------------------------------------------------- #

# Setup IDW example with new point classes
data_coords = np.meshgrid(np.arange(0, 10.0), np.arange(0, 10.0))
points = []
for x, y in zip(data_coords[0].flatten(), data_coords[1].flatten()):
    points.append(Point(x, y, value=np.sqrt(x**2.85 + y**2)))

# Setup point we're interpolating to
p = Point(x=5.5, y=5.5)

interp = Interpolate(points)
interp.calc(p=p)