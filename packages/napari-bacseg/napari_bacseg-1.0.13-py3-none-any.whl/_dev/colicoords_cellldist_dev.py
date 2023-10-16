# -*- coding: utf-8 -*-
"""
Created on Thu Sep 22 08:58:31 2022

@author: turnerp
"""

from glob2 import glob
import numpy as np
import pandas as pd
import tifffile
import shutil
import matplotlib.pyplot as plt
import pickle
# import psycopg2
import tifffile
import shutil
from skimage import exposure, img_as_ubyte
import os
from skimage import data
from skimage.registration import phase_cross_correlation
from skimage.registration._phase_cross_correlation import _upsampled_dft
from scipy.ndimage import fourier_shift
import scipy.ndimage
import cv2
import hashlib
import datetime
import json
from multiprocessing import Pool
import tqdm
import traceback
import tempfile
from colicoords import Data, Cell, CellPlot, data_to_cells, config, CellList

from cellpose import models
# from shapely import LineString

# with open('cellldistdev.pickle', 'rb') as handle:
#     cell_statistics = pickle.load(handle)


# data = [dat["ldist"] for dat in cell_statistics if dat["cell"]!=None]

# channels = np.unique([list(dat.keys()) for dat in data]).tolist()

# ldist_data = {}

# for channel in channels:
    
#     ldist = [dat[channel] for dat in data if dat[channel]!=None]
    
#     ldist = np.stack(ldist)
    
#     ldist_mean = np.nanmean(ldist, axis=0)
#     ldist_std = np.std(ldist, axis=0)
    
#     channel_dat = {channel + " mean": ldist_mean,
#                 channel + " std": ldist_std}
    
#     ldist_data = {**ldist_data, **channel_dat}

import psutil, os
p = psutil.Process( os.getpid() )
for dll in p.memory_maps():
    if "cellpose" in dll:
        print(dll.path)