import os
import subprocess
import numpy as np
import random
import cPickle
import cv2
import math
import xml.etree.cElementTree as ET


def assert_path(path, error_message):
    assert os.path.exists(path), error_message


def count_files(path, filename_starts_with=''):
    files = [f for f in os.listdir(path)if os.path.isfile(os.path.join(path, f))
                     and f.startswith(filename_starts_with)]
    return len(files)


def touch(fname, times=None):
    with open(fname, 'a'):
        os.utime(fname, times)


def init_directories():
    # Setup the directory structure.
    if not os.path.exists(destination_path):
        os.makedirs(os.path.join(destination_path, 'JPEGImages'))
        os.makedirs(os.path.join(destination_path, 'ImageSets', 'Main'))
        os.makedirs(os.path.join(destination_path, 'Annotations'))
        os.makedirs(os.path.join(destination_path, 'pickle_store'))

    # Flush the train-val-test split. A new split will be created each time this script is run.
    for f in os.listdir(os.path.join(destination_path, 'ImageSets', 'Main')):
        os.remove(os.path.join(destination_path, 'ImageSets', 'Main', f))

    # Creating empty files.
    touch(os.path.join(destination_path, 'ImageSets', 'Main', 'train.txt'))
    touch(os.path.join(destination_path, 'ImageSets', 'Main', 'val.txt'))
    touch(os.path.join(destination_path, 'ImageSets', 'Main', 'test.txt'))
    touch(os.path.join(destination_path, 'ImageSets', 'Main', 'trainval.txt'))


def split_video(video_file, image_name_prefix):
    return subprocess.check_output('ffmpeg -i ' + os.path.abspath(video_file) + ' '+ image_name_prefix +'%d.jpg', shell=True, cwd=os.path.join(destination_path, 'JPEGImages'))


def log(message, level='info'):
    formatters = {
        'GREEN': '\033[92m',
        'END': '\033[0m',
    }
    print ('{GREEN}<'+level+'>{END}\t' + message).format(**formatters)


def write_to_file(filename, content):
    f = open(filename, 'a')
    f.write(content+'\n')


# Based on the split ratio and the number of annotated images, directly create the split.
def simple_split(split_ratio):
    print split_ratio


def split_dataset(number_of_frames, split_ratio, file_name_prefix):
    assert sum(split_ratio) <= 1, 'Split ratio cannot be more than 1.'

    train, val, test = np.array(split_ratio) * number_of_frames

    test_images = random.sample(range(1, number_of_frames+1), int(test))
    val_images = random.sample(tuple(set(range(1, number_of_frames+1)) - set(test_images)), int(val))
    train_images = random.sample(tuple(set(range(1, number_of_frames+1)) - set(test_images) - set(val_images)), int(train))

    for index in train_images:
        write_to_file(os.path.join(destination_path, 'ImageSets', 'Main', 'train.txt'), file_name_prefix+str(index))
        write_to_file(os.path.join(destination_path, 'ImageSets', 'Main', 'trainval.txt'), file_name_prefix+str(index))

    for index in val_images:
        write_to_file(os.path.join(destination_path, 'ImageSets', 'Main', 'val.txt'), file_name_prefix+str(index))
        write_to_file(os.path.join(destination_path, 'ImageSets', 'Main', 'trainval.txt'), file_name_prefix+str(index))

    for index in test_images:
        write_to_file(os.path.join(destination_path, 'ImageSets', 'Main', 'test.txt'), file_name_prefix+str(index))


