# -*- coding: utf-8 -*-
"""
Created on Fri Jul  8 18:25:22 2022

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
# from napari_bacseg._utils_imagej import read_imagej_file
from skimage import data
from skimage.registration import phase_cross_correlation
from skimage.registration._phase_cross_correlation import _upsampled_dft
from scipy.ndimage import fourier_shift
import scipy
# from napari_bacseg._utils_cellpose import export_cellpose
# from napari_bacseg._utils_oufti import  export_oufti
# from napari_bacseg._utils_imagej import export_imagej
# from napari_bacseg._utils_json import import_coco_json, export_coco_json
import pickle
import xmltodict
import warnings
from astropy.io import fits




def read_xml(paths):
    
    files = {}
    
    for path in paths:

        with open(path) as fd:
            dat = xmltodict.parse(fd.read())["OME"]
            
            image_list = dat["Image"]
    
            if type(image_list)==dict:
                image_list = [image_list]
             
            for i in range(len(image_list)):
                img = image_list[i]
                
                objective_id = int(img["ObjectiveSettings"]["@ID"].split(":")[-1])
                objective_dat = dat["Instrument"]["Objective"][objective_id]
                objective_mag = float(objective_dat["@NominalMagnification"])
                objective_na = float(objective_dat["@LensNA"])
                
                pixel_size = float(img["Pixels"]["@PhysicalSizeX"])
                
                position_index = i
                microscope = "ScanR"
                light_source = "LED"
                
                
                channel_dict = {}
                
                for j in range(len(img["Pixels"]["Channel"])):
                    
                    channel_data = img["Pixels"]["Channel"][j]
                    
                    channel_dict[j] = dict(modality = channel_data["@IlluminationType"],
                                            channel = channel_data["@Name"],
                                            mode = channel_data["@AcquisitionMode"],
                                            well = channel_data["@ID"].split("W")[1].split("P")[0])
                
                primary_channel = ""
                
                for j in range(len(img["Pixels"]["TiffData"])):
                    
                    num_channels = img["Pixels"]["@SizeC"]
                    num_zstack = img["Pixels"]["@SizeZ"]
                    
                    tiff_data = img["Pixels"]["TiffData"][j]
                    
                    file_name = tiff_data["UUID"]["@FileName"]
                    file_path = os.path.abspath(path.replace(os.path.basename(path),file_name))
                    
                    try:
                        plane_data = img["Pixels"]["Plane"][j]
                        exposure_time = plane_data["@ExposureTime"]
                        posX = float(plane_data["@PositionX"])
                        posY = float(plane_data["@PositionY"])
                        posZ = float(plane_data["@PositionZ"])
                        channel_index = int(tiff_data["@FirstC"])
                        time_index = int(tiff_data["@FirstT"])
                        z_index = int(tiff_data["@FirstZ"])
                        channel_dat = channel_dict[channel_index]
                        modality = channel_dat["modality"]
                        channel = channel_dat["channel"]
                        well_index = int(channel_dat["well"])
                    except Exception:
                        well_index = None
                        modality = None
                        channel = None
                        exposure_time = None
                        posX = None
                        posY = None
                        posZ = None
                        exposure_time = None
                        
                    files[file_path] = dict(file_name = file_name,
                                            well_index = well_index,
                                            position_index = position_index,
                                            channel_index = channel_index,
                                            time_index = time_index,
                                            z_index = z_index,
                                            microscope = microscope,
                                            light_source = light_source,
                                            channel = channel,
                                            modality = modality,
                                            pixel_size = pixel_size,
                                            objective_magnification = objective_mag,
                                            objective_na = objective_na,
                                            posX = posX,
                                            posY = posY,
                                            posZ = posZ)

    return files





def read_scanr_directory(path):

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
        
    
    scanR_meta_files = [path.replace(os.path.basename(path),"") for path in file_paths]
    scanR_meta_files = np.unique(scanR_meta_files).tolist()
    scanR_meta_files = [glob(path + "*.ome.xml")[0] for path in scanR_meta_files if len(glob(path + "*.ome.xml")) > 0]
    
    file_info = read_xml(scanR_meta_files)
    
    files = []
    
    for path in file_paths:
        
        try:

            file = file_info[path]
            file["path"] = path
            
            folder = path.split("\\")[-3]
            parent_folder = path.split("\\")[-4]
            
            file["folder"] = folder
            file["parent_folder"] = parent_folder
    
            files.append(file)
            
        except Exception:
            pass
        
    files = pd.DataFrame(files)
    
    num_measurements = len(files.position_index.unique())

    import_limit = 5
    
    if import_limit=="None":
        import_limit = num_measurements
    else:
        if int(import_limit) > num_measurements:
            import_limit = num_measurements
    
    acquisitions = files.position_index.unique()[:int(import_limit)]
    
    files = files[files['position_index'] <= acquisitions[-1]]
    
    measurements = files.groupby(by=['parent_folder','position_index','time_index', "z_index"])
    channels = files["channel"].drop_duplicates().to_list()
    
    channel_num = str(len(files["channel"].unique()))
    
    print("Found " + str(len(measurements)) + " measurments in ScanR Folder(s) with " + channel_num + " channels.")

    return measurements, file_paths, channels, files




path = r"D:\Untreated_timelapse_correctexposure\data"
# path = r"D:\Unlearning Files\220525_ScanR_Agarose_CIP\BurntSlide_001\data"
# file_paths = glob(path + "\*.tif")



measurements, file_paths, channels, files = read_scanr_directory(path)

print(len(measurements))



# xx = files.groupby(['parent_folder','position_index','time_index', "z_index"], as_index=False).size()

# cols = ['parent_folder','position_index','time_index', "z_index"]


# files["count"] = pd.Series(zip(*[files[col].tolist() for col in cols]))
# df = pd.DataFrame(files['count'].value_counts().reset_index())



# measurements = measurements.apply( lambda measurements: measurements.iloc[0:10:1]).reset_index(drop=True)




# measurement = measurements.get_group(list(measurements.groups)[0])














