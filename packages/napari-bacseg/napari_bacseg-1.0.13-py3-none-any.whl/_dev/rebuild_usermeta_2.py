# -*- coding: utf-8 -*-
"""
Created on Tue Mar  1 18:44:12 2022

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



metadata_columns = ["date_uploaded",
                    "date_created",
                    "date_modified",
                    "file_name",
                    "channel",
                    "file_list",
                    "channel_list",
                    "segmentation_file",
                    "segmentation_channel",
                    "akseg_hash",
                    "user_initial",
                    "content",
                    "microscope",
                    "modality",
                    "source",
                    "stain",
                    "stain_target",
                    "antibiotic",
                    "treatment time (mins)",
                    "antibiotic concentration",
                    "mounting method",
                    "protocol",
                    "user_meta1",
                    "user_meta2",
                    "user_meta3",
                    "folder",
                    "parent_folder",
                    "segmented",
                    "labelled",
                    "segmentation_curated",
                    "label_curated",
                    "posX",
                    "posY",
                    "posZ",
                    "image_load_path",
                    "image_save_path",
                    "mask_load_path",
                    "mask_save_path",
                    "label_load_path",
                    "label_save_path"]









def read_tif(path):
    
    try:

        with tifffile.TiffFile(path) as tif:
            metadata = tif.pages[0].tags["ImageDescription"].value
            metadata = json.loads(metadata)
    except Exception:
        metadata = {}
        pass
            
    return metadata

def get_meta_value(meta,value):

    if value in meta.keys():
    
        data = meta[value]
    else:
        data = None
        
    return data

def check_metadata_format(metadata, expected_columns):

    if "stains" in metadata.columns:
        metadata = metadata.rename(columns={"stains": "stain"})

    missing_columns = list(set(expected_columns) - set(metadata.columns))
    extra_columns = list(set(metadata.columns) - set(expected_columns))

    all_columns = expected_columns + extra_columns

    metadata[missing_columns] = pd.DataFrame([[None] * len(missing_columns)], index=metadata.index)

    date = datetime.datetime.now()

    metadata.loc[metadata['date_uploaded'].isin(["None", None, np.nan, 0]),
                 ["date_uploaded", "date_created", "date_modified"]] = str(date)

    metadata = metadata[all_columns]

    metadata = metadata.astype({'segmented': bool, 'labelled': bool,
                                'segmentation_curated': bool, 'label_curated': bool})

    return metadata, all_columns


def get_filemeta(path):
    
    file_metadata = None
    
    try:
    
        meta = read_tif(path)
             
        file_name = path.split("\\")[-1]
        
        mask_path = path.replace("\\images\\","\\masks\\")
        
        mask = tifffile.imread(mask_path)
        
        unique_segmentations = np.unique(mask)
        unique_segmentations = np.delete(unique_segmentations, np.where(unique_segmentations==0))
        num_segmentations = len(unique_segmentations)
        
        num_segmentations = 0
        
        if "posX" in meta.keys():
            
            posX = meta['posX']
            posY = meta['posX']
            posZ = meta['posX']
            
        elif "StagePos_um" in meta.keys():
            posX,posY,posZ = meta["StagePos_um"]
        else:
            posX = 0
            posY = 0
            posZ = 0

        
        if "date_modified" in meta.keys():
            date_modified = meta["date_modfied"]
        else:
            date_modified = datetime.datetime.now()
            
        if "date_created" in meta.keys():
            date_created = meta["date_created"]
        else:
            date_created = datetime.datetime.now() 

        if "date_uploaded" in meta.keys():
            date_uploaded = meta["date_uploaded"]
        else:
            date_uploaded = datetime.datetime.now() 
            

        file_metadata = {"date_uploaded": date_uploaded,
                         "date_created": date_created,
                         "date_modified": date_modified,
                         "file_name": file_name,
                         "channel": get_meta_value(meta, "channel"),
                         "file_list": get_meta_value(meta, "file_list"),
                         "channel_list": get_meta_value(meta, "channel_list"),
                         "segmentation_file": get_meta_value(meta, "segmentation_file"),
                         "segmentation_channel": get_meta_value(meta, "segmentation_channel"),
                         "akseg_hash": get_meta_value(meta, "akseg_hash"),
                         "user_initial": get_meta_value(meta, "user_initial"),
                         "content": get_meta_value(meta, "image_content"),
                         "microscope": get_meta_value(meta, "microscope"),
                         "modality": get_meta_value(meta, "modality"),
                         "source": get_meta_value(meta, "light_source"),
                         "stain": get_meta_value(meta, "stain"),
                         "stain_target": get_meta_value(meta, "stain_target"),
                         "antibiotic": get_meta_value(meta, "antibiotic"),
                         "treatment time (mins)": get_meta_value(meta, "treatmenttime"),
                         "antibiotic concentration": get_meta_value(meta, "abxconcentration"),
                         "mounting method": get_meta_value(meta, "mount"),
                         "protocol": get_meta_value(meta, "protocol"),
                         "user_meta1": get_meta_value(meta, "usermeta1"),
                         "user_meta2": get_meta_value(meta, "usermeta2"),
                         "user_meta3": get_meta_value(meta, "usermeta3"),
                         "folder": get_meta_value(meta, "folder"),
                         "parent_folder": get_meta_value(meta, "parent_folder"),
                         "num_segmentations": num_segmentations,
                         "segmented": get_meta_value(meta, "segmented"),
                         "labelled": get_meta_value(meta, "labelled"),
                         "segmentation_curated": get_meta_value(meta, "segmentations_curated"),
                         "label_curated": get_meta_value(meta, "labels_curated"),
                         "posX": posX,
                         "posY": posY,
                         "posZ": posZ,
                         "image_load_path": get_meta_value(meta, "image_path"),
                         "image_save_path": path,
                         "mask_load_path": get_meta_value(meta, "mask_path"),
                         "mask_save_path": path.replace("\\images\\","\\masks\\"),
                         "label_load_path": get_meta_value(meta, "label_path"),
                         "label_save_path": path.replace("\\images\\","\\labels\\")}
        
        
        # file_metadata = pd.DataFrame.from_dict(file_metadata)
        
    except Exception:
        pass

    return file_metadata
                                 
   
    
user_initial = "PT"
paths = os.path.join(r"\\physics\dfs\DAQ\CondensedMatterGroups\AKGroup\Piers\AKSEG\Images", user_initial, "images")
paths = glob(paths + "*\**\*.tif")
paths = [path for path in paths if "_flows.tif" not in path]




# file_metadata = get_filemeta(paths[0])


if __name__=='__main__':

    with Pool() as p:
        
        d = list(tqdm.tqdm(p.imap(get_filemeta, paths), total=len(paths)))
        p.close()
        p.join()
        
        user_metadata = pd.DataFrame(d)
        
        user_metadata, expected_columns = check_metadata_format(user_metadata, metadata_columns)
        user_metadata = user_metadata[expected_columns]
        
        user_metadata.drop_duplicates(subset=['akseg_hash'], keep="first", inplace=True)
        
        user_metadata = user_metadata[user_metadata["user_initial"]isuser_initial]
                
        akgroup_dir = r"\\physics\dfs\DAQ\CondensedMatterGroups\AKGroup\Piers\AKSEG\Images"
        user_metadata_path = akgroup_dir + "\\" + user_initial + "\\" + user_initial + "_file_metadata.txt"   
        
        data = user_metadata[user_metadata["user_initial"]==user_initial]
        
        data.to_csv(user_metadata_path, sep=",", index = False)            



# for path in paths:
#     try:
#         file_metadata = get_filemeta(path)
#     except Exception:
#         print(path)
#         break
    





# akgroup_dir = r"\\physics\dfs\DAQ\CondensedMatterGroups\AKGroup\Piers\AKSEG\Images"
# user_initial = "PT"
# user_metadata_path = akgroup_dir + "\\" + user_initial + "\\" + user_initial + "_file_metadata.txt"
# user_metadata = pd.read_csv(user_metadata_path, sep=",")


# antibiotics = user_metadata["antibiotic"].unique()


# print(user_metadata.columns)


# xx = user_metadata[user_metadata["user_meta3"]is"Repeat 1"]


# user_metadata["segmentation_channel"] = user_metadata["segmentation_channel"].astype(str)
# user_metadata = user_metadata[user_metadata["segmentation_channel"]is"53d2"]

# for i in range(len(user_metadata)):
    
#     file_name = user_metadata["file_name"][i]
#     file_name_path = os.path.basename(user_metadata["image_save_path"][i])
    
#     if file_name!=file_name_path:
#         print(i)



