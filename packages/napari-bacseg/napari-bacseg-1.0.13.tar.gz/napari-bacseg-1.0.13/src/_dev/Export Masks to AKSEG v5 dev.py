# -*- coding: utf-8 -*-
"""
Created on Sun Oct 16 11:17:56 2022

@author: turnerp
"""

import tifffile
import os

# os.system(os.path.abspath(r"C:\\"))

path = r"'D:\\AKSEG Images\\Images\\Aleks\\Phenotype detection complete repeats new convention new antibiotics\\Repeat_7_20_09_22\\20220920_220920_1_1_AMR_AZ_MG1655_COAMOX+ETOH_DAPI+NR\\DAPI1\\pos_0\\220920_1_1_AMR_AZ_MG1655_COAMOX+ETOH_DAPI+NR_DAPI1_posXY0_channels_t0_posZ0.tif'"



# print(os.getcwd())

# print(os.path.abspath(path))

# print(path)

image = tifffile.imread(path)
