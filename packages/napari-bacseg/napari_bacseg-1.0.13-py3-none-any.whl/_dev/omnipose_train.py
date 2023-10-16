# -*- coding: utf-8 -*-
"""
Created on Fri Feb 17 10:21:55 2023

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


import torch



images = glob(r"C:\napari-akseg\src\napari_bacseg\_dev\omnipose_train\images\*.tif")
masks = glob(r"C:\napari-akseg\src\napari_bacseg\_dev\omnipose_train\masks\*.tif")

images = [tifffile.imread(path) for path in images]
masks = [tifffile.imread(path) for path in masks]

images = [np.swapaxes(img, -1, 0) for img in images]



import cellpose
import omnipose
from cellpose import models, dynamics




from omnipose.core import labels_to_flows, masks_to_flows, compute_masks
import torch

model = None
gpu = False

model_type = "cyto"

if torch.cuda.is_available():
    gpu = True
    torch.cuda.empty_cache()


OMNI_MODELS = ['bact_phase_cp',
                'bact_fluor_cp',
                'plant_cp', # 2D model
                'worm_cp',
                'cyto2_omni',
                'bact_phase_omni',
                'bact_fluor_omni',
                'plant_omni', #3D model 
                'worm_omni',
                'worm_bact_omni',
                'worm_high_res_omni']


if "_omni" in model_type:

    model = models.CellposeModel(diam_mean=15,
                                  model_type=model_type,
                                  gpu=gpu,
                                  net_avg=False)
    
    flows = omnipose.core.labels_to_flows(masks,
                                          use_gpu=False,
                                          device=None,
                                          redo_flows=False,
                                          omni=True)
    
else:
    
    model = models.CellposeModel(diam_mean=15,
                                  model_type=model_type,
                                  gpu=gpu,
                                  net_avg=False)
    
    flows = cellpose.dynamics.labels_to_flows(masks, use_gpu=False,
                                              device=None, redo_flows=False)
    
    
    
mask, flow, diam = model.eval(images,
                              diameter=15,
                              channels=[0, 0],
                              flow_threshold=0.9,
                              cellprob_threshold=0.1,
                              min_size=10,
                              batch_size = 3)


# pretrained_model = model.train(images,
#                                 flows,
#                                 channels = [0,0],
#                                 batch_size = 3,
#                                 n_epochs = 1,
#                                 save_path="",
#                                 save_every=1)    
    
    

































