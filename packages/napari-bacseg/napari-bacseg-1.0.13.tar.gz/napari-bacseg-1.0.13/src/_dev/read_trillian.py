from aicsimageio import AICSImage
from aicsimageio.readers import CziReader
import matplotlib.pyplot as plt
import numpy as np
from skimage import exposure
import pandas as pd
import os



import xmltodict
import itertools
from collections import ChainMap
 
 
def normalize99(X):
    """normalize image so 0.0 is 0.01st percentile and 1.0 is 99.99th percentile"""

    if np.max(X) > 0:
        X = X.copy()
        v_min, v_max = np.percentile(X[X != 0], (0.1, 99.9))
        X = exposure.rescale_intensity(X, in_range=(v_min, v_max))

    return X


def rescale01(x):
    """normalize image from 0 to 1"""

    if np.max(x) > 0:
        x = (x - np.min(x)) / (np.max(x) - np.min(x))

    return x

def etree_to_dict(t):
    return {t.tag : map(etree_to_dict, t.iterchildren()) or t.text}

def read_metadata(czi):

    metaadata = czi.read_subblock_metadata(xml=False)
    
    metadata_list = []
    
    for position, xml_metadata in metaadata:
        
        meta_tags = dict(xmltodict.parse(xml_metadata)["METADATA"]["Tags"])
        
        pixel_size = meta_tags["ImageScaling"]["ImageScaling"]["ImagePixelSize"]
        
        meta_tags.pop("DetectorState")
        meta_tags.pop("ImageScaling")
    
        for key, value in meta_tags.items():
            if key != "AcquisitionTime":
                meta_tags[key] = float(value)
        
        meta = {**position,**meta_tags}
        
        metadata_list.append(meta)
        
    metadata_list = pd.DataFrame(metadata_list)
    
    return metadata_list


def get_channel_dict(path):

    from czifile import CziFile
    import xmltodict
    
    czi = CziFile(path)
    metadata = czi.metadata()
    
    metadata = xmltodict.parse(metadata)["ImageDocument"]["Metadata"]
    
    channels_metadata = metadata["Information"]["Image"]["Dimensions"]["Channels"]["Channel"]
    
    channel_dict = {}
    
    for channel_index, channel_meta in enumerate(channels_metadata):
        
        channel_dict[channel_index] = {}
        
        for key,value in channel_meta.items():
            
            channel_dict[channel_index][key] = value
            
    return channel_dict
    



# path = "Snap-2388.czi"
# path = r"C:\Users\turnerp\Desktop\trillion\Experiment-1427.czi"
# # path = r"C:\Users\turnerp\Desktop\BSA DEV\WT_DAPI_PBS.czi"
# path = r"C:\Users\turnerp\Desktop\Trillian Nice FOVs\nice_quad_channel_WTdata.czi"


# from pylibCZIrw import czi as pyczi
# import json


# def get_pylibCZIrw_channel_dict(czidoc):
    
#     pixel_type = czidoc.total_bounding_box_no_pyramid
    
#     metadata = czidoc.metadata["ImageDocument"]["Metadata"]
    
#     channels_metadata = metadata["Information"]["Image"]["Dimensions"]["Channels"]["Channel"]
    
#     channel_dict = {}
    
#     for channel_index, channel_meta in enumerate(channels_metadata):
        
#         channel_dict[channel_index] = {}
        
#         for key,value in channel_meta.items():
            
#             channel_dict[channel_index][key] = value
    
#     return channel_dict
    

# with pyczi.open_czi(path) as czidoc:
    
#     # image_dims = czidoc.scenes_bounding_rectangle
    
#     image_dims = czidoc.total_bounding_box
#     scenes_dims = czidoc.scenes_bounding_rectangle

    
#     # help(czidoc)
    
#     # sorted_image_dims = {}
    
#     # dim_order = ["S","M","Z"]
    
#     # # if "S" in sorted_image_dims:
#     # #     sorted_image_dims[""]
    
            
            
            
            
            
    
    # metadata = xmltodict.parse(xml_metadata)
    
    # metdata = czidoc.raw_metadata
    
    # xx = json.dumps(md_dict["ImageDocument"]["Metadata"]["Information"]["Image"])
    


#     print(json.dumps(md_dict["ImageDocument"]["Metadata"]["Information"]["Image"], sort_keys=False, indent=4))

#     image_meta = md_dict["ImageDocument"]["Metadata"]["Information"]["Image"]
























# from czifile import CziFile, SubBlockSegment
# import xmltodict

# czi = CziFile(path)
# metadata = czi.metadata()

# metadata = xmltodict.parse(metadata)["ImageDocument"]["Metadata"]

# # sublocks = czi.subblock_directory

# # for i,block in enumerate(sublocks):
    
# #     if i == 1:
        
# #         block_start = block.start
# #         block_axes = block.axes
# #         block_mosaic_index = block.mosaic_index
# #         file_position = block.file_position
# #         file_part = block.file_part
        
# #         dimension_entries = block.dimension_entries
        
