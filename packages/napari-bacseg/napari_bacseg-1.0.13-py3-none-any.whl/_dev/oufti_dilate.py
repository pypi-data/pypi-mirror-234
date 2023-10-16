# -*- coding: utf-8 -*-
"""
Created on Tue Feb 21 13:39:25 2023

@author: turnerp
"""



import pandas as pd
import numpy as np
from glob2 import glob
import pickle
import os
import tifffile
import cv2

from shapely.geometry import LineString, LinearRing, Point
from shapely.geometry import Polygon
from shapely.geometry.polygon import orient
from shapely.ops import nearest_points
import matplotlib.path as mpltPath
from scipy.spatial.distance import cdist
from scipy.spatial import Voronoi
import warnings
import math
import matplotlib.pyplot as plt
from shapely.ops import nearest_points
from shapely.ops import linemerge, unary_union, polygonize
from shapely.geometry import LineString, Polygon
from shapely.geometry import mapping
from shapely.ops import split
import traceback
import scipy



def moving_average(line, padding = 5, iterations = 1):
    
    x, y = line[:,0], line[:,1]
    
    x = np.concatenate((x[-padding:] , x, x[:padding]))
    y = np.concatenate((y[-padding:] , y, y[:padding]))
    
    for i in range(iterations):
    
        y = np.convolve(y, np.ones(padding), 'same') / padding
        x = np.convolve(x, np.ones(padding), 'same') / padding
    
        x = np.array(x)
        y = np.array(y)
    
    x = x[padding:-padding]
    y = y[padding:-padding]
    
    line = np.stack([x,y]).T
    
    return line

def get_boundary_lines(mid_line, cnt, smooth=True, n_segments=100):

    cnt_array = cnt.reshape(-1, 2)

    if smooth:
        cnt_array = moving_average(cnt_array)

    polygon = Polygon(cnt_array)
    midline_linestring = LineString(mid_line)
    
    intersect_splitter = midline_linestring.intersection(polygon)
    geomcollect = split(polygon, midline_linestring)
    left_line, right_line = geomcollect.geoms[0], geomcollect.geoms[1]
    
    left_line = remove_intersecting(left_line, midline_linestring)
    right_line = remove_intersecting(right_line, midline_linestring)
    
    distances = np.min(cdist(left_line,right_line), axis=0)
    distances_flip = np.min(cdist(left_line,np.flip(right_line)), axis=0)

    distances = np.sum(np.take(distances, [0,-1]))
    distances_flip = np.sum(np.take(distances_flip, [0,-1]))

    if distances_flip > distances:
        
        right_line = np.flip(right_line, axis=0)
        
    p1 = (right_line[0] + left_line[0])/2
    p2 = (right_line[-1] + left_line[-1])/2
    
    p1 = find_closest_point(p1, midline_linestring)
    p2 = find_closest_point(p2, midline_linestring)
    
    left_line = np.concatenate(([p1], left_line, [p2]))
    right_line = np.concatenate(([p1], right_line, [p2]))
    
    right_line = np.flip(right_line,axis=0)
    
    left_lineString = LineString(left_line)
    right_lineString = LineString(right_line)

    left_lineString = resize_line(left_lineString, n_segments)
    right_lineString = resize_line(right_lineString, n_segments)

    left_line = np.array(left_lineString.xy).T
    right_line = np.array(right_lineString.xy).T
    mid_line = (left_line + np.flipud(right_line)) / 2

    return left_line, right_line, mid_line, cnt_array

