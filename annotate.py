import os
import subprocess


def assert_path(path, error_message):
    assert os.path.exists(path), error_message


def count_files(path, filename_starts_with=''):
    files = [f for f in os.listdir(path)if os.path.isfile(os.path.join(path, f))
                     and f.startswith(filename_starts_with)]
    return len(files)

def split_video(video_file, image_name_prefix):
    if not os.path.exists(destination_path):
        os.makedirs(os.path.join(destination_path, 'JPEGImages'))
        os.makedirs(os.path.join(destination_path, 'ImageSets', 'Main'))
        os.makedirs(os.path.join(destination_path, 'Annotations'))

    subprocess.call(['cd', os.path.join(destination_path, 'JPEGImages')])
    return subprocess.check_output(['ffmpeg', '-i', video_file, image_name_prefix + '%d.jpg'])


def split_and_annotate():
    assert_path(dataset_path, ''.join(e for e in dataset_path if e.isalnum()) + ' folder should be found in the cwd of this script.')

    for scene in videos_to_be_processed:
        path = os.path.join(dataset_path, 'videos', scene)
        assert_path(path, path + ' not found.')

        videos = videos_to_be_processed.get(scene)
        if len(videos) > 0:
            for video_index in videos.keys():
                video_path = os.path.join(path, 'video' + str(video_index))
                assert_path(video_path, video_path + ' not found.')
                assert count_files(video_path) == 1, video_path+' should contain one file.'
                print video_path

                # Check whether the video has already been made into frames
                jpeg_image_path = os.path.join(destination_path, 'JPEGImages')
                image_name_prefix = scene + '_video' + str(video_index) + '_'
                if count_files(jpeg_image_path, image_name_prefix) == 0:
                    # Split Video
                    video_file = os.path.join(video_path, 'video.mov')
                    split_video(video_file, image_name_prefix)



if __name__ == '__main__':

    # --------------------------------------------------------
    # videos_to_be_processed is a dictionary.
    # Keys in this dictionary should match the 'scenes' in Stanford Drone Dataset.
    # Value for each key is a tuple of dictionaries.
    #   - The number of items in the tuple can be atmost the number of videos each 'scene'
    #   - Each dictionary is of the form {video_number:fraction_of_images_to_be_split_into_trainVal_set}
    #   - eg1: {2:(.7, .2, .1)} means 0.7 fraction of the images from Video2, should be put into training set,
    #                                 0.2 fraction to validation set and
    #                                 0.1 fraction to test set.
    #                                 Also, training and validation images are merged into trainVal set.
    # --------------------------------------------------------
    #
    # --------------------------------------------------------
    # SDD contains the following 'scenes' and corresponding videos:
    # 'bookstore'   scene contains videos: (0, 1, 2, 3, 4, 5, 6)
    # 'coupa'       scene contains videos: (0, 1, 2, 3)
    # 'deathCircle' scene contains videos: (0, 1, 2, 3, 4)
    # 'gates'       scene contains videos: (0, 1, 2, 3, 4, 5, 6, 7, 8)
    # 'hyang'       scene contains videos: (0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14)
    # 'little'      scene contains videos: (0, 1, 2, 3)
    # 'nexus'       scene contains videos: (0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11)
    # 'quad'        scene contains videos: (0, 1, 2, 3)
    # --------------------------------------------------------
    #
    # videos_to_be_processed = {'bookstore': {0: (.6, .2, .2), 5: (.6, .2, .2)}}

    videos_to_be_processed = {'bookstore': {0: (.6, .2, .2)},
                              'coupa': {},
                              'deathCircle': {},
                              'gates': {},
                              'hyang': {},
                              'little': {},
                              'nexus': {},
                              'quad': {}}

    dataset_path = './StanfordDroneDataset'
    destination_path = os.path.join(dataset_path, 'sdd')

    split_and_annotate()