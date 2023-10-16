# -*- coding: utf-8 -*-
"""
Created on Thu Oct 27 09:02:13 2022

@author: turnerp
"""


import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import tifffile
import cv2
import os


path = r"\\physics\dfs\DAQ\CondensedMatterGroups\AKGroup\Piers\AKSEG\Images\PT\PT_file_metadata.txt"

metadata = pd.read_csv(path, sep = ",", low_memory=False)

metadata = metadata[metadata["user_meta1"]=="Gram Stain"]


metadata = metadata[(metadata["channel"]=="Trans") & (metadata["segmentation_curated"]==False)]



species = metadata.groupby(["content"]).count()

# # user_meta1 = metadata["user_meta1"].unique()