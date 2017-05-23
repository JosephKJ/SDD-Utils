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
```Python
python annotate.py 
```
The script assumes that the Stanford Drone Datased is unzipped in the cwd of the script inside a folder named `StanfordDroneDataset`. A soft link will also work. The name of the folder is configurable in the script. 


### Declarative definition
The videos to be processed and the train-validation-test split can be defined declaratively in the script. 

The `videos_to_be_processed` dictionary decides which videos should be processed and what would be its contribution towards train-validation-test set.

Key points:
* Keys in this dictionary should match the 'scenes' in Stanford Drone Dataset. 
* Value for each key is also a dictionary. The number of items in this dictionary(child), can atmost be the number of videos each 'scene'.
* Each item in this dictionary(child) is of the form {video_number:fraction_of_images_to_be_split_into_train_val_test_set}

Example:
```Python
videos_to_be_processed = {'bookstore': {0: (.5, .2, .3), 1: (.2, .1, .1)},
                              'coupa': {0: (.5, .2, .3)}}
```
Here, the first two videos from bookstore scene from Stanford Drone Dataset will be split into frames, with a train-validation-test split of `(.5, .2, .3)` and `(.2, .1, .1)` respectively. Then the first video from coupa scene will be processed similarly.


### Output
The Pascal VOC style annotations will be created in the location specified at `destination_folder_name` variable in the script. By default, it creates a folder named `sdd` inside the dataset folder. 

Output Folder Structure:
```Shell
cs17mtech01001@ubuntu:/media/sdj/Open_Datasets/StanfordDroneDataset/sdd$ ls
Annotations  ImageSets  JPEGImages  pickle_store
```


### FAQ

1. What will happen when I run the script multiple time? 

   Ans: If the videos specified in `videos_to_be_processed` dictionary is already made into frames, then those videos will not  be again split. The train-validation-test set will be resampled for each run. 


2. Suppose I need to have training and validation data from the first two videos of 'bookstore' scene and testing from the third video of 'deathCircle' scene, how would `videos_to_be_processed` dictionary look like?
   
```Python
videos_to_be_processed = {'bookstore': {0: (.5, .5, 0), 1: (.5, .5, 0)},
                        'deathCircle': {2: (0, 0, 1)}}
```
3. How many scenes are there in Stanford Drone Dataset? How many videos are there in each?

```Shell
SDD contains the following 'scenes' and corresponding videos:
    'bookstore'   scene contains videos: (0, 1, 2, 3, 4, 5, 6)
    'coupa'       scene contains videos: (0, 1, 2, 3)
    'deathCircle' scene contains videos: (0, 1, 2, 3, 4)
    'gates'       scene contains videos: (0, 1, 2, 3, 4, 5, 6, 7, 8)
    'hyang'       scene contains videos: (0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14)
    'little'      scene contains videos: (0, 1, 2, 3)
    'nexus'       scene contains videos: (0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11)
    'quad'        scene contains videos: (0, 1, 2, 3)
```
### Citation
A. Robicquet, A. Sadeghian, A. Alahi, S. Savarese, Learning Social Etiquette: Human Trajectory Prediction In Crowded Scenes in European Conference on Computer Vision (ECCV), 2016.
Dataset available [here](http://cvgl.stanford.edu/projects/uav_data/).
