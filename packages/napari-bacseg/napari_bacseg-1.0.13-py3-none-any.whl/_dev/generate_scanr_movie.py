# -*- coding: utf-8 -*-
"""
Created on Fri Jul  8 17:06:36 2022

@author: turnerp
"""

import numpy as np
import matplotlib.pyplot as plt
import tifffile
from skimage import exposure
from glob2 import glob

def normalize99(X):
    """ normalize image so 0.0==0.01st percentile and 1.0==99.99th percentile """

    if np.max(X) > 0:
        X = X.copy()
        v_min, v_max = np.percentile(X[X!=0], (1, 99))
        X = exposure.rescale_intensity(X, in_range=(v_min, v_max))

    return X

path = r"D:\Untreated_timelapse_correctexposure\data"
path = r"D:\220713_ScanR_WT_Timelapse\AgarosePad_003\data"



file_list = glob(path + "\*.tif")

file_list = [file for file in file_list if "Trans" not in file]



bf = []
nuc = []

for path in file_list:
    

    nuc.append(tifffile.imread(path))
    bf.append(tifffile.imread(path.replace("Hu","Trans")))
    

bf = np.stack(bf)
nuc = np.stack(nuc)

image = np.stack([bf,nuc])

image = np.moveaxis(image, 0, 1)

tifffile.imwrite("scanr_untreated_timelapse_bf.tif", bf)
tifffile.imwrite("scanr_untreated_timelapse_nuc.tif", nuc)