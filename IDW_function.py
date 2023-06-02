"""
Example of Inverse Distance Weighting (IDW) broken into a series of functions
"""
import matplotlib
matplotlib.use('TkAgg')
import numpy as np
from matplotlib import pyplot as plt

# -------------------------------------------------------------------------------------------------------------------- #
# Functions
# -------------------------------------------------------------------------------------------------------------------- #

def dist(x1, x2, y1, y2):
    """ Calculate distance between points (x1,y1) and (x2,y2)"""
    return ((x1-x2)**2 + (y1-y2)**2)**0.5

def calc_weight(x1, x2, y1, y2, power):
    """ Calculate inverse distance weight given (x1,y1) and (x2,y2) and power value power"""
    return 1/(dist(x1, x2, y1, y2)**power)

def idw(px: float, py: float, vxs: list, vys: list, values: list, power: float=2):
    """ Inverse Distance weighted interpolation to point (px, py)
    :param px: Interpolation point x value
    :param py: Interpolation point y value
    :param vxs: Data x values
    :param vys: Data y values
    :param values: Data values at points (vxs, vys)
    :param power: Power value (usually 2)
    :return: interpolated value at point (px, py)
    """
    weights = calc_weight(px, vxs, py, vys, power)
    return np.dot(weights, values)/weights.sum()

# -------------------------------------------------------------------------------------------------------------------- #
# Main
# -------------------------------------------------------------------------------------------------------------------- #

# Setup points to interpolate to
px = 5.5
py = 5.5

# Setup data points
data_xs, data_ys = np.meshgrid(np.arange(0, 10.0), np.arange(0, 10.0))
values = np.sqrt(data_xs**2.85 + data_ys**2)

# Plot
h = plt.contourf(np.arange(0, 10.0), np.arange(0, 10.0), values)
plt.axis('scaled')
plt.colorbar()
plt.plot(px, py, 'ro')

idw(px=px, py=py, vxs=data_xs.flatten(), vys=data_ys.flatten(), values=values.flatten())
