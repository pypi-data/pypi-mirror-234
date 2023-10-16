# -*- coding: utf-8 -*-
"""
Created on Thu May 26 11:53:44 2022

@author: turnerp
"""

from astropy.io import fits
from glob2 import glob
import os


paths = glob("D:\Alfredas\*.fits")


with fits.open(paths[0]) as hdul:
    header = dict(hdul[0].header)
    data = hdul[0].data
    
def read_fits(path, precision="native", multiframe_mode = 0, crop_mode = 0):

    image_name = os.path.basename(path)
    
    with fits.open(path) as hdul:
        
        image = hdul[0].data
        
        try:
            metadata = dict(hdul[0].header)
        except Exception:
            metadata = {}

    # image = crop_image(image, crop_mode)

    # image = get_frame(image, multiframe_mode)

    # image = rescale_image(image, precision=precision)

    # folder = os.path.abspath(path).split("\\")[-2]
    # parent_folder = os.path.abspath(path).split("\\")[-3]

    # if "image_name" not in metadata.keys():

    #     metadata["image_name"] = image_name
    #     metadata["channel"] = None
    #     metadata["segmentation_file"] = None
    #     metadata["segmentation_channel"] = None
    #     metadata["image_path"] = path
    #     metadata["mask_name"] = None
    #     metadata["mask_path"] = None
    #     metadata["label_name"] = None
    #     metadata["label_path"] = None
    #     metadata["crop_mode"] = crop_mode
    #     metadata["multiframe_mode"] = multiframe_mode
    #     metadata["folder"] = folder
    #     metadata["parent_folder"] = parent_folder
    #     metadata["dims"] = [image.shape[-1], image.shape[-2]]
    #     metadata["crop"] = [0, image.shape[-2], 0, image.shape[-1]]

    return image, metadata    