def annotate_frames(sdd_annotation_file, dest_path, filename_prefix, number_of_frames):

    # Pickle the actual SDD annotation
    pickle_file = os.path.join(destination_path, 'pickle_store', filename_prefix + 'annotation.pkl')
    if os.path.exists(pickle_file):
        with open(pickle_file, 'rb') as fid:
            sdd_annotation = cPickle.load(fid)
    else:
        sdd_annotation = np.genfromtxt(sdd_annotation_file, delimiter=' ', dtype=np.str)
        with open(pickle_file, 'wb') as fid:
            cPickle.dump(sdd_annotation, fid)

    # Create VOC style annotation.
    first_image_path = os.path.join(destination_path, 'JPEGImages', filename_prefix+'1.jpg')
    assert_path(first_image_path, 'Cannot find the images. Trying to access: ' + first_image_path)
    first_image = cv2.imread(first_image_path)
    height, width, depth = first_image.shape

    for frame_number in range(1, number_of_frames+1):
        annotation = ET.Element("annotation")
        ET.SubElement(annotation, "folder").text = destination_folder_name
        source = ET.SubElement(annotation, "source")
        ET.SubElement(source, "database").text = 'Stanford Drone Dataset'
        size = ET.SubElement(annotation, "size")
        ET.SubElement(size, "width").text = str(width)
        ET.SubElement(size, "height").text = str(height)
        ET.SubElement(size, "depth").text = str(depth)
        ET.SubElement(annotation, "segmented").text = '0'
        ET.SubElement(annotation, "filename").text = filename_prefix + str(frame_number)

        annotations_in_frame = sdd_annotation[sdd_annotation[:, 5] == str(frame_number)]

        has_an_annotation = False
        for annotation_data in annotations_in_frame:
            if int(annotation_data[6]) == 0 and int(annotation_data[7]) == 0 and int(annotation_data[8]) == 0:
                has_an_annotation = True
                object = ET.SubElement(annotation, "object")
                ET.SubElement(object, "name").text = annotation_data[9].replace('"','')
                ET.SubElement(object, "pose").text = 'Unspecified'
                ET.SubElement(object, "truncated").text = annotation_data[7] # occluded
                ET.SubElement(object, "difficult").text = '0'
                bndbox = ET.SubElement(object, "bndbox")
                ET.SubElement(bndbox, "xmin").text = annotation_data[1]
                ET.SubElement(bndbox, "ymin").text = annotation_data[2]
                ET.SubElement(bndbox, "xmax").text = annotation_data[3]
                ET.SubElement(bndbox, "ymax").text = annotation_data[4]

        xml_annotation = ET.ElementTree(annotation)
        if has_an_annotation:
            xml_annotation.write(os.path.join(dest_path, filename_prefix + str(frame_number) + ".xml"))


def calculate_share(num_training_images, num_val_images, num_testing_images):
    # Returns how many frame should be each videos in train/val/test sets.
    train_videos = 0
    val_videos = 0
    test_videos = 0
    for scene in videos_to_be_processed:
        path = os.path.join(dataset_path, 'videos', scene)
        assert_path(path, path + ' not found.')

        videos = videos_to_be_processed.get(scene)
        if len(videos) > 0:
            for video_index in videos.keys():
                split_ratio = videos.get(video_index)
                if split_ratio[0] == 1:
                    train_videos += 1
                elif split_ratio[1] == 1:
                    val_videos += 1
                elif split_ratio[2] == 1:
                    test_videos += 1

    return (num_training_images/train_videos, num_val_images/val_videos, num_testing_images/test_videos)


def split_dataset_uniformly(number_of_frames, split_ratio, share, file_name_prefix):
    index_of_one = split_ratio.index(1)
    share_of_this_video = share[index_of_one]
    skip_by = int(math.ceil(float(number_of_frames)/share_of_this_video))
    image_index = [i for i in range(1, number_of_frames+1, skip_by)]

    for index in image_index:
        if index_of_one == 0:
            # Training
            write_to_file(os.path.join(destination_path, 'ImageSets', 'Main', 'train.txt'),
                          file_name_prefix + str(index))
            write_to_file(os.path.join(destination_path, 'ImageSets', 'Main', 'trainval.txt'),
                          file_name_prefix + str(index))
        elif index_of_one == 1:
            # Validation
            write_to_file(os.path.join(destination_path, 'ImageSets', 'Main', 'val.txt'),
                          file_name_prefix + str(index))
            write_to_file(os.path.join(destination_path, 'ImageSets', 'Main', 'trainval.txt'),
                          file_name_prefix + str(index))
        elif index_of_one == 2:
            # Testing
            write_to_file(os.path.join(destination_path, 'ImageSets', 'Main', 'test.txt'),
                          file_name_prefix + str(index))


