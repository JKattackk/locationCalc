import math
import numpy as np
import pyperclip
from global_hotkeys import *
import os
import matplotlib.pyplot as plt
samples = 1000

def vectorMagnitude(v):
    mag = math.sqrt(v[0]**2 + v[1]**2 + v[2]**2)
    return mag

def vector(sphereOne, sphereTwo):
    v = [sphereTwo[0] - sphereOne[0], sphereTwo[1] - sphereOne[1], sphereTwo[2] - sphereOne[2]]
    return v



def valid_points(spheres, samples):
    validPoints = []
    for point in samples:
        for sphere in spheres:
            if vectorMagnitude(vector(sphere, point)) <= sphere[3]:
                validPoints.append(point)
    return validPoints


def sphere_intersection(spheres):
    #calculate vector between center of spheres
    #consider reworking this to only check new pairs against old best when sphere added
    bestOverlap = []
    spherePairs = [(s1, s2) for s1 in spheres for s2 in spheres if s1 != s2]
    for spherePair in spherePairs:
        overlap = spherePair[0][3] + spherePair[1][3] - vectorMagnitude(vector(spherePair[0], spherePair[1]))
        print(overlap)
        print(bestOverlap)
        print("\n")
        try:
            if bestOverlap[1] > overlap:
                bestOverlap = [spherePair, overlap]
        except:
            bestOverlap = [spherePair, overlap]
    
    v_u = vector(bestOverlap[0][0], bestOverlap[0][1])
    distance = vectorMagnitude(v_u)
    v_u = [x / distance for x in v_u]
    distCenter = (distance**2 + bestOverlap[0][0][3]**2 - (bestOverlap[0][1][3]**2)) / (2*distance)
    vCenter = [x * distCenter for x in v_u]
    centerPoint = [bestOverlap[0][0][0] + vCenter[0], bestOverlap[0][0][1] + vCenter[0], bestOverlap[0][0][2] + vCenter[0]]

    intersectionRadius = math.sqrt(bestOverlap[0][0][3]**2 - distCenter**2)
    if len(spheres) > 2:
        samples = sphere_scatter(centerPoint, intersectionRadius, samples)
        samples = valid_points(spheres, samples)



    ##calculate distance to center of two spheres



sphereList = [[0, 0, 0, 30], [5, 5, 5, 30], [20, 20, 20, 15], [40, 40, 40, 50], [40, 40, 40, 45]]
print(sphere_intersection(sphereList))
