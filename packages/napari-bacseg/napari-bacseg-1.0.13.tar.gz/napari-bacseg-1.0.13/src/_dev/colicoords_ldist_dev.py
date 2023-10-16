# -*- coding: utf-8 -*-
"""
Created on Thu Sep 15 16:06:27 2022

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


import shapely
import cellpose



with open('ldistdev.pickle', 'rb') as handle:
    cell_list, channel = pickle.load(handle)


 
# nbins = config.cfg.L_DIST_NBINS
# sigma = config.cfg.L_DIST_SIGMA
# sigma_arr = sigma / cell_list.length

# x_arr, out_arr = cell_list.l_dist(nbins, data_name=channel, norm_x=True, sigma=sigma_arr)

# x = x_arr[0]

# maxes = np.max(out_arr, axis=1)
# bools = maxes!=0
# n = np.sum(~bools)

# if n > 0:
#     print("Warning: removed {} curves with maximum zero".format(n))

# out_arr = out_arr[bools]
# out_arr = np.array([array + np.flip(array) for array in out_arr])

# a_max = np.max(out_arr, axis=1)
# out_arr = out_arr / a_max[:, np.newaxis]

# ldist_mean = np.nanmean(out_arr, axis=0)
# ldist_std = np.std(out_arr, axis=0)

# plt.plot(ldist_mean)
# plt.show()

# plt.plot(out_arr.T)
# plt.show()


def rescale01(x):
    """ normalize image from 0 to 1 """
    
    if np.max(x) > 0:
        
        x = (x - np.min(x)) / (np.max(x) - np.min(x))
        
    return x


# cell = cell_list[0]

ldist_data = []

for cell in cell_list:

    nbins = config.cfg.L_DIST_NBINS
    sigma = config.cfg.L_DIST_SIGMA
    sigma_arr = sigma / cell.length
    
    x_arr, out_arr = cell.l_dist(nbins, data_name=channel, norm_x=True, sigma=sigma_arr)
    
    max_val = np.max(out_arr)
    
    if max_val > 0:
        
        out_arr = out_arr + np.flip(out_arr)
          
        out_arr -= np.min(out_arr)
        out_arr = out_arr/np.max(out_arr)
        
        plt.plot(out_arr)
        plt.show()
        
        ldist_data.append(out_arr)
        
    else:
        
        ldist_data.append(None)
             
# ldist_data = [dat for dat in ldist_data if dat!=None]
        
# ldist_data = np.array(ldist_data)    

# ldist_mean = np.nanmean(ldist_data, axis=0)
# ldist_std = np.std(ldist_data, axis=0)

# plt.plot(ldist_mean)
# plt.show()





# ldist_mean = np.nanmean(out_arr, axis=0)
# ldist_std = np.std(out_arr, axis=0)

# plt.plot(ldist_mean)
# plt.show()


# ldist_mean = np.nanmean(out_arr, axis=0)
# ldist_std = np.std(out_arr, axis=0)












# plt.plot(ldist_mean)

# colicoords_dir = os.path.join(tempfile.gettempdir(),"colicoords")

# if os.path.isdir(colicoords_dir)!=True:
    
#     os.mkdir(colicoords_dir)
    
    
# temp_path = tempfile.TemporaryFile(suffix=".npy", dir=colicoords_dir).name


# import shutil
# shutil.rmtree(colicoords_dir)


# file_paths = glob(colicoords_dir + "\\*")


# dat = np.load(file_paths[0],allow_pickle=True).item()




