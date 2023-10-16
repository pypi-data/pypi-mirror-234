# -*- coding: utf-8 -*-
"""
Created on Thu Mar 23 13:55:01 2023

@author: turnerp
"""


import tifffile
import cv2
import numpy as np
import matplotlib.pyplot as plt


image_path = r"\\physics\dfs\DAQ\CondensedMatterGroups\AKGroup\Rasched\DeepsegMatTestimage.tif"
mask_path = r"\\physics\dfs\DAQ\CondensedMatterGroups\AKGroup\Rasched\DeepsegMatTest\mask.tif"


mask = tifffile.imread(mask_path)

mask1 = np.zeros(mask.shape,dtype=np.uint8)
mask1[mask!=0] = 1


plt.imshow(mask1)

mask2 = []

for mask_id in np.unique(mask):
    
    if mask_id != 0:
        
        mask_frame = np.zeros(mask.shape,dtype=np.uint8)
        mask_frame[mask==mask_id] = 1
        
        mask2.append(mask_frame)
        
mask2 = np.stack(mask2)


tifffile.imwrite(r"\\physics\dfs\DAQ\CondensedMatterGroups\AKGroup\Rasched\DeepsegMatTest\binary_mask.tif", mask1)
tifffile.imwrite(r"\\physics\dfs\DAQ\CondensedMatterGroups\AKGroup\Rasched\DeepsegMatTest\binary_mask_stack.tif", mask2)
        
    