"""
Example of Inverse Distance Weighting (IDW) in a procedural code
"""
import numpy as np

# Setup points to interpolate to
px = 5.5
py = 5.5

# Setup data points
data_xs, data_ys = np.meshgrid(np.arange(0, 10.0), np.arange(0, 10.0))
values = np.sqrt(data_xs**2.85 + data_ys**2).flatten()

# Initialize sums
total_weight = 0
weighted_sum = 0

for i, (x, y) in enumerate(zip(data_xs.flatten(), data_ys.flatten())):

    # Get distance between points
    distance = np.sqrt((x - px) ** 2 + (y - py) ** 2)

    # Calc weights based on distance
    if distance == 0:
        inverse_distance = 1.0  # Avoid division by zero
    else:
        inverse_distance = 1 / distance ** 2

    # Do maths
    total_weight += inverse_distance
    weighted_sum += inverse_distance * values[i]

print(f"Weighted value is: {weighted_sum/total_weight}")