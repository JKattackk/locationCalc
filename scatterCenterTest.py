import math
import numpy as np
import pyperclip
from global_hotkeys import *
import os
import matplotlib.pyplot as plt
samples = 1000
k = 5 
#factor for adjusting random distribution in sphere scattering
#k>3 will favour outer edge of sphere

def plot_points(plotPoints):
    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')
    for point in plotPoints:
        ax.scatter(xs = point[0], ys = point[1], zs = point[2], c='r', marker='o')
    ax.set_xlabel('X')
    ax.set_ylabel('Z')
    ax.set_zlabel('Y')
    ax.set_autoscale_on(True)
    plt.show()

def valid_points(spheres, samples):
    validPoints = []
    for point in samples:
        for sphere in spheres:
            if vectorMagnitude(vector(sphere, point)) <= sphere[3]:
                validPoints.append(point)
    return validPoints

def scatter_center(samples):
    xavg = 0
    yavg = 0
    zavg = 0

    for point in samples:
        xavg += point[0]
        yavg += point[1]
        zavg += point[2]
    xavg = xavg/len(samples)
    yavg = yavg/len(samples)
    zavg = zavg/len(samples)
    return [xavg, yavg, zavg]

def sphere_scatter(center, radius, samples):
    v = np.random.normal(0, 1, (samples, 3))
    v /= np.linalg.norm(v, axis = 1)[:, np.newaxis]
    rad = np.random.rand(samples) ** (1/3) * radius
    points = v * rad[:, np.newaxis]
    points = points + center
    return points


points = sphere_scatter([10, 10, 10], 12, 200)
print(points)
print(scatter_center(points))