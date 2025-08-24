import math
import numpy as np
import pyperclip
from global_hotkeys import *
import os
import matplotlib.pyplot as plt
import plotly.graph_objects as go

def_rad = 200
samples = 200000
maxPlotPoints = 20000
#factor for adjusting random distribution in sphere scattering
#k>3 will favour outer edge of sphere
k = 3

#def plot_shader(plotPoints):

def plot_points(plotPoints):
    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')
    for point in plotPoints[:maxPoints]:
        ax.scatter(xs = point[0], ys = point[1], zs = point[2], c='r', marker='o')
    ax.set_xlabel('X')
    ax.set_ylabel('Z')
    ax.set_zlabel('Y')
    ax.set_autoscale_on(True)
    plt.show()

def plot_scatter3d(points, max_points=200_000):
    points = np.array(points)
    n = len(points)
    
    if n > max_points:
        idx = np.random.choice(n, size=max_points, replace=False)
        points = points[idx]
    
    fig = go.Figure(data=[go.Scatter3d(
        x=points[:, 0],
        y=points[:, 2],
        z=points[:, 1],
        mode='markers',
        marker=dict(size=2, opacity=0.5)
    )])
    
    fig.update_layout(
        scene=dict(
            xaxis_title='X',
            yaxis_title='Z',
            zaxis_title='Y'
        ),
        title=f"3D Scatter ({len(points):,} points shown)"
    )
    fig.show()

def plot_volume(points, bins=50):
    points = np.array(points)
    H, edges = np.histogramdd(points, bins=bins)
    
    # Build voxel grid
    x_centers = (edges[0][:-1] + edges[0][1:]) / 2
    y_centers = (edges[1][:-1] + edges[1][1:]) / 2
    z_centers = (edges[2][:-1] + edges[2][1:]) / 2
    
    X, Y, Z = np.meshgrid(x_centers, y_centers, z_centers, indexing="ij")
    
    fig = go.Figure(data=go.Volume(
        x=X.flatten(),
        y=Y.flatten(),
        z=Z.flatten(),
        value=H.flatten(),
        isomin=1,          # min cutoff (ignore empty voxels)
        isomax=H.max(),    # max density
        opacity=0.1,       # transparency
        surface_count=15   # number of isosurfaces
    ))
    
    fig.update_layout(
        scene=dict(
            xaxis_title='X',
            yaxis_title='Y',
            zaxis_title='Z'
        ),
        title=f"3D Volume Rendering (bins={bins})"
    )
    fig.show()

def sphere_intersection(spheres):
    scatterSamples = None
    #calculate vector between center of spheres
    #consider reworking this to only check new pairs against old best when sphere added
    bestOverlap = []
    spherePairs = [(s1, s2) for s1 in spheres for s2 in spheres if s1 != s2]
    for spherePair in spherePairs:
        overlap = spherePair[0][3] + spherePair[1][3] - vector_magnitude(vector(spherePair[0], spherePair[1]))
        try:
            if bestOverlap[1] > overlap:
                bestOverlap = [spherePair, overlap]
        except:
            bestOverlap = [spherePair, overlap]
    
    v_u = vector(bestOverlap[0][0], bestOverlap[0][1])
    distance = vector_magnitude(v_u)
    v_u = [x / distance for x in v_u]
    distCenter = (distance**2 + bestOverlap[0][0][3]**2 - (bestOverlap[0][1][3]**2)) / (2*distance)
    vCenter = [x * distCenter for x in v_u]
    centerPoint = [bestOverlap[0][0][0] + vCenter[0], bestOverlap[0][0][1] + vCenter[1], bestOverlap[0][0][2] + vCenter[2]]

    intersectionRadius = math.sqrt(bestOverlap[0][0][3]**2 - distCenter**2)

    if len(spheres) > 2:
        
        scatterSamples = sphere_scatter(centerPoint, bestOverlap[1], intersectionRadius, v_u, samples)
        scatterSamples = valid_points(spheres, scatterSamples)
        if len(scatterSamples) > 0:
            scatterCenter = scatter_center(scatterSamples)
            scatterBounding = find_scatter_bounds(scatterSamples, scatterCenter)
            print("Center of scatter: ", scatterCenter)
            print(scatterBounding)
        else:
            print("center of intersection: ", [round(i) for i in centerPoint])
            print("intersection radius: ", round(intersectionRadius))
            print("intersection overlap: ", round(bestOverlap[1]))
            roundedVector = [f"{num:.2f}" for num in v_u]
            print("direction vector: ", roundedVector)
    else:
        print("center of intersection: ", [round(i) for i in centerPoint])
        print("intersection radius: ", round(intersectionRadius))
        print("intersection overlap: ", round(bestOverlap[1]))
        roundedVector = [f"{num:.2f}" for num in v_u]
        print("direction vector: ", roundedVector)
    return [[centerPoint, bestOverlap[1], intersectionRadius, v_u], scatterSamples]
    
def valid_points(spheres, scatterSamples):
    validPoints = []
    for point in scatterSamples:
        valid = True
        for sphere in spheres:
            if vector_magnitude(vector(sphere, point)) > sphere[3]:
                valid = False
        if valid:
            validPoints.append(point)
    return validPoints

