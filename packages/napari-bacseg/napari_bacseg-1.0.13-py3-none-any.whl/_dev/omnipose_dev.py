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
from tiler import Tiler, Merger
import os

def unfold_image(image, path, tile_shape = (1024,1024), overlap = 0):
    
    tiler_object = Tiler(data_shape=image.shape,
                                      tile_shape=tile_shape,
                                      overlap=overlap)

    tile_images = []

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

    return tile_images


path = glob(r"C:\napari-gapseq\src\napari_gapseq\dev\focus_test\Trans\*.tif")[6]
image = tifffile.imread(path)
image = unfold_image(image, path, (256,256))[20]



from cellpose import models, dynamics
from omnipose.core import labels_to_flows, masks_to_flows, compute_masks
import torch

model = None
gpu = False

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



model = models.CellposeModel(diam_mean=15,
                             model_type="bact_phase_omni",
                             gpu=gpu,
                             net_avg=True,
                             omni=True)

mask, flow, diam = model.eval([image],
                              diameter=15,
                              channels=[0, 0],
                              flow_threshold=0.9,
                              mask_threshold=0.1,
                              min_size=20,
                              batch_size = 3)
plt.imshow(image)
plt.show()
plt.imshow(mask[0])
plt.show()


# flows = labels_to_flows([mask], files=[flow_path], use_gpu=False, device=None, redo_flows=False)




















