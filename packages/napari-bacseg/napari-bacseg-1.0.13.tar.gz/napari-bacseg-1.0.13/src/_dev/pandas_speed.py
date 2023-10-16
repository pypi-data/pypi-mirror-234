# -*- coding: utf-8 -*-
"""
Created on Thu May  4 09:26:02 2023

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
import matplotlib.pyplot as plt
import time
import dask.dataframe as dd


def extract_list(data, mode = "file"):
    
    data = data.strip("[]").replace("'","").split(", ")
    
    return data




metadata_columns = ["date_uploaded", "date_created", "date_modified", "file_name", "channel", "file_list", "channel_list", "segmentation_file", "segmentation_channel", "akseg_hash",
            "user_initial", "content", "microscope", "modality", "source", "strain", "phenotype", "stain", "stain_target", "antibiotic", "treatment time (mins)", "antibiotic concentration",
            "mounting method", "protocol", "folder", "parent_folder", "num_segmentations", "image_laplacian", "image_focus", "image_debris", "segmented", "labelled", "segmentation_curated",
            "label_curated", "posX", "posY", "posZ", "image_load_path", "image_save_path", "mask_load_path", "mask_save_path", "label_load_path", "label_save_path", ]

required_columns = ["date_uploaded", "date_created", "date_modified","file_list", "channel_list", "segmentation_file", "segmentation_channel", "akseg_hash",
            "user_initial", "content", "microscope", "modality", "source", "strain", "phenotype", "stain", "stain_target", "antibiotic", "treatment time (mins)", "antibiotic concentration",
            "mounting method", "protocol", "folder", "parent_folder", "num_segmentations", "image_laplacian", "image_focus", "image_debris", "segmented", "labelled", "segmentation_curated",
            "label_curated", "posX", "posY", "posZ",]

dtypes = {"image_focus":"int8", "image_debris": "int8", "segmented":bool, "labelled":bool, "segmentation_curated":bool,
          "user_meta1": str, "user_meta2": str, "user_meta3": str, "user_meta4": str, "user_meta5": str, "user_meta6": str}


user_initial = "CF2"

user_metadata_path = os.path.join(r"\\physics\dfs\DAQ\CondensedMatterGroups\AKGroup\Piers\AKSEG\Images", user_initial, f"{user_initial}_file_metadata.txt")





# start_time = time.time()


# user_metadata = pd.read_csv(
#     user_metadata_path,
#     sep=",",
#     low_memory=False,
#     # dtype=dtypes,
#     usecols=metadata_columns)


# print(f"Completed. Duration: {(time.time() - start_time)/60:.2f} minutes.\n")


# with open('metadata_light.pickle', 'wb') as handle:
#     pickle.dump(user_metadata, handle, protocol=pickle.HIGHEST_PROTOCOL)

with open('metadata_light.pickle', 'rb') as handle:
    files = pickle.load(handle)


files["file_list"] = files["file_list"].apply(lambda data: extract_list(data, mode = "file"))
files["channel_list"] = files["channel_list"].apply(lambda data: extract_list(data, mode = "channel"))


files_exploded = files.explode(["file_list", "channel_list"])


column_dict = {col:"first" for col in files.columns if col not in ["segmentation_file","folder", "file_list", "channel_list","akseg_hash"]}


# files_compressed = files_exploded.groupby(["segmentation_file","folder"]).agg(
#     file_list = ("file_list", ",".join),
#     channel_list = ("channel_list", ",".join),
#     akseg_hash = ("akseg_hash", ",".join),
#     **column_dict

# ).reset_index()


files_compressed = files_exploded.groupby(["segmentation_file","folder"]).agg(
    {**{'file_list': lambda x: list(set(x.tolist())),
        'channel_list': lambda x: list(set(x.tolist())),
        'akseg_hash': lambda x: list(set(x.tolist())),
        **column_dict
        }}
    ).reset_index()[required_columns]

files_head = files.head()

memory_usage_files = sum(files.memory_usage(index=False, deep=True).tolist())/8/1e6
memory_usage_files_exploded = sum(files_exploded.memory_usage(index=False, deep=True).tolist())/8/1e6
memory_usage_files_compressed = sum(files_compressed.memory_usage(index=False, deep=True).tolist())/8/1e6


files_compressed_head = files_compressed.head()


