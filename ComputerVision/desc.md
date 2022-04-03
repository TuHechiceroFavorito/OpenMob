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
Run the following:
```
sudo apt-get install libatlas-base-dev
```

# Path detection


## References
- https://cocodataset.org/#home
- https://www.youtube.com/watch?v=HXDD7-EnGBY