# #         for entry in dimension_entries:
            
# #             help(entry)
            
# #             entry_dimension = entry.dimension
# #             entry_size = entry.size
# #             entry_start = entry.start
# #             entry_start_coordinate = entry.start_coordinate
# #             entry_axes = entry.axes
            
# #             pass
    
# #     pass


# blocks = SubBlockSegment(czi)








#     img_shape = czi.shape
#     img_dims = czi.axes
    
#     index_dims = []
    
#     for index_name in reversed(img_dims):
#         if index_name not in ["X","Y","0"]:
#             index_shape = img_shape[0]
            
#             dim_list = np.arange(index_shape).tolist()
#             dim_list = [{index_name:dim} for dim in dim_list]
            
#             index_dims.append(dim_list)

# dim_iter = list(itertools.product(*index_dims))
# dim_iter = [dict(ChainMap(*list(dim))) for dim in dim_iter]

# dim_iter = pd.DataFrame(dim_iter)
# key_dim_cols = dim_iter.columns.drop("C").tolist()

# image_stack = czi.asarray()

# for _, data in dim_iter.groupby(key_dim_cols):
    
#     for channel_index, czi_indeces in data.iterrows():
        
#         czi_indeces = czi_indeces.to_dict()
        
#         img =
        
#         img, img_shape = imread(path, **czi_indeces)
        
        # img = img.reshape(img.shape[-2:])
        
        # plt.imshow(img[500:1000,500:1000])
        # plt.show()



def get_czi_channel_dict(path):

    from czifile import CziFile
    import xmltodict
    
    czi = CziFile(path)
    metadata = czi.metadata()
    
    metadata = xmltodict.parse(metadata)["ImageDocument"]["Metadata"]
    
    channels_metadata = metadata["Information"]["Image"]["Dimensions"]["Channels"]["Channel"]
    
    channel_dict = {}
    
    for channel_name, channel_meta in enumerate(channels_metadata):
        
        channel_dict[channel_name] = {}
        
        for key,value in channel_meta.items():
            
            if key == "@Name":
                
                if value == "Bright":
                    value = "Bright Field"
                if value == "Phase":
                    value = "Phase Contrast"
                if value == "nilRe":
                    value = "Nile Red"
            
            channel_dict[channel_name][key] = value
            
    return channel_dict

def get_czi_dim_list(path):
    
    czi = CziFile(path)
        
    img_dims = czi.dims
    img_dims_shape = czi.get_dims_shape()
    img_size = czi.size
    pixel_type = czi.pixel_type
    
    index_dims = []
    
    for index_name in ["S","T","M","Z","C"]:
        
        if index_name in img_dims_shape[0].keys():
            index_shape = img_dims_shape[0][index_name][-1]
            
            dim_list = np.arange(index_shape).tolist()
            dim_list = [{index_name:dim} for dim in dim_list]

            index_dims.append(dim_list)
            
    dim_list = list(itertools.product(*index_dims))
    dim_list = [dict(ChainMap(*list(dim))) for dim in dim_list]
    
    for dim in dim_list:
        dim.update({"path":path})
        
    dim_list = pd.DataFrame(dim_list)
        
    return dim_list

def get_zeiss_measurements(paths, import_limit=None):

    czi_measurements = []
    
    for path in paths:
        
        if os.path.exists(path):
            
            dim_list = get_czi_dim_list(path)
            
            channel_dict = get_channel_dict(path)
            
            czi_measurements.append(dim_list)
     
    czi_measurements = pd.concat(czi_measurements)
            
    groupby_columns = czi_measurements.drop(["C"], axis =1).columns.tolist()
    
    if len(groupby_columns) == 1:
        groupby_columns = groupby_columns[0]
    
    czi_fovs = []
    
    for group, data in czi_measurements.groupby(groupby_columns):
        
        czi_fovs.append(data)
         
    if type(import_limit) == int:
        czi_measurements = pd.concat(czi_fovs[:import_limit])
    
    return czi_measurements


paths = ["Snap-2388.czi"]
# path = r"C:\Users\turnerp\Desktop\trillion\Experiment-1427.czi"
# path = r"C:\Users\turnerp\Desktop\BSA DEV\WT_DAPI_PBS.czi"
# paths = [r"C:\Users\turnerp\Desktop\Trillian Nice FOVs\nice_quad_channel_WTdata.czi"]

paths = ["Snap-2388.czi", r"C:\Users\turnerp\Desktop\trillion\Experiment-1427.czi"]


import_limit = None



# czi = CziFile(path)

# czi_images = {}

# dim_list = get_czi_dim_list(czi, import_limit)
# channel_dict = get_channel_dict(path)


from aicspylibczi import CziFile

channel_names = []

for path in paths:
    channel_dict = get_czi_channel_dict(path)
    
    for key,value in channel_dict.items():
        
        channel_names.append(value["@Name"])
        
channel_names = np.unique(channel_names)


zeiss_measurements = get_zeiss_measurements(paths, import_limit)    

