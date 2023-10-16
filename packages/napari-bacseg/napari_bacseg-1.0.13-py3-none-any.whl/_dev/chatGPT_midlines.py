

import tifffile
import cv2
import numpy as np
import matplotlib.pyplot as plt
import numpy as np
from skimage import measure, morphology, filters
from scipy.interpolate import splprep, splev
from scipy.sparse.csgraph import shortest_path
from skimage.measure import regionprops, label
from skimage.morphology import medial_axis

mask_path = r"test_mask.tif"

mask_stack = tifffile.imread(mask_path)

mask_ids = np.unique(mask_stack).tolist()[10:11]

for mask_id in mask_ids:
    
    smoothing= True
    num_points = 100
    
    binary_mask = np.zeros_like(mask_stack, dtype=np.uint8)
    binary_mask[mask_stack == mask_id] = 255
    
 
    skeleton, distance = medial_axis(binary_mask, return_distance=True)

    # Get the regions from the labeled binary mask
    labeled_mask = label(binary_mask)
    region = regionprops(labeled_mask)[0]

    # Determine the endpoints of the midline
    y1, x1 = np.unravel_index(np.argmax(distance * (skeleton > 0)), distance.shape).tolist()
    y2, x2 = region.perimeter
    midline_endpoints = [(x1, y1), (x2, y2)]

    # Draw the midline using the endpoints
    midline_mask = np.zeros_like(binary_mask)
    cv2.line(midline_mask, midline_endpoints[0], midline_endpoints[1], 1, thickness=2)

