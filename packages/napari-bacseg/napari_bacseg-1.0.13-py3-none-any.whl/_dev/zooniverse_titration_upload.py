# -*- coding: utf-8 -*-
"""
Created on Mon Mar 13 11:41:42 2023

@author: turnerp
"""

import json
import pandas as pd
import numpy as np
import tifffile
import matplotlib.pyplot as plt
import cv2
import scipy
from skimage.registration import phase_cross_correlation
from skimage.registration._phase_cross_correlation import _upsampled_dft
from skimage import exposure
from skimage import data
from imgaug import augmenters as iaa
import os
import tqdm
from multiprocessing import Pool
from glob2 import glob
import pickle
import re
import datetime
import tempfile
import hashlib
from tiler import Tiler, Merger
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
    
    imageL = image[:,:image.shape[-1]//2]
    imageR = image[:,image.shape[-1]//2:]  
    
    if np.mean(imageL) > np.mean(imageR):
        
        image = image[:,:image.shape[-1]//2]
    else:
        image = image[:,:image.shape[-1]//2]
        
    return image


def get_hash(img_path = None, img = None):
    
    hash_code = None
    
    if img is not None:
    
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



def get_folder(files):
    
    folder = ""
    parent_folder = ""

    paths = files["path"].tolist()
    
    print(paths)

    if len(paths) > 1:
        paths = np.array([path.split("\\") for path in paths]).T

        for i in range(len(paths)):
            if len(set(paths[i])) != 1:
                folder = str(paths[i - 1][0])
                parent_folder = str(paths[i - 2][0])

                break

    else:
        folder = paths[0].split("\\")[-2]
        parent_folder = paths[0].split("\\")[-3]

    return folder, parent_folder



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


  
def unfold_image(image, path, file_list, segmentation_file, tile_shape = (1024,1024), overlap = 0):
    
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
    


def read_nim_directory(path):
    
    if isinstance(path, list) == False:
        path = [path]

    if len(path) == 1:
        path = os.path.abspath(path[0])

        if os.path.isfile(path) == True:
            file_paths = [path]

        else:
            file_paths = glob(path + r"*\**\*.tif", recursive=True)
    else:
        file_paths = path

    file_paths = [file for file in file_paths if file.split(".")[-1] == "tif"]

    file_names = [path.split("\\")[-1] for path in file_paths]

    files = pd.DataFrame(columns=["path", "file_name", "folder", "parent_folder", "posX", "posY", "posZ", "laser", "timestamp", ])

    for i in range(len(file_paths)):
        try:
            path = file_paths[i]
            path = os.path.abspath(path)

            file_name = path.split("\\")[-1]
            folder = os.path.abspath(path).split("\\")[-2]
            parent_folder = os.path.abspath(path).split("\\")[-3]

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

                posX, posY, posZ = metadata["StagePos_um"]

                if True in laseractive:
                    laseractive = np.array(laseractive, dtype=bool)
                    laserpowers = np.array(laserpowers, dtype=float)
                    laserwavelength_nm = np.array(laserwavelength_nm, dtype=str)

                    # finds maximum active power
                    power = laserpowers[laseractive == True].max()

                    laser_index = np.where(laserpowers == power)

                    laser = laserwavelength_nm[laser_index][0]
                else:
                    laser = "White Light"

                file_name = path.split("\\")[-1]

                data = [path, file_name, posX, posY, posZ, laser, timestamp]

                files.loc[len(files)] = [path, file_name, folder, parent_folder, posX, posY, posZ, laser, timestamp, ]

        except:
            pass

    files[["posX", "posY", "posZ"]] = files[["posX", "posY", "posZ"]].round(decimals=0)

    files = files.sort_values(by=["timestamp", "posX", "posY", "laser"], ascending=True)
    files = files.reset_index(drop=True)
    files["aquisition"] = 0

    positions = files[["posX", "posY"]].drop_duplicates()
    channels = files["laser"].drop_duplicates().to_list()

    acquisition = 0
    lasers = []

    for i in range(len(positions)):
        posX = positions["posX"].iloc[i]
        posY = positions["posY"].iloc[i]

        data = files[(files["posX"] == posX) & (files["posY"] == posY)]

        indicies = data.index.values

        for index in indicies:
            laser = files.at[index, "laser"]

            if laser in lasers:
                acquisition += 1
                lasers = [laser]

            else:
                lasers.append(laser)

            files.at[index, "aquisition"] = acquisition

    num_measurements = len(files.aquisition.unique())

    folder, parent_folder = get_folder(files)

    files["folder"] = folder
    files["parent_folder"] = parent_folder

    measurements = files.groupby(by=["aquisition"])
    channels = files["laser"].drop_duplicates().to_list()

    channel_num = str(len(files["laser"].unique()))

    return files, measurements, file_paths, channels




def add_metadata(dat):
    
    path = dat["path"]
    file_name = dat["file_name"]
    
    dat["folder"] = path.split("\\")[-4]
    dat["parent_folder"] = path.split("\\")[-5]
    dat["antibiotic"] = "Ciprofloxacin"
    
    strain = {"36929":"36929","48480":"48480"}
    
    if "36929" in file_name:
        dat["strain"] = "36929"
    if "48480" in file_name:
        dat["strain"] = "48480"
    else:
        dat["stain"] = ""
    
    dat["abxconcentration"] = re.search(r"\[.*?]", file_name).group(0).strip("[]")
    
    if dat["laser"] == "532":
        dat["stain"] = "Nile Red"
        dat["stain_target"] = "Membrane"
        dat["source"] = dat["laser"] 
    else:
        dat["stain"] = "DAPI"
        dat["stain_target"] = "Nucleoid"
        dat["source"] = dat["laser"] 

    dat["channel"] = dat["laser"] 

    dat["content"] = "E.Coli Clinical"
    dat["microscope"] = "BIO-NIM"
    dat["modality"] = "Epifluorescence"
    dat["mount"] = 'Agarose Pads'
    dat["user_initial"] = "AZ"
    dat["protocol"] = ""
    dat["usermeta1"] = "2022 DL Paper"
    dat["usermeta2"] = "Titration"
    
    date_created = file_name.split("_")[0]
    date_created = datetime.datetime.strptime(date_created, '%y%m%d').strftime('%m/%d/%Y')
    
    dat["date_created"] = date_created
    
    dat["segmentation_channel"] = "Nile Red"


    return dat



def upload_files(dat, unfold=False, segmentation_channel = "532"):
    
    file_metadata_list = []
    
    try:
        
        segmentation_file = dat[dat["channel"]==segmentation_channel]["file_name"].iloc[0]

        file_list = dat["file_name"].tolist()
        channels = dat["channel"].tolist()
                
        for channel in dat.channel:
            
            meta = dat[dat["channel"]==channel].iloc[0].to_dict()
        
            path = meta["path"]
            folder = meta["folder"]
            user_initial = meta["user_initial"]
            
            images = tifffile.imread(path)
            
            images = np.mean(images, axis=0).astype(np.uint16)
            
            images = get_brightest_fov(images)
            
            if unfold:
                images, file_names, file_list_list, segmentation_file_list = unfold_image(images, path, file_list, segmentation_file)
            else:
                images = [images]
                file_names = [os.path.basename(path)]
                file_list_list = [file_list]
                segmentation_file_list = [segmentation_file]
                
            for img, file_name, upload_file_list, upload_segmentation_file in zip(images, file_names, file_list_list, segmentation_file_list):
                
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
                meta["layer_list"] = channels
                meta["channel_list"] = channels
                
        
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
                                  "file_list": upload_file_list,
                                  "channel_list": get_meta_value(meta, "channel_list"),
                                  "segmentation_file": upload_segmentation_file,
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
                                  "user_meta2": get_meta_value(meta, "usermeta1"),
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
        pass
    
    return file_metadata_list





# nim_directory = r"E:\Aleks\Aleks - DO NOT DELETE"

# files, measurements, file_paths, channels = read_nim_directory(nim_directory)
    

# with open('titration_measurements.pickle', 'wb') as handle:
#     pickle.dump([files, measurements, file_paths, channels], handle, protocol=pickle.HIGHEST_PROTOCOL)

# with open('titration_measurements.pickle', 'rb') as handle:
#     files, measurements, file_paths, channels = pickle.load(handle)


# files = files.apply(lambda dat: add_metadata(dat), axis=1)

# measurements = files.groupby(by=["aquisition"])
# channels = files["laser"].drop_duplicates().to_list()

# channel_num = str(len(files["laser"].unique()))


# with open('titration_measurements.pickle', 'wb') as handle:
#     pickle.dump([files, measurements, file_paths, channels], handle, protocol=pickle.HIGHEST_PROTOCOL)

with open('titration_measurements.pickle', 'rb') as handle:
    files, measurements, file_paths, channels = pickle.load(handle)


measurements = [measurements.get_group(list(measurements.groups)[i]) for i in np.arange(len(measurements))]

measurements = [dat for dat in measurements if len(dat)==2]

segmentation_channel = "532"

user_initial = "AZ"

user_metadata_path = os.path.join(r"\\physics\dfs\DAQ\CondensedMatterGroups\AKGroup\Piers\AKSEG\Images", user_initial, f"{user_initial}_file_metadata.txt")
user_metadata = pd.read_csv(user_metadata_path, sep=",", low_memory=False)



if __name__=='__main__':
    
    with Pool() as p:
        
        results = list(tqdm.tqdm(p.imap(upload_files,measurements), total=len(measurements)))
        p.close()
        p.join()
        
        results = [item for item in results if results!=None]
        results = [file_metadata for file_metadata_list in results for file_metadata in file_metadata_list if file_metadata!=None]
        
        new_metadata = pd.DataFrame.from_dict(results)

    with open('new_metadata.pickle', 'wb') as handle:
        pickle.dump(new_metadata, handle, protocol=pickle.HIGHEST_PROTOCOL)

    # with open('new_metadata.pickle', 'rb') as handle:
    #     new_metadata = pickle.load(handle)

    user_metadata = pd.concat([user_metadata,new_metadata],ignore_index=True).reset_index(drop=True)
    
    user_metadata = user_metadata.drop_duplicates(subset=['akseg_hash'],keep="last")
    
    user_metadata.to_csv(user_metadata_path, sep=",", index = False) 














































# nim_folders = glob(nim_directory+"\*")

# titration_files = []



# path = nim_folders[0]

# file_paths = glob(r"D:\Data_for_Piers\Titration\20220524_220523_1_1_AMR_AZ_36929_CIP+ETOH_DAPI+NR_[01]\NR1\pos_0\*.tif")

# if isinstance(path, list) == False:
#     path = [path]
    
# if len(path) == 1:
#     path = os.path.abspath(path[0])

#     print(path)

#     if os.path.isfile(path) == True:
#         file_paths = [path]
        
#     else:
#         file_paths = glob(path + r"*\*\*\*\*.tif")
#         print(len(file_paths))
# else:
#     file_paths = path

# # file_paths = [file for file in file_paths if file.split(".")[-1] == "tif"]

# # file_names = [path.split("\\")[-1] for path in file_paths]













# files, measurements, file_paths, channels = read_nim_directory(nim_foders[0])


# files, measurements, file_paths, channels = read_nim_directory(nim_directory)

# with open('titration_measurements.pickle', 'wb') as handle:
#     pickle.dump([files, measurements, file_paths, channels], handle, protocol=pickle.HIGHEST_PROTOCOL)

# with open('titration_measurements.pickle', 'rb') as handle:
#     files, measurements, file_paths, channels = pickle.load(handle)

