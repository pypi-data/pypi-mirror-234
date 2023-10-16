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
import pickle
from functools import partial
import pathlib
import traceback
import pathlib

def import_coco_json(json_path):

    try:
        json_path = os.path.splitext(json_path)[0] + ".txt"

        with open(json_path) as f:
            dat = json.load(f)

        h = dat["images"][0]["height"]
        w = dat["images"][0]["width"]

        mask = np.zeros((h, w), dtype=np.uint16)
        nmask = np.zeros((h, w), dtype=np.uint16)
        labels = np.zeros((h, w), dtype=np.uint16)

        categories = {}

        for i, cat in enumerate(dat["categories"]):
            cat_id = cat["id"]
            cat_name = cat["name"]

            categories[cat_id] = cat_name

        annotations = dat["annotations"]

        for i in range(len(annotations)):
            annotation = annotations[i]

            if "segmentation" in annotation.keys():
                annot = annotation["segmentation"][0]
                category_id = annotation["category_id"]

                cnt = np.array(annot).reshape(-1, 1, 2).astype(np.int32)

                cv2.drawContours(mask, [cnt], contourIdx=-1, color=i + 1, thickness=-1)
                cv2.drawContours(labels, [cnt], contourIdx=-1, color=category_id, thickness=-1, )

            if "nucleoid_segmentation" in annotation.keys():
                nucleoid_annot = annotation["nucleoid_segmentation"][0]

                cnt = (np.array(nucleoid_annot).reshape(-1, 1, 2).astype(np.int32))

                cv2.drawContours(nmask, [cnt], contourIdx=-1, color=i + 1, thickness=-1)

    except:
        mask, nmask, labels = None, None, None

    return mask, nmask, labels


def get_json_path(path):

    path = pathlib.Path(path)
    
    index = path.parts.index('images')
    
    parts = (*path.parts[:index],"json",*path.parts[index+1:])
    
    json_path =  pathlib.Path('').joinpath(*parts)
    json_path = str(json_path.with_suffix('.txt'))
    
    return json_path


def read_tif_meta(path):
    
    try:

        with tifffile.TiffFile(path) as tif:
            metadata = tif.pages[0].tags["ImageDescription"].value
            metadata = json.loads(metadata)
    except:
        metadata = {}
        pass
            
    return metadata


def update_akseg_paths(path, AKSEG_DIRECTORY, USER_INITIAL):

    path = pathlib.Path(path.replace("\\", "/"))
    AKSEG_DIRECTORY = pathlib.Path(AKSEG_DIRECTORY)

    index = path.parts.index(str(USER_INITIAL))
    
    parts = (*AKSEG_DIRECTORY.parts, "Images", *path.parts[index:])
    path = pathlib.Path('').joinpath(*parts)
    
    return path

def get_filemeta(path, current_metadata):
    
    try:
        
        json_path = get_json_path(path)
    
        file_name = os.path.basename(path)
        
        current_time = datetime.datetime.now()
        
        columns = current_metadata.iloc[:].columns.tolist()
        
        if file_name in current_metadata["file_name"].tolist():
            
            new_metadata = dict(current_metadata[current_metadata["file_name"] == file_name].iloc[0])
            
            for column in columns:
                
                if new_metadata[column] == None:
                    
                    img_meta = read_tif_meta(path)
                    
                    new_metadata[column] = query_img_meta(column, img_meta, path)
                
        else:
            
            new_metadata = {}
            
            img_meta = read_tif_meta(path)
            
            for column in columns:
                
                new_metadata[column] = query_img_meta(column, img_meta, path)
            
            
        try:
            
            mask, _, _ = import_coco_json(json_path)
            
            num_segmentations = len(np.unique(mask))

            new_metadata["num_segmentations"] = len(np.unique(mask))
            
            if num_segmentations > 1:
                
                new_metadata["segmented"] = True
                new_metadata["segmentation_curated"] = True
                
            else:
                
                new_metadata["segmented"] = False
                new_metadata["segmentation_curated"] = False
                
        except:
            import traceback
            print(new_metadata["mask_save_path"])
            print(traceback.format_exc())
            pass
            
        new_metadata = pd.DataFrame.from_dict([new_metadata])    
            
        new_metadata = new_metadata[columns]
            
    except:
        import traceback
        print(traceback.format_exc())
        
        new_metadata = None

    return new_metadata
                                 
    
