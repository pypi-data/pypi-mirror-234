# -*- coding: utf-8 -*-
"""
Created on Tue Nov 15 14:45:34 2022

@author: turnerp
"""

import pandas as pd
import numpy as np
from glob2 import glob
import pickle
import os
import tifffile
from omnipose.core import labels_to_flows, masks_to_flows, compute_masks
from cellpose import plot, models, io, dynamics
import omnipose

# from cellpose import models,metrics
# from cellpose import utils, models, io, dynamics

import matplotlib.pyplot as plt
from ast import literal_eval
from datetime import datetime
import shutil
import torch
import tqdm
from multiprocessing import Pool
from itertools import repeat
import math
import json









def load_files(file_list, device=None, use_gpu=False, recalculate=False):

    images = []
    image_paths = []
    
    masks = []
    mask_paths = []
    
    flows = []
    flow_paths = []
    
    files = []
    
    for i in range(len(file_list)):
        
        try:
            load_path = file_list[i]

            file_name = os.path.basename(load_path)
            
            load_folder = os.path.abspath(load_path).split("\\")[-3]
            
            image_path = load_path.replace(load_folder,"\\images\\")
            mask_path = load_path.replace(load_folder,"\\masks\\")
            flow_path = load_path.replace(load_folder,"\\flows\\")
            flow_dir = flow_path.replace(file_name,"")
            
            image_path = os.path.abspath(image_path)
            mask_path = os.path.abspath(mask_path)
            flow_path = os.path.abspath(flow_path)
            flow_save_path = flow_path.replace(".tif","_flows.tif")
            
            image = tifffile.imread(image_path)
        
            if os.path.exists(mask_path):
                mask = tifffile.imread(mask_path)
                
                annotations = len(np.unique(mask))
                
            else:
                mask = None
            
            if os.path.exists(flow_dir)==False:
                os.makedirs(flow_dir)
                
            if recalculate==True and os.path.isfile(flow_save_path):
                os.remove(flow_save_path)
                
            if annotations > 1:
                
                images.append(image)
                image_paths.append(image_path)
                
                masks.append(mask)
                mask_paths.append(image_path)
                
                flow_paths.append(flow_path)
                

        except Exception:
            pass
        

    uncomputed_flows = [path for path in flow_paths if os.path.exists(path.replace(".tif","_flows.tif"))==False]
    
    if len(uncomputed_flows)==0 and len(flow_paths) > 0:
        
        for flow_path in flow_paths:
            flows.append(tifffile.imread(flow_path.replace(".tif","_flows.tif")))
            
    else:
        
        if os.path.exists(mask_path):
            
            flows = dynamics.labels_to_flows(masks, files=flow_paths,
                                            use_gpu=False, device=None, redo_flows=False)
        

    files = {"images":images,
            "image_paths":image_paths,
            "masks":masks,
            "mask_paths":mask_paths,
            "flows":flows,
            "flow_paths":flow_paths}
    
    return files




image_path = r"C:\napari-bacseg\src\_dev\dev_dataset\images\fake_phase_22-09-17 wt NusGPAM_22.08.43_58_AKSEG.tif"
mask_path = r"C:\napari-bacseg\src\_dev\dev_dataset\masks\fake_phase_22-09-17 wt NusGPAM_22.08.43_58_AKSEG.tif"
# flow_path = r"C:\napari-akseg\src\napari_bacseg\_dev\dev_dataset\masks\fake_phase_22-09-17 wt NusGPAM_22.08.43_58_AKSEG_flows.tif"


image = tifffile.imread(image_path)
labels = tifffile.imread(mask_path)

# flows = labels_to_flows([mask])

# labels_to_flows = omnipose.core.labels_to_flows


# train_labels = [omnipose.utils.format_labels(mask)]

# # 
# labels_to_flows(train_labels)


masks, dists, boundaries, T, mu = omnipose.core.masks_to_flows(labels, omni=True) 

plt.imshow(mu[0])
plt.show()


# flows = [np.concatenate((labels[n][np.newaxis,:,:], 
#                          dist[n][np.newaxis,:,:], 
#                          veci[n], 
#                          heat[n][np.newaxis,:,:]), axis=0).astype(np.float32)
#             for n in range(nimg)] 



# flow = tifffile.imread(flow_path)

# flow = np.max(flow[2:4],axis=0)
# # 

# plt.imshow(flow[100:200,100:200])
# plt.show()

# flows = labels_to_flows([mask], files=[flow_path], use_gpu=False, device=None, redo_flows=False)


# masks, dists, T, mu = masks_to_flows(mask, dists=None, use_gpu=True, device=None, omni=True, dim=2)

# mask, p, tr = compute_masks(mu, dists, calc_trace=True)



# fig = plt.figure(figsize=(12,5))
# plot.show_segmentation(fig, image, mask, flow, channels=[0], omni=True, bg_color=0)












