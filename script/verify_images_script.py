#!/usr/bin/python3

## Path: script/verify_images.py
## Script to verify images and save the corrupted images to a csv file - default path is './save_.csv'
import os
from mb_utils.src import verify_image,logging
import argparse
import pandas as pd
from datetime import datetime

def verify_images_script(image_list: list , logger=None) -> dict:
    """
    script to verify images
    Input:
        image_list : list of image paths
    Output:
        dictionary of images and their status
    """
    assert(isinstance(image_list, list)) , "image_list should be a list"
    assert(len(image_list) > 0) , "image_list should not be empty"
    assert(all([isinstance(image, str) for image in image_list])) , "image_list should contain only strings"

    if logger:
        logger.info('Verifying images')
    image_dict = {image_list[i]:verify_image.verify_images(i) for i in range(len(image_list))}
    
    if logger:
        logger.info('Finished verifing images')
    return image_dict

def main(args):
    """
    main function
    """
    logger = logging.logger if args.logger else None
    image_list = args.image_list
    save_corrupted_paths = args.save_corrupted_paths
    if logger:
        logger.info('Starting verify_images_script')
    image_dict = verify_images_script(image_list, logger=logger)    
    if logger:
        logger.info('Finished verifing images srcipt')

    k = (list((image_dict.values())).count(False))
    if k == 0:
        print("All images are verified. No images are corrupted")
    else:
        print("Total number of corrupted images are: ", k)
        print("The list of corrupted images are: ")
        for i in image_dict:
            if image_dict[i] == False:
                print(i)    
    if save_corrupted_paths:
        now = datetime.now()
        dt_string = now.strftime("%Y%m%d_%H%M")
        path= './corrupted_image_paths/corrupt_paths_'+ dt_string +'.csv' 
        if logger:
            logger.info('Saving corrupted images to {}'.format(path))
        os.mkdir('./corrupted_image_paths') if not os.path.exists('./corrupted_image_paths') else None
        save_l=[i for i in image_dict if image_dict[i] == False]
        df = pd.DataFrame (save_l, columns = ['corrupted_image_paths'])
        df.to_csv(path, index=False)
        if logger:
            logger.info('Finished saving corrupted images to {}'.format(path))

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Verify images")
    parser.add_argument('-i', '--image_path_list', default=None, type=list,
                        help="list of image paths")
    parser.add_argument('-l', '--logger', default=False, type=bool, help="logger - default is None")
    parser.add_argument('-s', '--save_corrupted_paths', default=False, type=bool, 
                        help="save_corrupted_paths to corrupted image path folder with timestamp as csv - default is False")
    args = parser.parse_args()
    main(args)