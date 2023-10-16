# -*- coding: utf-8 -*-
"""
Created on Tue Oct 18 17:19:48 2022

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
import tempfile
# from datetime import datetime
from skimage.registration import phase_cross_correlation
from skimage.registration._phase_cross_correlation import _upsampled_dft
import tifffile
import matplotlib.pyplot as plt
import scipy



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



def get_filename_meta(file_name, folder, image_content = None, user_initial = None):

    mount = {'AGR':'Agarose Pads','CHI':'Chitosan','PLL':'Poly-l-lytsine'}
    protocol = {'AMRv1':'AMRv1','AMRv2':'AMRv2','AMRv3':'AMRv3'}
    user_initial = {'PT':'PT','AZ':'AZ','CF':'CF','SC':'SC'}
    image_content ={'MG1655LAB':'E.Coli MG1655','MG1655':'E.Coli MG1655','MG':'E.Coli MG1655',
                'L10081':'E.Coli Clinical',
                'L11037':'E.Coli Clinical',
                'L48480':'E.Coli Clinical',
                'L64017':'E.Coli Clinical',
                'L78172':'E.Coli Clinical',
                'L17667':'E.Coli Clinical',
                'L50615':'E.Coli Clinical',
                'L61712':'E.Coli Clinical',
                'L27723':'E.Coli Clinical',
                '10081':'E.Coli Clinical',
                '11037':'E.Coli Clinical',
                '48480':'E.Coli Clinical',
                '64017':'E.Coli Clinical',
                '78172':'E.Coli Clinical',
                '17667':'E.Coli Clinical',
                '50615':'E.Coli Clinical',
                '61712':'E.Coli Clinical',
                '27723':'E.Coli Clinical',
                '13834':'E.Coli Clinical',
                '13034':'E.Coli Clinical'}
    antibiotic = {'CIP':'Ciprofloxacin','RIF':'Rifampicin','KAN':'Kanamycin',
                  'AXC':'Amoxicillin/Clavulanate','XXX':None,'CRO':'Ceftriaxone',
                  'CIP+ETOH':'Ciprofloxacin','RIF+ETOH':'Rifampin',
                  'KAN+ETOH':'Kanamycin','CARB+ETOH':'Carbenicillin',
                  'WT+ETOH':'N/A',
                  "COAMOX+ETOH":"Co-amoxiclav","COAMOX+ETOH@20xEUCAST":"Co-amoxiclav",
                  "GENT+ETOH": "Gentamicin", "GENT+ETOH@20xEUCAST": "Gentamicin",
                  "CEFT+ETOH@20xEUCAST": "Ceftriaxone", "CEFT+ETOH": "Ceftriaxone"}
    abxconcentration = {'0XEUCAST':'0XEUCAST','1XEUCAST':'1XEUCAST','5XEUCAST':'5XEUCAST','20xEUCAST':"20XEUCAST",'[10xEUCAST]':"10XEUCAST",'[20xEUCAST]':"20XEUCAST",
                        '1XMIC':'1XMIC','2XMIC':'2XMIC','5XMIC':'5XMIC','10XMIC':'10XMIC'} 
    treatmenttime = {'0min':'0','10min':'10','20min':'20','30min':'30','60min':'60'}
    
    repeat = {"200818":0, "210325": 1, "210401": 2, "210403":4, "211019":5, "211025":6, "211201":7, "220223":8,
              "220816": 2, "220907":3, "220912":4, "220913":5, "220914":6, "220920":7, "220926":8}
    
    strain = {"64017":"64017", "48480":"48480", "17667":"17667", "13034":"13034"}
    
    meta_search = dict(mount=mount,
                       protocol=protocol,
                       user_initial=user_initial,
                       image_content=image_content,
                       antibiotic=antibiotic,
                       abxconcentration=abxconcentration,
                       treatmenttime=treatmenttime,
                       repeat=repeat,
                       strain = strain)
    
    meta = {}
    
    file_name_set = set(file_name.split("_"))
        
    for meta_id,value in meta_search.items():
        
        value = set(value)
        
        intersection = file_name_set.intersection(value)
        
        if len(intersection)==0:
            intersection = 'N/A'
        else:
            intersection = list(intersection)[0]
            intersection = meta_search[meta_id][intersection]
            
        meta[meta_id] = intersection
    
    
    if user_initial!=None:
        meta['user_initial']==user_initial
    
    if meta['user_initial']=='AZ':
        meta["mount"] = 'Agarose Pads'
        meta["protocol"] = 'AMRv1'
        meta["treatmenttime"] = '30min'
        
        
    if "_posXY" in file_name:
        
        fileXY = file_name.split("_posXY")[-1]
        
        if "_" in fileXY:
            fileXY = fileXY.split("_")[0]
            
        if ".tif" in fileXY:
            fileXY = fileXY.split(".tif")[0]    
            
        if fileXY.isnumeric()==False:
            fileXY = 0
        else:
            fileXY = int(fileXY)
    else:
        fileXY = 0
        
    if "_posZ" in file_name:
        
        fileZ = file_name.split("_posZ")[-1]
        
        if "_" in fileZ:
            fileZ = fileZ.split("_")[0]
            
        if ".tif" in fileZ:
            fileZ = fileZ.split(".tif")[0]    
        
        if fileZ.isnumeric()==False:
            fileZ = 0
        else:
            fileZ = int(fileXY)
    else:
        fileZ = 0
        
    meta["fileXY"] = fileXY
    meta["fileZ"] = fileZ
    
    
    if meta["antibiotic"]=="Ceftriaxone" or meta["antibiotic"]=="Co-amoxiclav":
        meta["treatmenttime"] = '60min'
        meta["abxconcentration"] = "20XEUCAST"
        
    if meta["antibiotic"]=="Rifampin" or meta["antibiotic"]=="Ciprofloxacin":
        meta["treatmenttime"] = '30min'
        meta["abxconcentration"] = "20XEUCAST"
       
    if meta["antibiotic"]=="N/A":
        meta["treatmenttime"] = 'N/A'
        
    return meta



def read_directory(file_paths):

    files = pd.DataFrame(columns=["date",
                                  "file_repeat",
                                  "path",
                                  "file_name",
                                  "file_name_length",
                                  "folder",
                                  "parent_folder",
                                  "posX",
                                  "posY",
                                  "posZ",
                                  "timestamp",
                                  "mount",
                                  "protocol",
                                  'user_initial',
                                  'image_content',
                                  'antibiotic',
                                  'abxconcentration',
                                  'treatmenttime',
                                  'repeat',
                                  'strain',
                                  'fileXY',
                                  'fileZ'])
    
    
    for i in range(len(file_paths)):
    
        path = file_paths[i]
        path = os.path.abspath(path)
    
        file_name = path.split("\\")[-1]
        folder = os.path.abspath(path).split("\\")[-2]
        parent_folder = os.path.abspath(path).split("\\")[-3]
        
        stain = file_name.split()
        
        data_folder = os.path.abspath(path).split("\\")[-4]
    
        with tifffile.TiffFile(path) as tif:
    
            tif_tags = {}
            for tag in tif.pages[0].tags.values():
                name, value = tag.name, tag.value
                tif_tags[name] = value
                
            try:
                
                if "ImageDescription" in tif_tags:
            
                    metadata = tif_tags["ImageDescription"]
                    metadata = json.loads(metadata)
            
                    laseractive = metadata["LaserActive"]
                    laserpowers = metadata["LaserPowerPercent"]
                    laserwavelength_nm = metadata["LaserWavelength_nm"]
                    timestamp = metadata["timestamp_us"]
        
                    posX, posY, posZ = metadata["StagePos_um"]
                
            except Exception:
                
                posX = 0
                posY = 0
                posZ = 0
                timestamp = None
                
                
        file_name = path.split("\\")[-1]
        
        date = file_name.split("_")[0]
        
        file_name_length = len(file_name.split("_"))
    
        data = [path, file_name, posX, posY, posZ, timestamp]
        
        if "_NR" in file_name:
            
            file_repeat = file_name.split("_NR")[1].split("_")[0]
            
        elif "_DAPI" in file_name:
            
            file_repeat = file_name.split("+NR_DAPI")[1].split("_")[0]
            
        else:
            
            file_repeat = file_name.split("_")[6]
        
        meta = get_filename_meta(file_name, folder)
        
        if file_name in mask_names:
            
            mask_path = mask_paths[mask_names.index(file_name)]
            
        else:
            
            mask_path = None
        
        if data_folder=="MG1655":
            
            meta["user_initial"] = "AZ"
            meta["mount"] = 'Agarose Pads'
            meta["protocol"] = 'AMRv1'
        
        files.loc[len(files)] = [date, file_repeat, path, file_name, file_name_length, folder, parent_folder, posX, posY, posZ, timestamp] + list(meta.values())

    return files




def add_element_to_file_name(file_name, search_element, new_element):
    
    file_name_data = file_name.split("_")

    condition_index = [i for i, dat in enumerate(file_name_data) if search_element in dat][0]
    
    file_name_data.insert(condition_index+1, new_element)
    
    file_name = "_".join(file_name_data)
    
    return file_name



def upload_data(dat):
    
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
            
            img = image_files[j]
            
            if os.path.exists(mask_path):
                mask = tifffile.imread(mask_path)
                label = np.zeros(mask.shape,dtype=np.uint16)
                label = autoClassify(mask,label)
            else:
                mask = np.zeros(img.shape, dtpye=np.uint8)
                label = np.zeros(img.shape, dtpye=np.uint8)
        
            contrast_limit, alpha, beta, gamma = autocontrast_values(img, clip_hist_percent=1)
            
            meta["image_name"] = os.path.basename(path)
            meta["file_name"] = os.path.basename(path)
            meta["image_path"] = path
            meta["folder"] = folder
            meta["parent_folder"] = parent_folder
            meta["akseg_hash"] = get_hash(img=img)
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
            meta["user_initial"] = dat["user_initial"]
            meta["image_content"]= dat["image_content"]
            meta['antibiotic'] = dat['antibiotic']
            meta["treatmenttime"] = dat["treatmenttime"]
            meta["abxconcentration"] = dat["abxconcentration"]
            meta["mount"] = dat["mount"]
            meta["protocol"] = dat["protocol"]
            meta["segmented"] = True
            meta["labelled"] = False
            meta["segmentations_curated"] = True
            meta["labels_curated"] = False
            meta["segmentations_ground_truth"] = True
            meta["labels_curated_ground_truth"] = False
            meta["file_list"] = file_list
            meta["layer_list"] = channels
            meta["channel_list"] = channels
            meta["channel"] = channel
            meta["segmentation_channel"] = segChannel
            meta["segmentation_file"] = segmentation_file
            meta["stain"] = "N/A"
            meta["microscope"] = 'JR-NIM'
            meta["modality"] = 'Epifluorescence'
            meta["light_source"] = channel
        
            img_shape = img.shape
            img_type = np.array(img).dtype
           
            image_path = meta["image_path"]
            
            image_path = os.path.join(image_path.split(os.path.basename(image_path))[0], file_name)
            
            usermeta1 = 'Zooniverse'
            
            usermeta3 = 'Repeat ' + str(repeat)
        
            if meta["image_content"]=='E.Coli MG1655':
                usermeta2 = 'Lab Strains'
            else:
                usermeta2 = 'Clinical Isolates'
        
            meta["usermeta1"] = usermeta1
            meta["usermeta2"] = usermeta2
            meta["usermeta3"] = usermeta3
            
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
        
            image_path = os.path.abspath(image_path + "\\" +  file_name)
            mask_path = os.path.abspath(mask_path + "\\" +  file_name)
            label_path = os.path.abspath(label_path + "\\" +  file_name)
            json_path = os.path.abspath(json_path + "\\" +  file_name)
            
            tifffile.imwrite(image_path, img, metadata=meta)
            tifffile.imwrite(mask_path, mask, metadata=meta)
            tifffile.imwrite(label_path, label, metadata=meta)
        
            export_coco_json(file_name, img, mask, label, json_path)
            
            date_uploaded = str(datetime.datetime.now())
            
            file_metadata = [date_uploaded,
                             date_uploaded,
                             date_uploaded,
                              file_name,
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
        print(traceback.format_exc())
        pass
        
    

    
    return user_metadata






def find_matching_mask(images,masks):

    images["mask_path"] = None
    images["mask_name"] = None
    
    for i in range(len(images)):
        
        try:
            
            dat = images.iloc[i].copy()
            
            antibiotic = dat["antibiotic"]
            repeat = dat["repeat"]
            fileXY = dat["fileXY"]
            
            mask = masks[(masks["antibiotic"]==dat["antibiotic"]) &
                          (masks["file_repeat"]==dat["file_repeat"]) &
                          (masks["fileXY"]==dat["fileXY"]) &
                          (masks["date"]==dat["date"]) &
                          (masks["strain"]==dat["strain"])]
            
            mask_path = mask["path"].unique()
            
            if len(mask_path)!=0:
                
                images.loc[i, "mask_path"] = mask_path[0]
                images.loc[i, "mask_name"] = os.path.basename(mask_path[0])
                
            else:
                images.loc[i, "mask_path"] = None
    
        except Exception:
            # print(traceback.format_exc())
            pass

    # images = images.dropna()

    return images









user_metadata_path = r"\\physics\dfs\DAQ\CondensedMatterGroups\AKGroup\Piers\AKSEG\Images\AZ\AZ_file_metadata.txt"
user_metadata = pd.read_csv(user_metadata_path, sep=",", low_memory=False)


# image_directory = r"D:\Data_for_Piers\Clinical_Isolates\All_images"
# mask_directory = r"D:\Data_for_Piers\Clinical_Isolates\All_segmentations"

# image_paths = glob(image_directory +  "*\**\*.tif")
# mask_paths = glob(mask_directory +  "*\**\*.tif")

# mask_names = [os.path.basename(path) for path in mask_paths]

# images = read_directory(image_paths)
# masks = read_directory(mask_paths)





# with open('data.pickle', 'wb') as handle:
#     pickle.dump([images,masks], handle, protocol=pickle.HIGHEST_PROTOCOL)
    
with open('data.pickle', 'rb') as handle:
    images,masks = pickle.load(handle)

images = find_matching_mask(images,masks)



# images["file_dates"] = images["file_name"].str.split("_").str[0]
# images["file_datetime"] = images["file_dates"].apply(lambda a: datetime.datetime.strptime(a, '%y%m%d').strftime('%m/%d/%Y'))

# antibiotics = np.unique(images.antibiotic)
# file_dates = np.unique(images.file_dates)

# images = images.sort_values(["repeat"])


# images["NR_file_name"] = None
# images["DAPI_file_name"] = None

images['NR_file_name'] = images["file_name"].apply(lambda x: add_element_to_file_name(x, "+", "NR")) 
images['DAPI_file_name'] = images["file_name"].apply(lambda x: add_element_to_file_name(x, "+", "DAPI")) 


# images = images[["NR_file_name","file_name","mask_path","file_repeat","fileXY"]]

# images = images.dropna()

# images = images[["NR_file_name","strain"]]

# images = images[images["file_name"].str.contains("211110_1_64017_NA_AMR_combined_1_CIP")]




# images = [images.iloc[index] for index in range(len(images))]


# if __name__=='__main__':
    
#     with Pool() as p:
        
#         d = list(tqdm.tqdm(p.imap(upload_data,images), total=len(images)))
#         p.close()
#         p.join()
        
#         new_metadata = pd.concat(d)

#     with open('new_metadata.pickle', 'wb') as handle:
#         pickle.dump(new_metadata, handle, protocol=pickle.HIGHEST_PROTOCOL)
    

with open('new_metadata.pickle', 'rb') as handle:
    new_metadata = pickle.load(handle)



user_metadata = pd.concat([user_metadata,new_metadata],ignore_index=True).reset_index(drop=True)

user_metadata = user_metadata.drop_duplicates(subset=['akseg_hash'],keep="last")

# new_metadata = new_metadata[new_metadata["user_meta3"]=="Zooniverse"]

user_metadata.to_csv(user_metadata_path, sep=",", index = False) 





# # # antibiotics = user_metadata["antibiotic"].unique()



# user_metadata = user_metadata[user_metadata["antibiotic"]is"Co-amoxiclav"]


# channels = user_metadata["channel"].unique().tolist()





























    








# with open('data.pickle', 'wb') as handle:
#     pickle.dump([images,masks], handle, protocol=pickle.HIGHEST_PROTOCOL)

# with open('data.pickle', 'rb') as handle:
#     images,masks = pickle.load(handle)


# images = images.sample(frac=1).reset_index()

# images = images[images["mask_path"]!=None]

# for i in range(100):
    
#     try:
    
#         dat = images.iloc[i]
        
#         image_path = dat["path"]
#         mask_path = dat["mask_path"]
        
#         image = tifffile.imread(image_path)[0]
#         mask = tifffile.imread(mask_path)
        
#         plt.imshow(image[200:500,100:300])
#         plt.show()
#         plt.imshow(mask[200:500,100:300])
#         plt.show()
#     except Exception:
#         pass
    








