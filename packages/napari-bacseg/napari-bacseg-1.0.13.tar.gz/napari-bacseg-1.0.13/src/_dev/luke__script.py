# -*- coding: utf-8 -*-
"""
Created on Wed Oct 19 16:59:03 2022

@author: turnerp
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import tifffile
import cv2
import os



def akseg_metadata():
    
    

    path = r"\\physics\dfs\DAQ\CondensedMatterGroups\AKGroup\Piers\AKSEG\Images\AZ\AZ_file_metadata.txt"
    
    metadata = pd.read_csv(path, sep = ",")
    
    metadata = metadata[(metadata["user_meta1"]=="2021 DL Paper") &
                        (metadata["user_meta2"]=="Lab Strains") &
                        (metadata["segmentation_curated"]==True)]
    
    antibiotic_list = metadata["antibiotic"].unique()
    
    return metadata, antibiotic_list


def find_contours(img):
    
    # finds contours of shapes, only returns the external contours of the shapes
    contours, hierarchy = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    contours = sorted(contours, key=cv2.contourArea, reverse=True)
    
    return contours

def analyse_contours(cnt):
    
    try:
        area = cv2.contourArea(cnt)
    except Exception:
        area = None

    try:
        hull = cv2.convexHull(cnt)
        hull_area = cv2.contourArea(hull)
        solidity = float(area) / hull_area
    except Exception:
        solidity = None
    
    # perimiter
    try:
        perimeter = cv2.arcLength(cnt, True)
    except Exception:
        perimeter = None
    
        # area/perimeter
    try:
        aOp = area / perimeter
    except Exception:
        aOp = None
    
    # bounding rectangle
    try:
        x, y, w, h = cv2.boundingRect(cnt)
        rect_area = w * h
        # cell crop
        y1, y2, x1, x2 = y, (y + h), x, (x + w)
    except Exception:
        y1, y2, x1, x2 = None, None, None, None
    
    # calculates moments, and centre of flake coordinates
    try:
        M = cv2.moments(cnt)
        cx = int(M['m10'] / M['m00'])
        cy = int(M['m01'] / M['m00'])
        cell_centre = [int(cx), int(cy)]
    except Exception:
        cx = None
        cy = None
        cell_centre = [None, None]
     
    contour_metrics = dict(numpy_BBOX=[x1, x2, y1, y2],
                           cell_centre=cell_centre,
                           cell_area=area,
                           circumference=perimeter,
                           solidity=solidity,
                           aOp=aOp)
    return contour_metrics

def merge_two_dicts(x, y):
    
    z = x.copy()
    z.update(y)
    
    return z

def get_contour_metrics(metadata):

    contour_dataset = []
    
    for i in range(len(metadata)):
        
        data = metadata.iloc[i]
        
        image_path = data["image_save_path"]
        mask_path = data["mask_save_path"]
        antibiotic = data["antibiotic"]
        
        image = tifffile.imread(image_path)
        mask = tifffile.imread(mask_path)
        
        mask_ids = np.unique(mask)
        
        file_name = os.path.basename(image_path)
    
        for j in range(len(mask_ids)):
            
            if j!=0:
            
                cell_mask = np.zeros(image.shape, dtype=np.uint8)
                cell_mask[mask==j] = 255
                
                contour = find_contours(cell_mask)[0]
                
                contour_metrics = analyse_contours(contour)
                file_info = dict(file_name=file_name, antibiotic=antibiotic)
                
                contour_metrics = merge_two_dicts(file_info, contour_metrics)
                
                contour_dataset.append(contour_metrics)
                
    contour_dataset = pd.DataFrame(contour_dataset)   

    return contour_dataset



metadata, antibiotic_list = akseg_metadata()

metadata = metadata.iloc[:100]

contour_dataset = get_contour_metrics(metadata)






 
                
            
            
            
            
            
            
            
            
            
            
            
            
            
            
        
        

        
        
        
        
    
    
    
    
    
    
    
    