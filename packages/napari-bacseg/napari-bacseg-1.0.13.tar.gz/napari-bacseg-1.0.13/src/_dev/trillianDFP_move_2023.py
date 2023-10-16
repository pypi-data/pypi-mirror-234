# -*- coding: utf-8 -*-
"""
Created on Tue Sep  5 16:52:46 2023

@author: turnerp
"""

import pandas as pd
import os
import numpy as np
from glob2 import glob
from aicspylibczi import CziFile
import itertools
from collections import ChainMap
import copy
import tifffile
import tempfile
import hashlib
from tiler import Tiler, Merger
import cv2
import datetime
import pathlib
import json
from multiprocessing import Pool
import tqdm
import pickle
import matplotlib.pyplot as plt
from functools import partial
import traceback


def export_coco_json(image_name, image, mask, nmask, label, file_path):
    
    file_path = os.path.splitext(file_path)[0] + ".txt"

    info = {"description": "COCO 2017 Dataset", "url": "http://cocodataset.org", "version": "1.0", "year": datetime.datetime.now().year, "contributor": "COCO Consortium", "date_created": datetime.datetime.now().strftime("%d/%m/%y"), }

    categories = [{"supercategory": "cell", "id": 1, "name": "single"}, {"supercategory": "cell", "id": 2, "name": "dividing"}, {"supercategory": "cell", "id": 3, "name": "divided"},
        {"supercategory": "cell", "id": 4, "name": "vertical"}, {"supercategory": "cell", "id": 5, "name": "broken"}, {"supercategory": "cell", "id": 6, "name": "edge"}, ]

    licenses = [{"url": "https://creativecommons.org/licenses/by-nc-nd/4.0/", "id": 1, "name": "Attribution-NonCommercial-NoDerivatives 4.0 International", }]

    height, width = image.shape[-2], image.shape[-1]

    images = [{"license": 1, "file_name": image_name, "coco_url": "", "height": height, "width": width, "date_captured": "", "flickr_url": "", "id": 0, }]

    mask_ids = np.unique(mask)

    annotations = []

    for j in range(len(mask_ids)):
        if j != 0:
            try:
                cnt_mask = mask.copy()

                cnt_mask[cnt_mask != j] = 0

                contours, _ = cv2.findContours(cnt_mask.astype(np.uint8), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE, )
                cnt = contours[0]

                # cnt coco bounding box
                x, y, w, h = cv2.boundingRect(cnt)
                y1, y2, x1, x2 = y, (y + h), x, (x + w)
                coco_BBOX = [x1, y1, h, w]

                # cnt area
                area = cv2.contourArea(cnt)

                segmentation = cnt.reshape(-1, 1).flatten()

                cnt_labels = np.unique(label[cnt_mask != 0])

                if len(cnt_labels) == 0:
                    cnt_label = 1

                else:
                    cnt_label = int(cnt_labels[0])

                annotation = {"segmentation": [segmentation.tolist()], "area": area, "iscrowd": 0, "image_id": 0, "bbox": coco_BBOX, "category_id": cnt_label, "id": j, }

                annotations.append(annotation)

            except:
                pass

    nmask_ids = np.unique(nmask)

    for j in range(len(nmask_ids)):
        if j != 0:
            try:
                cnt_mask = nmask.copy()

                cnt_mask[cnt_mask != j] = 0

                contours, _ = cv2.findContours(cnt_mask.astype(np.uint8), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE, )
                cnt = contours[0]

                # cnt coco bounding box
                x, y, w, h = cv2.boundingRect(cnt)
                y1, y2, x1, x2 = y, (y + h), x, (x + w)
                coco_BBOX = [x1, y1, h, w]

                # cnt area
                area = cv2.contourArea(cnt)

                segmentation = cnt.reshape(-1, 1).flatten()

                cnt_labels = np.unique(label[cnt_mask != 0])

                if len(cnt_labels) == 0:
                    cnt_label = 1

                else:
                    cnt_label = int(cnt_labels[0])

                annotation = {"nucleoid_segmentation": [segmentation.tolist()], "area": area, "iscrowd": 0, "image_id": 0, "bbox": coco_BBOX, "category_id": cnt_label, "id": j, }

                annotations.append(annotation)

            except:
                pass

    annotation = {"info": info, "licenses": licenses, "images": images, "annotations": annotations, "categories": categories, }

    with open(file_path, "w") as f:
        json.dump(annotation, f)

    return annotation
    
