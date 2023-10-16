import numpy as np
import cv2
from shapely.geometry import LineString, GeometryCollection
from shapely.geometry import Polygon, LinearRing, Point
from shapely.ops import nearest_points, split
from shapely.geometry.polygon import orient

import math
from skimage.morphology import medial_axis, skeletonize, thin
from scipy.spatial.distance import cdist
import warnings
import os
import scipy.io
import tifffile
from colicoords import Data, Cell, CellPlot, data_to_cells, CellList
import matplotlib.pyplot as plt
from skimage import exposure
from scipy.spatial import Voronoi
import matplotlib.path as mpltPath
import pickle
import traceback


def euclidian_distance(x1, y1, x2, y2):
    distance = ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5

    return distance


def polyarea(x, y):
    return 0.5 * np.abs(np.dot(x, np.roll(y, 1)) - np.dot(y, np.roll(x, 1)))


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

def find_contours(img):

    # finds contours of shapes, only returns the external contours of the shapes
    contours, hierarchy = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    contours = sorted(contours, key=cv2.contourArea, reverse=True)
    
    return contours

def moving_average(line, padding = 5, iterations = 1, mode="same"):
    
    x, y = line[:,0], line[:,1]
    
    x = np.concatenate((x[-padding:] , x, x[:padding]))
    y = np.concatenate((y[-padding:] , y, y[:padding]))
    
    for i in range(iterations):
    
        y = np.convolve(y, np.ones(padding), mode) / padding
        x = np.convolve(x, np.ones(padding), mode) / padding
    
        x = np.array(x)
        y = np.array(y)
    
    x = x[padding:-padding]
    y = y[padding:-padding]
    
    line = np.stack([x,y]).T
    
    return line

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

        mid_line = None

    return mid_line

def resize_line(mesh, mesh_length):

    distances = np.linspace(0, mesh.length, mesh_length)
    mesh = LineString([mesh.interpolate(distance) for distance in distances])

    return mesh


def get_boundary_lines(mid_line, cnt, smooth=True, n_segments=100):

    cnt_linestring = LinearRing(cnt.reshape(-1, 2))
    cnt_midlinestring = LineString(mid_line)

    intersection = cnt_midlinestring.intersection(cnt_linestring)
    intersection = np.array([[int(geom.xy[0][0]), int(geom.xy[1][0])] for geom in intersection.geoms])
    
    cnt_array = cnt.reshape(-1, 2)

    if smooth:
        cnt_array = moving_average(cnt_array)

    distance = cdist(cnt_array, intersection)

    cnt_end_indexes = sorted([np.argmin(dist).tolist() for dist in distance.T])

    cnt_array = np.roll(cnt_array, -cnt_end_indexes[0], 0)
    cnt_array = np.append(cnt_array, [cnt_array[0]], 0)

    left_line = cnt_array[:cnt_end_indexes[-1] - cnt_end_indexes[0] + 1]
    right_line = cnt_array[cnt_end_indexes[-1] - cnt_end_indexes[0]:]

    left_lineString = LineString(left_line)
    right_lineString = LineString(right_line)

    left_lineString = resize_line(left_lineString, n_segments)
    right_lineString = resize_line(right_lineString, n_segments)

    left_line = np.array(left_lineString.xy).T
    right_line = np.array(right_lineString.xy).T
    mid_line = (left_line + np.flipud(right_line)) / 2

    return left_line, right_line, mid_line, cnt_array



def fit_polyline(x, y, polys=[2,3], margin=50, poly_limits=None):

    with warnings.catch_warnings():

        warnings.filterwarnings('ignore')
        
        residual_list = []
        param_list = []
        
        for poly in polys:

            params, residuals, rank, singular_values, rcond = np.polyfit(x.copy(), y.copy(), poly, full = True)
            
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
    

def find_contours(img):

    # finds contours of shapes, only returns the external contours of the shapes
    contours, hierarchy = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    contours = sorted(contours, key=cv2.contourArea, reverse=True)
    
    return contours

def get_contour_data(mask):

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
            
            polygon = Polygon(cnt.reshape(-1,2))
            
            polygons.append(polygon)
            contours.append(cnt)
            contour_ids.append(id)
            
    return polygons, contours, contour_ids
       
     
def get_contour_index(midline,polygons,contour_ids):
    
    intersection_index = None
    
    try:
        
        intersection_lengths = []
        intersection_ids = []
        
        midline_points = [Point(point) for point in midline]
        
        for i, poly in enumerate(polygons):
            
            inside_points = [poly.contains(point) for point in midline_points if poly.contains(point)==True]
        
            if len(inside_points) > 0:
                
                intersection_lengths.append(len(inside_points))
                intersection_ids.append(contour_ids[i])
    
        if len(intersection_lengths)!=0:
            
            intersection_lengths, intersection_ids = zip(*sorted(zip(intersection_lengths, intersection_ids), reverse=True))
            
            intersection_index = contour_ids.index(intersection_ids[0]) 
            
    
    except Exception:
        pass
        

    return intersection_index


