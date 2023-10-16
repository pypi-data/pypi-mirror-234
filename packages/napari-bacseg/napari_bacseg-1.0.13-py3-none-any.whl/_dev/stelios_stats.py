# -*- coding: utf-8 -*-
"""
Created on Tue Nov 29 11:46:01 2022

@author: turnerp
"""

import tifffile
import cv2
import numpy as np
import matplotlib.pyplot as plt
import math

def euclidian_distance(x1, y1, x2, y2):
    distance = ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5

    return distance

def angle_of_line(x1, y1, x2, y2):
    try:
        angle = math.degrees(math.atan2(y2 - y1, x2 - x1))
    except Exception:
        angle = None

    return angle

def pca(pts):
    # Construct a buffer used by the pca analysis
    sz = len(pts)
    data_pts = np.empty((sz, 2), dtype=np.float64)
    for i in range(data_pts.shape[0]):
        data_pts[i, 0] = pts[i, 0, 0]
        data_pts[i, 1] = pts[i, 0, 1]

    # #removes duplicate contour points
    arr, uniq_cnt = np.unique(data_pts, axis=0, return_counts=True)
    data_pts = arr[uniq_cnt==1]

    # Perform PCA analysis
    mean = np.empty((0))
    mean, eigenvectors, eigenvalues = cv2.PCACompute2(data_pts, mean)

    # Store the center of the object
    cx, cy = (mean[0, 0], mean[0, 1])
    lx, ly = (cx + 0.02 * eigenvectors[0, 0] * eigenvalues[0, 0], cy + 0.02 * eigenvectors[0, 1] * eigenvalues[0, 0])
    wx, wy = (cx - 0.02 * eigenvectors[1, 0] * eigenvalues[1, 0], cy - 0.02 * eigenvectors[1, 1] * eigenvalues[1, 0])

    return cx, cy, lx, ly, wx, wy, data_pts


def get_pca_points(img, cnt, cx, cy, lx, ly, wx, wy):

    if (lx - cx)==0 or (wx - cx)==0:

        pca_error = True
        length = 0
        width = 0
        pca_points = {"lx1": 0, "ly1": 0, "lx2": 0, "ly2": 0,
                      "wx1": 0, "wy1": 0, "wx2": 0, "wy2": 0, }
    else:

        pca_error = False

        # get line slope and intercept
        length_slope = (ly - cy) / (lx - cx)
        length_intercept = cy - length_slope * cx
        width_slope = (wy - cy) / (wx - cx)
        width_intercept = cy - width_slope * cx

        lx1 = 0
        lx2 = max(img.shape)
        ly1 = length_slope * lx1 + length_intercept
        ly2 = length_slope * lx2 + length_intercept

        wx1 = 0
        wx2 = max(img.shape)
        wy1 = width_slope * wx1 + width_intercept
        wy2 = width_slope * wx2 + width_intercept

        contour_mask = np.zeros(img.shape, dtype=np.uint8)
        length_line_mask = np.zeros(img.shape, dtype=np.uint8)
        width_line_mask = np.zeros(img.shape, dtype=np.uint8)
        cv2.drawContours(contour_mask, [cnt], contourIdx=-1, color=(255, 255, 255), thickness=-1)
        cv2.line(length_line_mask, (int(lx1), int(ly1)), (int(lx2), int(ly2)), (255, 255, 255), 2)
        cv2.line(width_line_mask, (int(wx1), int(wy1)), (int(wx2), int(wy2)), (255, 255, 255), 2)

        Intersection = cv2.bitwise_and(contour_mask, length_line_mask)
        Intersection = np.array(np.where(Intersection.T==255)).T
        [[lx1, ly1], [lx2, ly2]] = np.array([Intersection[0], Intersection[-1]])

        Intersection = cv2.bitwise_and(contour_mask, width_line_mask)
        Intersection = np.array(np.where(Intersection.T==255)).T
        [[wx1, wy1], [wx2, wy2]] = np.array([Intersection[0], Intersection[-1]])

        pca_points = {"lx1": lx1, "ly1": ly1, "lx2": lx2, "ly2": ly2,
                      "wx1": wx1, "wy1": wy1, "wx2": wx2, "wy2": wy2, }

        length = euclidian_distance(lx1, ly1, lx2, ly2)
        width = euclidian_distance(wx1, wy1, wx2, wy2)

        angle = angle_of_line(lx1, ly1, lx2, ly2)

    return length, width, angle


def find_contours(img):
    
    """finds contour(s) of a mask"""

    # finds contours of shapes, only returns the external contours of the shapes
    contours, hierarchy = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    contours = sorted(contours, key=cv2.contourArea, reverse=True)
    
    return contours