def get_czi_dim_list(path, plate_info = {}):
    
    import xmltodict
    from czifile import CziFile

    czi = CziFile(path)
    metadata = czi.metadata()

    metadata = xmltodict.parse(metadata)["ImageDocument"]["Metadata"]

    scene_dict = get_czi_scene_dict(metadata)
    size_dict = get_czi_size_dict(metadata)
    channel_dict = get_czi_channel_dict(metadata)
    
    index_dims = []
    
    for index_name in ["S", "T", "M", "Z", "C"]:
        if index_name in size_dict.keys():
            index_shape = size_dict[index_name]
            
            dim_list = np.arange(index_shape).tolist()
            dim_list = [{index_name: dim} for dim in dim_list]
            
            index_dims.append(dim_list)
    
    dim_list = list(itertools.product(*index_dims))
    dim_list = [dict(ChainMap(*list(dim))) for dim in dim_list]
    
    groupby_cols = []
    
    for i, dim in enumerate(dim_list):
        
        czi_import_dict = {}
        
        if "S" in dim:
            dim = {**dim, **scene_dict[dim["S"]]}
            groupby_cols.append("S")
            czi_import_dict["S"] = dim["S"]
        
        if "C" in dim:
            dim = {**dim, **channel_dict[dim["C"]]}
            czi_import_dict["C"] = dim["C"]
        
        dim["czi_import_dict"] = czi_import_dict
        
        if "posZ" not in dim:
            dim["posZ"] = 0
        
        if "pillarID" in dim.keys() and len(plate_info) > 0:
            
            sample_info = plate_info[plate_info["GridRef"] == dim["pillarID"]]
            
            antibiotic = sample_info["Antibiotic"].values[0]
            strain = sample_info["Strain"].values[0].replace("L","")
            antibiotic_concentration = sample_info["Concentration"].values[0]
            treatment_time = sample_info["Time"].values[0]
            date_created = str(sample_info["Date"].values[0])
            mic = int(sample_info["MIC"].values[0])
            mic_breakpoint = int(sample_info["MIC Breakpoints"].values[0])
            
            date_created = datetime.datetime.strptime(date_created, '%d%m%y').strftime("%d/%m/%y")

            if antibiotic_concentration == "No treatment":
                antibiotic = "None"
                antibiotic_concentration = ""
                treatment_time = ""
                phenotype = "Untreated"
            else:
                
                if mic > mic_breakpoint:
                    phenotype = "Treated Resistant"
                else:
                    phenotype = "Treated Sensitive"
                
                if antibiotic == "GENT":
                    antibiotic = "Gentamicin"
                elif antibiotic == "CIP":
                    antibiotic = "Ciprofloxacin"
                
            dim["strain"] = strain
            dim["phenotype"] = phenotype
            dim["antibiotic"] = antibiotic
            dim["antibiotic concentration"] = antibiotic_concentration
            dim["treatment time (mins)"] = treatment_time
            dim["treatment time (mins)"] = phenotype
            
            dim["date_created"] = date_created
            dim["date_uploaded"] = datetime.datetime.now().strftime("%d/%m/%y")
            dim["date_modified"] = datetime.datetime.now().strftime("%d/%m/%y")
            
        
        dim_list[i] = dim
    
    for dim in dim_list:
        dim.update({"path": path})
    
    dim_df = pd.DataFrame(dim_list)
    
    groupby_cols = np.unique(groupby_cols).tolist()
        
    return dim_list, groupby_cols


def get_czi_scene_dict(metadata):
    
    dimensions = metadata["Information"]["Image"]["Dimensions"]
    
    scene_list = dimensions["S"]["Scenes"]["Scene"]
    
    scene_dict = {}
    
    for scene in scene_list:
        
        index = scene["@Index"]
        
        scene_dict[int(scene["@Index"])] = {"image_index":int(scene["@Index"]),
               "pillarID":scene["ArrayName"],
               "pillar_row_index":int(scene["Shape"]["RowIndex"]),
               "pillar_column_index":int(scene["Shape"]["ColumnIndex"]),
               "montageID":scene["@Name"],
               "posX":float(scene["CenterPosition"].split(",")[0]),
               "posY":float(scene["CenterPosition"].split(",")[1]),
               }
    
    return scene_dict

