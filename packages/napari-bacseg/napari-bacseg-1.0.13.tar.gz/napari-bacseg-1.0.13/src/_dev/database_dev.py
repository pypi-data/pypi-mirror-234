# -*- coding: utf-8 -*-
"""
Created on Thu Jul 21 13:57:09 2022

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
import mat4py
import datetime
import json
import matplotlib.pyplot as plt
import hashlib
import time
import pickle

def read_AKSEG_directory(path, import_limit=1):
    
    database_path = r"\\physics\dfs\DAQ\CondensedMatterGroups\AKGroup\Piers\AKSEG"

    database_dir = os.path.join(database_path, "Images")

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



def read_AKSEG_images(measurements, channels):
    
    database_path = r"\\physics\dfs\DAQ\CondensedMatterGroups\AKGroup\Piers\AKSEG"

    imported_images = {}
    iter = 1

    for i in range(len(measurements)):

        measurement = measurements.get_group(list(measurements.groups)[i])

        for j in range(len(channels)):

            channel = channels[j]

            measurement_channels = measurement["channel"].unique()

            if channel in measurement_channels:

                dat = measurement[measurement["channel"]==channel]

                print("loading image[" + str(channel) + "] " + str(i + 1) + " of " + str(len(measurements)))

                file_name = dat["file_name"].item()
                user_initial = dat["user_initial"].item()
                folder = dat["folder"].item()

                path = os.path.join(database_path,"Images",user_initial,"images",folder,file_name)

                image_path = os.path.abspath(path)
                mask_path = os.path.abspath(path.replace("\\images\\","\\masks\\"))
                label_path = os.path.abspath(path.replace("\\images\\","\\labels\\"))

                image = tifffile.imread(image_path)
                mask = tifffile.imread(mask_path)
                label = tifffile.imread(label_path)

                with tifffile.TiffFile(image_path) as tif:
                    try:
                        meta = tif.pages[0].tags["ImageDescription"].value
                        meta = json.loads(meta)
                    except Exception:
                        meta = {}

                meta["import_mode"] = "BacSeg"

            else:

                image = np.zeros((100,100), dtype=np.uint16)
                mask = np.zeros((100,100), dtype=np.uint16)
                label = np.zeros((100,100), dtype=np.uint16)

                meta = {}

                meta["image_name"] = "missing image channel"
                meta["image_path"] = "missing image channel"
                meta["folder"] = None,
                meta["parent_folder"] = None,
                meta["akseg_hash"] = None
                meta["fov_mode"] = None
                meta["import_mode"] = "BacSeg"
                meta["contrast_limit"] = None
                meta["contrast_alpha"] = None
                meta["contrast_beta"] = None
                meta["contrast_gamma"] = None
                meta["dims"] = [image.shape[-1], image.shape[-2]]
                meta["crop"] = [0, image.shape[-2], 0, image.shape[-1]]
                meta["light_source"] = channel

            if channel not in imported_images:
                imported_images[channel] = dict(images=[image], masks=[mask], classes=[label], metadata={i: meta})
            else:
                imported_images[channel]["images"].append(image)
                imported_images[channel]["masks"].append(mask)
                imported_images[channel]["classes"].append(label)
                imported_images[channel]["metadata"][i] = meta


    imported_data = dict(imported_images=imported_images)

    return imported_data

























# with open('database_dev.pickle', 'rb') as handle:
#     measurements, file_paths, channels = pickle.load(handle)



# database_path = r"\\physics\dfs\DAQ\CondensedMatterGroups\AKGroup\Piers\AKSEG"

# imported_images = {}
# iter = 1

# for i in range(len(measurements)):

#     measurement = measurements.get_group(list(measurements.groups)[i])

#     for j in range(len(channels)):

#         channel = channels[j]

#         measurement_channels = measurement["channel"].unique()

#         if channel in measurement_channels:

#             dat = measurement[measurement["channel"]==channel]

#             print("loading image[" + str(channel) + "] " + str(i + 1) + " of " + str(len(measurements)))

#             file_name = dat["file_name"].item()
#             user_initial = dat["user_initial"].item()
#             folder = dat["folder"].item()

#             path = os.path.join(database_path,"Images",user_initial,"images",folder,file_name)

#             image_path = os.path.abspath(path)
#             mask_path = os.path.abspath(path.replace("\\images\\","\\masks\\"))
#             label_path = os.path.abspath(path.replace("\\images\\","\\labels\\"))

#             image = tifffile.imread(image_path)
#             mask = tifffile.imread(mask_path)
#             label = tifffile.imread(label_path)

#             with tifffile.TiffFile(image_path) as tif:
#                 try:
#                     meta = tif.pages[0].tags["ImageDescription"].value
#                     meta = json.loads(meta)
#                 except Exception:
#                     meta = {}

#             meta["import_mode"] = "BacSeg"

#         else:

#             image = np.zeros((100,100), dtype=np.uint16)
#             mask = np.zeros((100,100), dtype=np.uint16)
#             label = np.zeros((100,100), dtype=np.uint16)

#             meta = {}

#             meta["image_name"] = "missing image channel"
#             meta["image_path"] = "missing image channel"
#             meta["folder"] = None,
#             meta["parent_folder"] = None,
#             meta["akseg_hash"] = None
#             meta["fov_mode"] = None
#             meta["import_mode"] = "BacSeg"
#             meta["contrast_limit"] = None
#             meta["contrast_alpha"] = None
#             meta["contrast_beta"] = None
#             meta["contrast_gamma"] = None
#             meta["dims"] = [image.shape[-1], image.shape[-2]]
#             meta["crop"] = [0, image.shape[-2], 0, image.shape[-1]]
#             meta["light_source"] = channel

#         if channel not in imported_images:
#             imported_images[channel] = dict(images=[image], masks=[mask], classes=[label], metadata={i: meta})
#         else:
#             imported_images[channel]["images"].append(image)
#             imported_images[channel]["masks"].append(mask)
#             imported_images[channel]["classes"].append(label)
#             imported_images[channel]["metadata"][i] = meta


# imported_data = dict(imported_images=imported_images)








