# -*- coding: utf-8 -*-
"""
Created on Wed Oct 19 15:08:44 2022

@author: turnerp
"""

import tifffile
import os
from glob2 import glob
import shutil
import numpy as np
import pandas as pd
import json
import pickle
import tifffile
import matplotlib.pyplot as plt
import cv2
import hashlib
import datetime
from multiprocessing import Pool
import tqdm
import traceback
from functools import partial
import hashlib
import tempfile




# aksegdir = r"\\physics\dfs\DAQ\CondensedMatterGroups\AKGroup\Piers\AKSEG\Images"

# users = glob(aksegdir + "*\*")
# users = [user.split("\\")[-1] for user in users]

# akseg_stats = []

# for user in users:
      
#     num_images = 0
#     num_cells = 0
    
#     userdir = aksegdir + "\\" + user
    
#     image_files = glob(userdir  + "\\" + "images" + "*\**\*.tif")
    
#     num_images = len(image_files)
    
#     json_files = glob(userdir  + "\\" + "json" + "*\**\*.txt")
    
#     for json_path in json_files:
        
#         try:
        
#             with open(json_path, 'r') as f:
#                 annotations = json.load(f)["annotations"]
                
#                 num_cells += len(annotations)
                
#                 print(user, num_images, num_cells)
                
#         except Exception:
#             pass
            
#     user_data = {"user":user, "num_images": num_images, "num_cells": num_cells}
    
#     akseg_stats.append(user_data)
            
            
# with open('akseg_stats.pickle', 'wb') as handle:
#     pickle.dump(akseg_stats, handle, protocol=pickle.HIGHEST_PROTOCOL)     
        

with open('akseg_stats.pickle', 'rb') as handle:
    akseg_stats = pickle.load(handle)


akseg_stats = pd.DataFrame(akseg_stats)

akseg_stats = akseg_stats[~akseg_stats["user"].isin(["DEV","EL"])]