def update_list(spheres, newSphere, removedSpheres):
    updatedList = []
    addNewSphere = True
    for sphere in spheres:
        if vector_magnitude(vector(sphere, newSphere)) + newSphere[3] <= sphere[3]:
            if sphere[3] <= newSphere[3]:
                updatedList.append(sphere)
                addNewSphere = False
        else:
            updatedList.append(sphere)
    if addNewSphere == True:
        updatedList.append(newSphere)
    else:
        removedSpheres.append(newSphere)

    return [updatedList, removedSpheres]

def scatter_center(scatterSamples):
    xavg = 0
    yavg = 0
    zavg = 0

    for point in scatterSamples:
        xavg += point[0]
        yavg += point[1]
        zavg += point[2]
    xavg = xavg/len(scatterSamples)
    yavg = yavg/len(scatterSamples)
    zavg = zavg/len(scatterSamples)
    return [int(xavg), int(yavg), int(zavg)]

def vector_magnitude(v):
    mag = math.sqrt(v[0]**2 + v[1]**2 + v[2]**2)
    return mag

def vector(sphereOne, sphereTwo):
    v = [sphereTwo[0] - sphereOne[0], sphereTwo[1] - sphereOne[1], sphereTwo[2] - sphereOne[2]]
    return v

def sphere_scatter(center, radius, samples):
    v = np.random.normal(0, 1, (samples, 3))
    v /= np.linalg.norm(v, axis = 1)[:, np.newaxis]
    rad = np.random.rand(samples) ** (1/k) * radius
    points = v * rad[:, np.newaxis]
    points = points + center
    return points

def find_scatter_bounds(scatterPoints, center):
    scatterPoints = (np.array(scatterPoints) - np.array(center))
    xbounds = np.array([0, 0])
    ybounds = np.array([0, 0])
    zbounds = np.array([0, 0])
    for point in scatterPoints:
        if point[0] > xbounds[1]:
            xbounds[1] = point[0]
        if point[0] < xbounds[0]:
            xbounds[0] = point[0]

        if point[1] > ybounds[1]:
            ybounds[1] = point[1]
        if point[1] < ybounds[0]:
            ybounds[0] = point[1]

        if point[2] > zbounds[1]:
            zbounds[1] = point[2]
        if point[2] < zbounds[0]:
            zbounds[0] = point[2]
    #return {"x":xbounds.astype(int).tolist(), "y": ybounds.astype(int).tolist(), "z": zbounds.astype(int).tolist()}
    return {"x": (xbounds + center[0]).astype(int).tolist(), "y": (ybounds + center[1]).astype(int).tolist(), "z": (zbounds + center[2]).astype(int).tolist()}

def cyl_scatter(center, d1, radius, vector, samples):
    
    #d1 is the distance along vector v
    vector = np.array(vector)
    #let v be one coordinate axis and generate random points along this axis between -.5d1 and .5d1
    v1 = [scale*vector for scale in np.random.uniform(-.5*d1, .5*d1, samples)]

    #determine vector2 orthogonal to vector
    if np.allclose(vector, [0,0,1]):
        not_parallel = np.array([1,0,0])
    else:
        not_parallel = np.array([0,0,1])
    vector2 = np.cross(vector, not_parallel)
    vector2 = [i / np.linalg.norm(vector2) for i in vector2]

    #determine vector3 orthogonal to both vector and vector1
    #these 3 vectors form the basis of a new coordinate system

    vector3 = np.cross(vector, vector2)

    theta = np.random.uniform(0, 2 * np.pi, samples)
    r = radius * np.sqrt(np.random.uniform(0, 1, samples))
    v2 = (r * np.cos(theta))
    v2 = [np.multiply(a, vector2) for a in  v2]

    v3 = (r * np.sin(theta))
    v3 = [np.multiply(b, vector3) for b in  v3]

    circPoints = [v1[i] + v2[i] + v3[i] + center for i in range(len(v1))]
    return circPoints


while True:
    os.system('cls')
    sphereList = []
    removedSpheres = []
    scatterSamples = None

    while True:
        print("enter a point from clip board or enter 'reset' to reset")
        userInput = input()
        if userInput == "r":
            break
        elif userInput == "p":
            if scatterSamples is not None:
                plot_scatter3d(scatterSamples, maxPlotPoints)
            else:
                scatterSamples = cyl_scatter(result[0], result[1], result[2], result[3], samples)
                scatterSamples = valid_points(sphereList, scatterSamples)
                if len(scatterSamples) > 0:
                    plot_scatter3d(scatterSamples, maxPlotPoints)
        elif userInput == "u":
            try:
                removedSpheres.append(sphereList.pop())
            except:
                print("no sphere to remove")
        else:
            try:
                rad = int(userInput)
            except:
                rad = def_rad

            ############
                
            os.system('cls')
            inputBuff = pyperclip.paste().split()[6:9:1]
            newSphere = [float(item) for item in inputBuff]
            newSphere.append(rad)

            [sphereList, removedSpheres] = update_list(sphereList, newSphere, removedSpheres)
            
            if len(removedSpheres) >= 1:
                print("inactive spheres")
                for sphere in removedSpheres:
                    print(sphere)
                print("\n")

            print("active spheres:")
            for sphere in sphereList:
                print(sphere)
            print("\n")
            if len(sphereList) >=2:
                [result, scatterSamples] = sphere_intersection(sphereList)


        
        



