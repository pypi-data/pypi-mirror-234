# -*- coding: utf-8 -*-
"""
Created on Fri Sep  2 12:46:40 2022

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


def normalize99(X):
    """ normalize image so 0.0==0.01st percentile and 1.0==99.99th percentile """
    X = X.copy()
    
    if np.max(X) > 0:
        
        v_min, v_max = np.percentile(X[X!=0], (0.01, 99.99))
        X = exposure.rescale_intensity(X, in_range=(v_min, v_max))
        
    return X

def rescale01(x):
    """ normalize image from 0 to 1 """
    
    if np.max(x) > 0:

        x = (x - np.min(x)) / (np.max(x) - np.min(x))
           
    x = x.astype(np.float64)

    return x


def align_images(images):
    
    shift, error, diffphase = phase_cross_correlation(images[0], images[1], upsample_factor=100)
    images[1] = scipy.ndimage.shift(images[1], shift)
    
    images = np.stack([images[0],images[1],np.zeros(images[0].shape,dtype=np.uint16)])
    
    images = np.moveaxis(images,0,-1)
    
    images = images.astype(np.uint16)
    
    return images
        
def align_rgb_image(image):
    
    img0 = image[:,:,0]
    img1 = image[:,:,1]
    
    shift, error, diffphase = phase_cross_correlation(img0, img1, upsample_factor=100)
    img1 = scipy.ndimage.shift(img1, shift)
    
    shift_distance = (shift[0]**2 + shift[1]**2)**0.5 

    image[:,:,1] = img1
    
    return image, shift_distance


def find_contours(img):
    # finds contours of shapes, only returns the external contours of the shapes

    contours, hierarchy = cv2.findContours(img,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
    contours = sorted(contours, key=cv2.contourArea, reverse=True)
    
    return contours


def process_image(image):
    
    process_image = np.zeros(image.shape, dtype=np.uint8)
    
    for i in range(image.shape[-1]):
        
        img = image[:,:,i]
        
        img = normalize99(img)
        img = rescale01(img)
        
        img = (img*255).astype(np.uint8)
        
        process_image[:,:,i] = img
        
        
    return process_image


def resize_image(image_size, h, w, cell_image_crop):
    
    if h < image_size[0] and w < image_size[1]:
        
        seq = iaa.CenterPadToFixedSize(height=image_size[0], width=image_size[1])
        seq_det = seq.to_deterministic()
        cell_image_crop = seq_det.augment_images([cell_image_crop])[0]
        
    else:
        
        cell_image_crop = None

    return cell_image_crop


def export_zooniverse_cells(measurement):
    
    try:

        measurement.sort_values(["channel"], inplace=True, ascending=False)
        
        if "Ciprofloxacin" in measurement.antibiotic.tolist():
            phenotype = "treated"
        else:
            phenotype = "untreated"
        
        images = []
        
        mask_path = measurement.mask_save_path.tolist()[0]
        
        for path in measurement.image_save_path:
            
            images.append(tifffile.imread(path))
          
        mask = tifffile.imread(mask_path) 
        
        images = np.stack([images[0],images[1],np.zeros(images[0].shape,dtype=np.uint16)])
        image = np.moveaxis(images,0,-1)
        image = image.astype(np.uint16)
        
        mask_ids = np.unique(mask)
        
        strain = os.path.basename(mask_path).split("_")[2]
        
        file_index = 0
        
        export_directory = os.path.join(zooniverse_path)
        
        if os.path.exists(export_directory)==False:
            os.makedirs(export_directory)
        
        for mask_id in mask_ids:
            
            cnt_mask = np.zeros(mask.shape,dtype = np.uint8)
            cnt_mask[mask==mask_id] = 255
            
            cnt = find_contours(cnt_mask)[0]
            
            x, y, w, h = cv2.boundingRect(cnt)
            y1, y2, x1, x2 = y, (y + h), x, (x + w)
            
            
            if y1 > 0 and y2 < cnt_mask.shape[0] and x1 > 0 and x2 < cnt_mask.shape[1]:
                
                file_index +=1
                
                image_crop = image.copy()
                
                cnt_mask = cnt_mask[y1:y2,x1:x2]
                image_crop = image_crop[y1:y2,x1:x2,:]
                
                image_crop = process_image(image_crop)
                image_crop, shift_distance = align_rgb_image(image_crop)
                
                if shift_distance < 0.3:
                    
                    image_crop[cnt_mask == 0] = 0
                    
                    h, w = (y2-y1),(x2-x1)
                    
                    image_crop = resize_image((64,64), h, w, image_crop)
                    
                    if image_crop is not None:
                    
                        image_crop = cv2.resize(image_crop, (256,256), interpolation= cv2.INTER_LINEAR)
                    
                        cell_image_name = os.path.basename(mask_path).replace(".tif",f"_cell{file_index}.tif")
                        
                        cell_image_path = os.path.join(export_directory, cell_image_name)
                        
                        tifffile.imwrite(cell_image_path,image_crop)
                        
    except Exception:
        import traceback
        print(traceback.format_exc())
        pass
        

# zooniverse_path = r"\\physics\dfs\DAQ\CondensedMatterGroups\AKGroup\Piers\Zooniverse\dataset2022_ti"
zooniverse_path = r"C:\Users\turnerp\Documents\ZooniverseTest_titrations"

user_metadata_path = r"\\physics\dfs\DAQ\CondensedMatterGroups\AKGroup\Piers\AKSEG\Images\AZ\AZ_file_metadata.txt"
user_metadata = pd.read_csv(user_metadata_path, sep=",", low_memory=False)

user_metadata = user_metadata[user_metadata["parent_folder"] == "Aleks - DO NOT DELETE"]

user_metadata["path"] = user_metadata["image_save_path"]

channels = user_metadata["channel"].unique().tolist()
file_paths = user_metadata["image_save_path"].tolist()
measurements = user_metadata.groupby(["segmentation_file"])

measurements = [measurements.get_group(list(measurements.groups)[i]) for i in range(len(measurements))]


export_zooniverse_cells(measurements[50].copy())


if __name__=='__main__':
    
    with Pool() as p:
        
        d = list(tqdm.tqdm(p.imap(export_zooniverse_cells,measurements), total=len(measurements)))
        p.close()
        p.join()
        
        new_metadata = pd.concat(d)


        
        

        
        
    


# contours = find_contours(mask.astype(np.uint8))

# for cnt in contours:
    
#     cnt_mask = np.zeros(mask.shape,dtype = np.uint8)
#     cnt_mask[mask==mask_id] = 255
    
#     x, y, w, h = cv2.boundingRect(cnt)
#     y1, y2, x1, x2 = y, (y + h), x, (x + w)

#     # appends contour to list if the bounding coordinates are along the edge of the image
#     if y1 > 0 and y2 < cnt_mask.shape[0] and x1 > 0 and x2 < cnt_mask.shape[1]:
        
#         print(True)





















