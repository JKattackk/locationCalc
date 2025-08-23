# locationCalc
 Calculating location of object using points along outer radius of known detection range

Problem:
A tool makes a noise to alert you when you are within x units of an object.
Using two or more points along the outer radius of this detection range calculate the most likely position(s) of the object in 3D space.



___________________________________________________________________________________________________________________________________________________________________________________

Approach (1):
- Using two points on a flat plain calculate the overlap of two circles of radius (x) centered on each point.
- Calculate the center of mass of the overlap to determine the most likely location of the item on the 2d plane.
- use the locations of the two points to estimate the radius of the detection circle on the flat plane
- use the radius of the circle on the flat plane to estimate the location of the circle on the vertical axis
(The larger the difference between radius of the circle on the flat plane and the radius x, the further below or above the plane is relative to the object.)
___________________________________________________________________________________________________________________________________________________________________________________

Approach (2):
- Approximate pair of spheres with smallest overlap by determining pair of spheres with smallest overlap along vector from one center to the other
- Calculate center of overlap along vector from one center to the other center
- Calculate radius of circle where spheres intersect plane normal to vector
- Calculate radius of circle parallel / intersecting vector

- Use cube(?) bounding both circles to generate random scatter points
- Eliminate points which do not overlap with all spheres
- Calculate / approximate center of volume represented by valid points

display?
- For first two spheres
    - radius of each circle
    - formula for plane of each circle?
        -  could help to quickly tell user which direction needs to be narrowed down
    - seperate engine for plotting maybe? (on request)
        - drawing two circles instead of scattering

- Sebsequent spheres
    - center of scattered points
    - 
    - scatter plot of points contained in spheres (on request)

___________________________________________________________________________________________________________________________________________________________________________________