import os

def split_and_annotate(videos_to_be_processed):
    pass

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

    videos_to_be_processed = {'bookstore': ({0:(.7, .2, .1)}),
                              'coupa': (),
                              'deathCircle': (),
                              'gates': (),
                              'hyang': (),
                              'little': (),
                              'nexus': (),
                              'quad': ()}

    assert os.path.exists("./StanfordDroneDataset"), "StanfordDroneDataset should be found in the cwd of this script."

    split_and_annotate(videos_to_be_processed)