# SDD-Utils
A couple of utilities that can be used with Stanford Drone Dataset.

## 1. Create Pascal VOC style annotations
This utility helps to convert the videos and annotations in Stanford Drone Dataset into Pascal VOC style images and annotations. 

The utility basically does three tasks in the following sequence:
* Split the video into frames
* Create Pascal VOC style annotation for each of the frame in the video
* Create train-validation-test split for the frames

This will come handy when we want to test existing Object Detection algorithms on Stanford Drone Dataset. This will enable us to train a network with minimal code change as most of the Object Detection algorithms do ship code to train on Pascal VOC. 

### Prerequisites
* ffmpeg library
* python 2.7

### Usage
`
python annotate.py 
`

### Declarative definition
The videos to be processed and the train-validation-test split can be defined declaratively in the script. 

The `videos_to_be_processed` dictionary decides which videos should be processed and what would be its contribution towards train-validation-test set.

Key points:
* Keys in this dictionary should match the 'scenes' in Stanford Drone Dataset. Value for each key is also a dictionary.
* The number of items in the dictionary, can atmost be the number of videos each 'scene'
* Each item in the dictionary is of the form {video_number:fraction_of_images_to_be_split_into_train_val_test_set}

Example
```Python
    videos_to_be_processed = {'bookstore': {0: (.5, .2, .3), 1: (.2, .1, .1)},
                              'coupa': {0: (.5, .2, .3)}}
```
Here, the first two videos from bookstore scene from Stanford Drone Dataset will be used, with a train-validation-test split of `(.5, .2, .3)` and `(.2, .1, .1)` respectively.
