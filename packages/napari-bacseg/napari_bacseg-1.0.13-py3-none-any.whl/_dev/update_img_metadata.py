# -*- coding: utf-8 -*-
"""
Created on Fri Feb 10 15:44:30 2023

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
import time




user_initial = "CF"
user_metadata_path = os.path.join(r"\\physics\dfs\DAQ\CondensedMatterGroups\AKGroup\Piers\AKSEG\Images", user_initial, f"{user_initial}_file_metadata.txt")
user_metadata = pd.read_csv(user_metadata_path, sep=",", low_memory=False)

user_metadata = user_metadata[user_metadata["microscope"]is"ScanR"]


path = user_metadata.iloc[-1].image_save_path

image = tifffile.imread(path)

tif = tifffile.TiffFile(path, mode='r+b')
tif_metadata = tif.pages[0].tags["ImageDescription"].value
tif_metadata = json.loads(tif_metadata)


start_time = time.time()
image = tifffile.imread(path)
tifffile.imwrite("testimg.tif",image, metadata=tif_metadata)
print(f"Completed. Duration: {(time.time() - start_time)} seconds.\n")

time.sleep(1)

start_time = time.time()
tif = tifffile.TiffFile("testimg.tif", mode='r+b')
tif_metadata = tif.pages[0].tags["ImageDescription"].value
tif_metadata = json.loads(tif_metadata)
tif_metadata["xxx"] = "xxx"
tif_metadata = json.dumps(tif_metadata)
tif.pages[0].tags["ImageDescription"].overwrite(tif_metadata)
print(f"Completed. Duration: {(time.time() - start_time)} seconds.\n")



def update_metadata(path, metadata):
    
    try:
    
        tif = tifffile.TiffFile(path, mode='r+b')
        metadata = json.dumps(metadata)
        tif.pages[0].tags["ImageDescription"].overwrite(metadata)
    
    except Exception:
        print(traceback.format_exc())
        pass
    