def get_czi_size_dict(metadata):
    
    image_information = metadata["Information"]["Image"]

    size_dict = {}

    for key, value in image_information.items():
        
        if "Size" in key:
            
            key = key.replace("Size","")
            
            if key not in ["X","Y"] and int(value) > 1:
        
                size_dict[key] = int(value)
    
    return size_dict

def get_czi_channel_dict(metadata):

    channels = metadata["Information"]["Image"]["Dimensions"]["Channels"]["Channel"]
    
    channel_dict = {}

    for channel in channels:
        
        channel_name = channel["@Name"]
        
        if channel_name == "Bright":
            
            channel_name = "Bright Field"
            source = 'White Light'
            modality = channel_name
            stain = ""
            stain_target = ""
            
        elif channel_name == "Phase":
            
            channel_name = "Phase Contrast"
            source = 'White Light'
            modality = channel_name
            stain = ""
            stain_target = ""
            
        elif channel_name == "AF647":
            
            channel_name = "WGA-647"
            source = 'LED'
            modality = 'Epifluorescence'
            stain = channel_name
            stain_target = "membrane"
            
        elif channel_name == "AF488":
            
            channel_name = "WGA-488"
            source = 'LED'
            modality = 'Epifluorescence'
            stain = channel_name
            stain_target = "membrane"
            
        elif channel_name == "Fm143":
            
            channel_name = "FM 1-43"  
            source = 'LED'
            modality = 'Epifluorescence'
            stain = channel_name
            stain_target = "membrane"
            
            
        elif channel_name == "Fm464":
            
            channel_name = "FM 4-64"   
            source = 'LED'
            modality = 'Epifluorescence'
            stain = channel_name
            stain_target = "membrane"
            
        elif channel_name == "DAPI":
             
            source = 'LED'
            modality = 'Epifluorescence'
            stain = channel_name
            stain_target = "nucleoid"
            
        elif channel_name == "Nile Red":
             
            source = 'LED'
            modality = 'Epifluorescence'
            stain = channel_name
            stain_target = "membrane"
        
        channel_dict[int(channel["@Id"].split(":")[-1])] = {"channel_name":channel_name,
                                                            "source":source,
                                                            "modality":modality,
                                                            "stain":stain,
                                                            "stain_target":stain_target}
        
    return channel_dict



def get_zeiss_measurements(path, plate_info, import_limit="None"):

    dim_list, groupby_columns = get_czi_dim_list(path, plate_info)
    
    czi_measurements = pd.DataFrame(dim_list)
    
    czi_fovs = []
    
    if len(groupby_columns) == 1:
        groupby_columns = groupby_columns[0]

    for group, data in czi_measurements.groupby(groupby_columns):
        czi_fovs.append(data)
    
    if type(import_limit) == int:
        import_limit = int(import_limit)
    
        czi_fovs = czi_fovs[:import_limit]
        num_measurements = len(czi_fovs)
    
    else:
        num_measurements = len(czi_fovs)
    
    channel_names = czi_measurements.channel_name.unique().tolist()

    return czi_fovs, channel_names

def get_hash(img_path=None, img=None):
    
    if img is not None:
        img_path = tempfile.TemporaryFile(suffix=".tif").name
        tifffile.imwrite(img_path, img)

        with open(img_path, "rb") as f:
            bytes = f.read()  # read entire file as bytes
            hash_code = hashlib.sha256(bytes).hexdigest()

        os.remove(img_path)

    else:
        with open(img_path, "rb") as f:
            bytes = f.read()  # read entire file as bytes
            hash_code = hashlib.sha256(bytes).hexdigest()

    return hash_code

