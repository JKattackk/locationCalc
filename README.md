# locationCalc
 Calculating potential locations of an object based on overlap of spheres.

___________________________________________________________________________________________________________________________________________________________________________________

Using the tool:

 - entering 'r' resets the search
 - entering 'p' attempts to plot the potential points

 
Entering anything else attempts to create a sphere from inputs.

**one number entered:**
Number is outer radius of sphere.  
Attempts to grab sphere coordinates from clipboard.

**two numbers entered:**
First number is out radius.  Second number is inner radius. 
Attempts to grab sphere coordinates from clipboard.

**three numbers entered:**
Entered numbers are center coordinate.  Uses default outer radius and inner radius of zero.

**four numbers entered:**
First three numbers are center coordinate.  Fourth number is outer radius.  Inner radius is zero

**five numbers entered:**
First three numbers are center coordinate.  Fourth number is outer radius.  Fifth number is inner radius.

Inner radius can be used to creat hollow spheres (object within outer radius but not within inner radius) or to create 'void spheres'  for inner radius >= outer radius (object not within inner radius).
I reccommend creating at least one thin hollow sphere (using the edge of a detection range) or one small overlap (two spheres which barely overlap) to limit the volume in which points are scattered.


brainstorm / notes stuff (not neccessarily kept up to date) vvv
___________________________________________________________________________________________________________________________________________________________________________________

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

___________________________________________________________________________________________________________________________________________________________________________________

INNER RADIUS

New types of spheres
 - hollow sphere with inner radius r1 and outer radius r2
    - r2 < r1
 - spherical "void" zone
    - r2 >= r1

hollow sphere with hollow sphere or standard sphere should just work(?) with the standard method of calculating area given the user doesnt enter an extremely thin sphere.
extremely thin spheres may require a new approach

void spheres need to be recognized and treated differently.
if two normal spheres (standard or hollow) exist the scatter can just be generated from those and void spheres can be removed from the area during point testing
if a single normal or hollow sphere exists we will generate the points using sphere_scatter (add support for inner/outer radius for use with hollow spheres?) and void spheres can be removed from that.

When should a sphere be considered redundant?
case 1: sphere contained within another sphere
sphere with smaller radius should be saved, larger sphere can be discarded.
case 2: void sphere contained within void sphere
sphere with smaller radius should be discarded.

hollow sphere intersections not yet decided

New issues:
 - a sphere and a "sherical void" do not overlap, making the standard method of generating scatter not work
