

import numpy as np
import tifffile
import scipy
import matplotlib.pyplot as plt
from skimage import exposure
from skimage.registration import phase_cross_correlation
import copy
import cv2

images = tifffile.imread(r"\\physics\dfs\DAQ\CondensedMatterGroups\AKGroup\Piers\From Hafez\DUP_correct bleach timelapse-1secon5off.tif")

images = [img for img in images]

def normalize99(X):
    """normalize image so 0.0 is 0.01st percentile and 1.0 is 99.99th percentile"""

    if np.max(X) > 0:
        X = X.copy()
        v_min, v_max = np.percentile(X[X != 0], (0.1, 99.9))
        X = exposure.rescale_intensity(X, in_range=(v_min, v_max))

    return X


def process_image(img):
    
    img = normalize99(img)
    
    img = cv2.GaussianBlur(img,(5,5),0)
    _,img = cv2.threshold(img,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    
    return img


images[0] = normalize99(images[0])

for i in range(len(images)-1):
    
    anchor_image = normalize99(images[0])
    anchor_binary = process_image(images[0])
    
    target_image = images[i+1]
    target_binary = process_image(images[i+1])

    
    shift, error, diffphase = phase_cross_correlation(anchor_binary, target_binary, upsample_factor=100)
    shifted_img = scipy.ndimage.shift(target_image, shift)
    
    images[i+1] = normalize99(shifted_img)
    

images = np.stack(images)

tifffile.imwrite(r"\\physics\dfs\DAQ\CondensedMatterGroups\AKGroup\Piers\From Hafez\DUP_correct bleach timelapse-1secon5off_undrifted.tif", images)
