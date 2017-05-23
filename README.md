# SDD-Utils
A couple of utilities that can be used with Stanford Drone Dataset.

## 1. Create Pascal VOC style annotations
This utility helps to convert the videos and annotations in Stanford Drone Dataset into Pascal VOC style images and annotations. 

The utility basically does three tasks in the following sequence:
* Split the video into frames
* Create Pascal VOC style annotation for each of the frame in the video
* Create train-validation-test split for the frames

This will come handy when we want to test existing Object Detection algorithms on Stanford Drone Dataset. This will enable us to train a network with minimal code change as most of the Object Detection algorithms do ship code to train on Pascal VOC. 