zeiss_images = {}

for path, dim_list in zeiss_measurements.groupby("path"):
    
    dim_list = dim_list.drop("path",axis=1).dropna(axis=1)
    
    czi = CziFile(path)
    channel_dict = get_channel_dict(path)
    
    key_dim_cols = dim_list.columns.tolist()
    key_dim_cols = dim_list.columns.drop(["C"]).tolist()
    
    if key_dim_cols == []:
        
        images, img_shape = czi.read_image()
        
        fov_channels = []
        
        for channel_index, img_channel in enumerate(images):
            
            meta = channel_dict[channel_index]
            
            channel_name = meta["@Name"]
            
            fov_channels.append(channel_name)
            
            if channel_name not in zeiss_images:
                zeiss_images[channel_name] = dict(images=[img_channel], masks=[], nmasks=[], classes=[], metadata={0: meta}, )
            else:
                zeiss_images[channel_name]["images"].append(img_channel)
                zeiss_images[channel_name]["metadata"][0] = meta
        
        missing_channels = [channel for channel in channel_names if channel not in fov_channels]
        
        for channel_name in missing_channels:
            
            img_channel = np.zeros_like(img_channel)
            
            if channel_name not in zeiss_images:
                zeiss_images[channel_name] = dict(images=[img_channel], masks=[], nmasks=[], classes=[], metadata={0: {}}, )
            else:
                zeiss_images[channel_name]["images"].append(img_channel)
                zeiss_images[channel_name]["metadata"][0] = meta
            
    else:
        
        iter = 0
        
        for i, (_, data) in enumerate(dim_list.groupby(key_dim_cols)):
            
            data = data.reset_index(drop=True).dropna().astype(int)
            
            fov_channels = []
            
            for channel_index, czi_indeces in data.iterrows():
                
                czi_indeces = czi_indeces.to_dict()
                
                img, img_shape = czi.read_image(**czi_indeces)
                
                img_channel = img.reshape(img.shape[-2:])
                
                meta = channel_dict[channel_index]
                
                channel_name = meta["@Name"]
                
                fov_channels.append(channel_name)
                
                if channel_name not in zeiss_images:
                    zeiss_images[channel_name] = dict(images=[img_channel], masks=[], nmasks=[], classes=[], metadata={i: meta}, )
                else:
                    zeiss_images[channel_name]["images"].append(img_channel)
                    zeiss_images[channel_name]["metadata"][i] = meta
                
            missing_channels = [channel for channel in channel_names if channel not in fov_channels]
            
            for channel_name in missing_channels:
                
                img_channel = np.zeros_like(img_channel)
                
                if channel_name not in zeiss_images:
                    zeiss_images[channel_name] = dict(images=[img_channel], masks=[], nmasks=[], classes=[], metadata={0: {}}, )
                else:
                    zeiss_images[channel_name]["images"].append(img_channel)
                    zeiss_images[channel_name]["metadata"][0] = meta
























































# index_dims = []

# for index_name in reversed(img_dims):
#     if index_name not in ["X","Y"]:
#         index_shape = img_dims_shape[0][index_name][-1]
        
#         dim_list = np.arange(index_shape).tolist()
#         dim_list = [{index_name:dim} for dim in dim_list]
        
#         index_dims.append(dim_list)

# dim_iter = list(itertools.product(*index_dims))
# dim_iter = [dict(ChainMap(*list(dim))) for dim in dim_iter]

# dim_iter = pd.DataFrame(dim_iter)
# key_dim_cols = dim_iter.columns.drop("C").tolist()

# for _, data in dim_iter.groupby(key_dim_cols):
    
#     for channel_index, czi_indeces in data.iterrows():
        
#         czi_indeces = czi_indeces.to_dict()
        
#         img, img_shape = czi.read_image(**czi_indeces)
        
#         img = img.reshape(img.shape[-2:])
        
#         plt.imshow(img[500:1000,500:1000])
#         plt.show()
        


    



# sample_dict = dim_iter[0]
# desired_order_list = img_dims


# reordered_dict = {k: sample_dict[k] for k in desired_order_list}

# for dim in dim_iter:
    
#     img, img_dims = czi.read_image(**dim)
    
#     C,X,Y = img.shape[-3:]
    
#     image_channels = img.flat[:C*X*Y].reshape(C,X,Y)
    
#     for chanel_index, img in enumerate(image_channels):
        
#         if chanel_index == 1:
#             plt.imshow(img[500:1000,500:1000])
#             plt.show()
        
        
    
    
    
    


    




# iter_dims = img_size[:-3]

# for S in range(iter_dims[0]):
    
#     for j in range(iter_dims[0]):
        
#         for channel in range(img_size[-3]):
            
#             czi.read_image(S=13, Z=16)



# The Z-dimension.
# The C-dimension ("channel").
# The T-dimension ("time").
# The R-dimension ("rotation").
# The S-dimension ("scene").
# The I-dimension ("illumination").
# The H-dimension ("phase").
# The V-dimension ("view").

