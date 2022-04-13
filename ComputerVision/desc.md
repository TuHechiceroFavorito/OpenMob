# Computer Vision
One of the main features of OpenMob is the ability to recognise and avoid objects. _object_detection.py_ takes care of this part.
Another crutial ability is to be able to distinguish the edge of the path to follow and be able to adjust to it. _path_detection_.py takes care of this part of the job

# Object detection

## The detector
The class _Detector_ will look at the camera and start analysing the images. It will look for different objects on the image. This objects are listed in _Object_Detection_Files/coco.names_. The detector will get a box per object recognised. Then, it will use this boxes as bounderies for the free ways on the image. It will measure the width on the image of all of them an select the bigger one. If the middle point of this path is to the left of the screen, it will return _LEFT_. Otherwise, it will return _RIGHT_. If there are no objects in the way, it will return _FREE_.

## _Object_Detection_File_ folder
This folder contains the model that OpenCV uses to detect objects. It was taken from the Coco database, which according to our research, is the best option to run on a Raspberry Pi taking into account accuracy and efficiency.

## Debugging
### SystemError: <class 'cv2.dnn_DetectionModel'> returned a result with an error set
Check the path for loading the models, it might be a misspelling, so it's not really loading any model.

### ImportError: libcblas.so.3: cannot open shared object file: No such file or directory

# Path detection
## Detection algorithm
The Eagle will be navigating different pathways that won't always be delimited by a clear line. They will be certainly delimited in someway. In most cases, there will be a change in color as the ground transitions from a walkable surface to a non-walkable one. In order to detect this limits, several steps of processing are needed:

We are using OpenCV to detect the edges using changes in color in the imaged captured by the camera. Eventhough for some cases we won't have a specific edge, there will be a change in color. It's this change in color that the algorithm uses to detect edges. We can use this property to detect the 'edges' of the path.
This will give a mask composed of black and white pixels. The white ones will represents the edges detected by OpenCV. This edges can be anything from a straight line to random shapes. We're only interested in straight lines or slightly curved ones. To detect them, we pass this mask through a line detection algorithm (Hough). As a result, we get all a list of points that represnt the start and end point of this detected lines.

At this stage, we have a set of lines that are present in the image. From them, we need to get rid of lines that have nothing to do with the path, find the correct path and determine the point in space at which the Eagle should be heading to correctly follow this path.
First we order all the pair of points. We determine their slope and intercept, and separate them in left or right (positive or negative slope). This distinction is to find the lines that describe each side of the path.
Once both sets of lines are separated and parametised, we'll have a list of lines for both sides. Some of them will represent something that has nothing to do with the path. However, most of them describe the same line: the limit of the path, what we are looking for. How do we determine which one to use?
Assuming that a big proportion of these lines represent the same line of the path, we can use the median to find a good description of the slope and the intercept. This method also prevents big errors due to outliers, which is a big problem with the average.

After this step, we are left with the slope and the intercept of both the right and left limit. Now we need to find where the vehicle should be heading in order to properly follow this path.
By testing the algorithm, be found that the camera actually has the same perspective properties as the human eye. Specifically, all straight lines coming from the plane normal to the observer converge in a point called fuge point. This fuge point will always follow the path, even if there is a curve. By finding this fuge point, we can determine whether is needed to turn or not.

The fuge point is where all lines meet. So once we have the limits parametised, we can solve the system and find the point where they both meet. Once we have the coordinates in pixels of this point, we can make a decision. If the point is too far away from the center given a threshold value, the Eagle should turn to the opposite side to correct this. Otherwise, the vehicle is heading towards a good direction.

## References
- https://cocodataset.org/#home
- https://www.youtube.com/watch?v=HXDD7-EnGBY