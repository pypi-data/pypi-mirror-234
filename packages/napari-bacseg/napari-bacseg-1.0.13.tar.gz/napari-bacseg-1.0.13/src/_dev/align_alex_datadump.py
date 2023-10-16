# -*- coding: utf-8 -*-
"""
Created on Thu Jan 12 11:56:42 2023

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
    
    meta_search = dict(mount=mount,
                       protocol=protocol,
                       user_initial=user_initial,
                       image_content=image_content,
                       antibiotic=antibiotic,
                       abxconcentration=abxconcentration,
                       treatmenttime=treatmenttime,
                       repeat=repeat)
    
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
                                  'fileXY',
                                  'fileZ'])
    
    
    for i in range(len(file_paths)):
    
        path = file_paths[i]
        path = os.path.abspath(path)
    
        file_name = path.split("\\")[-1]
        folder = os.path.abspath(path).split("\\")[-2]
        parent_folder = os.path.abspath(path).split("\\")[-3]
        
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

def find_matching_mask(images,masks):

    images["mask_path"] = None
    
    for i in range(len(images)):
        
        dat = images.iloc[i].copy()
        
        antibiotic = dat["antibiotic"]
        repeat = dat["repeat"]
        fileXY = dat["fileXY"]
        
        mask = masks[(masks["antibiotic"]==dat["antibiotic"]) &
                      (masks["file_repeat"]==dat["file_repeat"]) &
                      (masks["fileXY"]==dat["fileXY"]) &
                      (masks["date"]==dat["date"])]
        
        mask_path = mask["path"]
        
        if len(mask_path)!=0:
            
            images.loc[i, "mask_path"] = mask["path"].item()

    return images


def add_element_to_file_name(file_name, search_element, new_element):
    
    file_name_data = file_name.split("_")

    condition_index = [i for i, dat in enumerate(file_name_data) if search_element in dat][0]
    
    file_name_data.insert(condition_index+1, new_element)
    
    file_name = "_".join(file_name_data)
    
    return file_name


user_metadata_path = r"\\physics\dfs\DAQ\CondensedMatterGroups\AKGroup\Piers\AKSEG\Images\AZ\AZ_file_metadata.txt"
user_metadata = pd.read_csv(user_metadata_path, sep=",", low_memory=False)


image_directory = r"D:\Data_for_Piers\MG1655\All_images"
mask_directory = r"D:\Data_for_Piers\MG1655\All_segmentations"

image_paths = glob(image_directory +  "*\**\*.tif")
mask_paths = glob(mask_directory +  "*\**\*.tif")

mask_names = [os.path.basename(path) for path in mask_paths]

images = read_directory(image_paths)
masks = read_directory(mask_paths)

images = find_matching_mask(images,masks)

with open('data.pickle', 'wb') as handle:
    pickle.dump([images,masks], handle, protocol=pickle.HIGHEST_PROTOCOL)

with open('data.pickle', 'rb') as handle:
    images,masks = pickle.load(handle)