def split_and_annotate(num_training_images=None, num_val_images=None, num_testing_images=None):
    assert_path(dataset_path, ''.join(e for e in dataset_path if e.isalnum()) + ' folder should be found in the cwd of this script.')
    init_directories()
    if num_training_images is not None and num_val_images is not None and num_testing_images is not None:
        share = calculate_share(num_training_images, num_val_images, num_testing_images)
    for scene in videos_to_be_processed:
        path = os.path.join(dataset_path, 'videos', scene)
        assert_path(path, path + ' not found.')

        videos = videos_to_be_processed.get(scene)
        if len(videos) > 0:
            for video_index in videos.keys():
                video_path = os.path.join(path, 'video' + str(video_index))
                assert_path(video_path, video_path + ' not found.')
                assert count_files(video_path) == 1, video_path+' should contain one file.'

                # Split video into frames
                # Check whether the video has already been made into frames
                jpeg_image_path = os.path.join(destination_path, 'JPEGImages')
                image_name_prefix = scene + '_video' + str(video_index) + '_'
                video_file = os.path.join(video_path, 'video.mov')
                if count_files(jpeg_image_path, image_name_prefix) == 0:
                    # Split Video
                    log('Splitting ' + video_file)
                    split_video(video_file, image_name_prefix)
                    log('Splitting ' + video_file + ' complete.')

                    # Annotate
                    log('Annotating frames from ' + video_file)
                    sdd_annotation_file = os.path.join(dataset_path, 'annotations', scene,
                                                       'video' + str(video_index), 'annotations.txt')
                    assert_path(sdd_annotation_file, 'Annotation file not found. '
                                                     'Trying to access ' + sdd_annotation_file)
                    dest_path = os.path.join(destination_path, 'Annotations')
                    number_of_frames = count_files(jpeg_image_path, image_name_prefix)
                    annotate_frames(sdd_annotation_file, dest_path, image_name_prefix, number_of_frames)
                    log('Annotation Complete.')

                else:
                    log(video_file + ' is already split into frames. Skipping...')

                # Create train-val-test split
                number_of_frames = count_files(jpeg_image_path, image_name_prefix)
                split_ratio = videos.get(video_index)
                if num_training_images is not None and num_val_images is not None and num_testing_images is not None:
                    # split_dataset_uniformly(number_of_frames, split_ratio, share, image_name_prefix)
                    simple_split(split_ratio)
                else:
                    split_dataset(number_of_frames, split_ratio, image_name_prefix)
                log('Successfully created train-val-test split.')
    log('Done.')


if __name__ == '__main__':

    # --------------------------------------------------------
    # videos_to_be_processed is a dictionary.
    # Keys in this dictionary should match the 'scenes' in Stanford Drone Dataset.
    # Value for each key is also a dictionary.
    #   - The number of items in the dictionary, can atmost be the number of videos each 'scene'
    #   - Each item in the dictionary is of the form {video_number:fraction_of_images_to_be_split_into_train_val_test_set}
    #   - eg: {2:(.7, .2, .1)} means 0.7 fraction of the images from Video2, should be put into training set,
    #                                0.2 fraction to validation set and
    #                                0.1 fraction to test set.
    #                                Also, training and validation images are merged into trainVal set.
    # --------------------------------------------------------

    # videos_to_be_processed = {'bookstore': {0: (.5, .2, .3)},
    #                           'coupa': {0: (.5, .2, .3)},
    #                           'deathCircle': {0: (.5, .2, .3)},
    #                           'gates': {0: (.5, .2, .3)},
    #                           'hyang': {0: (.5, .2, .3)},
    #                           'little': {0: (.5, .2, .3)},
    #                           'nexus': {0: (.5, .2, .3)},
    #                           'quad': {0: (.5, .2, .3)}}

    # Uniform Sub Sampling : Split should contain only 0 / 1
    # videos_to_be_processed = {'bookstore': {1: (1, 0, 0), 2: (0, 1, 0), 3: (0, 0, 1)},
    #                           'coupa': {0: (1, 0, 0), 2: (0, 1, 0), 3: (0, 0, 1)},
    #                           'deathCircle': {0: (1, 0, 0), 2: (0, 1, 0), 3: (0, 0, 1)},
    #                           'gates': {0: (1, 0, 0), 2: (0, 1, 0), 3: (0, 0, 1)},
    #                           'hyang': {0: (1, 0, 0), 2: (0, 1, 0), 3: (0, 0, 1)},
    #                           'little': {0: (1, 0, 0), 2: (0, 1, 0), 3: (0, 0, 1)},
    #                           'nexus': {0: (1, 0, 0), 2: (0, 1, 0), 3: (0, 0, 1)},
    #                           'quad': {0: (1, 0, 0), 2: (0, 1, 0), 3: (0, 0, 1)}}

    # Train/Val : 1, 4, 5, 6
    # Test: 2, 3
    videos_to_be_processed = {'bookstore': {1: (1, 0, 0), 2: (0, 0, 1), 3: (0, 0, 1), 4: (1, 0, 0), 5: (1, 0, 0), 6: (1, 0, 0)}}

    num_training_images = 40000
    num_val_images = 10000
    num_testing_images = 20000

    dataset_path = './StanfordDroneDataset'
    destination_folder_name = 'sdd_train_test_bookstore'
    destination_path = os.path.join(dataset_path, destination_folder_name)

    # split_and_annotate()
    split_and_annotate(num_training_images, num_val_images, num_testing_images)