def import_zeiss_fov(fov, tile_shape=(1024,1024), overlap = 0):

    zeiss_images = {}
    
    try:
    
        for _, channel_data in fov.iterrows():
            
            path = channel_data["path"]
            channel_name = channel_data["channel_name"]
            
            image_name = os.path.basename(path)
            
            import_dict = channel_data["czi_import_dict"]
            
            czi = CziFile(path)
            
            img_channel, img_shape = czi.read_image(**import_dict)
            img_channel = np.reshape(img_channel, img_channel.shape[-2:])
            
            meta = copy.deepcopy(channel_data).to_dict()
            
            image_name = image_name.replace(".czi","") + f"_{channel_name}"
            for key,value in import_dict.items():
                image_name += f"_{key}{value}"
            image_name += ".tif"
            
            if type(tile_shape) != tuple or len(tile_shape) == 0:
                
                akseg_hash = get_hash(img=img_channel)
                contrast_limit = np.percentile(img_channel, (1, 99))
                contrast_limit = [int(contrast_limit[0] * 0.5), int(contrast_limit[1] * 2), ]
                
                meta["akseg_hash"] = akseg_hash
                meta["image_name"] = image_name
                meta["image_path"] = path
                meta["folder"] = path.split(os.sep)[-2]
                meta["mask_name"] = None
                meta["mask_path"] = None
                meta["label_name"] = None
                meta["label_path"] = None
                meta["import_mode"] = "image"
                meta["contrast_limit"] = contrast_limit
                meta["contrast_alpha"] = 0
                meta["contrast_beta"] = 0
                meta["contrast_gamma"] = 0
                meta["dims"] = [img_channel.shape[-1], img_channel.shape[-2]]
                meta["crop"] = [0, img_channel.shape[-2], 0, img_channel.shape[-1], ]
                
                zeiss_images[channel_name] = dict(images=[img_channel], masks=[], nmasks=[], classes=[], metadata={0: meta}, )
        
            else:
                
                tiler_object = Tiler(data_shape=img_channel.shape,
                                      tile_shape=tile_shape)
                
                
                tile_index = 0
                
                for tile_id, tile_img in tiler_object.iterate(img_channel):
                    
                    bbox = np.array(tiler_object.get_tile_bbox(tile_id=tile_id))
                    bbox = bbox[..., [-2, -1]]
                    y1, x1, y2, x2 = (bbox[0][0], bbox[0][1], bbox[1][0], bbox[1][1],)
            
                    if y2 > img_channel.shape[-2]:
                        y2 = img_channel.shape[-2]
                    if x2 > img_channel.shape[-1]:
                        x2 = img_channel.shape[-1]

                    x2 = x2 - x1
                    x1 = 0
                    y2 = y2 - y1
                    y1 = 0  
                    
                    if (y2 - y1, x2 - x1) ==tile_shape:
                        
                        tile_meta = copy.deepcopy(meta)
                        
                        akseg_hash = get_hash(img=tile_img)
                        contrast_limit = np.percentile(tile_img, (1, 99))
                        contrast_limit = [int(contrast_limit[0] * 0.5), int(contrast_limit[1] * 2), ]
                            
                        tile_name = str(image_name).split(".")[0] + "_tile" + str(tile_index) + ".tif"
                        
                        tile_meta["akseg_hash"] = akseg_hash
                        tile_meta["image_name"] = tile_name
                        tile_meta["image_path"] = path
                        tile_meta["folder"] = path.split(os.sep)[-2]
                        tile_meta["mask_name"] = None
                        tile_meta["mask_path"] = None
                        tile_meta["label_name"] = None
                        tile_meta["label_path"] = None
                        tile_meta["import_mode"] = "image"
                        tile_meta["contrast_limit"] = contrast_limit
                        tile_meta["contrast_alpha"] = 0
                        tile_meta["contrast_beta"] = 0
                        tile_meta["contrast_gamma"] = 0
                        tile_meta["dims"] = [img_channel.shape[-1], img_channel.shape[-2]]
                        tile_meta["crop"] = [0, img_channel.shape[-2], 0, img_channel.shape[-1], ]
                        
                        if channel_name not in zeiss_images:
                            zeiss_images[channel_name] = dict(images=[tile_img], masks=[], nmasks=[], classes=[], metadata={tile_index: tile_meta}, )
                        else:
                            zeiss_images[channel_name]["images"].append(tile_img)
                            zeiss_images[channel_name]["metadata"][tile_index] = tile_meta
                        
                        tile_index +=1
    except:
        pass

    return zeiss_images