def query_img_meta(key, img_meta, path):
    
    if key in img_meta.keys():
        
        value = img_meta[key]
    
    elif key == "file_name":
        value = os.path.basename(path)
    elif key == "user_meta1":
        value = img_meta["usermeta1"]
    elif key == "user_meta2":
        value = img_meta["usermeta2"]
    elif key == "user_meta3":
        value = img_meta["usermeta3"]
    elif key == "content":
        value = img_meta["image_content"]
    elif key == "source":
        value = img_meta["light_source"]
    elif key == "mounting method":
        value = img_meta["mount"]
    elif key == "treatment time (mins)":
        value = img_meta["treatmenttime"]
    elif key == "antibiotic concentration":
        value = img_meta["abxconcentration"]
    elif key == "segmentation_curated":
        value = img_meta["segmentations_curated"]
    elif key == "label_curated":
        value = img_meta["labels_curated"]
    elif key == "date_uploaded":
        value = datetime.datetime.now()
    elif key == "date_created":
        value = datetime.datetime.now()
    elif key == "date_modified":
        value = datetime.datetime.now()
    elif key == "image_save_path":
        value = path
    elif key == "image_load_path":
        value = None
    elif key == "mask_load_path":
        value = None
    elif key == "mask_save_path":
        value = path.replace("\\images\\","\\masks\\")
    elif key == "label_load_path":
        value = None
    elif key == "label_save_path":
        value = path.replace("\\images\\","\\labels\\")
    elif key == "num_segmentations":
        value = None
    else:
        value = None
        
    return value    
    
    
user_initial = "PT"   
    
akseg_directory = r"\\physics\dfs\DAQ\CondensedMatterGroups\AKGroup\Piers\AKSEG" 

user_metadata_path = os.path.join(akseg_directory, "Images", user_initial, f"{user_initial}_file_metadata.txt")
user_image_directory = os.path.join(akseg_directory, "Images", user_initial, "images")

current_metadata = pd.read_csv(f"{user_initial}_file_metadata.txt", sep=",", low_memory=False)
    
# image_paths = glob(user_image_directory + "\Trillian Nice FOVs\*.tif")


# if __name__ == '__main__':

#     with Pool() as p:
        
#         results = list(tqdm.tqdm(p.imap(partial(
#             get_filemeta,
#             current_metadata=current_metadata), 
#             image_paths), 
#             total=len(image_paths)))
        
#         p.close()
#         p.join()
        
#         results = [dat for dat in results if dat is not None]
        
#         new_metadata = pd.concat(results).reset_index(drop=True)

#         new_metadata["image_save_path"] = new_metadata["image_save_path"].apply(lambda path: update_akseg_paths(path, akseg_directory, user_initial))
#         new_metadata["mask_save_path"] = new_metadata["mask_save_path"].apply(lambda path: update_akseg_paths(path, akseg_directory, user_initial))
#         new_metadata["label_save_path"] = new_metadata["label_save_path"].apply(lambda path: update_akseg_paths(path, akseg_directory, user_initial))
        
#         with open('akseg_metadata.pickle', 'wb') as handle:
#             pickle.dump([current_metadata,new_metadata], handle, protocol=pickle.HIGHEST_PROTOCOL)
#         with open('akseg_metadata.pickle', 'rb') as handle:
#             current_metadata,new_metadata = pickle.load(handle)
        
        
        
#         # metadata = pd.concat([current_metadata,new_metadata])
#         # metadata.drop_duplicates(subset=['akseg_hash'], keep="first", inplace=True)
        
        
#         # current_metadata.to_csv(f"{user_initial}_file_metadata.txt", sep=",", index = False)  
#         # new_metadata.to_csv(user_metadata_path, sep=",", index = False)  
        
    


with open('akseg_metadata.pickle', 'rb') as handle:
    _,new_metadata = pickle.load(handle)

metadata = pd.concat([current_metadata,new_metadata])
metadata.drop_duplicates(subset=['akseg_hash'], keep="first", inplace=True)


metadata.to_csv(user_metadata_path, sep=",", index = False)