def get_midline_boundary_lines(midline, cnt, smooth=True, n_segments=100):
    
    cnt_array = cnt.reshape(-1, 2)

    if smooth:
        cnt_array = moving_average(cnt_array)
    
    cnt_LinearRing = LinearRing(cnt.reshape(-1,2))
    
    midline_start_point = Point(midline[0])
    midline_end_point = Point(midline[-1])
    
    if cnt_LinearRing.intersection(midline_start_point).length==0:
        
        start_intersection = np.array(nearest_points(cnt_LinearRing, midline_start_point)[-1].xy).T[0]
        
    if cnt_LinearRing.intersection(midline_end_point).length==0:
        
        end_intersection = np.array(nearest_points(cnt_LinearRing, midline_end_point)[0].xy).T[0]
        
    intersection = np.array([start_intersection,end_intersection])
    
    distance = cdist(cnt_array, intersection)

    cnt_end_indexes = sorted([np.argmin(dist).tolist() for dist in distance.T])
    
    cnt_array = np.roll(cnt_array, -cnt_end_indexes[0], 0)
    cnt_array = np.append(cnt_array, [cnt_array[0]], 0)

    left_line = cnt_array[:cnt_end_indexes[-1] - cnt_end_indexes[0] + 1]
    right_line = cnt_array[cnt_end_indexes[-1] - cnt_end_indexes[0]:]

    left_lineString = LineString(left_line)
    right_lineString = LineString(right_line)

    left_lineString = resize_line(left_lineString, n_segments)
    right_lineString = resize_line(right_lineString, n_segments)

    left_line = np.array(left_lineString.xy).T
    right_line = np.array(right_lineString.xy).T
    mid_line = (left_line + np.flipud(right_line)) / 2
    
    end_intersections = np.array([mid_line[0],mid_line[-1]])
    end_indicies = np.argmin(cdist(end_intersections, midline), axis=1)
    end_indicies, end_intersections = zip(*sorted(zip(end_indicies, end_intersections), reverse=False))
    end_intersections = list(end_intersections)
    
    return left_line, right_line, mid_line, cnt_array, end_intersections
    
    
def trim_midline(cnt_array, midline, margin = 5, n_segments = 100):
    
    cnt_lineString = LineString(cnt_array)
    midline_lineString = LineString(midline)

    end_intersections = midline_lineString.intersection(cnt_lineString)

    if end_intersections.type=="MultiPoint":

        end_intersections = np.array([dat.xy for dat in end_intersections.geoms]).reshape(-1, 2)

        end_indicies = np.argmin(cdist(end_intersections, midline), axis=1)
        end_indicies, end_intersections = zip(*sorted(zip(end_indicies, end_intersections), reverse=False))
        end_intersections = list(end_intersections)

        index1, index2 = end_indicies

        margin = margin

        if index1 >= margin:
            index1 -= margin
        if index2 <= len(midline) + margin:
            index2 += margin

        midline = midline[index1:index2]

    return midline, end_intersections
    
    
    

def get_oufti_data(image, mask, midlines=None):

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

        for i in range(20,30):

            try:
                
                cnt = contours[i]

                midline = get_voronoi_midline(cnt)
                
                left_line, right_line, _, cnt_array = get_boundary_lines(midline, cnt, smooth=True)
                
                midline, end_intersections = trim_midline(cnt_array, midline)
                
                plt.plot(*left_line.T)
                plt.plot(*right_line.T)
                plt.plot(*midline.T)
                plt.show()
                
                oufti_dict = {"cnt": cnt,
                              "cnt_array": cnt_array,
                              "midline": midline,
                              "end_intersections": midline,
                              "left_line": left_line,
                              "right_line": right_line,
                              "mask_shape": mask.shape}

                oufti_data.append(oufti_dict)

            except Exception:
                print(traceback.format_exc())
                pass

    else:

        for i in range(20,26):

            try:

                midline = midlines[i]
                midline = np.flip(midline)
                
                index = get_contour_index(midline, polygons, contour_ids)
                
                if index!=None:
                    
                    cnt = contours[index]
                    
                    midline = find_endpoints(midline, cnt)
                    
                    left_line, right_line, _, cnt_array, end_intersections = get_midline_boundary_lines(midline, cnt, smooth=True)
                    
                    midline = centre_midline(left_line, right_line, midline)
                    
                    
                        
                    # plt.plot(*left_line.T)
                    # plt.plot(*right_line.T)
                    # plt.plot(*midline.T)
                    # plt.show()
                

                    oufti_dict = {"cnt": cnt,
                                  "end_intersections": end_intersections,
                                  "cnt_array": cnt_array,
                                  "mid_line": midline,
                                  "left_line": left_line,
                                  "right_line": right_line,
                                  "mask_shape": mask.shape}

                    oufti_data.append(oufti_dict)

            except Exception:
                print(traceback.format_exc())
                pass

    return oufti_data



    
    
    

    







