import math
import numpy as np
import pyperclip
from global_hotkeys import *
import os
rad = 150

def overlap_center(x1, y1, x2, y2, r=150):
    # Distance between centers
    dx = x2 - x1
    dy = y2 - y1
    d = math.hypot(dx, dy)

    # Check for no overlap or identical centers
    if d >= 2 * r or d == 0:
        return None  # No overlap or circles are coincident

    # Distance from center A to line joining intersection points
    a = (r**2 - r**2 + d**2) / (2 * d)
    h = math.sqrt(r**2 - a**2)

    # Midpoint between A and B
    xm = x1 + a * dx / d
    ym = y1 + a * dy / d

    # Intersection points (not needed unless you want them)
    rx = -dy * (h / d)
    ry = dx * (h / d)

    xi1 = xm + rx
    yi1 = ym + ry
    xi2 = xm - rx
    yi2 = ym - ry

    # Midpoint of the chord = better approximation of overlap center
    center_x = (xi1 + xi2) / 2
    center_y = (yi1 + yi2) / 2

    return (center_x, center_y)
    """
    Args:
        x1, z1: Coordinates of the first circle's center
        x2, z2: Coordinates of the second circle's center
        rad: Radius of both circles (default: 150)
    Returns:
        (x, z) coordinates of the overlap center, or None if no overlap
    """
    # Calculate distance between centers
    distance = math.sqrt((x2 - x1)**2 + (z2 - z1)**2)
    
    # Check if circles overlap
    if distance >= 2 * radius:
        return None  # No overlap
    
    # Check if one circle is completely inside the other
    if distance == 0:
        return (x1, z1)  # Same center
    
    # Calculate the overlap center (midpoint of the intersection chord)
    # This is the point along the line connecting the centers
    ratio = distance / (2 * radius)
    
    # Parameter along the line from center1 to center2 (0 to 1)
    t = 0.5 * (1 + ratio)
    
    # Calculate the overlap center coordinates
    overlap_x = x1 + t * (x2 - x1)
    overlap_z = z1 + t * (z2 - z1)
    
    return (overlap_x, overlap_z)
def circle_radius(center, point1, point2, r):
    d1 = math.sqrt(((point1[0] - center[0]) ** 2) + ((point1[2] - center[1]) ** 2))
    return d1
def elevation_range(rad, r_circle):
    return math.sqrt((rad ** 2) - (r_circle ** 2))

while True:
    os.system('cls')

    print("waiting for first point:")
    input()
    inputBuff = pyperclip.paste().split()[6:9:1]
    print(inputBuff)
    point1 = [float(item) for item in inputBuff] 

    print("waiting for second point:\n")
    input()
    inputBuff = pyperclip.paste().split()[6:9:1]
    print(inputBuff)
    point2 = [float(item) for item in inputBuff]

    centerPoint = overlap_center(point1[0], point1[2], point2[0], point2[2], rad)
    print(centerPoint)

    circleRad = circle_radius(centerPoint, point1, point2, rad)
    elevation = elevation_range(rad, circleRad)

    print("elevation: ", elevation)
    print("enter to reset")
    input()

