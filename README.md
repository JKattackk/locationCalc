# locationCalc
 Calculating location of object using overlap of detection spheres

Problem:
A tool makes a noise to alert you when you are within x units of an object.
Using two or more points along the outer radius of this detection range calculate the most likely position(s) of the object in 3D space.

Usage:
Currently somewhat integrated with Minecraft.  
Use F3+C to copy coordinates to clipboard.
press enter in console to add a sphere with the default radius
enter a radius to add a sphere with a custom radius

enter 'u' to remove the last active sphere
enter 'p' to show a plot of the area
enter 'r' to reset the search

___________________________________________________________________________________________________________________________________________________________________________________

Approach (1):
- Using two points on a flat plain calculate the overlap of two circles of radius (x) centered on each point.
- Calculate the center of mass of the overlap to determine the most likely location of the item on the 2d plane.
- use the locations of the two points to estimate the radius of the detection circle on the flat plane
- use the radius of the circle on the flat plane to estimate the location of the circle on the vertical axis
(The larger the difference between radius of the circle on the flat plane and the radius x, the further below or above the plane is relative to the object.)
___________________________________________________________________________________________________________________________________________________________________________________

Approach (2) - active:
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
       could help to quickly tell user which direction needs to be narrowed down
    - seperate engine for plotting maybe? (on request)
         drawing two circles instead of scattering

- Sebsequent spheres
    - center of scattered points
    - 
    - scatter plot of points contained in spheres (on request)

___________________________________________________________________________________________________________________________________________________________________________________

Issues / to change

~~Sometimes fails to find points within intersection area when area becomes small.~~
~~considering changing approach instead of increasing the number of samples.~~
 - ~~does this only occur when the radius of instersection and overlap distance are very different?~~
    - ~~use radius and overlap distance to create cube bounding point generation instead of generating a sphere encompassing the larger of the two~~
         ~~could greatly cut down on the total area the points have to cover and therefore increase the likelihood of generated points being within intersection~~

 - ~~generate a lower ammount of points and retry with larger ammounts if too few points are found?~~
    - ~~still pretty brute force, should be a better solution~~
fixed error with calculating center of intersection that was likely causing the failure to find points.
also implemented cylindrical scattering to fit scattered points more closely to the initial overlap used

Clean up terminal view or add GUI (I dont like making gui's)

Actually go through and comment the code

Further adjust plot and maybe find a way to open it in a dedicated window

~~add option for plotting during two spheres~~
implemented.


___________________________________________________________________________________________________________________________________________________________________________________

Possible future features:

 - enable use of inner and outer radius for detection spheres
    - enables useful tools to quickly narrow search area
        - location is not within radius (r2 >= r1)
        - location is between r1 and r2
    - can cause multiple disconnected search areas (?)
        - some way to recognize seperate areas and tell the user multiple centers / ranges instead of giving one in the center of multiple areas
        - maybe changing plot method?
    