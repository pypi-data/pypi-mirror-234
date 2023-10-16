# -*- coding: utf-8 -*-
"""
Created on Thu Feb  2 09:21:43 2023

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
                    "num_segmentations",
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


def autocontrast_values(image, clip_hist_percent=1):

    # calculate histogram
    img = np.asarray(image)

    flat = img.flatten()
    hist = get_histogram(flat, (2 ** 16) - 1)
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

    img = cv2.convertScaleAbs(image, alpha=alpha, beta=beta)

    # calculate gamma value
    mid = 0.5
    mean = np.mean(img).astype(np.uint8)
    gamma = np.log(mid * 255) / np.log(mean)
    gamma = gamma

    contrast_limit = [minimum_gray, maximum_gray]

    return contrast_limit, alpha, beta, gamma

def read_tif(path, align=True):

    with tifffile.TiffFile(path) as tif:
        try:
            metadata = tif.pages[0].tags["ImageDescription"].value
            metadata = json.loads(metadata)
        except Exception:
            metadata = {}

    if align:
        
        image = tifffile.imread(path)
        
        img0 = image[0]
        img1 = image[1]
        
        shift, error, diffphase = phase_cross_correlation(img0, img1, upsample_factor=100)
        img1 = scipy.ndimage.shift(img1, shift)
        
        image = np.stack([img0,img1])
    
    return image, metadata

def get_brightest_fov(image):
    
    imageL = image[0,:,:image.shape[2]//2]
    imageR = image[0,:,image.shape[2]//2:]  
    
    if np.mean(imageL) > np.mean(imageR):
        
        image = image[:,:,:image.shape[2]//2]
    else:
        image = image[:,:,:image.shape[2]//2]
        
    return image


def get_hash(img_path = None, img = None):
    
    hash_code = None
    
    if img!=None:
    
        img_path = tempfile.TemporaryFile(suffix=".tif").name
        
        tifffile.imwrite(img_path,img)
        
        with open(img_path, "rb") as f:
            bytes = f.read()  # read entire file as bytes
            
            hash_code =  hashlib.sha256(bytes).hexdigest()
        
        os.remove(img_path)
    
    return hash_code

def autoClassify(mask,label):

    label_ids = np.unique(label)
    mask_ids = np.unique(mask)

    if len(label_ids)==1:

        label = np.zeros(label.shape, dtype=np.uint16)

        for mask_id in mask_ids:

            if mask_id!=0:

                cnt_mask = np.zeros(label.shape,dtype = np.uint8)
                cnt_mask[mask==mask_id] = 255

                cnt, _ = cv2.findContours(cnt_mask.astype(np.uint8),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)

                x, y, w, h = cv2.boundingRect(cnt[0])
                y1, y2, x1, x2 = y, (y + h), x, (x + w)

                # appends contour to list if the bounding coordinates are along the edge of the image
                if y1 > 0 and y2 < cnt_mask.shape[0] and x1 > 0 and x2 < cnt_mask.shape[1]:

                    label[mask==mask_id] = 1

                else:

                    label[mask==mask_id] = 6
                    
    return label


def read_xml(paths):

    try:

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
                    
                    well_name = img["@Name"]
              
              
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
                            well_position = int(well_name.split(",")[0].split(" ")[-1])
                            
                        
                            well_position_name = str(well_name.split("(")[-1].split(")")[0])
                            
                            well_row = str(well_position_name[0]).lower()
                            well_column = int(well_position_name[1:])
                            well_column_transpose = ord(well_row) - 96
                            well_row_transpose = chr(ord('@')+well_column)
                            
                            well_position_name_transpose =  str(well_row_transpose) + str(well_column_transpose)
                            
                            
                            fov_index = int(img["@ID"].split("P")[-1])
                            
                            if modality=="Transmitted":
                                modality = "Bright Field"
                                
                            if channel in ["Nile Red", "FM4-64", "WGA-488", "WGA-647"]:
                                stain_target = "Membrane"
                                stain = channel
                            elif channel in ["Cy3","Cy5"]:
                                stain_target = "Ribosome"
                                stain = channel
                            elif channel in ["DAPI"]:
                                stain_target = "Nucleoid"
                                stain = channel
                            else:
                                stain_target = None
                                stain = None
                            
                            
                            split_path = path.split("\\")

                            if len(split_path) >= 4:
                                folder = path.split("\\")[-4]
                            else:
                                folder = ""
                        
                            if len(split_path) >= 5:
                                parent_folder = path.split("\\")[-5]
                            else:
                                parent_folder = ""
                                

                            file_path = file_path.replace(".ome.xml",file_name)
                            
                        except Exception:
                            print(traceback.format_exc())
                            well_index = None
                            modality = None
                            channel = None
                            exposure_time = None
                            posX = None
                            posY = None
                            posZ = None
                            exposure_time = None
                            well_position = None
                            well_position_name = None
                            stain_target = None
                            folder = None
                            parent_folder = None
                            fov_index = None
                            well_position_name_transpose = None

                        files[file_name] = dict(file_name=file_name,
                                                path=file_path.replace(".ome.xml",file_name),
                                                well_position = well_position,
                                                well_position_name = well_position_name,
                                                well_position_name_transpose = well_position_name_transpose,
                                                well_index=well_index,
                                                position_index=position_index,
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
                                                posZ=posZ,
                                                stain = stain,
                                                stain_target = stain_target,
                                                folder=folder,
                                                parent_folder=parent_folder,
                                                fov_index=fov_index)
    except Exception:
            pass

    return files



def read_tif(path, align=True):

    with tifffile.TiffFile(path) as tif:
        try:
            metadata = tif.pages[0].tags["ImageDescription"].value
            metadata = json.loads(metadata)
        except Exception:
            metadata = {}

    if align:
        
        image = tifffile.imread(path)
        
        img0 = image[0]
        img1 = image[1]
        
        shift, error, diffphase = phase_cross_correlation(img0, img1, upsample_factor=100)
        img1 = scipy.ndimage.shift(img1, shift)
        
        image = np.stack([img0,img1])
    
    return image, metadata


def upload_data(dat):
    
    try:
        
        user_metadata = pd.DataFrame(columns=metadata_columns)
        
        channels = ["532","405"]
        
        file_list = dat[["NR_file_name","DAPI_file_name"]].tolist()
        
        segChannel = '532'
        segmentation_file = file_list[0]
        
        image_files, meta = read_tif(dat["path"])
        
        for j in range(len(channels)):
            
            channel = channels[j]
            
            path = dat["path"]
            mask_path = dat["mask_path"]
            
            file_name = file_list[j]
    
            laser = channel
            folder = dat["folder"]
            parent_folder = dat["parent_folder"]
            user_initial = dat["user_initial"]
            repeat = dat["repeat"]
            
    except Exception:
        pass


  
def unfold_image(image, path, file_list, segmentation_file, tile_shape = (256,256), overlap = 0):
    
    tiler_object = Tiler(data_shape=image.shape,
                                      tile_shape=tile_shape,
                                      overlap=overlap)

    tile_images = []
    tile_file_names = []
    file_list_list = []
    segmentation_file_list = []
    
    num_image_tiles = 0
    
    file_name = os.path.basename(path)
    
    for tile_id, tile in tiler_object.iterate(image):

        bbox = np.array(tiler_object.get_tile_bbox(tile_id=tile_id))
    
        y1, x1, y2, x2 = bbox[0][0], bbox[0][1], bbox[1][0], bbox[1][1]
        
        if y2 > image.shape[-2]:
            y2 = image.shape[-2]
        if x2 > image.shape[-1]:
            x2 = image.shape[-1]

        x2 = x2 - x1
        x1 = 0
        y2 = y2 - y1
        y1 = 0

        if (y2 - y1, x2 - x1)==tile_shape:

            num_image_tiles += 1
            tile_images.append(tile)
            
            tile_file_names.append(file_name.replace(".tif",f"_tile{num_image_tiles}.tif"))
            segmentation_file_list.append(segmentation_file.replace(".tif",f"_tile{num_image_tiles}.tif"))
            
            file_list_list.append([file_name.replace(".tif",f"_tile{num_image_tiles}.tif") for file_name in file_list])
            
    return tile_images, tile_file_names, file_list_list, segmentation_file_list
    
    
def get_meta_value(meta,value):

    if value in meta.keys():
    
        data = meta[value]
    else:
        data = None
        
    return data
    


def upload_files(dat, unfold=True):
    
    file_metadata_list = []
    
    try:
        
        focused_image_data, index_list = get_focused_image_data(dat, unfold)

        for image_index in np.unique(index_list):
            
            for channel in focused_image_data.keys():
        
                image_dat = focused_image_data[channel][image_index]
                
                segmentation_file = image_dat["segmentation_file"]
                segmentation_channel = "Trans"
            
                file_list = image_dat["file_list"]
                channel_list = image_dat["channel_list"]
                
                img = image_dat["images"]
                meta = image_dat["meta_list"]
                file_name = image_dat["file_names"]
                folder = meta["folder"]
                
                mask = np.zeros_like(img)
                label = np.zeros_like(img)
                
                contrast_limit, alpha, beta, gamma = autocontrast_values(img, clip_hist_percent=1)
                
                meta["akseg_hash"] = get_hash(img=img)
                meta["contrast_limit"] = contrast_limit
                meta["contrast_alpha"] = alpha
                meta["contrast_beta"] = beta
                meta["contrast_gamma"] = gamma
                meta["dims"] = [img.shape[-1], img.shape[-2]]
                meta["crop"] = [0, img.shape[-2], 0, img.shape[-1]]
                meta["file_list"] = file_list
                meta["layer_list"] = channel_list
                meta["channel_list"] = channel_list
                
                akseg_dir = r"\\physics\dfs\DAQ\CondensedMatterGroups\AKGroup\Piers\AKSEG\Images"
                # akseg_dir = r"C:\Users\turnerp\Documents\Upload"
            
                image_path = os.path.abspath(akseg_dir + r"\\" + user_initial + "\\images\\" + folder + "\\")
                mask_path = os.path.abspath(akseg_dir +  r"\\" + user_initial + "\\masks\\" + folder + "\\")
                label_path = os.path.abspath(akseg_dir +  r"\\" + user_initial + "\\labels\\" + folder + "\\")
                json_path = os.path.abspath(akseg_dir +  r"\\" + user_initial + "\\json\\" + folder + "\\")
                
                if os.path.exists(image_path)==False:
                    try:
                        os.makedirs(image_path)
                    except Exception:
                        pass
            
                if os.path.exists(mask_path)==False:
                    try:
                        os.makedirs(mask_path)
                    except Exception:
                        pass
                    
                if os.path.exists(label_path)==False:
                    try:
                        os.makedirs(label_path)
                    except Exception:
                        pass
            
                if os.path.exists(json_path)==False:
                    try:
                        os.makedirs(json_path)
                    except Exception:
                        pass
            
                image_path = os.path.abspath(image_path + "\\" +  file_name)
                mask_path = os.path.abspath(mask_path + "\\" +  file_name)
                label_path = os.path.abspath(label_path + "\\" +  file_name)
                json_path = os.path.abspath(json_path + "\\" +  file_name)
        
                img_meta = meta
                img_meta["image_name"] = file_name
        
                tifffile.imwrite(image_path, img, metadata=img_meta)
                tifffile.imwrite(mask_path, mask, metadata=img_meta)
                tifffile.imwrite(label_path, label, metadata=img_meta)
            
                export_coco_json(file_name, img, mask, label, json_path)
                
                date_uploaded = str(datetime.datetime.now())
                
                file_metadata = {"date_uploaded": date_uploaded,
                                  "date_created": get_meta_value(meta, "date_created"),
                                  "date_modified": date_uploaded,
                                  "file_name": file_name,
                                  "channel": get_meta_value(meta, "channel"),
                                  "file_list": file_list,
                                  "channel_list": get_meta_value(meta, "channel_list"),
                                  "segmentation_file": segmentation_file,
                                  "segmentation_channel": segmentation_channel,
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
                                  "num_segmentations": 0,
                                  "segmented": False,
                                  "labelled": False,
                                  "segmentation_curated": False,
                                  "label_curated": False,
                                  "posX": get_meta_value(meta, "posX"),
                                  "posY": get_meta_value(meta, "posY"),
                                  "posZ": get_meta_value(meta, "posZ"),
                                  "image_load_path": get_meta_value(meta, "path"),
                                  "image_save_path": image_path,
                                  "mask_load_path": get_meta_value(meta, "mask_path"),
                                  "mask_save_path": mask_path,
                                  "label_load_path": get_meta_value(meta, "label_path"),
                                  "label_save_path": json_path}
                
                file_metadata_list.append(file_metadata)
     
    except Exception:
        print(traceback.format_exc())
        file_metadata_list.append(None)
        
    return file_metadata_list


def extract_list(data, mode="file"):

    data = data.strip("[]").replace("'", "").split(", ")

    return data


def get_focused_image_data(dat, unfold):
    
    try:

   
        segmentation_channel = "Trans"
        channels = dat["channel"].unique().tolist()
        
        image_data = {}
        
        for channel in dat.channel.unique():
            
            if channel not in image_data.keys():
                image_data[channel] = {}
                
            for z_index in dat.z_index.unique():
        
                file_list = dat[dat["z_index"]==z_index]["file_name"].tolist()
                channel_list = dat[dat["z_index"]==z_index]["channel"].tolist()
                
                segmentation_file = dat[(dat["channel"]==segmentation_channel) & (dat["z_index"]is z_index)]["file_name"].item()
                z_dat = dat[(dat["channel"]==channel) & (dat["z_index"]is z_index)].iloc[0]
            
                meta = z_dat.to_dict()
            
                path = meta["path"]
                folder = meta["folder"]
                user_initial = meta["user_initial"]
                
                images = tifffile.imread(path)
                
                if unfold:
                    images, file_names, file_list_list, segmentation_file_list = unfold_image(images, path, file_list, segmentation_file)
                    
                else:
                    images = [images]
                    file_names = [os.path.basename(path)]
                    file_list_list = [file_list]
                    segmentation_file_list = [segmentation_file]
            
    
                for tile_index in range(len(images)):
                    
                    image_laplacian = cv2.Laplacian(images[tile_index], cv2.CV_64F).var()
                                        
                    if tile_index not in image_data[channel].keys():
                        image_data[channel][tile_index] = {"images":[], "file_names":[],
                                                           "file_list":[], "segmentation_file":[],
                                                           "image_laplacian":[], "channel_list":[],
                                                           "meta_list":[]}
                                        
                    image_data[channel][tile_index]["images"].append(images[tile_index])
                    image_data[channel][tile_index]["file_names"].append(file_names[tile_index])
                    image_data[channel][tile_index]["file_list"].append(file_list_list[tile_index])
                    image_data[channel][tile_index]["segmentation_file"].append(segmentation_file_list[tile_index])
                    image_data[channel][tile_index]["image_laplacian"].append(image_laplacian)
                    image_data[channel][tile_index]["channel_list"].append(channel_list)
                    image_data[channel][tile_index]["meta_list"].append(meta)
                    
                    num_images = len(image_data[channel][tile_index]["images"])
                
    
        focused_image_data = {}
        
        index_list = []
        
        for tile_index in image_data["DAPI"].keys():
            
            laplacian_list = image_data["DAPI"][tile_index]["image_laplacian"]
            
            best_z_index = np.argmax(laplacian_list)
            
            img =  image_data["Trans"][tile_index]["images"][best_z_index]
            
            for channel in image_data.keys():
                
                channel_data = image_data[channel][tile_index]
                
                image_laplacian = image_data["DAPI"][tile_index]["image_laplacian"][best_z_index]
                
                if image_laplacian > 60000:
                    
                    index_list.append(tile_index)
                    
                    if channel not in focused_image_data.keys():
                        focused_image_data[channel] = {}
                    
                    if tile_index not in focused_image_data[channel].keys():
                        focused_image_data[channel][tile_index] = {}
                    
                    for key, value in channel_data.items():
                        
                        focused_image_data[channel][tile_index][key] = value[best_z_index]
                    

        index_list = np.unique(index_list).tolist()

    except Exception:
        print(traceback.format_exc())
        focused_image_data==None
        num_images = 0

    return focused_image_data, index_list



user_initial = "CF"


files = glob(r"D:\DFP Data\130223_ConorDFP_Plate2_NR+DAPI\Agarose Pillar_001\data\*.xml")  

file_data = read_xml(files)


upload_data = []

for file_name,data in file_data.items():
    
    well_position_name = data["well_position_name_transpose"]
    
    column = well_position_name[0]
    row = int(well_position_name[1:])
    
    if column=="A":
        antibiotic = "None"
        antibiotic_contration = ""
    elif column=="B":
        antibiotic = "Ciprofloxacin"
        antibiotic_contration = "10XEUCAST"
    elif column=="C":
        antibiotic = "Gentamicin"
        antibiotic_contration = "10XEUCAST"
    elif column=="D":
        antibiotic = "Ceftriaxone"
        antibiotic_contration = "3XEUCAST"
    elif column=="E":
        antibiotic = "Ciprofloxacin"
        antibiotic_contration = "1XEUCAST"
        
    if row in [1,2]:
        repeat = 1
        usermeta3 = f"{repeat}-{[1,2].index(row)+1}"
    if row in [3,4]:
        repeat = 2
        usermeta3 = f"{repeat}-{[3,4].index(row)+1}"
    if row in [5,6]:
        repeat = 3
        usermeta3 = f"{repeat}-{[5,6].index(row)+1}"
    if row in [7,8]:
        repeat = 4
        usermeta3 = f"{repeat}-{[7,8].index(row)+1}"
        
    if column in ["A","B"]:
        strain = "L48480"
    elif column in ["C","D"]:
        strain = "L11037"
    else:
        strain = ""
        
    if data["time_index"]==0:
        
        file_data[file_name]["user_initial"] = user_initial
        file_data[file_name]["antibiotic"] = antibiotic
        file_data[file_name]["abxconcentration"] = antibiotic_contration
        file_data[file_name]["repeat"] = repeat
        file_data[file_name]["usermeta1"] = "Direct From Plate"
        file_data[file_name]["usermeta2"] = "Plate2_zstack"
        file_data[file_name]["usermeta3"] = usermeta3
        file_data[file_name]["protocol"] = ""
        file_data[file_name]["image_content"] = "E.Coli"
        file_data[file_name]["mount"] = "Agarose Pillars"
        file_data[file_name]["strain"] = strain
        
        upload_data.append(file_data[file_name])

upload_data = pd.DataFrame.from_dict(upload_data)

upload_data = upload_data.sort_values(["well_position","position_index","z_index"])
    
upload_data = upload_data.groupby(["well_position_name","fov_index"])

upload_data = [upload_data.get_group(list(upload_data.groups)[index]) for index in range(len(upload_data))]

unfold = True

user_metadata_path = os.path.join(r"\\physics\dfs\DAQ\CondensedMatterGroups\AKGroup\Piers\AKSEG\Images", user_initial, f"{user_initial}_file_metadata.txt")
user_metadata = pd.read_csv(user_metadata_path, sep=",", low_memory=False)

# if __name__=='__main__':
    
#     with Pool() as p:
        
#         results = list(tqdm.tqdm(p.imap(upload_files,upload_data), total=len(upload_data)))
#         p.close()
#         p.join()
        
#         results = [item for item in results if results!=None]
#         results = [file_metadata for file_metadata_list in results for file_metadata in file_metadata_list if file_metadata!=None]
        
#         new_metadata = pd.DataFrame.from_dict(results)

#     with open('new_metadata.pickle', 'wb') as handle:
#         pickle.dump(new_metadata, handle, protocol=pickle.HIGHEST_PROTOCOL)

#     # with open('new_metadata.pickle', 'rb') as handle:
#     #     new_metadata = pickle.load(handle)

#     user_metadata = pd.concat([user_metadata,new_metadata],ignore_index=True).reset_index(drop=True)
    
#     user_metadata = user_metadata.drop_duplicates(subset=['akseg_hash'],keep="last")
    
#     user_metadata.to_csv(user_metadata_path, sep=",", index = False) 
            

    
        


    
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        