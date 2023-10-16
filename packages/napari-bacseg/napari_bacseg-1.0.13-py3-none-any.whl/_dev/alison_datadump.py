# -*- coding: utf-8 -*-
"""
Created on Fri Oct 28 09:31:21 2022

@author: turnerp
"""

import tifffile
import os
from glob2 import glob
import shutil
import numpy as np
import pandas as pd
import json
import pickle
import tifffile
import matplotlib.pyplot as plt
import cv2
import hashlib
import datetime
from multiprocessing import Pool
import tqdm
import traceback
from functools import partial
import hashlib
import tempfile
import xmltodict
from tiler import Tiler, Merger

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

def read_tif(path):

    with tifffile.TiffFile(path) as tif:
        try:
            metadata = tif.pages[0].tags["ImageDescription"].value
            metadata = json.loads(metadata)
        except Exception:
            metadata = {}

    image = tifffile.imread(path)
    
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
    
    if img!=None:
    
        img_path = tempfile.TemporaryFile(suffix=".tif").name
        
        tifffile.imwrite(img_path,img)

    with open(img_path, "rb") as f:
        bytes = f.read()  # read entire file as bytes
        
        hash_code =  hashlib.sha256(bytes).hexdigest()
        
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
    
    files = {}

    for path in paths:
        
        folder = path.split("\\")[-4]
        parent_folder = path.split("\\")[-5]

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
                    content = "E.Coli MG1655"
                    
                    if "Cam" in folder:
                        antibiotic = "Kanamycin"
                    elif "Cip" in folder:
                        antibiotic = "Ciprofloxacin"
                    else:
                        antibiotic = None

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
                                            channel_index=channel_index,
                                            content = content,
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
                                            antibiotic=antibiotic)

    return files



    
    



def read_scanr_directory(path, import_limit = "None"):

    if isinstance(path, list)==False:
        path = [path]
    
    if len(path)==1:
    
        path = os.path.abspath(path[0])

        if os.path.isfile(path)==True:

            selected_paths = [path]
            image_path = os.path.abspath(path)
            file_directory = os.path.abspath(image_path.split(image_path.split("\\")[-1])[0])
            file_paths = glob(file_directory + "*\*.tif")

        else:
            file_paths = glob(path + "*\**\*.tif", recursive=True)
            selected_paths = []
    else:
        selected_paths = [os.path.abspath(path) for path in path]
        image_path = os.path.abspath(path[0])
        file_directory = os.path.abspath(image_path.split(image_path.split("\\")[-1])[0])
        file_paths = glob(file_directory + "*\*.tif")


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

            file["folder"] = folder
            file["parent_folder"] = parent_folder

            files.append(file)

        except Exception:
            pass

    files = pd.DataFrame(files)

    num_measurements = len(files.position_index.unique())

    if import_limit=="None":
        import_limit = num_measurements
    else:
        if int(import_limit) > num_measurements:
            import_limit = num_measurements

    acquisitions = files.position_index.unique()[:int(import_limit)]

    files = files[files['position_index'] <= acquisitions[-1]]

    measurements = files.groupby(by=['folder', 'position_index', 'time_index', "z_index"])

    return files,measurements


