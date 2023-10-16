# -*- coding: utf-8 -*-
"""
Created on Thu Apr 20 12:52:40 2023

@author: turnerp
"""

import pandas as pd
import numpy as np
import pickle
import xmltodict
import os
from glob2 import glob
import tifffile
import json
import scipy
import cv2
from skimage.registration import phase_cross_correlation
from skimage.registration._phase_cross_correlation import _upsampled_dft
import tempfile
import hashlib
from tiler import Tiler, Merger
import datetime
from multiprocessing import Pool
import tqdm
import traceback
from functools import partial
import matplotlib.pyplot as plt


def add_scale_bar(image,
                  pixel_resolution = 100, pixel_resolution_units = "nm",
                  scalebar_size = 20, scalebar_size_units = "um",
                  scalebar_colour = "white", scalebar_thickness = 10, scalebar_margin = 50):

    h,w = image.shape
    
    if pixel_resolution_units != "nm":
        pixel_resolution = pixel_resolution*1000
    
    scalebar_size = 20
    scalebar_size_inits = "um"
    
    if scalebar_size_units != "nm":
        scalebar_size = scalebar_size*1000
       
    scalebar_len = int(scalebar_size/pixel_resolution)    
       
    if scalebar_colour == "white":
        bit_depth = str(image.dtype)
        bit_depth = int(bit_depth.replace("uint",""))
        colour = ((2**bit_depth)-1)
    else:
        colour = 0
    
    scalebar_pos = (w-scalebar_margin - scalebar_len, h-scalebar_margin) # Position of the scale bar in the image (in pixels)
    
    image = cv2.rectangle(image, scalebar_pos, (scalebar_pos[0]+scalebar_len, scalebar_pos[1]+scalebar_thickness), colour, -1)
    
    return image

user_initial = "CF"

user_metadata_path = os.path.join(r"\\physics\dfs\DAQ\CondensedMatterGroups\AKGroup\Piers\AKSEG\Images", user_initial, f"{user_initial}_file_metadata.txt")
user_metadata = pd.read_csv(user_metadata_path, sep=",", low_memory=False)




path = user_metadata.iloc[0]["image_save_path"]

image = tifffile.imread(path)

image = add_scale_bar(image)


plt.imshow(image)
plt.show()