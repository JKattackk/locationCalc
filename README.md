# locationCalc
Tool for determining the potential locations based on a set of spheres in 3D-space.
Takes a set of spheres, hollow spheres, or empty spheres (exclusionary zones) and determines valid locations based upon the set.
Valid locations are considered to be locations where the filled parts of all spheres overlap, and the empty portions (empty spheres or the inside of  hollow spheres) do not overlap.

Equivalent statement examples if using the tool to locate an item:
Filled spheres - "The item is within (radius) units of the sphere center"
Hollow spheres - "The item is within (outer radius) units of the center, but not within (inner radius) units of the sphere center
Empty/void spheres - "The item is not within (inner radius) units of the sphere center)

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

Inner radius can be used to creat hollow spheres (object within outer radius but not within inner radius) or to create 'void spheres'  for inner radius >= outer radius (object not within inner radius).  I reccommend creating at least one thin hollow sphere (using the edge of a detection range) or one small overlap (two spheres which barely overlap) to limit the volume in which points are scattered.