def fit_polyline(x, y, polys=[2, 3], margin=50, poly_limits=None):

    with warnings.catch_warnings():

        warnings.filterwarnings('ignore')

        residual_list = []
        param_list = []

        for poly in polys:
            params, residuals, rank, singular_values, rcond = np.polyfit(x.copy(), y.copy(), poly, full=True)

            residual_list.append(residuals[0])
            param_list.append(params)

        residual_list, param_list = zip(*sorted(zip(residual_list, param_list), reverse=True))

        params = param_list[0]

        p = np.poly1d(params)
        poly_params = p.c[:2]

        if poly_limits!=None:

            if len(poly_limits)==len(poly_params):

                for i, limit in enumerate(poly_limits):

                    if limit!=None:

                        if abs(poly_params[i]) >= limit:
                            params = np.polyfit(x.copy(), y.copy(), 1)
                            p = np.poly1d(params)

        x1 = np.min(x) - margin
        x2 = np.max(x) + margin

        x = np.linspace(x1, x2, 100)
        y = p(x)

        fit_line = np.stack([x, y]).T

    return fit_line


def get_voronoi_midline(cnt, smooth=True, voronoi_distance=2,
                        poly_margin=10, poly_limits=[None, 1],
                        extend = True, vertices = 100):

    try:

        polygon = cnt.reshape(-1, 2)

        if smooth:
            polygon = moving_average(polygon)

        path = mpltPath.Path(polygon)

        vor = Voronoi(cnt.reshape(-1, 2))

        vX = vor.vertices.T[0]
        vZ = vor.vertices.T[1]
        vorMask = (vX >= polygon.T[0].min()) & (vX <= polygon.T[0].max()) & (vZ >= polygon.T[1].min()) & (
                    vZ <= polygon.T[1].max())
        verts = vor.vertices[vorMask]

        insideMask = path.contains_points(verts)

        verts = verts[insideMask]

        polygon_distances = np.min(cdist(verts, polygon), axis=1)

        verts = verts[polygon_distances > voronoi_distance]

        mid_line = fit_polyline(verts[:, 0], verts[:, 1], polys=[2,3], margin=poly_margin, poly_limits=poly_limits)

        if extend==False:

            _, _, mid_line, _ = get_boundary_lines(mid_line, cnt)

        mid_line = LineString(mid_line)
        mid_line = resize_line(mid_line, vertices)
        mid_line = np.array(mid_line.xy).T
        
        
    except Exception:
        import traceback
        print(traceback.format_exc())

        mid_line = None

    return mid_line


def resize_line(mesh, mesh_length):

    distances = np.linspace(0, mesh.length, mesh_length)
    mesh = LineString([mesh.interpolate(distance) for distance in distances])

    return mesh


def line_to_array(mesh):
    mesh = np.array([mesh.xy[0][:], mesh.xy[1][:]]).T.reshape(-1, 1, 2)

    return mesh


def euclidian_distance(x1, y1, x2, y2):
    distance = ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5

    return distance


def polyarea(x, y):
    return 0.5 * np.abs(np.dot(x, np.roll(y, 1)) - np.dot(y, np.roll(x, 1)))


def rotate_contour(cnt, angle=90, units="DEGREES"):
    
    cnt = cnt.copy()

    x = cnt[:,:, 1]
    y = cnt[:,:, 0]

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


def rotate_model(model, shift_xy, angle=-90, units="DEGREES"):
    
    x = model[:, 1].copy()
    y = model[:, 0].copy()

    x_shift, y_shift = shift_xy[0], shift_xy[1]

    # Shift to origin (0,0)
    x = x - x_shift
    y = y - y_shift

    # Convert degrees to radians
    if units=="DEGREES":
        angle = math.radians(angle)

    # Rotation matrix multiplication to get rotated x & y
    xr = (x * math.cos(angle)) - (y * math.sin(angle)) + x_shift
    yr = (x * math.sin(angle)) + (y * math.cos(angle)) + y_shift

    model[:, 0] = yr
    model[:, 1] = xr

    return model