def generate_bacseg_paths(akseg_directory, user_initial, folder, image_name, segmentation_file):
    
    image_dir = os.path.join(akseg_directory,"Images", user_initial,"images",folder)
    mask_dir = os.path.join(akseg_directory,"Images", user_initial,"masks",folder)
    label_dir = os.path.join(akseg_directory,"Images", user_initial,"labels",folder)
    json_dir = os.path.join(akseg_directory,"Images", user_initial,"json",folder)
    
    segmentation_file_json = pathlib.Path(segmentation_file).with_suffix('.txt')
    
    
    if os.path.exists(image_dir)==False:
        try:
            os.makedirs(image_dir)
        except Exception:
            pass
       
    if os.path.exists(mask_dir)==False:
        try:
            os.makedirs(mask_dir)
        except Exception:
            pass
        
    if os.path.exists(label_dir)==False:
        try:
            os.makedirs(label_dir)
        except Exception:
            pass
       
    if os.path.exists(json_dir)==False:
        try:
            os.makedirs(json_dir)
        except Exception:
            pass

    image_save_path = os.path.join(image_dir, image_name)
    mask_save_path = os.path.join(mask_dir, segmentation_file)
    label_save_path = os.path.join(label_dir, segmentation_file)
    json_save_path = os.path.join(json_dir, segmentation_file_json)
        
    paths = dict(image_save_path=image_save_path, 
                 mask_save_path=mask_save_path, 
                 label_save_path=label_save_path, 
                 json_save_path=json_save_path)

    return paths


def append_generic_metadata(imported_data, akseg_directory, user_initial = "PT", segmentation_channel = "Phase Contrast"):

    channel_list_dict = {}
    
    for channel, channel_data in imported_data.items():
        
        for i, (img, metadata) in enumerate(zip(channel_data["images"],channel_data["metadata"].values())):
            
            image_name = metadata["image_name"]
            channel_name = metadata["channel_name"]
            
            if i not in channel_list_dict.keys():
                channel_list_dict[i] = {"channel_list":[], "file_list":[], "segmentation_file":"", "segmentation_channel":""}
                
            if channel_name not in channel_list_dict[i]["channel_list"]:
                channel_list_dict[i]["channel_list"].append(channel_name)
                
            if image_name not in channel_list_dict[i]["file_list"]:
                channel_list_dict[i]["file_list"].append(image_name)
                
            if channel_name == segmentation_channel:
                channel_list_dict[i]["segmentation_file"] = image_name
                channel_list_dict[i]["segmentation_channel"] = channel_name
                
    for channel, channel_data in imported_data.items():
        
        for i, (img, metadata) in enumerate(zip(channel_data["images"],channel_data["metadata"].values())):
            
            image_laplacian = cv2.Laplacian(img, cv2.CV_64F).var()
            
            image_name = metadata["image_name"]
            image_path = os.path.normpath(metadata["image_path"])
            
            folder = image_path.split(os.sep)[-2]
            parent_folder = image_path.split(os.sep)[-3]
            
            channel_name = metadata["channel_name"]
            
            file_list = channel_list_dict[i]["file_list"]
            channel_list = channel_list_dict[i]["channel_list"]
            segmentation_file = channel_list_dict[i]["segmentation_file"]
            segmentation_channel = channel_list_dict[i]["segmentation_channel"]
            
            imported_data[channel]["metadata"][i]["file_name"] = image_name
            imported_data[channel]["metadata"][i]["channel"] = channel
            imported_data[channel]["metadata"][i]["folder"] = folder
            imported_data[channel]["metadata"][i]["parent_folder"] = parent_folder
            
            imported_data[channel]["metadata"][i]["segmentation_file"] = segmentation_file
            imported_data[channel]["metadata"][i]["segmentation_channel"] = segmentation_channel
            imported_data[channel]["metadata"][i]["num_segmentations"] = 0
            
            imported_data[channel]["metadata"][i]["file_list"] = file_list
            imported_data[channel]["metadata"][i]["channel_list"] = channel_list
            imported_data[channel]["metadata"][i]["image_laplacian"] = image_laplacian
    
            imported_data[channel]["metadata"][i]["segmented"] = False
            imported_data[channel]["metadata"][i]["labelled"] = False
            imported_data[channel]["metadata"][i]["segmentation_curated"] = False
            imported_data[channel]["metadata"][i]["label_curated"] = False
            
            imported_data[channel]["metadata"][i]["image_load_path"] = image_path
            imported_data[channel]["metadata"][i]["mask_load_path"] = ""
            imported_data[channel]["metadata"][i]["label_load_path"] = ""
            
            imported_data[channel]["metadata"][i]["image_focus"] = 0
            imported_data[channel]["metadata"][i]["image_debris"] = 0
            
            paths = generate_bacseg_paths(akseg_directory, user_initial, folder, image_name, segmentation_file)
            
            imported_data[channel]["metadata"][i]["image_save_path"] = paths["image_save_path"]
            imported_data[channel]["metadata"][i]["mask_save_path"] = paths["mask_save_path"]
            imported_data[channel]["metadata"][i]["label_save_path"] = paths["label_save_path"]
            imported_data[channel]["metadata"][i]["json_save_path"] = paths["json_save_path"]

    return imported_data

