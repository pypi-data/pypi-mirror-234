# -*- coding: utf-8 -*-
"""
Created on Thu May 26 13:20:01 2022

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
import pickle
from multiprocessing import Pool
import tqdm
from functools import partial





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
                    file_path = os.path.abspath(path.replace(os.path.basename(path), file_name))

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

                    files[file_path] = dict(file_name=file_name,
                                            well_index=well_index,
                                            position_index=position_index,
                                            position = position_index,
                                            channel_index=channel_index,
                                            time_index=time_index,
                                            z_index=z_index,
                                            microscope=microscope,
                                            light_source=light_source,
                                            channel=channel,
                                            modality=modality,
                                            pixel_size=pixel_size,
                                            objective_magnification=objective_mag,
                                            objective_na=objective_na,
                                            exposure_time = exposure_time,
                                            posX=posX,
                                            posY=posY,
                                            posZ=posZ)

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
            
            folder = path.split("\\")[-4]
            parent_folder = path.split("\\")[-5]
            mounting_method = folder.split("_")[2]
            
            antibiotic_table = {'CIP':'Ciprofloxacin','RIF':'Rifampin','KAN':'Kanamycin',
                                'CIP+ETOH':'Ciprofloxacin','RIF+ETOH':'Rifampin',
                                'KAN+ETOH':'Kanamycin','CARB+ETOH':'Carbenicillin',
                                'WT+ETOH':'N/A',"WT":"N/A"}
            
            antibiotic_code = folder.split("_")[3]
            
            antibiotic = antibiotic_table[antibiotic_code]
            
            file["folder"] = folder
            file["parent_folder"] = parent_folder
            file["user_initial"] = "PT"
            file["microscope"] = "ScanR"
            file["mounting_method"] = mounting_method
            file["zstack"] = int(file["file_name"].split("--")[3].replace("Z",""))
            file["antibiotic"] = antibiotic
    
            files.append(file)
            
        except Exception:
            pass
        
    files = pd.DataFrame(files)

    num_measurements = len(files.position_index.unique())

    import_limit = 'None'

    if import_limit=="None":
        import_limit = num_measurements
    else:
        if int(import_limit) > num_measurements:
            import_limit = num_measurements

    acquisitions = files.position_index.unique()[:int(import_limit)]

    files = files[files['position_index'] <= acquisitions[-1]]

    measurements = files.groupby(by=['parent_folder', 'position_index', 'time_index', "z_index"])
    channels = files["channel"].drop_duplicates().to_list()

    channel_num = str(len(files["channel"].unique()))
    
    return measurements, file_paths, channels, files


def read_nim_directory(path):

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

    file_names = [path.split("\\")[-1] for path in file_paths]

    files = pd.DataFrame(columns=["path",
                                  "file_name",
                                  "folder",
                                  "parent_folder",
                                  "posX",
                                  "posY",
                                  "posZ",
                                  "laser",
                                  "timestamp",
                                  "exposure_time",
                                  "channel",
                                  "microscope",
                                  "mounting_method",
                                  "antibiotic"])

    for i in range(len(file_paths)):
        
        try:

            path = file_paths[i]
            path = os.path.abspath(path)
    
            file_name = path.split("\\")[-1]
            folder = os.path.abspath(path).split("\\")[-4]
            parent_folder = os.path.abspath(path).split("\\")[-5]
            mounting_method = folder.split("_")[2]
            
            antibiotic_table = {'CIP':'Ciprofloxacin','RIF':'Rifampin','KAN':'Kanamycin',
                                'CIP+ETOH':'Ciprofloxacin','RIF+ETOH':'Rifampin',
                                'KAN+ETOH':'Kanamycin','CARB+ETOH':'Carbenicillin',
                                'WT+ETOH':'N/A',"WT":"N/A"}
            
            antibiotic_code = folder.split("_")[3]
            
            antibiotic = antibiotic_table[antibiotic_code]
            
            with tifffile.TiffFile(path) as tif:
    
                tif_tags = {}
                for tag in tif.pages[0].tags.values():
                    name, value = tag.name, tag.value
                    tif_tags[name] = value
                    
            if "ImageDescription" in tif_tags:
                
                metadata = tif_tags["ImageDescription"]
                metadata = json.loads(metadata)
        
                laseractive = metadata["LaserActive"]
                laserpowers = metadata["LaserPowerPercent"]
                laserwavelength_nm = metadata["LaserWavelength_nm"]
                timestamp = metadata["timestamp_us"]
                exposure_time = metadata["Exposure_ms"]
        
                posX, posY, posZ = metadata["StagePos_um"]
        
                if True in laseractive:
                    laseractive = np.array(laseractive, dtype=bool)
                    laserpowers = np.array(laserpowers, dtype=float)
                    laserwavelength_nm = np.array(laserwavelength_nm, dtype=str)
        
                    # finds maximum active power
                    power = laserpowers[laseractive==True].max()
        
                    laser_index = np.where(laserpowers==power)
        
                    laser = laserwavelength_nm[laser_index][0]
                else:
                    laser = "White Light"
        
    
                if metadata["InstrumentSerial"]=='6D699GN6':
                    microscope = 'BIO-NIM'
                elif metadata["InstrumentSerial"]=='2EC5XTUC':
                    microscope = 'JR-NIM'
                elif metadata["InstrumentSerial"]=='Micron':
                    microscope = "Micron-NIM"

                file_name = path.split("\\")[-1]
        
                data = [path, file_name, posX, posY, posZ, laser, timestamp, exposure_time]
        
                files.loc[len(files)] = [path, file_name, folder, parent_folder, posX, posY, posZ, laser, timestamp, exposure_time, laser, microscope, mounting_method, antibiotic]
                
        except Exception:
            print(traceback.format_exc())

    files[["posX", "posY", "posZ"]] = files[["posX", "posY", "posZ"]].round(decimals=1)
    files["posZ"] = files["posZ"]

    files = files.sort_values(by=['posX', 'posY', 'posY', 'timestamp', 'laser'], ascending=True)
    files = files.reset_index(drop=True)
    files["aquisition"] = 0
    files["position"] = 0
    
    files = files[files["laser"]is not "White Light"]

    positions = files[['posX', 'posY']].drop_duplicates()
    channels = files["laser"].drop_duplicates().to_list()

    acquisition = 0
    lasers = []

    for i in range(len(positions)):

        posX = positions["posX"].iloc[i]
        posY = positions["posY"].iloc[i]

        data = files[(files["posX"]==posX) & (files["posY"]==posY)]

        indicies = data.index.values

        for index in indicies:

            laser = files.at[index, 'laser']

            if laser in lasers:

                acquisition += 1
                lasers = [laser]

            else:
                lasers.append(laser)

            files.at[index, 'aquisition'] = acquisition
            files.at[index, 'position'] = i

    num_measurements = len(files.aquisition.unique())

    import_limit = 'None'

    if import_limit=="None":
        import_limit = num_measurements
    else:
        if int(import_limit) > num_measurements:
            import_limit = num_measurements

    acquisitions = files.aquisition.unique()[:int(import_limit)]

    files = files[files['aquisition'] <= acquisitions[-1]]

    files = coerce_nim_zvalues(files)
    
    measurements = files.groupby(by=['posX', 'posY'])
    channels = files["laser"].drop_duplicates().to_list()

    channel_num = str(len(files["laser"].unique()))

    return measurements, file_paths, channels, files

def get_folder(files):

    folder = ""
    parent_folder = ""

    paths = files["path"].tolist()

    if len(paths) > 1:

        paths = np.array([path.split("\\") for path in paths]).T

        for i in range(len(paths)):

            if len(set(paths[i]))!=1:
                folder = str(paths[i - 1][0])
                parent_folder = str(paths[i - 2][0])

                break

    else:

        folder = paths[0].split("\\")[-2]
        parent_folder = paths[0].split("\\")[-3]

    return folder, parent_folder


def read_image_file(path, multiframe_mode = 2, crop_mode = 3):
    
    image_name = os.path.basename(path)

    if os.path.splitext(image_name)[1]=='.fits':

        with fits.open(path) as hdul:
            image = hdul[0].data
            metadata = {}
    else:

        with tifffile.TiffFile(path) as tif:
            try:
                metadata = tif.pages[0].tags["ImageDescription"].value
                metadata = json.loads(metadata)
            except Exception:
                metadata = {}

        image = tifffile.imread(path)

    image = crop_image(image, crop_mode)

    image = get_frame(image, multiframe_mode)
    
    image = rescale_image(image)

    folder = os.path.abspath(path).split("\\")[-2]
    parent_folder = os.path.abspath(path).split("\\")[-3]
    
    image_laplacian = int(cv2.Laplacian(image, cv2.CV_64F).var())
    

    thresh_image = normalize99(image)
    thresh_image = (rescale01(thresh_image)*255).astype(np.uint8)
    
    (T, thresh) = cv2.threshold(thresh_image, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)

    image_laplacian = int(cv2.Laplacian(image[thresh!=0], cv2.CV_64F).var())
    
    metadata["image_name"] = image_name
    metadata["channel"] = None
    metadata["segmentation_file"] = None
    metadata["segmentation_channel"] = None
    metadata["image_path"] = path
    metadata["mask_name"] = None
    metadata["mask_path"] = None
    metadata["label_name"] = None
    metadata["label_path"] = None
    metadata["crop_mode"] = 3
    metadata["multiframe_mode"] = 2
    metadata["folder"] = folder
    metadata["parent_folder"] = parent_folder
    metadata["dims"] = [image.shape[-1], image.shape[-2]]
    metadata["crop"] = [0, image.shape[-2], 0, image.shape[-1]]
    metadata["image_laplacian"] = image_laplacian

    return image, metadata, image_laplacian
                
         
     
      
def get_frame(img, multiframe_mode):

    if len(img.shape) > 2:

        if multiframe_mode==0:

            img = img[0,:,:]

        elif multiframe_mode==1:

            img = np.max(img, axis=0)

        elif multiframe_mode==2:

            img = np.mean(img, axis=0).astype(np.uint16)

        elif multiframe_mode==3:

            img = np.sum(img, axis=0)
            
        elif multiframe_mode==4:

            img = img[:10,:,:]
            img = np.mean(img, axis=0).astype(np.uint16) 
            
    return img

def crop_image(img, crop_mode=0):

    if crop_mode!=0:

        if len(img.shape) > 2:
            imgL = img[:,:,:img.shape[-1] // 2]
            imgR = img[:,:, img.shape[-1] // 2:]
        else:
            imgL = img[:,:img.shape[-1] // 2]
            imgR = img[:, img.shape[-1] // 2:]

        if crop_mode==1:
            img = imgL
        if crop_mode==2:
            img = imgR

        if crop_mode==3:
            if np.mean(imgL) > np.mean(imgR):
                img = imgL
            else:
                img = imgR

    return img

def rescale_image(image, precision="int16"):

    precision_dict = {"int8": np.uint8, "int16": np.uint16, "int32": np.uint32, "native": image.dtype}

    dtype = precision_dict[precision]

    if "int" in str(dtype):
        max_value = np.iinfo(dtype).max - 1
    else:
        max_value = np.finfo(dtype).max - 1

    if precision!="native":
        image = ((image - np.min(image)) / np.max(image)) * max_value
        image = image.astype(dtype)

    return image

def find_nearest(array, value):
    array = np.asarray(array)
    idx = (np.abs(array - value)).argmin()
    return array[idx]

def coerce_nim_zvalues(nim_files):
    
    for position in nim_files["position"].unique():
        
        data = nim_files[nim_files["position"]==position]
        
        indicies = data.index.values
        
        true_z_list = data['posZ'].value_counts().sort_values(ascending=False).iloc[:3].index.tolist()
        
        current_z_list = data['posZ'].tolist()
        
        new_z_list = [find_nearest(true_z_list,z) for z in current_z_list]
        
        nim_files.loc[nim_files['position']==position, 'posZ'] = new_z_list
        
    return nim_files



def find_focus_position(measurement):

    exposure_time = measurement["exposure_time"].unique().max()
    
    dat = measurement[(measurement["exposure_time"]==exposure_time) & (measurement["channel"].isin(["Cy3","473", "532"]))]
    
    paths = dat["path"].tolist()
    zlist = dat["posZ"].tolist()
    
    image, metadata, image_laplacian = zip(*[read_image_file(path) for path in paths])
    
    image, metadata, zlist, image_laplacian_sorted = zip(*sorted(zip(image, metadata, zlist, image_laplacian), key=lambda x: x[-1]))
    
    focus_index = np.argmax(image_laplacian_sorted)
    
    z_focused = zlist[0]
    
    z_blurred = zlist[-1]
        
    return [z_focused, z_blurred]
    

def sort_fovs(fovs, mode = 'NIM'):

    files = pd.DataFrame()
    
    for i in range(len(fovs)):
        
        try:
        
            fov = fovs.get_group(list(fovs.groups)[i]).copy()
            
            exposure_list = fov["exposure_time"].unique().tolist()
            
            fov["short_exposure"] = 'False'
            fov["blurred"] = 'N/A'
            
            fov.loc[fov["exposure_time"]==min(exposure_list), "short_exposure"] = 'True'
            
            if mode=='NIM':
                
                focus_list = fov["posZ"].unique().tolist()
                
                focus_list = [focus_list[0]] + [focus_list[-1]]
                
                # fov = fov[fov["posZ"].isin(focus_list)]
                
                fov.loc[fov["posZ"]==focus_list[1], "blurred"] = 'True'
                fov.loc[fov["posZ"]==focus_list[0], "blurred"] = 'False'
                

            if mode=="ScanR":
                
                if 'Agarose' in fov["mounting_method"].unique().tolist():
                    
                    # fov = fov[fov["zstack"].isin([1,3])]
                    fov.loc[fov["zstack"]==2, "blurred"] = 'False'
                    fov.loc[fov["zstack"]==0, "blurred"] = 'True'
                    
        
                if 'Chitosan' in fov["mounting_method"].unique().tolist():
                    
                    # fov = fov[fov["zstack"].isin([1,3])]
                    fov.loc[fov["zstack"]==2, "blurred"] = 'False'
                    fov.loc[fov["zstack"]==4, "blurred"] = 'True'
                    
                    
            if mode=="Troodos":
                
                fov["blurred"] = 'False'
                
            
            if len(files)==0:
                
                files = fov
                
            else:
                
                files = pd.concat([files, fov])
                
        except Exception:
            print(traceback.format_exc())
            pass
            
    files = files.reset_index(drop=True)
    
    measurements = files.groupby(by=['folder','position',"short_exposure","blurred", "posZ"])
    
    return measurements, files
    

def normalize99(X):
    """ normalize image so 0.0==0.01st percentile and 1.0==99.99th percentile """
    
    if np.max(X) > 0:
        
        X = X.copy()
        v_min, v_max = np.percentile(X[X!=0], (0.01, 99.99))
        X = exposure.rescale_intensity(X, in_range=(v_min, v_max))
        
    return X

def rescale01(x):
    """ normalize image from 0 to 1 """
    
    if np.max(x) > 0:
        
        x = (x - np.min(x)) / (np.max(x) - np.min(x))
        
    return x

def get_histogram(image, bins):
    """calculates and returns histogram"""

    # array with size of bins, set to zeros
    histogram = np.zeros(bins)

    # loop through pixels and sum up counts of pixels

    for pixel in image:
        try:
            histogram[pixel] += 1
        except Exception:
            pass

    return histogram


def cumsum(a):
    """cumulative sum function"""

    a = iter(a)
    b = [next(a)]
    for i in a:
        b.append(b[-1] + i)
    return np.array(b)

def autocontrast_values(image, clip_hist_percent=0.001):

    # calculate histogram
    hist, bin_edges = np.histogram(image, bins=(2 ** 16) - 1)
    hist_size = len(hist)

    # calculate cumulative distribution from the histogram
    accumulator = cumsum(hist)

    # Locate points to clip
    maximum = accumulator[-1]
    clip_hist_percent *= (maximum / 100.0)
    clip_hist_percent /= 2.0

    # Locate left cut
    minimum_gray = 0
    try:
        while accumulator[minimum_gray] < clip_hist_percent:
            minimum_gray += 1
    except Exception:
        pass

    # Locate right cut
    maximum_gray = hist_size - 1
    try:
        while accumulator[maximum_gray] >= (maximum - clip_hist_percent):
            maximum_gray -= 1
    except Exception:
        pass

    # Calculate alpha and beta values
    alpha = 255 / (maximum_gray - minimum_gray)
    beta = -minimum_gray * alpha

    # calculate gamma value
    img = cv2.convertScaleAbs(image, alpha=alpha, beta=beta)
    mid = 0.5
    mean = np.mean(img)
    gamma = np.log(mid * 255) / np.log(mean)

    if gamma > 2:
        gamma = 2
    if gamma < 0.2:
        gamma = 0.2

    if maximum_gray > minimum_gray:
        contrast_limit = [minimum_gray, maximum_gray]
    else:
        contrast_limit = [np.min(image),np.max(image)]

    return contrast_limit, alpha, beta, gamma


def get_hash(img_path):

    with open(img_path, "rb") as f:
        bytes = f.read()  # read entire file as bytes

        return hashlib.sha256(bytes).hexdigest()

def export_coco_json(image_name, image, mask, label, file_path):

    file_path = os.path.splitext(file_path)[0] + ".txt"

    info = {"description": "COCO 2017 Dataset",
            "url": "http://cocodataset.org",
            "version": "1.0",
            "year": datetime.datetime.now().year,
            "contributor": "COCO Consortium",
            "date_created": datetime.datetime.now().strftime("%d/%m/%y")}

    categories = [{"supercategory": "cell", "id": 1, "name": "single"},
                  {"supercategory": "cell", "id": 2, "name": "dividing"},
                  {"supercategory": "cell", "id": 3, "name": "divided"},
                  {"supercategory": "cell", "id": 4, "name": "vertical"},
                  {"supercategory": "cell", "id": 5, "name": "broken"},
                  {"supercategory": "cell", "id": 6, "name": "edge"}]

    licenses = [{"url": "https://creativecommons.org/licenses/by-nc-nd/4.0/",
                 "id": 1,
                 "name": "Attribution-NonCommercial-NoDerivatives 4.0 International"}]

    height, width = image.shape[-2], image.shape[-1]

    images = [{"license": 1,
               "file_name": image_name,
               "coco_url": "",
               "height": height,
               "width": width,
               "date_captured": "",
               "flickr_url": "",
               "id": 0
               }]

    mask_ids = np.unique(mask)

    annotations = []

    for j in range(len(mask_ids)):

        if j!=0:

            try:
                cnt_mask = mask.copy()

                cnt_mask[cnt_mask!=j] = 0

                contours, _ = cv2.findContours(cnt_mask.astype(np.uint8),
                                               cv2.RETR_EXTERNAL,
                                               cv2.CHAIN_APPROX_NONE)
                cnt = contours[0]

                # cnt coco bounding box
                x, y, w, h = cv2.boundingRect(cnt)
                y1, y2, x1, x2 = y, (y + h), x, (x + w)
                coco_BBOX = [x1, y1, h, w]

                # cnt area
                area = cv2.contourArea(cnt)

                segmentation = cnt.reshape(-1, 1).flatten()

                cnt_labels = np.unique(label[cnt_mask!=0])

                if len(cnt_labels)==0:

                    cnt_label = 1

                else:
                    cnt_label = int(cnt_labels[0])

                annotation = {"segmentation": [segmentation.tolist()],
                              "area": area,
                              "iscrowd": 0,
                              "image_id": 0,
                              "bbox": coco_BBOX,
                              "category_id": cnt_label,
                              "id": j
                              }

                annotations.append(annotation)

            except Exception:
                pass

    annotation = {"info": info,
                  "licenses": licenses,
                  "images": images,
                  "annotations": annotations,
                  "categories": categories
                  }

    with open(file_path, "w") as f:
        json.dump(annotation, f)

    return annotation




def move_files(i, measurements):
    
    try:
        
        measurement = measurements.get_group(list(measurements.groups)[i])

        channels = measurement["channel"].tolist()
        channels = [str(channel) for channel in channels]
        
        channel_list = []
        file_list = []
        file_list_copy = file_list
        segChannel = ''
        segmentation_file = ''
        mask = []
            
        for channel in channels:
        
            dat = measurement[measurement["channel"]ischannel]
            path = dat["path"].item()
            file_name = os.path.basename(path)
            
            if channel in ["Cy3","Cy3-2","473", "532"]:
                segChannel = channel
                segmentation_file = file_name
            
            file_list.append(file_name)
            channel_list.append(channel)
        
        for j in range(len(channels)):
        
            channel = channels[j]
        
            if channel in channels and segmentation_file!='': 
                
                dat = measurement[measurement["channel"]ischannel]
          
                path = dat["path"].item()
                file_name = dat["file_name"].item()
                folder = dat["folder"].item()
                parent_folder = dat["parent_folder"].item()
                user_initial = 'PT'
                short_exposure = dat["short_exposure"].item()
                blurred = dat["blurred"].item()
                mounting_method = dat["mounting_method"].item()
                microscope = dat["microscope"].item()
                akseg_hash = get_hash(path)
                
                if microscope=="ScanR":
                    img, meta, _ = read_image_file(path, multiframe_mode = 2, crop_mode = 0)
                    
                if 'NIM' in microscope:
                    
                    if short_exposure=='True':
                        
                        img, meta, _ = read_image_file(path, multiframe_mode = 0, crop_mode = 3)
                        
                    else:
                        
                        img, meta, _ = read_image_file(path, multiframe_mode = 2, crop_mode = 3)
                        
                if 'Troodos' in microscope:
                    
                    extension = "." + file_name.split(".")[-1]
                    
                    if short_exposure=='True':
                        
                        img, meta, _ = read_image_file(path, multiframe_mode = 4, crop_mode = 0)
                        path = path.replace(".fits","_SE.tif")
                        akseg_hash = akseg_hash+"SE"
                        file_name = os.path.basename(path)
                        file_list = [file.replace(extension,"_SE.tif") for file in file_list_copy]
                        segmentation_file = segmentation_file.replace(extension,"_SE.tif")
                    else:
                        
                        img, meta, _ = read_image_file(path, multiframe_mode = 2, crop_mode = 0)
                        path = path.replace(".fits","_LE.tif")
                        akseg_hash = akseg_hash+"LE"
                        file_name = os.path.basename(path)
                        file_list = [file.replace(extension,"_LE.tif") for file in file_list_copy]
                        segmentation_file = segmentation_file.replace(extension,"_LE.tif")

                if "CIP" in folder:
                    antibiotic = 'Ciprofloxacin'
                    treatment_time ='30min'
                else:
                    antibiotic = 'None'
                    treatment_time =''
                    
                mask = np.zeros(img.shape,dtype=np.uint16)
                label = np.zeros(mask.shape,dtype=np.uint16)
                    
                contrast_limit, alpha, beta, gamma = autocontrast_values(img, clip_hist_percent=1)
                

                meta["image_name"] = file_name
                meta["file_name"] = file_name
                meta["image_path"] = path
                meta["folder"] = folder
                meta["parent_folder"] = parent_folder
                meta["akseg_hash"] = akseg_hash
                meta["nim_laser_mode"] = "All"
                meta["nim_multiframe_mode"] = "Average Frames"
                meta["nim_channel_mode"] = "Brightest Channel"
                meta["import_mode"] = "NIM"
                meta["contrast_limit"] = contrast_limit
                meta["contrast_alpha"] = alpha
                meta["contrast_beta"] = beta
                meta["contrast_gamma"] = gamma
                meta["dims"] = [img.shape[-1], img.shape[-2]]
                meta["crop"] = [0, img.shape[-2], 0, img.shape[-1]]
                meta["user_initial"] = 'PT'
                meta["image_content"]= 'E.Coli MG1655'
                meta['antibiotic'] = antibiotic
                meta["treatmenttime"] = treatment_time
                meta["abxconcentration"] = ''
                meta["mount"] = mounting_method
                meta["protocol"] = ''
                meta["segmented"] = False
                meta["labelled"] = False
                meta["segmentations_curated"] = False
                meta["labels_curated"] = False
                meta["segmentations_ground_truth"] = False
                meta["labels_curated_ground_truth"] = False
                meta["file_list"] = file_list
                meta["layer_list"] = channel_list
                meta["channel_list"] = channel_list
                meta["channel"] = channel
                meta["segmentation_channel"] = segChannel
                meta["segmentation_file"] = segmentation_file
                meta["stain"] = "N/A"
                meta["modality"] = 'Epifluorescence'
                meta['microscope'] = microscope
                
                usermeta1 = 'Unlearning Paper'
                
                if short_exposure=='True':
                    usermeta2 = 'short exposure'
                elif short_exposure=='False':
                    usermeta2 = 'normal exposure'
                else:
                    usermeta2 = ''
                    
                if blurred=='True':
                    usermeta3 = 'blurred'
                elif blurred=='False':
                    usermeta3 = 'focused'
                else:
                    usermeta3 = ''
                    
                if microscope=="ScanR":
                    meta["light_source"] = "LED"
                elif "NIM" in microscope:
                    meta["light_source"] = channel
                else:
                    meta["light_source"] = ''
                    
                meta["usermeta1"] = usermeta1
                meta["usermeta2"] = usermeta2
                meta["usermeta3"] = usermeta3
            
                image_path = os.path.abspath(r"\\physics\dfs\DAQ\CondensedMatterGroups\AKGroup\Piers\AKSEG\Images" + r"\\" + user_initial + "\\images\\" + folder + "\\")
                mask_path = os.path.abspath(r"\\physics\dfs\DAQ\CondensedMatterGroups\AKGroup\Piers\AKSEG\Images" +  r"\\" + user_initial + "\\masks\\" + folder + "\\")
                label_path = os.path.abspath(r"\\physics\dfs\DAQ\CondensedMatterGroups\AKGroup\Piers\AKSEG\Images" +  r"\\" + user_initial + "\\labels\\" + folder + "\\")
                json_path = os.path.abspath(r"\\physics\dfs\DAQ\CondensedMatterGroups\AKGroup\Piers\AKSEG\Images" +  r"\\" + user_initial + "\\json\\" + folder + "\\")

        
                if os.path.exists(image_path)==False:
                    os.makedirs(image_path)
            
                if os.path.exists(mask_path)==False:
                    os.makedirs(mask_path)
                    
                if os.path.exists(label_path)==False:
                    os.makedirs(label_path)
            
                if os.path.exists(json_path)==False:
                    os.makedirs(json_path)
        
                image_path = os.path.abspath(image_path + "\\" +  file_name)
                mask_path = os.path.abspath(mask_path + "\\" +  file_name)
                label_path = os.path.abspath(label_path + "\\" +  file_name)
                json_path = os.path.abspath(json_path + "\\" +  file_name)
                
                print(image_path)
                
                tifffile.imwrite(image_path, img, metadata=meta)
                tifffile.imwrite(mask_path, mask, metadata=meta)
                tifffile.imwrite(label_path, label, metadata=meta)
            
                export_coco_json(file_name, img, mask, label, json_path)
                
                date_uploaded = datetime.datetime.now()
                
                file_metadata = [date_uploaded,
                                  file_name,
                                  meta["channel"],
                                  meta["file_list"],
                                  meta["channel_list"],
                                  meta["segmentation_file"],
                                  meta["segmentation_channel"],
                                  meta["akseg_hash"],
                                  meta["user_initial"],
                                  meta["image_content"],
                                  meta["microscope"],
                                  meta["modality"],
                                  meta["light_source"],
                                  meta["stain"],
                                  meta["antibiotic"],
                                  meta["treatmenttime"],
                                  meta["abxconcentration"],
                                  meta["mount"],
                                  meta["protocol"],
                                  meta["usermeta1"],
                                  meta["usermeta2"],
                                  meta["usermeta3"],
                                  meta["folder"],
                                  meta["parent_folder"],
                                  meta["segmented"],
                                  meta["labelled"],
                                  meta["segmentations_curated"],
                                  meta["labels_curated"],
                                  meta["segmentations_ground_truth"],
                                  meta["labels_curated_ground_truth"],
                                  meta["image_path"],
                                  image_path,
                                  mask_path,
                                  mask_path,
                                  label_path,
                                  label_path]
                
    except Exception:
        print(traceback.format_exc())

    return


         
def read_troodos_directory(paths):

    files = []
    
    for path in paths:
        
        file = {}
        
        file_name = os.path.basename(path)
        
        folder = path.split("\\")[-2]
        parent_folder = path.split("\\")[-3]
        mounting_method = folder.split("_")[2]
        
        antibiotic_table = {'CIP':'Ciprofloxacin','RIF':'Rifampin','KAN':'Kanamycin',
                            'CIP+ETOH':'Ciprofloxacin','RIF+ETOH':'Rifampin',
                            'KAN+ETOH':'Kanamycin','CARB+ETOH':'Carbenicillin',
                            'WT+ETOH':'N/A',"WT":"N/A"}
        
        antibiotic_code = folder.split("_")[3]
        
        antibiotic = antibiotic_table[antibiotic_code]
        
    
        file["file_name"] = file_name
        file["path"] = path
        file["folder"] = folder
        file["parent_folder"] = parent_folder
        file["user_initial"] = "PT"
        file["microscope"] = "Troodos"
        file["mounting_method"] = mounting_method
        file["channel"] = ""
        file["exposure_time"] = 0.03
        file["posZ"] = 0
        file["antibiotic"] = antibiotic
        
        files.append(file)
    
    files = pd.DataFrame(files)
    
    for folder in files.folder.unique():
        
        channels = ["Bright Field","405","473"]
        
        data = files[files["folder"]==folder]
        
        positions = [i for i in range(len(data)//3) for j in range(3)]
        
        indicies = data.index.values
        
        channels = channels * int(len(files[files["folder"]isfolder])/3)
        
        files.loc[indicies, "channel"] = channels
        files.loc[indicies, "position"] = positions
        
        
    for i in range(len(files)):
    
        data = files.iloc[i]  
        
        if data["channel"]=="Bright Field":
            
            files.loc[i,"modality"] = "Bright Field"
            files.loc[i,"light_source"] = "White Light"
        else:
            
            files.loc[i, "modality"] = "Epifluorescence"
            files.loc[i,"light_source"] = data["channel"]
    
    files_long = files.copy()
    
    files["exposure_time"] = files["exposure_time"]*100 
    
    files = pd.concat((files,files_long))
    
    measurements = files.groupby(by=['folder', 'position'])
    
    return measurements, files
     
def get_AMR_measurements(files, blurred = "False", short_exposure = "False", microscope = "BIO-NIM", mounting_method = "Agarose"):

    files = files[(files["blurred"]==blurred) & (files["short_exposure"]==short_exposure) & (files["mounting_method"]==mounting_method) & (files["microscope"]==microscope)]
    
    measurements = files.groupby(by=['folder', 'position'])
    
    return measurements, files


# path = r"D:\Unlearning Files\220525_ScanR_Agarose_CIP"
# path = r"D:\Unlearning Files\220523_MICRON-NIM_Agarose_CIP"
# path = r"D:\Unlearning Files"


# if isinstance(path, list)==False:
#     path = [path]

# if len(path)==1:

#     path = os.path.abspath(path[0])

#     if os.path.isfile(path)==True:
#         file_paths = [path]

#     else:

#         file_paths = glob(path + "*\**\*.tif", recursive=True)
# else:
#     file_paths = path
    
# file_paths = file_paths + glob(r"D:\Unlearning Files" + "*\**\*.fits", recursive=True)

# with open('file_paths.pickle', 'wb') as handle:
#     pickle.dump(file_paths, handle, protocol=pickle.HIGHEST_PROTOCOL)

with open('file_paths.pickle', 'rb') as handle:
    file_paths = pickle.load(handle)

# nim_file_paths = [path for path in file_paths if "NIM" in path.split("\\")[2]]
# scanr_file_paths = [path for path in file_paths if "ScanR" in path.split("\\")[2]]
# troodos_file_paths = [path for path in file_paths if "Troodos" in path.split("\\")[2]]

# nim_measurements, file_paths, channels, nim_files = read_nim_directory(nim_file_paths)
# scanr_measurements, file_paths, channels, scanr_files = read_scanr_directory(scanr_file_paths)
# troodos_measurements, troodos_files = read_troodos_directory(troodos_file_paths)

# nim_measurements, nim_files = sort_fovs(nim_measurements, mode = 'NIM')
# scanr_measurements, scanr_files = sort_fovs(scanr_measurements, mode = 'ScanR')
# troodos_measurements, troodos_files = sort_fovs(troodos_measurements, mode = 'Troodos')


# with open('measurements.pickle', 'wb') as handle:
#     pickle.dump([nim_measurements,scanr_measurements, nim_files, scanr_files, troodos_measurements, troodos_files], handle, protocol=pickle.HIGHEST_PROTOCOL)

with open('measurements.pickle', 'rb') as handle:
    nim_measurements,scanr_measurements, nim_files, scanr_files, troodos_measurements, troodos_files = pickle.load(handle)



# measurement = scanr_measurements.get_group(list(scanr_measurements.groups)[0])
# move_files(0, scanr_measurements)











def export_AMR_images(measurements,i = 0, directory = "AMR_Images/"):
    
    try:
    
        measurement = measurements.get_group(list(measurements.groups)[i])
        
        channels = measurement["channel"].tolist()
        channels = [str(channel) for channel in channels]
        
        channel_list = []
        file_list = []
        file_list_copy = file_list
        segChannel = ''
        segmentation_file = ''
        mask = []
        
        if "Bright Field" in channels:
            
            channels.remove("Bright Field")
            
        for channel in channels:
        
            dat = measurement[measurement["channel"]ischannel]
            path = dat["path"].item()
            file_name = os.path.basename(path)
            
            if channel in ["Cy3","Cy3-2","473", "532"]:
                segChannel = channel
                segmentation_file = file_name
            else:
        
                file_list.append(file_name)
                channel_list.append(channel)
                
            
        channel_list.insert(0, segChannel)
        file_list.insert(0,segmentation_file)
        
        images = []
        
        for j in range(len(channel_list)):
        
            channel = channel_list[j]
        
            if channel in channel_list and segmentation_file!='': 
                
                dat = measurement[measurement["channel"]ischannel]
          
                path = dat["path"].item()
                file_name = dat["file_name"].item()
                folder = dat["folder"].item()
                parent_folder = dat["parent_folder"].item()
                user_initial = 'PT'
                short_exposure = dat["short_exposure"].item()
                blurred = dat["blurred"].item()
                mounting_method = dat["mounting_method"].item()
                microscope = dat["microscope"].item()
                akseg_hash = get_hash(path)
                
            
                if microscope=="ScanR":
                    img, meta, _ = read_image_file(path, multiframe_mode = 2, crop_mode = 0)
                    
                if 'NIM' in microscope:
                    
                    if short_exposure=='True':
                        
                        img, meta, _ = read_image_file(path, multiframe_mode = 0, crop_mode = 3)
                        
                    else:
                        
                        img, meta, _ = read_image_file(path, multiframe_mode = 2, crop_mode = 3)
                        
                if 'Troodos' in microscope:
                    
                    extension = "." + file_name.split(".")[-1]
                    
                    if short_exposure=='True':
                        
                        img, meta, _ = read_image_file(path, multiframe_mode = 4, crop_mode = 0)
                        
                    else:
                        
                        img, meta, _ = read_image_file(path, multiframe_mode = 2, crop_mode = 0)
        
        
                img = normalize99(img)
                img = rescale01(img)*255
                
                images.append(img)
        
                
        if len(images)!=0:
            
            if len(images)==2:
                
                images.append(np.zeros_like(images[0]))
            
            image = np.stack(images,axis=-1).astype(np.uint8)
            
            export_name = [microscope,mounting_method,file_name]
            
            export_name = "_".join(export_name)
            
            export_path = os.path.join(directory,export_name)
            
            if ".fits" in export_path:
                
                export_path = export_path.replace(".fits",".tif")
            
            tifffile.imwrite(export_path, image)
            
    except Exception:
        pass

        
    
    


 
    

# measurements, files = get_AMR_measurements(nim_files, microscope = "Micron-NIM", mounting_method="Agarose")

# for i in range(10):
#     image = export_AMR_images(measurements, i)   
    
# measurements, files = get_AMR_measurements(nim_files, microscope = "Micron-NIM", mounting_method="Chitosan")

# for i in range(10):
#     image = export_AMR_images(measurements, i)   
    
# measurements, files = get_AMR_measurements(nim_files, microscope = "BIO-NIM", mounting_method="Agarose")

# for i in range(10):
#     image = export_AMR_images(measurements, i)   
    
# measurements, files = get_AMR_measurements(nim_files, microscope = "BIO-NIM", mounting_method="Chitosan")

# for i in range(10):
#     image = export_AMR_images(measurements, i)   
    
# measurements, files = get_AMR_measurements(nim_files, microscope = "JR-NIM", mounting_method="Agarose")

# for i in range(10):
#     image = export_AMR_images(measurements, i)   
    
# measurements, files = get_AMR_measurements(nim_files, microscope = "JR-NIM", mounting_method="Chitosan")

# for i in range(10):
#     image = export_AMR_images(measurements, i)   
    
# measurements, files = get_AMR_measurements(scanr_files, microscope = "ScanR", mounting_method="Chitosan")

# for i in range(10):
#     image = export_AMR_images(measurements, i)   
    
# measurements, files = get_AMR_measurements(scanr_files, microscope = "ScanR", mounting_method="Agarose")

# for i in range(10):
#     image = export_AMR_images(measurements, i)   
    
# measurements, files = get_AMR_measurements(troodos_files, microscope = "Troodos", mounting_method="Chitosan")

# for i in range(10):
#     image = export_AMR_images(measurements, i)   
    
# measurements, files = get_AMR_measurements(troodos_files, microscope = "Troodos", mounting_method="Agarose")

# for i in range(10):
    
#     image = export_AMR_images(measurements, i)   
    






# if __name__=='__main__':
    
#     measurements = scanr_measurements
    
#     mnum = np.arange(len(measurements))
    
#     with Pool() as p:
        
#         d = list(tqdm.tqdm(p.imap(partial(move_files, measurements=measurements),mnum), total=len(mnum)))
#         p.close()
#         p.join()


# if __name__=='__main__':
    
#     measurements = nim_measurements
    
#     mnum = np.arange(len(measurements))
    
#     with Pool() as p:
        
#         d = list(tqdm.tqdm(p.imap(partial(move_files, measurements=measurements),mnum), total=len(mnum)))
#         p.close()
#         p.join()



if __name__=='__main__':
    
    measurements = troodos_measurements
    
    # move_files(0, measurements)
        
    mnum = np.arange(len(measurements))
    
    with Pool() as p:
        
        d = list(tqdm.tqdm(p.imap(partial(move_files, measurements=measurements),mnum), total=len(mnum)))
        p.close()
        p.join()




















# measurements = None

# for i in range(len(nim_measurements)):

#     fov = scanr_measurements.get_group(list(scanr_measurements.groups)[i]).reset_index(drop=True)
    
#     # if fov["position"]==0:
    
#     if measurements==None:
        
#         measurements = fov
        
#     else:
        
#         measurements = pd.concat((measurements,fov))
        
        
# measurements = scanr_measurements.get_group(list(scanr_measurements.groups)[0])
        










# measurements = measurements[(measurements["position"]==1) & (measurements["parent_folder"]=="20220524_220524_BIO-NIM_Agarose_CIP")]

# image = measurements[(measurements["blurred"]==False) &
#                             (measurements["short_exposure"]==True) &
#                             (measurements["channel"].isin(["473","532","Cy3","Cy3-2"])isFalse)]["path"].item()

# image = tifffile.imread(image)

# image_laplacian = int(cv2.Laplacian(image[0:200,0:200], cv2.CV_64F).var())


# print(image_laplacian)

# image = np.mean(image,0)

# plt.imshow(image[0:200,0:200])
# plt.show()







# nim_fov = nim_measurements.get_group(list(nim_measurements.groups)[0])
# scanr_fov = scanr_measurements.get_group(list(scanr_measurements.groups)[0])




# measurements = pd.DataFrame()

# for i in range(1):
    
#     fov = nim_measurements.get_group(list(nim_measurements.groups)[i])
    
#     exposure_list = fov["exposure_time"].unique().tolist()
#     focus_list = find_focus_position(fov)
    
#     fov = fov[fov["posZ"].isin(focus_list)]
    
#     fov["short_exposure"] = False
#     fov.loc[fov["exposure_time"]==max(exposure_list), "short_exposure"] = True
    
#     fov["blurred"] = False
#     fov.loc[fov["posZ"]==focus_list[0], "blurred"] = True

#     if len(measurements)==0:
        
#         measurements = fov
        
#     else:
        
#         measurements = pd.concat([measurements, fov])
        
# measurements = measurements.reset_index(drop=True)

# measurements = measurements.groupby(by=['parent_folder','position',"short_exposure","blurred"])










# fov = nim_measurements.get_group(list(nim_measurements.groups)[0])

        
    
    # for i in range(len(positions)):

    #     posX = positions["posX"].iloc[i]
    #     posY = positions["posY"].iloc[i]

    #     data = files[(files["posX"]==posX) & (files["posY"]==posY)]

    #     indicies = data.index.values

    #     for index in indicies:

    #         laser = files.at[index, 'laser']

    #         if laser in lasers:

    #             acquisition += 1
    #             lasers = [laser]

    #         else:
    #             lasers.append(laser)

    #         files.at[index, 'aquisition'] = acquisition
    #         files.at[index, 'position'] = i
    
    
    
#     exposure_list = fov["exposure_time"].unique().tolist()
#     focus_list = find_focus_position(fov)
    
#     fov = fov[fov["posZ"].isin(focus_list)]
    
#     print(len(fov))
    
#     fov["short_exposure"] = False
#     fov.loc[fov["exposure_time"]==max(exposure_list), "short_exposure"] = True

#     fov["blurred"] = False
#     fov.loc[fov["posZ"]==focus_list[0], "blurred"] = True
    
#     if len(measurements)==0:
        
#         measurements = fov
        
#     else:
        
#         measurements = pd.concat([measurements, fov])
        
# measurements = measurements.reset_index(drop=True)

# measurements = measurements.groupby(by=['parent_folder','position',"short_exposure","blurred"])

















# measurements = pd.DataFrame()

# for i in range(1):
    
#     measurement = nim_measurements.get_group(list(nim_measurements.groups)[i])
    
#     exposure_time = measurement["exposure_time"].unique().max()
    
#     dat = measurement[(measurement["exposure_time"]==exposure_time) & (measurement["channel"].isin(["Cy3","473", "532"]))]



# with open('measurements.pickle', 'wb') as handle:
#     pickle.dump(measurements, handle, protocol=pickle.HIGHEST_PROTOCOL)

# with open('measurements.pickle', 'rb') as handle:
#     measurements = pickle.load(handle)


    
# i = 0    
# measurement = measurements.get_group(list(measurements.groups)[i])

# channels = measurement["channel"].tolist()

# channel_list = []
# file_list = []
# segChannel = ''
# segmentation_file = ''
# mask = []
    
# for channel in channels:

#     dat = measurement[measurement["channel"]ischannel]
#     path = dat["path"].item()
#     file_name = os.path.basename(path)
    
#     if channel=='Cy3' or channel=="Cy3-2":
#         segChannel = channel
#         segmentation_file = file_name
    
#     segmented = False
#     labelled = False
#     segmentation_curated = False
#     label_curated = False
#     segmentation_ground_truth = False
#     label_ground_truth = False
        
    
#     file_list.append(file_name)
#     channel_list.append(channel)

# for j in range(len(channels)):

#     channel = channels[j]

#     if channel in channels and segmentation_file!='': 
        
#         dat = measurement[measurement["channel"]ischannel]
  
#         path = dat["path"].item()
#         file_name = dat["file_name"].item()
#         folder = dat["folder"].item()
#         parent_folder = dat["parent_folder"].item()
#         user_initial = dat["user_initial"].item()

        # image, meta = read_tif(path)

        # image = get_brightest_fov(image)
        
        # img = np.mean(image,axis=0).astype(np.uint16)
        
        # if segmentation_file.split(".")[0] in mask_files:
        #     mask_path = mask_paths[mask_files.index(segmentation_file.split(".")[0])]
        #     mask = tifffile.imread(mask_path)
        # else:
        #     mask = np.zeros(img.shape,dtype=np.uint16)
            
        # label = np.zeros(mask.shape,dtype=np.uint16)
        # label = autoClassify(mask,label)
            
        # contrast_limit, alpha, beta, gamma = autocontrast_values(img, clip_hist_percent=1)    

    
    
    
    
    
    
    
    
    
                


    

    # measurement_channels = measurement["channel"].tolist()
    
    # for channel in channels:

    #     if channel in measurement_channels:

    #         dat = measurement[measurement["channel"]ischannel]
            
    #         paths = dat["path"].tolist()
            
    #         image, metadata, image_laplacian = zip(*[read_image_file(path) for path in paths])
            
    #         image, metadata, image_laplacian = zip(*sorted(zip(image, metadata, image_laplacian), key=lambda x: x[-1]))
            
    #         for img in image:
                
    #             plt.imshow(img)
    #             plt.show()
            
            
            
            
































