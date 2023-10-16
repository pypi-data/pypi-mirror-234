# -*- coding: utf-8 -*-
"""
Created on Tue Jun 28 15:21:03 2022

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






path = os.path.abspath(r"\\cmwt188\d\Piers\AKSEG CMWT188")

file_paths = glob(path + "*\*\*\*.txt", recursive=False)

file_paths = [path for path in file_paths if "metadata.txt" in path]

user_metadata = pd.DataFrame()

for path in file_paths:
    
    metadata = pd.read_csv(path, sep=",")
    
    if "date_modified" not in metadata.columns.tolist():
            metadata.insert(1, "date_modified",metadata["date_uploaded"])
            metadata.insert(1, "date_created",metadata["date_uploaded"])
            metadata.insert(30, "posX",0)
            metadata.insert(31, "posY",0)
            metadata.insert(32, "posZ",0)
    
    
    if len(user_metadata)==0:
        user_metadata = metadata
    else:
        user_metadata = pd.concat((user_metadata,metadata))


user_metadata = user_metadata[user_metadata["segmentation_file"]!="missing image channel"]

segmentation_files = user_metadata["segmentation_file"].unique()
num_measurements = len(segmentation_files)




























def read_AKSEG_directory(self, path, import_limit=1):

    database_dir = os.path.join(self.database_path, "Images")

    if isinstance(path, list)==False:
        path = [path]

    if len(path)==1:

        path = os.path.abspath(path[0])

        if os.path.isfile(path)==True:
            file_paths = [path]

        else:

            file_paths = glob(path + "*\**\*.tif", recursive=True)
    else:
        file_paths = path

    file_paths = [file for file in file_paths if file.split(".")[-1]=="tif"]

    files = pd.DataFrame(columns=["path",
                                  "folder",
                                  "user_initial",
                                  "file_name",
                                  "channel",
                                  "file_list",
                                  "channel_list",
                                  "segmentation_file",
                                  "segmentation_channel",
                                  "segmented",
                                  "labelled",
                                  "segmentation_curated",
                                  "label_curated",
                                  "posX",
                                  "posY",
                                  "posZ",
                                  "timestamp"])

    for i in range(len(file_paths)):

        path = file_paths[i]
        path = os.path.abspath(path)

        path = os.path.join(database_dir, path.split("\\" + path.split("\\")[-5] + "\\")[-1])

        file_name = path.split("\\")[-1]
        folder = path.split("\\")[-5]

        with tifffile.TiffFile(path) as tif:

            meta = tif.pages[0].tags["ImageDescription"].value

            meta = json.loads(meta)

            user_initial = meta["user_initial"]
            segmentation_channel = meta["segmentation_channel"]
            file_list = meta["file_list"]
            channel = meta["channel"]
            channel_list = meta["channel_list"]
            segmentation_channel = meta["segmentation_channel"]
            segmentation_file = meta["segmentation_file"]
            segmented = meta["segmented"]
            labelled = meta["labelled"]
            segmentations_curated = meta["segmentations_curated"]
            labels_curated = meta["labels_curated"]

            if "posX" in meta.keys():
                posX = meta['posX']
                posY = meta['posX']
                posZ = meta['posX']
            else:
                posX = 0
                posY = 0
                posZ = 0

            if "timestamp" in meta.keys():
                timestamp = meta["timestamp"]
            else:
                timestamp = 0

            data = [path,
                    folder,
                    user_initial,
                    file_name,
                    channel,
                    file_list,
                    channel_list,
                    segmentation_file,
                    segmentation_channel,
                    segmented,
                    labelled,
                    segmentations_curated,
                    labels_curated,
                    posX,
                    posY,
                    posZ,
                    timestamp]

            files.loc[len(files)] = data

    files["file_name"] = files["file_list"]
    files["channel"] = files["channel_list"]

    files = files.explode(["file_name", "channel"]).drop_duplicates("file_name").dropna()

    files["path"] = files.apply(lambda x: (x['path'].replace(os.path.basename(x['path']), "") + x["file_name"]), axis=1)

    files = files[files["segmentation_file"]!="missing image channel"]

    segmentation_files = files["segmentation_file"].unique()
    num_measurements = len(segmentation_files)

    if import_limit=="All":
        import_limit = num_measurements
    else:
        if int(import_limit) > num_measurements:
            import_limit = num_measurements

    files = files[files["segmentation_file"].isin(segmentation_files[:int(import_limit)])]

    channels = files.explode("channel_list")["channel_list"].unique().tolist()

    files.sort_values(by=['posX', 'posY', 'posZ'], ascending=True)

    measurements = files.groupby("segmentation_file")

    return measurements, file_paths, channels