def process_scanr_file(path, file_list, segmentation_file, tile_shape=(500,500), overlap = 10):
    
    image_name = path.split("\\")[-1]
    
    img = tifffile.imread(path)
    
    img = img[:, img.shape[-1] // 2:]
    
    tile_images = []
    tile_names = []
    tile_file_list = []
    tile_segmentation_file_list = []
    
    tiler_object = Tiler(data_shape=img.shape,
                          tile_shape=tile_shape,
                          overlap=overlap)

    for tile_id, tile in tiler_object.iterate(img):
        
        bbox = np.array(tiler_object.get_tile_bbox(tile_id=tile_id))
        bbox = bbox[..., [-2, -1]]
        y1, x1, y2, x2 = bbox[0][0], bbox[0][1], bbox[1][0], bbox[1][1]

        if y2 > img.shape[-2]:
            y2 = img.shape[-2]
        if x2 > img.shape[-1]:
            x2 = img.shape[-1]

        x2 = x2 - x1
        x1 = 0
        y2 = y2 - y1
        y1 = 0
        
        if (y2-y1, x2-x1)==tile_shape:
        
            tile_name = str(image_name).split(".")[0] + "_tile" + str(tile_id) + ".tif"
    
            tile_images.append(tile)
            tile_names.append(tile_name)
            
            tile_file_list.append([file.split(".")[0] + "_tile" + str(tile_id) + ".tif" for file in file_list])
            tile_segmentation_file_list.append(str(segmentation_file).split(".")[0] + "_tile" + str(tile_id) + ".tif")
            
    return tile_images, tile_names, tile_file_list, tile_segmentation_file_list



def upload_gramstain_data(measurement):
    
    try:

        user_metadata = pd.DataFrame(columns=["date_uploaded",
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
                                              "label_save_path"])
        
        segmentation_file = measurement[measurement["channel"]=="Trans"]["file_name"].item()
        file_list = measurement["file_name"].tolist()
        
        image_content = measurement["species_shortname"].unique()[0]
        
        channels = measurement["channel"].tolist()
        
        user_initial = "PT"
        
        for channel in channels:
        
            dat = measurement[measurement["channel"]ischannel]
        
            path = dat["path"].item()
            laser = 'LED'
            folder = dat["folder"].item()
            parent_folder = dat["parent_folder"].item()
            modality = dat["modality"].item()
            antibiotic = dat["antibiotic"].item()
            
            tiles_images, tiles_names, tiles_file_list, tile_segmentation_file_list = process_scanr_file(path, file_list, segmentation_file)
            
            meta = {}
            
            for i in range(len(tiles_images)):
                
                img = tiles_images[i]
                
                mask = np.zeros_like(img)
                label = np.zeros_like(img)
                
                image_name = tiles_names[i]
                tile_file_list = tiles_file_list[i]
                tile_segmentation_file = tile_segmentation_file_list[i]
                
                contrast_limit, alpha, beta, gamma = autocontrast_values(img)
            
                meta["image_name"] = image_name
                meta["image_path"] = path
                meta["folder"] = folder
                meta["parent_folder"] = parent_folder
                meta["akseg_hash"] = get_hash(img_path=path)
                meta["import_mode"] = "ScanR"
                meta["contrast_limit"] = contrast_limit
                meta["contrast_alpha"] = alpha
                meta["contrast_beta"] = beta
                meta["contrast_gamma"] = gamma
                meta["dims"] = [img.shape[-1], img.shape[-2]]
                meta["crop"] = [0, img.shape[-2], 0, img.shape[-1]]
            
                meta["InstrumentSerial"] = 'NA'
                meta["microscope"] = 'ScanR'
                meta["modality"] = 'Epifluorescence'
                meta["light_source"] = 'LED'
                meta["stain"] = ""
            
                img_shape = img.shape
                img_type = np.array(img).dtype
            
                meta["akseg_hash"] = get_hash(img=img)
                
                meta["user_initial"] = "PT"
                meta["image_content"]= image_content
                meta['antibiotic'] = antibiotic
                meta["treatmenttime"] = ""
                meta["abxconcentration"] = ""
                meta["mount"] = "Agarose Pads"
                meta["protocol"] = ""
                
                meta["segmented"] = False
                meta["labelled"] = False
                meta["segmentations_curated"] = False
                meta["labels_curated"] = False
                
                meta["file_list"] = tile_file_list
                meta["layer_list"] = channels
                meta["channel_list"] = channels
                meta["channel"] = channel
                meta["segmentation_channel"] = 'Trans'
                meta["segmentation_file"] = tile_segmentation_file
        
                meta["usermeta1"] = "Gram Stain"
                meta["usermeta2"] = None
                meta["usermeta3"] = None
        
                akseg_dir = r"\\physics\dfs\DAQ\CondensedMatterGroups\AKGroup\Piers\AKSEG\Images"
            
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
                   
                image_path = os.path.abspath(image_path + "\\" +  image_name)
                mask_path = os.path.abspath(mask_path + "\\" +  image_name)
                label_path = os.path.abspath(label_path + "\\" +  image_name)
                json_path = os.path.abspath(json_path + "\\" +  image_name)
                
                tifffile.imwrite(image_path, img, metadata=meta)
                tifffile.imwrite(mask_path, mask, metadata=meta)
                tifffile.imwrite(label_path, label, metadata=meta)
                   
                export_coco_json(image_name, img, mask, label, json_path)
                
                date_uploaded = str(datetime.datetime.now())
                
                file_metadata = [date_uploaded,
                                 date_uploaded,
                                 date_uploaded,
                                  image_name,
                                  channel,
                                  str(meta["file_list"]),
                                  str(meta["channel_list"]),
                                  meta["segmentation_file"],
                                  str(meta["segmentation_channel"]),
                                  meta["akseg_hash"],
                                  meta["user_initial"],
                                  meta["image_content"],
                                  meta["microscope"],
                                  meta["modality"],
                                  meta["light_source"],
                                  str(meta["stain"]),
                                  meta["antibiotic"],
                                  meta["treatmenttime"],
                                  meta["abxconcentration"],
                                  meta["mount"],
                                  meta["protocol"],
                                  meta["usermeta1"],
                                  meta["usermeta2"],
                                  meta["usermeta3"],
                                  folder,
                                  parent_folder,
                                  meta["segmented"],
                                  meta["labelled"],
                                  meta["segmentations_curated"],
                                  meta["labels_curated"],
                                  dat["posX"],
                                  dat["posY"],
                                  dat["posZ"],
                                  meta["image_path"],
                                  image_path,
                                  mask_path,
                                  mask_path,
                                  label_path,
                                  label_path]
                
                user_metadata.loc[len(user_metadata)] = file_metadata
                
    except Exception:
        user_metadata = None
        print(traceback.format_exc())
        pass
            
    return user_metadata

user_metadata_path = r"\\physics\dfs\DAQ\CondensedMatterGroups\AKGroup\Piers\AKSEG\Images\AF\AF_file_metadata.txt"
akseg_metadata = pd.read_csv(user_metadata_path, sep = ",", low_memory=False)


gram_metadata = akseg_metadata[akseg_metadata["user_meta1"]=="Gram Stain"]

file_directory = r"\\physics\dfs\DAQ\CondensedMatterGroups\AKGroup\Alison\20221021 ScanR MG1655 L17667 Cam Cip"


files, measurements = read_scanr_directory(file_directory)


# species = files["species_shortname"].unique().tolist()


# measurements = [measurements.get_group(list(measurements.groups)[i]) for i in np.arange(len(measurements))]

# if __name__=='__main__':
    
#     with Pool() as p:
        
#         d = list(tqdm.tqdm(p.imap(upload_gramstain_data,measurements), total=len(measurements)))
#         p.close()
#         p.join()
        
#         d = [dat for dat in d if dat!=None]
        
#         new_metadata = pd.concat(d)

#     with open('new_metadata.pickle', 'wb') as handle:
#         pickle.dump(new_metadata, handle, protocol=pickle.HIGHEST_PROTOCOL)

#     with open('new_metadata.pickle', 'rb') as handle:
#         new_metadata = pickle.load(handle)
    
#     akseg_metadata = pd.concat((akseg_metadata,new_metadata))
    
#     akseg_metadata.drop_duplicates(subset=['akseg_hash'], keep="last", inplace=True)
    
#     # gram_metadata = akseg_metadata[akseg_metadata["user_meta1"]=="Gram Stain"]
    
#     akseg_metadata.to_csv(user_metadata_path, sep=",", index = False)
    
    
    