def get_crop(cnt, mask):
    
    x, y, w, h = cv2.boundingRect(cnt)
    y1, y2, x1, x2 = y, (y + h), x, (x + w)
    
    
    edge = False
    if x1==0:
        edge = True
    if y1==0:
        edge = True
    if x2==mask.shape[1]:
        edge = True
    if y2==mask.shape[0]:
        edge = True
    
    cell_stats = dict(x1=x1,
                      x2=x2,
                      y1=y1,
                      y2=y2,
                      edge=edge)
    
    return cell_stats

def crop_image(img, cell_stats):
    
    x1 = cell_stats["x1"]
    x2 = cell_stats["x2"]
    y1 = cell_stats["y1"]
    y2 = cell_stats["y2"]
    
    img = img[y1:y2,x1:x2]
    
    return img



def get_contour_statistics(cnt, image, pixel_size):

    # cell area
    try:
        area = cv2.contourArea(cnt) * pixel_size**2
    except Exception:
        area = None

    # convex hull
    try:
        hull = cv2.convexHull(cnt)
        hull_area = cv2.contourArea(hull)
        solidity = float(area) / hull_area
    except Exception:
        solidity = None

    # perimiter
    try:
        perimeter = cv2.arcLength(cnt, True) * pixel_size
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

    # cell length and width from PCA analysis
    try:
        cx, cy, lx, ly, wx, wy, data_pts = pca(cnt)
        length, width, angle = get_pca_points(image, cnt, cx, cy, lx, ly, wx, wy)
        radius = width/2
        length = length * pixel_size
        width = width * pixel_size
        radius = radius * pixel_size

    except Exception:
        length = None
        width = None
        radius = None

    # asepct ratio
    try:
        aspect_ratio = length / width
    except Exception:
        aspect_ratio = None

    contour_statistics = dict(cell_centre=cell_centre,
                              cell_area=area,
                              cell_length=length,
                              cell_width=width,
                              cell_radius=radius,
                              aspect_ratio=aspect_ratio,
                              circumference=perimeter,
                              solidity=solidity,
                              aOp=aOp)
    
    return contour_statistics


def get_image_statistics(cell_image, cell_mask, cell_background):
    
    try:
        cell_brightness = int(np.mean(cell_image[cell_mask!=0]))
        cell_background_brightness = int(np.mean(cell_image[cell_background!=0]))
        cell_contrast = cell_brightness / cell_background_brightness
        cell_laplacian = int(cv2.Laplacian(cell_image, cv2.CV_64F).var())
    except Exception:
        cell_brightness = None
        cell_contrast = None
        cell_laplacian = None
            
    stats = {"cell_brightness": cell_brightness,
             "cell_background_brightness": cell_background_brightness,
              "cell_contrast": cell_contrast,
              "cell_laplacian": cell_laplacian}
    
    return stats


def get_cell_statistics(image, mask):

    mask_ids = np.unique(mask)
    cell_statistics = []
    
    for mask_id in mask_ids:
        
        if mask_id!=0:
            
            try:
            
                cell_mask = np.zeros(mask.shape, dtype=np.uint8)
                cell_background = np.zeros(mask.shape, dtype=np.uint8)
                
                cell_mask[mask==mask_id] = 255
                cell_background[mask==0] = 255
                cell_background[mask==mask_id] = 0
                
                img = image.copy()
                
                cnt = find_contours(cell_mask)[0]
                
                cell_stats = get_crop(cnt, mask)
                
                if cell_stats["edge"]==False:
                    
                    cell_img = crop_image(img, cell_stats)
                    
                    cell_mask = crop_image(cell_mask, cell_stats)
                    cell_background = crop_image(cell_background, cell_stats)
                    
                    img_masked = cell_img.copy()
                    img_background_masked = cell_img.copy()
                    
                    img_masked[cell_mask!=255]=0
                    img_background_masked[cell_background!=255]=0
                    
                    contour_stats = get_contour_statistics(cnt, image, pixel_size=0.1)
                    image_stats = get_image_statistics(cell_img, cell_mask, cell_background)
                    
                    cell_stats = {**cell_stats, **contour_stats, **image_stats}
                    
                    cell_statistics.append(cell_stats)
                    
            except Exception:
                pass
                
    return cell_statistics



image = tifffile.imread("test_image.tif")
mask = tifffile.imread("test_mask.tif")



cell_statistics = get_cell_statistics(image, mask)
            
            
        
        
        
        
    
    



