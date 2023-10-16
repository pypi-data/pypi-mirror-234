# -*- coding: utf-8 -*-
"""
Created on Tue Aug 16 10:26:33 2022

@author: turnerp
"""

import tifffile
from PIL import Image, ExifTags
import numpy as np
import matplotlib.pyplot as plt

path = r"C:\Users\turnerp\Downloads\stride.jpg"

img = Image.open(path)

img = np.asarray(img)

if len(img.shape) < 3:
    img = np.expand_dims(img, 0)
else:
    img = np.moveaxis(img, -1, 0)


tifffile.imwrite(r"C:\Users\turnerp\Downloads\stride.tif",img)




# exif = { ExifTags.TAGS[k]: v for k, v in img._getexif().items() if k in ExifTags.TAGS }