def append_specific_metadata(imported_data, segmentation_channel = "Phase Contrast"):
    
    for channel, channel_data in imported_data.items():
        
        for i, (img, metadata) in enumerate(zip(channel_data["images"],channel_data["metadata"].values())):
            
            image_name = metadata["image_name"]
            
            channel_name = metadata["channel_name"]
            
            species_code = "E.Coli"
            plate_name = metadata["folder"].split("_")[2]
            strain = metadata["strain"]
            
            pillar_row_index = metadata["pillar_row_index"]
            
            plate_index = int(plate_name.replace("Plate",""))
            
            species_name = "E.Coli"
            content = species_name
            
            imported_data[channel]["metadata"][i]["species_code"] = species_code
            imported_data[channel]["metadata"][i]["species_name"] = species_name
            imported_data[channel]["metadata"][i]["species_shape"] = "Rod"
            
            imported_data[channel]["metadata"][i]["strain"] = strain
            imported_data[channel]["metadata"][i]["content"] = content
            imported_data[channel]["metadata"][i]["protocol"] = ""
            
            imported_data[channel]["metadata"][i]["user_initial"] = "PT"
            
            imported_data[channel]["metadata"][i]["microscope"] = "Trillian"
            imported_data[channel]["metadata"][i]["mounting method"] = "Agarose Pads"
            
            imported_data[channel]["metadata"][i]["user_meta1"] = "Trillian DFP Sept23"
            imported_data[channel]["metadata"][i]["user_meta2"] = f"Repeat{pillar_row_index}"
            imported_data[channel]["metadata"][i]["user_meta3"] = ""
            imported_data[channel]["metadata"][i]["user_meta4"] = ""
            imported_data[channel]["metadata"][i]["user_meta5"] = ""
            imported_data[channel]["metadata"][i]["user_meta6"] = ""
            
    return imported_data


def upload_data(imported_data, user_metadata_columns):
    
    file_meta_list = []
    
    try:

        for channel, channel_data in imported_data.items():
            
            for i, (img, metadata) in enumerate(zip(channel_data["images"],channel_data["metadata"].values())):
                
                file_meta = {}
                
                file_meta = {}
            
                for column in user_metadata_columns:
                    
                    if column in metadata.keys():
                        
                        file_meta[column] = metadata[column]
        
                image_name = metadata["image_name"]
                image_channel = metadata["channel"]
                segmentation_channel = metadata["segmentation_channel"]
                
                image_save_path = metadata["image_save_path"]
                mask_save_path = metadata["mask_save_path"]
                label_save_path = metadata["label_save_path"]
                json_save_path = metadata["json_save_path"]
                
                mask = np.zeros(img.shape, dtype=np.uint16)
                
                tifffile.imwrite(image_save_path, img, metadata=metadata)
                
                if image_channel == segmentation_channel:
                    
                    export_coco_json(image_name, img, mask, mask, mask, json_save_path)
                    
                    tifffile.imwrite(mask_save_path, mask, metadata=metadata)
                    tifffile.imwrite(label_save_path, mask, metadata=metadata)
                    
                file_meta_list.append(file_meta)
                
    except:
        print(traceback.format_exc())
        pass
            
    return file_meta_list


