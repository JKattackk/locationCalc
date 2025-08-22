import math
import numpy as np
import pyperclip
from global_hotkeys import *
import os
import matplotlib.pyplot as plt

def_rad = 200
plotResolution = .2 #points per meters squared
plotExtension = 5 #factor to increase radius when generating plot points

EPS = 1e-9


def _violation_and_argmax(x, spheres):
    """Return (max_violation, idx) for point x with respect to spheres.
    violation for sphere i is d(x, c_i) - r_i. Feasible if max_violation <= 0.
    """
    x = np.asarray(x, dtype=float)
    centers = np.array([s[:3] for s in spheres], dtype=float)
    radii = np.array([s[3] for s in spheres], dtype=float)
    dists = np.linalg.norm(centers - x, axis=1)
    viol = dists - radii
    k = int(np.argmax(viol))
    return float(viol[k]), k


def _aabb_intersection(spheres):
    """Axis-aligned bounding box of the intersection of all sphere AABBs.
    Returns (lo, hi) where lo/hi are 3-vectors. If empty, returns (None, None).
    """
    centers = np.array([s[:3] for s in spheres], dtype=float)
    radii = np.array([s[3] for s in spheres], dtype=float)
    lo = np.max(centers - radii[:, None], axis=0)
    hi = np.min(centers + radii[:, None], axis=0)
    if np.any(lo > hi):
        return None, None
    return lo, hi


def _random_points_in_box(lo, hi, n):
    return lo + (hi - lo) * np.random.rand(n, 3)


def _chebyshev_center(spheres, x0=None, iters=500, step0=0.25):
    """Approximate Chebyshev center of the intersection (center of the largest
    inscribed ball). Uses subgradient ascent on g(x) = min_i (r_i - ||x-c_i||).
    Returns (x, inner_radius_estimate, max_violation).
    """
    centers = np.array([s[:3] for s in spheres], dtype=float)
    if x0 is None:
        x = centers.mean(axis=0)
    else:
        x = np.array(x0, dtype=float)

    best_x = x.copy()
    best_val = -np.inf

    for t in range(1, iters + 1):
        # Identify the most "active" (tightest) sphere
        dists = np.linalg.norm(centers - x, axis=1)
        margins = np.array([s[3] for s in spheres], dtype=float) - dists
        k = int(np.argmin(margins))  # tightest constraint
        val = margins[k]
        if val > best_val:
            best_val = val
            best_x = x.copy()

        # Subgradient step to increase the tightest margin
        if dists[k] < EPS:
            # If exactly at a center, nudge randomly
            direction = np.random.randn(3)
            direction /= (np.linalg.norm(direction) + EPS)
        else:
            direction = (x - centers[k]) / dists[k]

        step = step0 / np.sqrt(t)
        x = x + step * direction

    # Final stats at best_x
    viol, _ = _violation_and_argmax(best_x, spheres)
    inner_r = -viol  # if positive, it's the radius of largest contained ball
    return best_x, inner_r, viol

