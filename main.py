import math
import numpy as np
import pyperclip
from global_hotkeys import *
import os
import plotly.graph_objects as go

def_rad = 200
samples = 200000
maxPlotPoints = 10000

#factor for adjusting random distribution in sphere scattering
#k>3 will favour outer edge of sphere
k = 3


### PLOTTING ###
""" def plot_points(plotPoints):
    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')
    for point in plotPoints[:maxPoints]:
        ax.scatter(xs = point[0], ys = point[1], zs = point[2], c='r', marker='o')
    ax.set_xlabel('X')
    ax.set_ylabel('Z')
    ax.set_zlabel('Y')
    ax.set_autoscale_on(True)
    plt.show() """

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
    fig.update_scenes(aspectmode="data")
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

### 3D TOOLS ###
def vector(pointOne, pointTwo):
    """Calculates and returns the vector from pointOne to pointTwo"""
    v = [pointTwo[0] - pointOne[0], pointTwo[1] - pointOne[1], pointTwo[2] - pointOne[2]]
    return v

def vector_magnitude(v):
    """Calculates and returns the magnitude of a vector v"""
    mag = math.sqrt(v[0]**2 + v[1]**2 + v[2]**2)
    return mag

### SCATTERING TOOLS ###
def sphere_scatter(center, r1, samples):
    """generates and returns a uniform scatter with radius r1 about point center
    returns list of points [[x, y, z], [x, y, z],  ... ]"""
    v = np.random.normal(0, 1, (samples, 3))
    v /= np.linalg.norm(v, axis = 1)[:, np.newaxis]
    rad = np.random.rand(samples) ** (1/k) * r1
    points = v * rad[:, np.newaxis]
    points = points + center
    return points

def cyl_scatter(center, d1, radius, vector, samples):
    """generates and returns a random cylindrical distribution

    center = [x, y, z]      defines the center point of the cylinder
    d1 defines the height of the cylinder
    radius defines the radius of the cylinder
    vector = [x, y, z]      defines the unit vector along which the height of the cylinder is parallel (each circle of the cylinder would lie on a plane normal to this vector)
    
    returns a list of points [[x, y, z], [x, y, z],  ... ]"""
    #d1 is the distance along vector v
    vector = np.array(vector)
    #let vector be one coordinate axis and generate random points along this axis between -.5d1 and .5d1
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

def scatter_center(scatterSamples):
    """determines the average coordinates of a set of 3D points
    scatterSamples = [[x, y, z], [x, y, z],  ... ]
    returns [xavg, yavg, zavg] as integers"""
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

def find_scatter_bounds(scatterPoints, center):
    """Finds the max and min (x, y, z) for the scatter
    returns {"x": [xmin, xmax], "y": [ymin, ymax], "z": [zmin, zmax]}"""
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

### OTHER ###
def sphere_intersection(spheres):#needs doc
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
        scatterSamples = cyl_scatter(centerPoint, bestOverlap[1], intersectionRadius, v_u, samples)
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
    
def valid_points(spheres, scatterSamples):#needs doc
    """Checks a list of 3D points against a list of spheres.
    Points are considered valid when contained within all spheres in sphere list and not contained within the inner radius of any spheres within the list.

    scatterSamples = [[x, y, z], [x, y, z],  ... ]
    spheres = [[x, y, z, r1, r2], [x, y, z, r1, r2],  ... ]
    where r1 is outer radius of the sphere and r2 is the inner radius of the sphere

    setting r2 to zero creates a non-hollow sphere
    r2>r1 creates a 'void sphere' where contained points are invalid
    
    returns validPoints = [[x, y, z], [x, y, z],  ... ]"""
    validPoints = []
    for point in scatterSamples:
        valid = True
        for sphere in spheres:
            if vector_magnitude(vector(sphere, point)) > sphere[3] or vector_magnitude(vector(sphere, point)) < sphere[4] :
                valid = False
        if valid:
            validPoints.append(point)
    return validPoints

def update_list(spheres, newSphere, removedSpheres):#needs doc
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

def get_numbers(inputString):
    inputNumbers = []
    inputString = inputString.split(" ")
    for string in inputString:
        try:
            inputNumbers.append(float(string))
        except:
            print(string, " not a valid number, ignoring")
    return inputNumbers

def make_sphere(inputNumbers):
    ## attempting to make new sphere
    newSphere = []
    if len(inputNumbers) == 0:
        #uses default radius and gets coordinates from clipboard
        [rad1, rad2] = [def_rad, 0]
        pastedNumbers = get_numbers(pyperclip.paste())
        if len(pastedNumbers) < 3:
            print("no valid coordinates in clipboard")
        else:
            newSphere = pastedNumbers[0:2]
            newSphere.extend([rad1, rad2])
    elif len(inputNumbers) == 1:
        #uses input as outer radius, gets coordinates from clipboard
        [rad1, rad2] = [inputNumbers[0], 0]
        pastedNumbers = get_numbers(pyperclip.paste())
        if len(pastedNumbers) < 3:
            print("no valid coordinates in clipboard")
        else:
            newSphere = pastedNumbers[0:2]
            newSphere.extend([rad1, rad2])
    elif len(inputNumbers) == 2:
        #uses inputs as inner and outer radius, gets coordinates from clipboard
        [rad1, rad2] = [inputNumbers[0], inputNumbers[1]]
        pastedNumbers = get_numbers(pyperclip.paste())
        if len(pastedNumbers) < 3:
            print("no valid coordinates in clipboard")
        else:
            newSphere = pastedNumbers[0:2]
            newSphere.extend([rad1, rad2])
    elif len(inputNumbers) == 3:
        #uses inputs as coordinates, uses default radius
        [rad1, rad2] = [def_rad, 0]
        newSphere = inputNumbers[0:2]
        newSphere = newSphere.extend[rad1, rad2]
    elif len(inputNumbers) > 3:
        #uses inputs as coordinates and radius. if only four numbers entered assumes inner radius of zero.
        newSphere = inputNumbers
        if len(newSphere) < 5:
            newSphere.append(0)
    return newSphere

while True:
    os.system('cls')
    sphereList = []
    voidSpheres = []
    removedSpheres = []
    scatterSamples = None

    while True:
        print("waiting for input: ")
        userInput = input()
        if userInput == "r":
            break
        elif userInput == "p":
            if scatterSamples is not None:
                plot_scatter3d(scatterSamples, maxPlotPoints)
            else:
                if len(sphereList) > 1:
                    scatterSamples = cyl_scatter(result[0], result[1], result[2], result[3], samples)
                elif len(sphereList) == 1:
                    scatterSamples = sphere_scatter(sphereList[0][0:3], sphereList[0][3], samples)
                scatterSamples = valid_points(sphereList, scatterSamples)
                if len(scatterSamples) > 0:
                    plot_scatter3d(scatterSamples, maxPlotPoints)
        elif userInput == "u":
            try:
                removedSpheres.append(sphereList.pop())
            except:
                print("no sphere to remove")
                ############################
        else:
            inputNumbers = get_numbers(userInput)
            if len(inputNumbers) > 5:
                print("invalid input")
            else:
                newSphere = make_sphere(inputNumbers)
                if newSphere != None:
                    os.system('cls')
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


            



        



