# SDD-Utils
A couple of utilities that can be used with Stanford Drone Dataset.

## Create Pascal VOC style annotations
This utility will cut the videos into frames and then create Pascal VOC style annotations for each frame. 

This will come handy when we want to test existing Object Detection algorithms on Stanford Drone Dataset. This will enable us to train a network with minimal code change as most of the Object Detection algorithms do ship code to train on Pascal VOC. 