def check_channels_missing(imported_data):
    
    channel_dict = {}
    
    for channel, channel_data in imported_data.items():
        
        for i, (img, metadata) in enumerate(zip(channel_data["images"],channel_data["metadata"].values())):
            
            if channel not in channel_dict.keys():
                channel_dict[channel] = 0
            else:
                channel_dict[channel] +=1
    
    if len(set(channel_dict.values())) == 1:
        channels_missing = False
    else:
        channels_missing = True
        
    return channels_missing


def upload_fov(fov, tile_shape=(), akseg_directory = "", user_initial = "PT", segmentation_channel = "Phase Contrast"):

    imported_data = import_zeiss_fov(fov, 
                                      tile_shape=tile_shape)
    
    imported_data = append_generic_metadata(imported_data, 
                                            akseg_directory=akseg_directory, 
                                            user_initial = user_initial, 
                                            segmentation_channel = segmentation_channel)
    imported_data = append_specific_metadata(imported_data)
    
    channels_missing = check_channels_missing(imported_data)
    
    if channels_missing == False:
        
        file_meta_list = upload_data(imported_data, user_metadata_columns)
        
    else:
        
        file_meta_list = []

    return file_meta_list












os.chdir(r"G:\Piers\DFP Sept2023")
      
akseg_directory = r"\\physics\dfs\DAQ\CondensedMatterGroups\AKGroup\Piers\AKSEG" 

user_metadata_path = r"\\physics\dfs\DAQ\CondensedMatterGroups\AKGroup\Piers\AKSEG\Images\PT\PT_file_metadata.txt"

user_metadata = pd.read_csv(user_metadata_path, converters={'channel_list': lambda x: x.strip("[]").split(", "),
                                                'file_list': lambda x: x.strip("[]").split(", ")}, low_memory=False)

user_metadata = user_metadata[user_metadata["user_meta1"] != "Trillian DFP Sept23"]

user_metadata_columns = user_metadata.columns.tolist()

user_initial = "PT"

path = r"G:\Piers\DFP Sept2023\040923_DFP_Plate2_Gentamicin\040923_DFP_Gentamicin_TOP.czi"  

plate_info = pd.read_excel("Sample_sheet_DFP_May_June_July_2023.xlsx")
 
plate_info = plate_info[(plate_info["Plate"] == "Plate_2") &
                        (plate_info["Antibiotic"] == "GENT")]

czi_fovs, channel_names = get_zeiss_measurements(path, plate_info)

if __name__=='__main__':
    
    new_metadata = []
    
    with Pool(12) as p:
        
        file_meta = list(tqdm.tqdm(
            p.imap(
                partial(
                    upload_fov,
                    tile_shape=(1024,1024),
                    akseg_directory=akseg_directory,
                    user_initial = "PT", 
                    segmentation_channel = "Phase Contrast"
                    ),
                czi_fovs), 
            total=len(czi_fovs)))
        
        p.close()
        p.join()
 
        file_meta = [dat for dat in file_meta if file_meta !=None]
        
        for meta in file_meta:
            new_metadata.extend(meta)
        
    with open('new_metadata.pickle', 'wb') as handle:
        pickle.dump(new_metadata, handle, protocol=pickle.HIGHEST_PROTOCOL)

    with open('new_metadata.pickle', 'rb') as handle:
        new_metadata = pickle.load(handle)

    new_metadata = pd.DataFrame(new_metadata)
    
    new_metadata.drop_duplicates(subset=['akseg_hash','segmentation_file'], keep="last", inplace=True)  

    user_metadata = pd.concat((user_metadata,new_metadata))
    
    user_metadata.drop_duplicates(subset=['akseg_hash'], keep="last", inplace=True)  
    
    user_metadata.to_csv(user_metadata_path, sep=",", index = False)
    
    
    
    
    
    
    
    
#     with CziFile(path) as czi:
        
#         image = czi.asarray(S=0, C=0)
        
        # help(czi)
  
        
# import czifile

# ci


# help(czifile)
    

# path = fov["path"].unique()[0]

# import czifile

# with czifile.CziFile(path) as czi:
    
#     pass


