def common_sphere_intersection(
    spheres,
    samples=50000,
    refine_iters=600,
    tolerance=1e-6,
    return_points=False,
    random_seed=None,
):
    """
    Approximate the common intersection region of multiple spheres.

    Parameters
    ----------
    spheres : list[(x,y,z,r)]
        Sphere centers and radii.
    samples : int
        Number of random samples for a quick feasible point search.
    refine_iters : int
        Iterations for Chebyshev-center refinement.
    tolerance : float
        Numerical tolerance on feasibility (<= 0 means strictly feasible).
    return_points : bool
        If True, also return a down-sampled set of points lying in the
        intersection (useful for visualization).
    random_seed : int or None
        RNG seed for reproducibility.

    Returns
    -------
    dict with keys:
        'feasible' : bool
        'center' : (x,y,z) of approximate Chebyshev center (if feasible)
        'inner_radius' : radius of the largest ball guaranteed inside the
            intersection (>= 0 when feasible; 0 when tangency)
        'max_violation' : positive value means infeasible by that margin
        'aabb' : (lo, hi) bounding box used for sampling (if any)
        'points' : (N,3) array of feasible sample points (if return_points)
    """
    rng = np.random.default_rng(random_seed)
    spheres = [(float(x), float(y), float(z), float(r)) for (x, y, z, r) in spheres]

    lo, hi = _aabb_intersection(spheres)
    result = {
        'feasible': False,
        'center': None,
        'inner_radius': 0.0,
        'max_violation': None,
        'aabb': (lo, hi),
    }

    if lo is None:
        result['max_violation'] = np.inf
        return result

    # Quick sampling to find a feasible point (if one exists)
    P = _random_points_in_box(lo, hi, samples) if samples > 0 else np.empty((0, 3))
    if samples > 0:
        centers = np.array([s[:3] for s in spheres], dtype=float)
        radii = np.array([s[3] for s in spheres], dtype=float)
        diffs = P[:, None, :] - centers[None, :, :]
        dists = np.linalg.norm(diffs, axis=2)
        inside = (dists <= radii[None, :] + tolerance).all(axis=1)
        feasible_points = P[inside]
    else:
        feasible_points = np.empty((0, 3))

    x0 = feasible_points.mean(axis=0) if feasible_points.size else np.mean([s[:3] for s in spheres], axis=0)

    # Refine Chebyshev center (works whether or not we found a feasible point)
    x_star, inner_r, viol = _chebyshev_center(spheres, x0=x0, iters=refine_iters)

    result.update({
        'center': tuple(map(float, x_star)),
        'inner_radius': float(max(0.0, inner_r)),
        'max_violation': float(max(0.0, viol)),
        'feasible': bool(viol <= tolerance),
    })

    if return_points:
        # Down-sample feasible points for plotting if too many
        if len(feasible_points) > 2000:
            idx = rng.choice(len(feasible_points), size=2000, replace=False)
            feasible_points = feasible_points[idx]
            result['points'] = feasible_points

    return result

def plotPoints(plotPoints, center):
    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')
    ax.scatter(xs = plotPoints['x'], ys = plotPoints['z'], zs = plotPoints['y'], c='r', marker='o')
    ax.set_xlabel('X')
    ax.set_ylabel('Z')
    ax.set_zlabel('Y')
    ax.set_autoscale_on(True)
    plt.show()

def scatterPoints(spheres, center, radius):
    spheres = [(float(x), float(y), float(z), float(r)) for (x, y, z, r) in spheres]
    
    generationRange = radius*plotExtension
    samples = (2*int(generationRange*plotResolution))**3
    testPoints = np.array([center[0] - generationRange + 2*generationRange*np.random.rand(samples), 
                  center[1] - generationRange + 2*generationRange*np.random.rand(samples), 
                  center[2] - generationRange + 2*generationRange*np.random.rand(samples)]).T
    validxVals = []
    validyVals = []
    validzVals = []
    for point in testPoints:
        valid = True
        for sphere in spheres:
            dist = math.sqrt(((point[0]-sphere[0])**2) + ((point[1]-sphere[1])**2) + ((point[2]-sphere[2])**2))
            if dist > sphere[3]:
                valid = False
                break
        if valid:
            validxVals.append(point[0])
            validyVals.append(point[1])
            validzVals.append(point[2])
    return {'x': validxVals, 'y': validyVals, 'z': validzVals}

while True:
    os.system('cls')
    points = []
    result = None
    while True:
        print("enter a point from clip board or enter 'reset' to reset")
        userInput = input()
        if userInput == "reset":
            break
        elif userInput == "plot":
            if result is not None:
                plotPoints(scatterPoints(points, center = result['center'], radius = result['inner_radius']), result['center'])
            else:
                print("Please add more points")
        else:
            try:
                rad = int(userInput)
            except:
                rad = def_rad
                
            os.system('cls')
            inputBuff = pyperclip.paste().split()[6:9:1]
            inputBuffFloat = [float(item) for item in inputBuff]
            inputBuffFloat.append(rad)
            points.append(inputBuffFloat)

            print("entered points:")
            for item in points:
                print(item)

            if len(points) > 1:
                result = common_sphere_intersection(
                    points, samples = 20000, refine_iters = 1200, return_points = False)
                print("possible locations:")
                print("center: ", result["center"], "radius: ", result['inner_radius'])

        
        



