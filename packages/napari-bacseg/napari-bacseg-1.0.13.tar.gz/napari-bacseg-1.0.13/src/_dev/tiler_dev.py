# -*- coding: utf-8 -*-
"""
Created on Thu Jul 21 16:39:48 2022

@author: turnerp
"""


import traceback

import numpy as np
from skimage import exposure
import cv2
import tifffile
import os
from glob2 import glob
import pandas as pd
import mat4py
import datetime
import json
import matplotlib.pyplot as plt
import hashlib
import time
import pickle
from tiler import Tiler, Merger

from numpy.lib.stride_tricks import as_strided


path = r"D:\Unlearning Files\220525_ScanR_Agarose_CIP\BurntSlide_001\data"

files = glob(path + "*\*.tif")


image = []

for i in range(3):

    image.append(tifffile.imread(files[i]))
    
    
image = np.stack(image)

    

tiler = Tiler(data_shape=image[0].shape,
                    tile_shape=(500, 500),
                    channel_dimension=None,
                    overlap = 100)




tiled_image = []
bboxes = []

for i in range(image.shape[0]):
    
    img = np.expand_dims(image[i],0)
        
    tiles = []
    
    for tile_id, tile in tiler.iterate(image[i]):
        
        bbox = tiler.get_tile_bbox_position(tile_id)
        
        tiles.append(tile)
        
    tiles = np.stack(tiles)
    tiled_image.append(tiles)
    
image = np.stack(tiled_image)




merger = Merger(tiler)

merged_image = []

for i in range(1):
    
    merger.reset()
        
    for j in range(image.data.shape[1]):
        
        img = image[i,j].copy()
        
        merger.add(j, img.data)
        
    merged = merger.merge(dtype=img.dtype)
    
image = np.stack(image)






