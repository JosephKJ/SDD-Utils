def split_and_annotate():
    pass

if __name__ == '__main__':
    videos_to_be_processed = {'bookstore':(0,1,2,3,4,5,6),
                              'coupa':(0,1,2,3),
                              'deathCircle':(0,1,2,3,4),
                              'gates':(0,1,2,3,4,5,6,7,8),
                              'hyang':(0,1,2,3,4,5,6,7,8,9,10,11,12,13,14),
                              'little':(0,1,2,3),
                              'nexus':(0,1,2,3,4,5,6,7,8,9,10,11),
                              'quad':(0,1,2,3)}
    videos_to_be_processed = {'bookstore': (0),
                              'coupa': (),
                              'deathCircle': (),
                              'gates': (),
                              'hyang': (),
                              'little': (),
                              'nexus': (),
                              'quad': ()}


    percent_of_test_images = 0.3

    split_and_annotate(videos_to_be_processed, percent_of_test_images)