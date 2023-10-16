# -*- coding: utf-8 -*-
"""
Created on Mon Jun 20 11:21:06 2022

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
# import mat4py
import datetime
import json
import matplotlib.pyplot as plt
import hashlib
# from napari_bacseg._utils_json import import_coco_json, export_coco_json
import time
from multiprocessing import Pool
import tqdm
from functools import partial

path = r"\\cmwt188\d\Piers\AKSEG CMWT188\Images\PT\PT_file_metadata.txt"

user_metadata = pd.read_csv(path, sep=",")



# if "date_modified" not in user_metadata.columns.tolist():
#         user_metadata.insert(1, "date_modified",user_metadata["date_uploaded"])
#         user_metadata.insert(1, "date_created",user_metadata["date_uploaded"])
#         user_metadata.insert(30, "posX",0)
#         user_metadata.insert(31, "posY",0)
#         user_metadata.insert(32, "posZ",0)
    
    




# def update_usermetadata(i,user_metadata):
    
#     data = user_metadata.iloc[[i]]

#     if "date_modified" not in data.columns.tolist():
        
#         file_name = data.file_name.item()
#         file_path = data.image_save_path.item()
        
#         posX = 0
#         posY = 0
#         posZ = 0
#         date_created = np.nan
    
#         try:
            
#             date_created = os.path.getctime(file_path) 
#             date_created = datetime.datetime.fromtimestamp(date_created)
    
#             with tifffile.TiffFile(file_path) as tif:
        
#                 meta = tif.pages[0].tags["ImageDescription"].value
        
#                 meta = json.loads(meta)
                
#                 if "posX" in meta.keys():
                    
#                     posX = meta['posX']
#                     posY = meta['posX']
#                     posZ = meta['posX']
                    
#                 elif "StagePos_um" in meta.keys():
#                     posX,posY,posZ = meta["StagePos_um"]
                          
#         except Exception:
#             print(traceback.format_exc())
            
#         data.insert(1, "date_modified",user_metadata["date_uploaded"])
#         data.insert(1, "date_created",date_created)
#         data.insert(30, "posX",posX)
#         data.insert(31, "posY",posY)
#         data.insert(32, "posZ",posZ)
        
#     return data
    
    
# if __name__=='__main__':
    
#     mnum = np.arange(len(user_metadata))
    
#     with Pool() as p:
        
#         d = list(tqdm.tqdm(p.imap_unordered(partial(update_usermetadata, user_metadata=user_metadata),mnum), total=len(mnum)))
#         p.close()
#         p.join()
        
#         user_metadata = pd.concat(d)
       
#         user_metadata.to_csv(path, sep=",", index = False)   

# user_metadata = pd.read_csv(path, sep=","):
    
#     if "date_modified" not in data.columns.tolist():
    
    