def find_endpoints(mid_line, cnt, n_segments = 100):
    
    cnt_array = cnt.reshape(-1, 2)
    
    cnt_LinearRing = LinearRing(cnt.reshape(-1,2))
    
    midline_lineString = LineString(mid_line)
    midline_lineString = resize_line(midline_lineString, n_segments)

    distances = np.linspace(0, midline_lineString.length, n_segments)
    
    middle_distance = distances[len(distances)//2]
    
    mid_line_segment = LineString([midline_lineString.interpolate(middle_distance - 0.01),
                                   midline_lineString.interpolate(middle_distance + 0.01)])

    left_bisector = mid_line_segment.parallel_offset(100, 'left')
    right_bisector = mid_line_segment.parallel_offset(100, 'right')
    
    left_bisector = left_bisector.boundary.geoms[1]
    right_bisector = right_bisector.boundary.geoms[0]

    bisector = LineString([left_bisector, right_bisector])
    
    intersection = bisector.intersection(cnt_LinearRing)
    
    if intersection.type=="MultiPoint":
        
        intersecting_points = np.array([list((p.x, p.y)) for p in intersection.geoms])
        
        # print(intersecting_points)
        
        split_data = split(Polygon(cnt_array), bisector)
        
        left_line, right_line = [np.array(dat.exterior.coords.xy).T.tolist() for dat in split_data.geoms]
        
        left_line = np.roll(left_line, len(left_line)//2, 0)
        
        left_line_average = moving_average(np.array(left_line), mode="valid", padding = 5, iterations=1)
        right_line_average = moving_average(np.array(right_line), mode="valid", padding = 5, iterations=1)
        
                
        left_line_grad = abs(np.gradient(np.gradient(left_line_average[:,1])))
        right_line_grad = abs(np.gradient(np.gradient(right_line_average[:,1])))


        
        # # # # plt.plot(*overlapping.T)
        # plt.plot(*np.array(right_line)[1:-1].T)
        # plt.plot(*np.array(left_line)[:-5].T)
        plt.plot(*np.array(right_line_average)[1:-1].T)
        plt.plot(*np.array(left_line_average)[:-5].T)
        plt.show()
        plt.plot(left_line_grad)
        plt.plot(right_line_grad)
        plt.show()
        
        # print(np.array(split_data[0]))
        
        
        
        
        
        
    

    

    
    
    
    # midline_start = mid_line[:len(mid_line)//2]
    # midline_end = mid_line[len(mid_line)//2:]

        
    
    
    
    # midline_start = mid_line[:len(mid_line)//2]
    # midline_end = mid_line[len(mid_line)//2:]
    
    # mesh_start = np.vstack((right_line[len(right_line)//2:], left_line[:len(left_line)//2]))
    # mesh_end = np.vstack((left_line[len(left_line)//2:],right_line[:len(right_line)//2]))
    
    # mesh_end = mesh_end[len(mesh_end)//4:-len(mesh_end)//4]
    # mesh_start = mesh_start[len(mesh_start)//4:-len(mesh_start)//4]
    
    # mesh_start = moving_average(mesh_start, mode="valid", padding = 10, iterations=2)
    # mesh_end = moving_average(mesh_end, mode="valid", padding = 10, iterations = 2)
    
    # mesh_start_grad = abs(np.gradient(np.gradient(mesh_start[:,1])))
    # mesh_end_grad = abs(np.gradient(np.gradient(mesh_end[:,1])))
    
    # mesh_start_pole = mesh_start[np.argmax(mesh_start_grad)]
    # mesh_end_pole = mesh_end[np.argmax(mesh_end_grad)]
    
    # mid_line[0] = mesh_start_pole
    # mid_line[-1] = mesh_end_pole
    
    return mid_line
    

        
    

def centre_midline(left_line, right_line, midline, interpolate_line=True, fit_segments = 100, export_segments = 6):
    
    from scipy import interpolate
    from scipy.interpolate import splev
    
    left_LineString = LineString(left_line)
    right_LineString = LineString(right_line)
    
    midline_LineString = LineString(midline)
    midline_LineString = resize_line(midline_LineString, fit_segments)
    
    midline = np.array(midline_LineString.xy).T
    
    for i in range(1,len(midline)-1):
        
        point = Point(midline[i])
        
        left_intersection = np.array(nearest_points(left_LineString, point)[0].xy).T[0]
        right_intersection = np.array(nearest_points(right_LineString, point)[0].xy).T[0]
        
        new_point = np.mean([left_intersection,right_intersection], axis=0)
        
        midline[i] = new_point
    
    midline_LineString = LineString(midline)
    midline_LineString = resize_line(midline_LineString, export_segments)
    
    midline = np.array(midline_LineString.xy).T
    
    if interpolate_line==True:
        
        midline = interpolate_data(midline, export_segments = export_segments)

    return midline
        
        
    
def interpolate_data(line, export_segments=100, method="quadratic"):
    
    from scipy import interpolate
    from scipy.interpolate import splev
    
    interpolations_methods = ['slinear', 'quadratic', 'cubic']
    
    x = line[:,0]
    y = line[:,1]

    # Linear length along the line:
    distance = np.cumsum( np.sqrt(np.sum( np.diff(line, axis=0)**2, axis=1 )) )
    distance = np.insert(distance, 0, 0)

    alpha = np.linspace(distance.min(), int(distance.max()), 100)
    interpolator =  interpolate.interp1d(distance, line, kind=method, axis=0)
    
    interpolated_points = interpolator(alpha)

    out_x = interpolated_points.T[0]
    out_y = interpolated_points.T[1]

    out_line = np.stack([out_x,out_y]).T
    
    line = np.vstack((line[0],out_line,line[-1]))

    return line

    
    



def get_mesh(oufti_dict, bisector_length = 100, n_segments = 100):

    left_line = oufti_dict["left_line"]
    right_line = oufti_dict["right_line"]
    mid_line = oufti_dict["mid_line"]
    cnt_array = oufti_dict["cnt_array"]

    left_lineString = LineString(left_line)
    right_lineString = LineString(right_line)

    left_lineString = resize_line(left_lineString, n_segments)
    right_lineString = resize_line(right_lineString, n_segments)

    midline_lineString = LineString(mid_line)
    midline_lineString = resize_line(midline_lineString, n_segments)

    distances = np.linspace(0, midline_lineString.length, n_segments)

    mid_line_segments = [LineString([midline_lineString.interpolate(distance - 0.01),
                                     midline_lineString.interpolate(distance + 0.01)]) for distance in distances]

    right_line_data = [mid_line[0].tolist()]
    left_line_data = [mid_line[0].tolist()]

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

    right_line_data.append(mid_line[-1].tolist())
    left_line_data.append(mid_line[-1].tolist())

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


with open('midlines.pickle', 'rb') as handle:
    image,mask,midlines,midline_ids = pickle.load(handle)
    
    
    
oufti_data = get_oufti_data(image, mask, midlines)
    
    
    
    

# with open('oufti_data.pickle', 'rb') as handle:
#    mask_stack, image_stack, meta_stack = pickle.load(handle)
        
    
# for i in range(1):

#     mask = mask_stack[i]
#     image = image_stack[i]
#     meta = meta_stack[i]

#     if "midlines" in meta.keys():
#         midlines = meta["midlines"]
#     else:
#         midlines = None

#     oufti_data = get_oufti_data(image, mask, midlines)
    
    # for oufti_dict in oufti_data:
        
    #     get_mesh(oufti_dict, bisector_length = 100, n_segments = 100)
    

    # for j in range(10):
        
    #     dat = oufti_data[j]
        
    #     plt.plot(*dat["cnt_array"].T)
    #     plt.plot(*dat["midline"].T)
    #     plt.show()

   
   
   
    
    
    
    
# polygons, contours, contour_ids = get_contour_data(mask)





# new_midlines = []

# new_contours = []

# for i in range(10,11):
    
#     midline = midlines[i][5:-5]
#     midline = np.flip(midline)
    
#     index = get_intersection_index(midline,polygons,contour_ids)
    
#     if index!=None:
    
#         cnt = contours[index]
        
#         midline = check_midlines_intersecting(cnt, midline)
        
        
        
    
    
    
    
    
    
    # # cnt = contours[intersection_index]
    
    # pts = midline.reshape(-1,2).astype(int)
    
    # x, y, w, h = cv2.boundingRect(cnt)
    # y1, y2, x1, x2 = y, (y + h), x, (x + w)
    
    # img = image.copy()
    
    # img = cv2.polylines(img, [pts], False, 255, 1)
    # cv2.drawContours(img, [cnt], contourIdx=-1, color=(1, 1, 1), thickness=1)
    
    # plt.imshow(img[y1:y2,x1:x2])
    # plt.show()
    
    

    
    
    



        
    
    
    
    
    
    
    
    
    

    
    
    
    

            
        
        
    


    
    
    
    
    
    
    
    
    