def trim_midline(left_line, right_line, mid_line, margin=10):
    
    try:

        start_point = left_line[0]
        end_point = left_line[-1] 
        
        start_index = np.argmin(cdist([start_point],mid_line))
        end_index = np.argmin(cdist([end_point],mid_line))
        
        if start_index > end_index:
            start_index, end_index = end_index, start_index
        
        end_intersections = [mid_line[start_index], mid_line[end_index]]
        
        margin = 10
    
        if start_index >= margin:
            start_index -= margin
        if end_index <= len(mid_line) + margin:
            end_index += margin
            
        mid_line = mid_line[start_index:end_index]
        
    except Exception:
        pass
    
    return mid_line, end_intersections

def dilate_contour(cnt, dilation=0.2):
    
    mesh_length = len(cnt)
    
    cnt = Polygon(cnt.reshape(-1, 2))

    cnt = cnt.buffer(dilation, join_style=2)
    
    cnt = np.array([list(point) for point in cnt.exterior.coords])
    
    cnt = LineString(cnt)
    cnt = resize_line(cnt, mesh_length)
    
    cnt = np.array(cnt.xy).T
    
    cnt = cnt.reshape(-1, 1, 2)

    return cnt

def get_oufti_data(image, mask, midlines=None):

    mesh_length = 100

    mask_ids = np.unique(mask)

    polygons = []
    contours = []
    contour_ids = []

    for i in range(len(mask_ids)):

        id = mask_ids[i]

        if id!=0:

            cell_mask = np.zeros(mask.shape, dtype=np.uint8)
            cell_mask[mask==id] = 255

            cnt, _ = cv2.findContours(cell_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

            cnt = cnt[0]

            polygon = Polygon(cnt.reshape(-1, 2))

            polygons.append(polygon)
            contours.append(cnt)
            contour_ids.append(id)

    oufti_data = []

    if midlines==None:

        for i in range(len(contours)):

            try:

                cnt = contours[i]

                x, y, w, h = cv2.boundingRect(cnt)
                
                cnt = dilate_contour(cnt, 1)
    
                if h > w:
                    cnt90 = cnt.copy()
                    cnt90, shift_xy = rotate_contour(cnt90, angle=90)
                    mid_line = get_voronoi_midline(cnt90)
                    mid_line = rotate_model(mid_line, shift_xy, angle=-90)
    
                else:
                    mid_line = get_voronoi_midline(cnt)
                    
                    
                left_line, right_line, _, cnt_array = get_boundary_lines(mid_line, cnt, smooth=True, n_segments=100)
                
                mid_line, end_intersections = trim_midline(left_line, right_line, mid_line, margin=10)

                oufti_dict = {"cnt": cnt,
                              "end_intersections": end_intersections,
                              "cnt_array": cnt_array,
                              "mid_line": mid_line,
                              "left_line": left_line,
                              "right_line": right_line,
                              "mask_shape": mask.shape,
                              "mesh_length": mesh_length}

                oufti_data.append(oufti_dict)

            except Exception:
                pass

    return oufti_data


def find_closest_point(point, line):
    
    point = Point(point)

    pol_ext = LinearRing(line)
    d = pol_ext.project(point)
    p = pol_ext.interpolate(d)
    closet_point = list(p.coords)[0]
    
    return closet_point
    
def remove_intersecting(line, intersecting_line):
    
    line = LineString(line.exterior)
    
    intersection = line.intersection(intersecting_line)
    intersection = np.array([[geom.xy[0][0], geom.xy[1][0]] for geom in intersection.geoms])
    
    line = np.array(line.xy).T
    
    distance = cdist(line, intersection)
    end_indexes = sorted([np.argmin(dist).tolist() for dist in distance.T])
    
    end_indexes = np.unique(end_indexes).tolist()
    
    if end_indexes[1] - end_indexes[0] > 1:
        
        line = np.roll(line, -end_indexes[1], 0)
        distance = cdist(line, intersection)
        end_indexes = sorted([np.argmin(dist).tolist() for dist in distance.T])
        
    overlap_length = abs(end_indexes[0] - end_indexes[-1])

    line = np.roll(line, -end_indexes[0], 0)
    line = line[overlap_length:]

    distances = cdist(line,np.array(intersecting_line.xy).T)
    distances = np.min(distances,axis=1)
    del_indexes = np.argwhere(distances < 0.5).flatten()
    
    line = np.delete(line, del_indexes, axis=0)

    return line

def compute_line_metrics(mesh):
    steplength = euclidian_distance(mesh[1:, 0] + mesh[1:, 2], mesh[1:, 1] + mesh[1:, 3], mesh[:-1, 0] + mesh[:-1, 2],
                                    mesh[:-1, 1] + mesh[:-1, 3]) / 2

    steparea = []
    for i in range(len(mesh) - 1):
        steparea.append(
            polyarea([*mesh[i:i + 2, 0], *mesh[i:i + 2, 2][::-1]], [*mesh[i:i + 2, 1], *mesh[i:i + 2, 3][::-1]]))

    steparea = np.array(steparea)

    d = euclidian_distance(mesh[:, 0], mesh[:, 1], mesh[:, 2], mesh[:, 3])
    stepvolume = (d[:-1] * d[1:] + (d[:-1] - d[1:]) ** 2 / 3) * steplength * math.pi / 4

    return steplength, steparea, stepvolume

def get_mesh(oufti_dict, bisector_length=100, n_segments=100):
    
    left_line = oufti_dict["left_line"]
    right_line = oufti_dict["right_line"]
    mid_line = oufti_dict["mid_line"]
    cnt_array = oufti_dict["cnt_array"]
    end_intersections = oufti_dict["end_intersections"]
    n_segments = oufti_dict["mesh_length"]

    left_lineString = LineString(left_line)
    right_lineString = LineString(right_line)

    left_lineString = resize_line(left_lineString, n_segments)
    right_lineString = resize_line(right_lineString, n_segments)

    midline_lineString = LineString(mid_line)
    midline_lineString = resize_line(midline_lineString, n_segments)

    distances = np.linspace(0, midline_lineString.length, n_segments)[1:]

    mid_line_segments = [LineString([midline_lineString.interpolate(distance - 0.01),
                                     midline_lineString.interpolate(distance + 0.01)]) for distance in distances]

    right_line_data = [end_intersections[0].tolist()]
    left_line_data = [end_intersections[0].tolist()]

    for segment in mid_line_segments:

        left_bisector = segment.parallel_offset(bisector_length, 'left')
        right_bisector = segment.parallel_offset(bisector_length, 'right')

        left_bisector = left_bisector.boundary.geoms[1]
        right_bisector = right_bisector.boundary.geoms[0]

        bisector = LineString([left_bisector, right_bisector])

        left_intersection = bisector.intersection(left_lineString)
        right_intersection = bisector.intersection(right_lineString)

        if left_intersection.type=="Point" and right_intersection.type=="Point":
            right_line_data.append(np.array(left_intersection.xy).reshape(2).tolist())
            left_line_data.append(np.array(right_intersection.xy).reshape(2).tolist())

    right_line_data.append(end_intersections[-1].tolist())
    left_line_data.append(end_intersections[-1].tolist())

    left_line_data = np.array(left_line_data)
    right_line_data = np.array(right_line_data)

    mesh = np.hstack((left_line_data, right_line_data))
    model = np.vstack((left_line_data, np.flipud(right_line_data)))
    
    mesh = mesh + 1
    model = model + 1

    steplength, steparea, stepvolume = compute_line_metrics(mesh)

    polygon = Polygon(model)
    polygon = orient(polygon)

    boundingbox = np.asarray(polygon.bounds)

    boundingbox[0:2] = np.floor(boundingbox[0:2])
    boundingbox[2:4] = np.ceil(boundingbox[2:4])
    boundingbox[2:4] = boundingbox[2:4] - boundingbox[0:2]
    boundingbox = boundingbox.astype(float)

    return mesh, model, steplength, steparea, stepvolume, boundingbox

def export_oufti(image, oufti_data, file_path):
    file_path = os.path.splitext(file_path)[0] + ".mat"

    cell_data = []

    for i in range(len(oufti_data)):

        try:

            mesh, model, steplength, steparea, stepvolume, boundingbox = get_mesh(oufti_data[i])

            cell_struct = {'mesh': mesh,
                           'model': model,
                           'birthframe': 1,
                           'divisions': [],
                           'ancestors': [],
                           'descendants': [],
                           'timelapse': False,
                           'algorithm': 5,
                           'polarity': 0,
                           'stage': 1,
                           'box': boundingbox,
                           'steplength': steplength,
                           'length': np.sum(steplength),
                           'lengthvector': steplength,
                           'steparea': steparea,
                           'area': np.sum(steparea),
                           'stepvolume': stepvolume.T,
                           'volume': np.sum(stepvolume)}

            cell_data.append(cell_struct)

        except Exception:
            print(traceback.format_exc())
            pass

    cellListN = len(cell_data)
    cellList = np.zeros((1,), dtype=object)
    cellList_items = np.zeros((1, cellListN), dtype=object)

    microbeTrackerParamsString = "% This file contains MicrobeTracker settings optimized for wildtype E. coli cells at 0.114 um/pixel resolution (using algorithm 4)\n\nalgorithm = 4\n\n% Pixel-based parameters\nareaMin = 120\nareaMax = 2200\nthresFactorM = 1\nthresFactorF = 1\nsplitregions = 1\nedgemode = logvalley\nedgeSigmaL = 3\nedveSigmaV = 1\nvalleythresh1 = 0\nvalleythresh2 = 1\nerodeNum = 1\nopennum = 0\nthreshminlevel = 0.02\n\n% Constraint parameters\nfmeshstep = 1\ncellwidth =6.5\nfsmooth = 18\nimageforce = 4\nwspringconst = 0.3\nrigidityRange = 2.5\nrigidity = 1\nrigidityRangeB = 8\nrigidityB = 5\nattrCoeff = 0.1\nrepCoeff = 0.3\nattrRegion = 4\nhoralign = 0.2\neqaldist = 2.5\n\n% Image force parameters\nfitqualitymax = 0.5\nforceWeights = 0.25 0.5 0.25\ndmapThres = 2\ndmapPower = 2\ngradSmoothArea = 0.5\nrepArea = 0.9\nattrPower = 4\nneighRep = 0.15\n\n% Mesh creation parameters\nroiBorder = 20.5\nnoCellBorder = 5\nmaxmesh = 1000\nmaxCellNumber = 2000\nmaxRegNumber = 10000\nmeshStep = 1\nmeshTolerance = 0.01\n\n% Fitting parameters\nfitConvLevel = 0.0001\nfitMaxIter = 500\nmoveall = 0.1\nfitStep = 0.2\nfitStepM = 0.6\n\n% Joining and splitting\nsplitThreshold = 0.35\njoindist = 5\njoinangle = 0.8\njoinWhenReuse = 0\nsplit1 = 0\n\n% Other\nbgrErodeNum = 5\nsgnResize = 1\naligndepth = 1"

    for i in range(len(cell_data)):
        cellList_items[0, i] = cell_data[i]

    cellList[0] = cellList_items

    p = [];
    paramString = np.empty((len(microbeTrackerParamsString.split('\n')), 1), dtype=object)
    paramSplit = microbeTrackerParamsString.split('\n')
    for p_index in range(len(microbeTrackerParamsString.split('\n'))):
        paramString[p_index] = paramSplit[p_index]

    outdict = {'cellList': cellList,
               'cellListN': cellListN,
               'coefPCA': [],
               'mCell': [],
               'p': [],
               'paramString': paramString,
               'rawPhaseFolder': [],
               'shiftfluo': np.zeros((2, 2)),
               'shiftframes': [],
               'weights': []}

    scipy.io.savemat(file_path, outdict)
    print(True)



images = glob(r"C:\napari-akseg\src\napari_bacseg\_dev\omnipose_train\images\*.tif")
masks = glob(r"C:\napari-akseg\src\napari_bacseg\_dev\omnipose_train\masks\*.tif")

images = [tifffile.imread(path) for path in images]
masks = [tifffile.imread(path) for path in masks]




image = images[0]
mask = masks[0]

oufti_data = get_oufti_data(image, mask)

export_oufti(image, oufti_data, "test_oufti.mat")

tifffile.imwrite("test_image.tif",image)

bisector_length = 100

for i in range(10,11):
    
    oufti_dict = oufti_data[i]
    
    left_line = oufti_dict["left_line"]
    right_line = oufti_dict["right_line"]
    mid_line = oufti_dict["mid_line"]
    cnt_array = oufti_dict["cnt_array"]
    end_intersections = oufti_dict["end_intersections"]
    n_segments = oufti_dict["mesh_length"]
    
    
    plt.plot(*left_line.T)
    plt.plot(*mid_line.T)
    plt.plot(*right_line.T)
    # plt.show()

    left_lineString = LineString(left_line)
    right_lineString = LineString(right_line)

    left_lineString = resize_line(left_lineString, n_segments)
    right_lineString = resize_line(right_lineString, n_segments)

    midline_lineString = LineString(mid_line)
    midline_lineString = resize_line(midline_lineString, n_segments)

    distances = np.linspace(0, midline_lineString.length, n_segments)[1:]

    mid_line_segments = [LineString([midline_lineString.interpolate(distance - 0.01),
                                      midline_lineString.interpolate(distance + 0.01)]) for distance in distances]

    right_line_data = [end_intersections[0].tolist()]
    left_line_data = [end_intersections[0].tolist()]

    for segment in mid_line_segments:

        left_bisector = segment.parallel_offset(bisector_length, 'left')
        right_bisector = segment.parallel_offset(bisector_length, 'right')

        left_bisector = left_bisector.boundary.geoms[1]
        right_bisector = right_bisector.boundary.geoms[0]

        bisector = LineString([left_bisector, right_bisector])

        left_intersection = bisector.intersection(left_lineString)
        right_intersection = bisector.intersection(right_lineString)

        if left_intersection.geom_type=="Point" and right_intersection.geom_type=="Point":
            right_line_data.append(np.array(left_intersection.xy).reshape(2).tolist())
            left_line_data.append(np.array(right_intersection.xy).reshape(2).tolist())

    right_line_data.append(end_intersections[-1].tolist())
    left_line_data.append(end_intersections[-1].tolist())

    left_line_data = np.array(left_line_data)
    right_line_data = np.array(right_line_data)
    
    plt.plot(*left_line_data.T)
    plt.plot(*mid_line.T)
    plt.plot(*right_line_data.T)
    plt.show()

    # mesh = np.hstack((left_line_data, right_line_data))
    # model = np.vstack((left_line_data, np.flipud(right_line_data)))
    
    


























# mesh_length = 10


# midlines = None


# mesh_length = 10

# mask_ids = np.unique(mask)

# polygons = []
# contours = []
# contour_ids = []

# for i in range(len(mask_ids)):

#     id = mask_ids[i]

#     if id!=0:

#         cell_mask = np.zeros(mask.shape, dtype=np.uint8)
#         cell_mask[mask==id] = 255

#         cnt, _ = cv2.findContours(cell_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

#         cnt = cnt[0]

#         polygon = Polygon(cnt.reshape(-1, 2))

#         polygons.append(polygon)
#         contours.append(cnt)
#         contour_ids.append(id)

# oufti_data = []

# if midlines==None:

#     for i in range(0,42):

#         try:

#             cnt = contours[i]

#             x, y, w, h = cv2.boundingRect(cnt)
            
#             edge = check_edge(cnt, mask)
            
#             # if edge==False:
            
#             cnt = dilate_contour(cnt, 1)

#             if h > w:
#                 cnt90 = cnt.copy()
#                 cnt90, shift_xy = rotate_contour(cnt90, angle=90)
#                 mid_line = get_voronoi_midline(cnt90)
#                 mid_line = rotate_model(mid_line, shift_xy, angle=-90)

#             else:
#                 mid_line = get_voronoi_midline(cnt)
                
                
#             left_line, right_line, _, cnt_array = get_boundary_lines(mid_line, cnt, smooth=True, n_segments=100)
            
#             mid_line, _ = trim_midline(left_line, right_line, mid_line, margin=10)


#             # start_point = find_closest_point(start_point, LineString(mid_line))
#             # end_point = find_closest_point(end_point, LineString(mid_line))

#             # start_index = np.argwhere(mid_lineisstart_point)
            
            
            
#             # mid_line, end_intersections = trim_midline(cnt_array, mid_line)
            
            
            
#             # cnt_end_indexes = sorted([np.argmin(dist).tolist() for dist in cnt_distance.T])
            
            
#             # plt.plot(*cnt.reshape(-1,2).T)
#             plt.plot(*left_line.T)

#             plt.plot(*right_line.T)
#             plt.plot(*mid_line.T)
#             plt.title(str(i))
#             plt.show()
#             plt.close()

                
                
                
                
                
                
                
                
                
                
                # intersecting_line = line
                # line = right_line
                
                
                # intersection = line.intersection(intersecting_line)
                # intersection = np.array([[geom.xy[0][0], geom.xy[1][0]] for geom in intersection.geoms])
                
                # line = np.array(line.xy).T
                
                # distance = cdist(line, intersection)
                # end_indexes = sorted([np.argmin(dist).tolist() for dist in distance.T])
                
                # if end_indexes[1] - end_indexes[0] > 1:
                    
                #     line = np.roll(line, -end_indexes[1], 0)
                #     distance = cdist(line, intersection)
                #     end_indexes = sorted([np.argmin(dist).tolist() for dist in distance.T])
                    

                # overlap_length = abs(end_indexes[0] - end_indexes[-1])
                
                # line = np.roll(line, -end_indexes[0], 0)
                # line = line[overlap_length:]
                
                
                

                                
                # left_line = np.array(left_line.xy).T
                # right_line = np.array(right_line.xy).T
                
                
                # distances = cdist(right_line,left_line)
                
                # intersection = np.argwhere(np.min(distances, axis=-1) < 0.1).flatten()
                
      
                # # intersection_indeces = np.arange(intersection[0]+1,intersection[-1]-1,1)
                
                # # left_line = np.delete(left_line, intersection_indeces, axis=0)
                
                # left_line = left_line[2:80]
                
                
                
                
                # # intersection = left_line.intersection(right_line)
                # # intersection = np.array([[geom.xy[0][0], geom.xy[1][0]] for geom in intersection.geoms])
                
                # left_line = np.array(left_line.xy).T
                # right_line = np.array(right_line.xy).T
                
                
                
                
                
                
                
                
                
                
                
                
                # left_line = np.array([list(point) for point in left_line if point not in intersection]) 
                # right_line = np.array([list(point) for point in right_line if point not in intersection]) 
                
 
                
                
                
                
                
                # left_line = np.array([list(point) for point in left_line if point not in intersection]) 
                # right_line = np.array([list(point) for point in right_line if point not in intersection]) 

                # left_line = delete_intersection(left_line)
                # right_line = delete_intersection(right_line)
                
                
                
                # left_line = np.delete(left_line, [max_index], axis=0)
                
                
                
                # # left_line = np.delete(left_line, [0,1,2,3,4], axis=0)


                # left_line = left_line[5:,:]
                




                # merged = linemerge([polygon.boundary, line])
                # borders = unary_union(merged)
                # polygons = list(polygonize(borders))
                
                # left_line, right_line = polygons
                
                # left_line = resize_line(LineString(left_line.exterior), 100)
                # right_line = resize_line(LineString(right_line.exterior), 100)
                
                # intersection = left_line.intersection(right_line)
                # intersection = np.array([[geom.xy[0][0], geom.xy[1][0]] for geom in intersection.geoms])
                
                # left_line = np.array(left_line.xy).T
                # right_line = np.array(right_line.xy).T
                
                # left_line = np.unique(left_line, axis=-1)
                # right_line = np.unique(right_line, axis=-1)
                
                # left_line = np.array([point for point in left_line if point not in intersection])
                # right_line = np.array([point for point in right_line if point not in intersection])
                
                # left_line = np.array([list(point.xy) for point in left_line if point not in intersection]) 
                # right_line = np.array([list(point.xy) for point in right_line if point not in intersection]) 
                
                # left_line = np.unique(left_line, axis=-1)
                # right_line = np.unique(right_line, axis=-1)
                
                # left_line = [point for point in left_line if point not in in]
                
                
                
                
                # for element in left_line:
                #     if element in intersection:
                #         print(element)
                
                
                
                # # left_line = left_line[:63]

 


                
                # left_line
                
                
                # plt.plot(*left_line.T)
                # plt.show()
                
                    
                # cnt_linestring = LinearRing(cnt.reshape(-1, 2))
                # cnt_midlinestring = LineString(mid_line)

                # intersection = cnt_midlinestring.intersection(cnt_linestring)
                # intersection = np.array([[int(geom.xy[0][0]), int(geom.xy[1][0])] for geom in intersection.geoms])

                # cnt_array = cnt.reshape(-1, 2)

                # if smooth:
                #     cnt_array = moving_average(cnt_array)

                # cnt_distance = cdist(cnt_array, intersection)
                # cnt_end_indexes = sorted([np.argmin(dist).tolist() for dist in cnt_distance.T])
                

                # cnt_array = np.roll(cnt_array, -cnt_end_indexes[0], 0)
                # cnt_array = np.append(cnt_array, [cnt_array[0]], 0)

                # left_line = cnt_array[1:cnt_end_indexes[-1] - cnt_end_indexes[0]+1]
                # right_line = cnt_array[cnt_end_indexes[-1] - cnt_end_indexes[0] + 1:]
                
                # mid_line_distance = cdist(midline,intersection)
                # mid_line_end_indexes = sorted([np.argmin(dist).tolist() for dist in mid_line_distance.T])
                
                # # left_line = np.concatenate(([midline[mid_line_end_indexes[0]]],left_line, [midline[mid_line_end_indexes[-1]]]))
                # # right_line = np.concatenate(([midline[mid_line_end_indexes[0]]],left_line, [midline[mid_line_end_indexes[-1]]]))
                
                

                # left_lineString = LineString(left_line)
                # right_lineString = LineString(right_line)

                # left_lineString = resize_line(left_lineString, n_segments)
                # right_lineString = resize_line(right_lineString, n_segments)

                # left_line = np.array(left_lineString.xy).T
                # right_line = np.array(right_lineString.xy).T
                # mid_line = (left_line + np.flipud(right_line)) / 2
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    
    
                # left_line, right_line, _, cnt_array = get_boundary_lines(midline, cnt, smooth=False)
    
        
                # midline, end_intersections = trim_midline(cnt_array, midline, margin=10)
                
                # plt.plot(*cnt.reshape(-1,2).T)
                # plt.plot(*left_line.T)
                # plt.plot(*right_line.T)
                # plt.plot(*midline.T)
                # plt.show()
                

        # except Exception:
        #     import traceback
        #     print(i,traceback.format_exc())
        #     pass





