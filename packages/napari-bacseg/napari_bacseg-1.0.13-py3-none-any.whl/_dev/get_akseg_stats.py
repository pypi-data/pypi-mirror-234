# -*- coding: utf-8 -*-
"""
Created on Fri Oct 21 08:49:20 2022

@author: turnerp
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import tifffile
import cv2
import os
import math
from skimage import exposure
import tempfile
import traceback
import json
from multiprocessing import Pool
import tqdm
import warnings
from colicoords import Data, Cell, config
import pickle


def rotate_contour(cnt, angle=90, units="DEGREES"):

    x = cnt[:,:, 1].copy()
    y = cnt[:,:, 0].copy()

    x_shift, y_shift = sum(x) / len(x), sum(y) / len(y)

    # Shift to origin (0,0)
    x = x - int(x_shift)
    y = y - int(y_shift)

    # Convert degrees to radians
    if units=="DEGREES":
        angle = math.radians(angle)

    # Rotation matrix multiplication to get rotated x & y
    xr = (x * math.cos(angle)) - (y * math.sin(angle)) + x_shift
    yr = (x * math.sin(angle)) + (y * math.cos(angle)) + y_shift

    cnt[:,:, 0] = yr
    cnt[:,:, 1] = xr

    shift_xy = [x_shift[0], y_shift[0]]

    return cnt, shift_xy


def rotate_image(image, shift_xy, angle=90):

    x_shift, y_shift = shift_xy

    (h, w) = image.shape[:2]

    # Perform image rotation
    M = cv2.getRotationMatrix2D((y_shift, x_shift), angle, 1.0)
    image = cv2.warpAffine(image, M, (w, h))

    return image, shift_xy


def import_coco_json(json_path):

    with open(json_path, 'r') as f:
        dat = json.load(f)

    h = dat["images"][0]["height"]
    w = dat["images"][0]["width"]

    mask = np.zeros((h, w), dtype=np.uint16)
    labels = np.zeros((h, w), dtype=np.uint16)

    categories = {}

    for i, cat in enumerate(dat["categories"]):
        cat_id = cat["id"]
        cat_name = cat["name"]

        categories[cat_id] = cat_name

    annotations = dat["annotations"]

    for i in range(len(annotations)):
        annot = annotations[i]["segmentation"][0]
        category_id = annotations[i]["category_id"]

        cnt = np.array(annot).reshape(-1, 1, 2).astype(np.int32)

        cv2.drawContours(mask, [cnt], contourIdx=-1, color=i + 1, thickness=-1)
        cv2.drawContours(labels, [cnt], contourIdx=-1, color=category_id, thickness=-1)

    return mask, labels


def normalize99(X):
    """ normalize image so 0.0==0.01st percentile and 1.0==99.99th percentile """

    if np.max(X) > 0:
        X = X.copy()
        v_min, v_max = np.percentile(X[X!=0], (1, 99))
        X = exposure.rescale_intensity(X, in_range=(v_min, v_max))

    return X


def determine_overlap(cnt_num, contours, image):
    try:

        # gets current contour of interest
        cnt = contours[cnt_num]

        # number of pixels in contour
        cnt_pixels = len(cnt)

        # gets all other contours
        cnts = contours.copy()
        del cnts[cnt_num]

        # create mask of all contours, without contour of interest. Contours are filled
        cnts_mask = np.zeros(image.shape, dtype=np.uint8)
        cv2.drawContours(cnts_mask, cnts, contourIdx=-1, color=(1, 1, 1), thickness=-1)

        # create mask of contour of interest. Only the contour outline==drawn.
        cnt_mask = np.zeros(image.shape, dtype=np.uint8)
        cv2.drawContours(cnt_mask, [cnt], contourIdx=-1, color=(1, 1, 1), thickness=1)

        # dilate the contours mask. Neighbouring contours will now overlap.
        kernel = np.ones((3, 3), np.uint8)
        cnts_mask = cv2.dilate(cnts_mask, kernel, iterations=1)

        # get overlapping pixels
        overlap = cv2.bitwise_and(cnt_mask, cnts_mask)

        # count the number of overlapping pixels
        overlap_pixels = len(overlap[overlap==1])

        # calculate the overlap percentage
        overlap_percentage = int((overlap_pixels / cnt_pixels) * 100)

    except Exception:
        overlap_percentage = None

    return overlap_percentage


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

    contour_statistics = dict(numpy_BBOX=[x1, x2, y1, y2],
                              coco_BBOX=[x1, y1, h, w],
                              pascal_BBOX=[x1, y1, x2, y2],
                              cell_centre=cell_centre,
                              cell_area=area,
                              cell_length=length,
                              cell_width=width,
                              cell_radius=radius,
                              aspect_ratio=aspect_ratio,
                              circumference=perimeter,
                              solidity=solidity,
                              aOp=aOp)

    return contour_statistics


def angle_of_line(x1, y1, x2, y2):
    try:
        angle = math.degrees(math.atan2(y2 - y1, x2 - x1))
    except Exception:
        angle = None

    return angle


def euclidian_distance(x1, y1, x2, y2):
    distance = ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5

    return distance


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

def rotate_contour(cnt, angle=90, units="DEGREES"):

    x = cnt[:,:, 1].copy()
    y = cnt[:,:, 0].copy()

    x_shift, y_shift = sum(x) / len(x), sum(y) / len(y)

    # Shift to origin (0,0)
    x = x - int(x_shift)
    y = y - int(y_shift)

    # Convert degrees to radians
    if units=="DEGREES":
        angle = math.radians(angle)

    # Rotation matrix multiplication to get rotated x & y
    xr = (x * math.cos(angle)) - (y * math.sin(angle)) + x_shift
    yr = (x * math.sin(angle)) + (y * math.cos(angle)) + y_shift

    cnt[:,:, 0] = yr
    cnt[:,:, 1] = xr

    shift_xy = [x_shift[0], y_shift[0]]

    return cnt, shift_xy


def rotate_image(image, shift_xy, angle=90):

    x_shift, y_shift = shift_xy

    (h, w) = image.shape[:2]

    # Perform image rotation
    M = cv2.getRotationMatrix2D((y_shift, x_shift), angle, 1.0)
    image = cv2.warpAffine(image, M, (w, h))

    return image, shift_xy


def akseg_metadata():
    
    path = r"\\physics\dfs\DAQ\CondensedMatterGroups\AKGroup\Piers\AKSEG\Images\AZ\AZ_file_metadata.txt"
    
    metadata = pd.read_csv(path, sep = ",")
    
    metadata = metadata[(metadata["user_meta1"]=="2021 DL Paper") &
                        (metadata["user_meta2"]=="Lab Strains") &
                        (metadata["segmentation_curated"]==True)]
    
    antibiotic_list = metadata["antibiotic"].unique()
    
    channels = metadata.explode("channel_list")["channel_list"].unique().tolist()
    
    measurements = metadata.groupby("segmentation_file")

    return measurements


def find_contours(img):
    
    # finds contours of shapes, only returns the external contours of the shapes
    contours, hierarchy = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    contours = sorted(contours, key=cv2.contourArea, reverse=True)
    
    return contours


def merge_two_dicts(x, y):
    
    z = x.copy()
    z.update(y)
    
    return z








def fit_colicoords(images, measurement_channels, mask, mask_id, pixel_size):
    
    cell_images = images.copy()
    
    inverted_cell_mask = np.zeros(mask.shape, dtype=np.uint8)
    cell_mask = np.zeros(mask.shape, dtype=np.uint8)
    
    inverted_cell_mask[mask!=0] = 1
    inverted_cell_mask[mask==mask_id] = 0

    cell_mask[maskismask_id] = 1

    cnt = find_contours(cell_mask)[0]

    x, y, w, h = cv2.boundingRect(cnt)
    
    if h > w:
        vertical = True
        cell_mask = np.zeros(mask.shape, dtype=np.uint8)
        cnt, shift_xy = rotate_contour(cnt, angle=90)
        cell_images, shift_xy = rotate_image(cell_images, shift_xy, angle=90)
        inverted_cell_mask, shift_xy = rotate_image(inverted_cell_mask, shift_xy, angle=90)
        cv2.drawContours(cell_mask, [cnt], -1, 1, -1)
        
    else:
        vertical = False
        shift_xy = None
        
    x, y, w, h = cv2.boundingRect(cnt)
    y1, y2, x1, x2 = y, (y + h), x, (x + w)

    m = 5

    edge = False

    if y1 - 5 > 0:
        y1 = y1 - 5
    else:
        y1 = 0
        edge = True

    if y2 + 5 < cell_mask.shape[0]:
        y2 = y2 + 5
    else:
        y2 = cell_mask.shape[0]
        edge = True

    if x1 - 5 > 0:
        x1 = x1 - 5
    else:
        x1 = 0
        edge = True

    if x2 + 5 < cell_mask.shape[1]:
        x2 = x2 + 5
    else:
        x2 = cell_mask.shape[1]
        edge = True

    if edge==False:

        h, w = y2 - y1, x2 - x1
    
        inverted_cell_mask = inverted_cell_mask[y1:y2, x1:x2]
        cell_mask = cell_mask[y1:y2, x1:x2]
        cell_images = cell_images[:,y1:y2, x1:x2]
        
        cell_images[:,inverted_cell_mask==1] = 0
        cell_images = normalize99(cell_images)
        
        with warnings.catch_warnings():
            warnings.filterwarnings("ignore")
    
            data = Data()
            data.add_data(cell_mask, 'binary')
            
            for i in range(len(cell_images)):
                data.add_data(cell_images[i], 'fluorescence', name=measurement_channels[i])
                
            cell = Cell(data)
            
            colicoords_length = float(cell.length * pixel_size)
            colicoords_radius = float(cell.radius * pixel_size)
            colicoords_area = float(cell.area * pixel_size**2)
            colicoords_circumference = float(cell.circumference * pixel_size)
            colicoords_aspect_ratio = float(cell.length/(cell.radius*2))
            
            colicoords_ldist_405 = get_cell_ldist(cell, measurement_channels[0])
            colicoords_ldist_532 = get_cell_ldist(cell, measurement_channels[1])
            
    else:
        
        colicoords_length = None
        colicoords_radius = None
        colicoords_area = None
        colicoords_circumference = None
        colicoords_aspect_ratio = None
        colicoords_ldist_405 = None
        colicoords_ldist_532 = None
            
    colicoords_stats = dict(colicoords_length = colicoords_length,
                            colicoords_radius = colicoords_radius,
                            colicoords_area = colicoords_area,
                            colicoords_circumference = colicoords_circumference,
                            colicoords_aspect_ratio = colicoords_aspect_ratio,
                            colicoords_ldist_405 = colicoords_ldist_405,
                            colicoords_ldist_532 = colicoords_ldist_532)

    return colicoords_stats                        
        
        
            
            
            

        
            
            
            
            
            
            
            

    

def get_cell_ldist(cell, channel):

    nbins = config.cfg.L_DIST_NBINS
    sigma = config.cfg.L_DIST_SIGMA
    sigma_arr = sigma / cell.length

    x_arr, out_arr = cell.l_dist(nbins, data_name=channel, norm_x=True, sigma=sigma_arr)

    max_val = np.max(out_arr)

    if max_val > 0:
        out_arr = out_arr + np.flip(out_arr)

        out_arr -= np.min(out_arr)
        out_arr = out_arr / np.max(out_arr)
        
        out_arr = out_arr.astype(float)

    else:

        out_arr = None

    return out_arr




def get_cell_images(image, mask, cell_image, cell_mask, mask_id, layer_names, colicoords_dir):

    cell_image = image.copy()

    inverted_cell_mask = np.zeros(mask.shape, dtype=np.uint8)
    inverted_cell_mask[mask!=0] = 1
    inverted_cell_mask[mask==mask_id] = 0

    cnt = find_contours(cell_mask)[0]

    x, y, w, h = cv2.boundingRect(cnt)

    if h > w:
        vertical = True
        cell_mask = np.zeros(mask.shape, dtype=np.uint8)
        cnt, shift_xy = rotate_contour(cnt, angle=90)
        cell_image, shift_xy = rotate_image(cell_image, shift_xy, angle=90)
        inverted_cell_mask, shift_xy = rotate_image(inverted_cell_mask, shift_xy, angle=90)
        cv2.drawContours(cell_mask, [cnt], -1, 1, -1)
    else:
        vertical = False
        shift_xy = None

    x, y, w, h = cv2.boundingRect(cnt)
    y1, y2, x1, x2 = y, (y + h), x, (x + w)

    m = 5

    edge = False

    if y1 - 5 > 0:
        y1 = y1 - 5
    else:
        y1 = 0
        edge = True

    if y2 + 5 < cell_mask.shape[0]:
        y2 = y2 + 5
    else:
        y2 = cell_mask.shape[0]
        edge = True

    if x1 - 5 > 0:
        x1 = x1 - 5
    else:
        x1 = 0
        edge = True

    if x2 + 5 < cell_mask.shape[1]:
        x2 = x2 + 5
    else:
        x2 = cell_mask.shape[1]
        edge = True

    h, w = y2 - y1, x2 - x1

    inverted_cell_mask = inverted_cell_mask[y1:y2, x1:x2]
    cell_mask = cell_mask[y1:y2, x1:x2]
    cell_image = cell_image[:,y1:y2, x1:x2]

    for i in range(len(cell_image)):

        cell_img = cell_image[i].copy()
        cell_img[inverted_cell_mask==1] = 0
        cell_img = normalize99(cell_img)
        cell_image[i] = cell_img

    offset = [y1, x1]
    box = [y1, y2, x1, x2]

    cell_images = dict(cell_image=cell_image,
                       cell_mask=cell_mask,
                       channels=layer_names,
                       offset=offset,
                       shift_xy=shift_xy,
                       box=box,
                       edge=edge,
                       vertical=vertical,
                       mask_id=mask_id,
                       contour=cnt)

    temp_path = tempfile.TemporaryFile(prefix="colicoords", suffix=".npy", dir=colicoords_dir).name

    np.save(temp_path,cell_images)

    return temp_path


def get_layer_statistics(image, cell_mask, box, layer_names):

    layer_statistics = {}

    for i in range(len(image)):

        layer = layer_names[i]

        x1, x2, y1, y2 = box

        cell_image_crop = image[i][y1:y2, x1:x2].copy()
        cell_mask_crop = cell_mask[y1:y2, x1:x2].copy()

        try:
            cell_brightness = int(np.mean(cell_image_crop[cell_mask_crop!=0]))
            cell_background_brightness = int(np.mean(cell_image_crop[cell_mask_crop==0]))
            cell_contrast = cell_brightness / cell_background_brightness
            cell_laplacian = int(cv2.Laplacian(cell_image_crop, cv2.CV_64F).var())
        except Exception:
            cell_brightness = None
            cell_contrast = None
            cell_laplacian = None

        stats = {"cell_brightness[" + layer + "]": cell_brightness,
                 "cell_contrast[" + layer + "]": cell_contrast,
                 "cell_laplacian[" + layer + "]": cell_laplacian}

        layer_statistics = {**layer_statistics, **stats}

    layer_statistics = {key: value for key, value in sorted(layer_statistics.items())}

    return layer_statistics


def get_measurement_statistics(measurement):
    
    cell_statistics = []

    measurement = measurement[measurement["channel"].isin(["405","532"])]
    
    file_name = measurement["segmentation_file"].unique()[0]
    antibiotic = measurement["antibiotic"].unique()[0]
    
    file_names = measurement["file_name"].unique()
    measurement_channels = measurement["channel"].unique()
    
    mask = tifffile.imread(measurement.iloc[0]["mask_save_path"])
    
    label = tifffile.imread(measurement.iloc[0]["label_save_path"])
    
    cell_dict = {1: "Single", 2: "Dividing", 3: "Divided", 4: "Broken", 5: "Vertical", 6: "Edge"}
    
    image_stats = {}
    
    pixel_size = 0.116999998688698
    
    images = []
    
    file_info = dict(file_name=file_name, antibiotic=antibiotic)
    
    for i in range(len(measurement)):
        
        channel = measurement_channels[i]
        
        path = measurement.iloc[i]["image_save_path"]
        img = tifffile.imread(path)
        
        images.append(img)
        
        dat = {"image_brightness[" + channel + "]": int(np.mean(img)),
                "image_laplacian[" + channel + "]": int(cv2.Laplacian(img, cv2.CV_64F).var())}
    
        image_stats = {**image_stats, **dat}
        
    images = np.stack(images)
  
    contours = []
    contour_mask_ids = []
    cell_types = []
    mask_ids = np.unique(mask)
    
    for j in range(len(mask_ids)):
    
        mask_id = mask_ids[j]
    
        if mask_id!=0:
    
            cell_mask = np.zeros(mask.shape, dtype=np.uint8)
            cell_mask[mask==mask_id] = 1
    
            cnt = find_contours(cell_mask)[0]

            contours.append(cnt)
            contour_mask_ids.append(mask_id)
            
            try:
                background = np.zeros(mask.shape, dtype=np.uint8)
                cv2.drawContours(background, contours, contourIdx=-1, color=(1, 1, 1), thickness=-1)
            except Exception:
                background = None

    for j in range(len(contours)):
    
        try:
    
            cnt = contours[j]
            mask_id = contour_mask_ids[j]
    
            cell_mask = np.zeros(mask.shape, dtype=np.uint8)
            cv2.drawContours(cell_mask, [cnt], contourIdx=-1, color=(1, 1, 1), thickness=-1)
    
            overlap_percentage = determine_overlap(j, contours, mask)
    
            contour_statistics = get_contour_statistics(cnt, mask, pixel_size)
    
            box = contour_statistics["numpy_BBOX"]
    
            layer_stats = get_layer_statistics(images, cell_mask, box, measurement_channels)
            
            colicoords_stats = fit_colicoords(images, measurement_channels, mask, mask_id, pixel_size)
            
            morphology_stats = dict(file_names=file_names,
                                    colicoords=False,
                                    pixel_size_um=pixel_size,
                                    opencv_length=contour_statistics["cell_length"],
                                    opencv_radius=(contour_statistics["cell_radius"]),
                                    opencv_area=contour_statistics["cell_area"],
                                    opencv_circumference=contour_statistics["circumference"],
                                    opencv_aspect_ratio=contour_statistics["aspect_ratio"],
                                    opencv_solidity=contour_statistics["solidity"],
                                    overlap_percentage=overlap_percentage,
                                    box=box)
    
            stats = {**file_info, **morphology_stats, **image_stats, **layer_stats, **colicoords_stats}
            
            cell_statistics.append(stats)
    
        except Exception:
            stats = None
            print(traceback.format_exc())
            pass
          
    cell_statistics = [stats for stats in cell_statistics if stats!=None]   
          
    cell_statistics = pd.DataFrame(cell_statistics)
        
    return cell_statistics



measurements = akseg_metadata()


measurements = [measurements.get_group(list(measurements.groups)[index]) for index in range(len(measurements))][:10]



measurement = measurements[0]


# stats =  get_measurement_statistics(measurement)
    


if __name__=='__main__':
    
    with Pool() as p:
        
        pool_data = list(tqdm.tqdm(p.imap(get_measurement_statistics,measurements), total=len(measurements)))
        p.close()
        p.join()
        
        pool_data = pd.concat(pool_data)
        
        # with open('pool_data.pickle', 'wb') as handle:
        #     pickle.dump(pool_data, handle, protocol=pickle.HIGHEST_PROTOCOL)
    








    


