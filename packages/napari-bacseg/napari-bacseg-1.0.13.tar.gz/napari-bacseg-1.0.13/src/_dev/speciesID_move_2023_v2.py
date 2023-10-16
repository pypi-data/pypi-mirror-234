
import pandas as pd
import os
import numpy as np
from glob2 import glob
from aicspylibczi import CziFile
import itertools
from collections import ChainMap
import copy
import tifffile
import tempfile
import hashlib
from tiler import Tiler, Merger
import cv2
import datetime
import pathlib
import json
from multiprocessing import Pool
import tqdm
import pickle

os.chdir(r"G:\Piers\SpeciesID DAPI-FM143-WGA647")


def export_coco_json(image_name, image, mask, nmask, label, file_path):
    
    file_path = os.path.splitext(file_path)[0] + ".txt"

    info = {"description": "COCO 2017 Dataset", "url": "http://cocodataset.org", "version": "1.0", "year": datetime.datetime.now().year, "contributor": "COCO Consortium", "date_created": datetime.datetime.now().strftime("%d/%m/%y"), }

    categories = [{"supercategory": "cell", "id": 1, "name": "single"}, {"supercategory": "cell", "id": 2, "name": "dividing"}, {"supercategory": "cell", "id": 3, "name": "divided"},
        {"supercategory": "cell", "id": 4, "name": "vertical"}, {"supercategory": "cell", "id": 5, "name": "broken"}, {"supercategory": "cell", "id": 6, "name": "edge"}, ]

    licenses = [{"url": "https://creativecommons.org/licenses/by-nc-nd/4.0/", "id": 1, "name": "Attribution-NonCommercial-NoDerivatives 4.0 International", }]

    height, width = image.shape[-2], image.shape[-1]

    images = [{"license": 1, "file_name": image_name, "coco_url": "", "height": height, "width": width, "date_captured": "", "flickr_url": "", "id": 0, }]

    mask_ids = np.unique(mask)

    annotations = []

    for j in range(len(mask_ids)):
        if j != 0:
            try:
                cnt_mask = mask.copy()

                cnt_mask[cnt_mask != j] = 0

                contours, _ = cv2.findContours(cnt_mask.astype(np.uint8), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE, )
                cnt = contours[0]

                # cnt coco bounding box
                x, y, w, h = cv2.boundingRect(cnt)
                y1, y2, x1, x2 = y, (y + h), x, (x + w)
                coco_BBOX = [x1, y1, h, w]

                # cnt area
                area = cv2.contourArea(cnt)

                segmentation = cnt.reshape(-1, 1).flatten()

                cnt_labels = np.unique(label[cnt_mask != 0])

                if len(cnt_labels) == 0:
                    cnt_label = 1

                else:
                    cnt_label = int(cnt_labels[0])

                annotation = {"segmentation": [segmentation.tolist()], "area": area, "iscrowd": 0, "image_id": 0, "bbox": coco_BBOX, "category_id": cnt_label, "id": j, }

                annotations.append(annotation)

            except:
                pass

    nmask_ids = np.unique(nmask)

    for j in range(len(nmask_ids)):
        if j != 0:
            try:
                cnt_mask = nmask.copy()

                cnt_mask[cnt_mask != j] = 0

                contours, _ = cv2.findContours(cnt_mask.astype(np.uint8), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE, )
                cnt = contours[0]

                # cnt coco bounding box
                x, y, w, h = cv2.boundingRect(cnt)
                y1, y2, x1, x2 = y, (y + h), x, (x + w)
                coco_BBOX = [x1, y1, h, w]

                # cnt area
                area = cv2.contourArea(cnt)

                segmentation = cnt.reshape(-1, 1).flatten()

                cnt_labels = np.unique(label[cnt_mask != 0])

                if len(cnt_labels) == 0:
                    cnt_label = 1

                else:
                    cnt_label = int(cnt_labels[0])

                annotation = {"nucleoid_segmentation": [segmentation.tolist()], "area": area, "iscrowd": 0, "image_id": 0, "bbox": coco_BBOX, "category_id": cnt_label, "id": j, }

                annotations.append(annotation)

            except:
                pass

    annotation = {"info": info, "licenses": licenses, "images": images, "annotations": annotations, "categories": categories, }

    with open(file_path, "w") as f:
        json.dump(annotation, f)

    return annotation


def get_species_info():
    
    species_dict = {'BSB': {'species_name': 'streptococcus agalactiae', 'gram': 'positive', 'shape':'cocci', 'formations':['chain']},
                    'ECOL': {'species_name': 'escherichia coli', 'gram': 'negative', 'shape':'rod', 'formations':[]},
                    'EFM': {'species_name': 'enterococcus faecium', 'gram': 'positive', 'shape':'cocci', 'formations':['pair','chain']},
                    'EF': {'species_name': 'enterococcus faecalis', 'gram': 'negative', 'shape':'cocci', 'formations':['pair','chain']},
                    'ENTC': {'species_name': 'enterobacter cloacae', 'gram': 'negative', 'shape':'rod', 'formations':[]},
                    'KLAE': {'species_name': 'klebsiella aerogenes', 'gram': 'negative', 'shape':'rod', 'formations':[]},
                    'KLPN': {'species_name': 'klebsiella pneumoniae', 'gram': 'negative', 'shape':'rod', 'formations':[]},
                    'LMON': {'species_name': 'listeria monocytogenes', 'gram': 'positive', 'shape':'rod', 'formations':[]},
                    'PSAR': {'species_name': 'pseudomonas aeruginosa', 'gram': 'negative', 'shape':'rod', 'formations':[]},
                    'PSMA': {'species_name': 'stenotrophomonas maltophilia', 'gram': 'negative', 'shape':'rod', 'formations':[]},
                    'SAUR': {'species_name': 'staphylococcus aureus', 'gram': 'positive', 'shape':'cocci', 'formations':['cluster']},
                    'SEPI': {'species_name': 'staphylococcus epidermidis', 'gram': 'positive', 'shape':'cocci', 'formations':['cluster']},
                    'SERM': {'species_name': 'serratia marcescens', 'gram': 'negative', 'shape':'rod', 'formations':[]},
                    'SLUG': {'species_name': 'staphylococcus lugdunensis', 'gram': 'positive', 'shape':'cocci', 'formations':['pair','cluster']},
                    'STCP': {'species_name': 'staphylococcus capitis', 'gram': 'positive', 'shape':'cocci', 'formations':['cluster']},
                    'SAENA': {'species_name': 'salmonella enterica', 'gram': 'negative', 'shape':'rod', 'formations':[]},
                    'ACAA': {'species_name': 'acinetobacter baumannii', 'gram': 'negative', 'shape':'rod', 'formations':[]},
                    'BAFR': {'species_name': 'bacteriodes fragilis', 'gram': 'negative', 'shape':'rod', 'formations':[]},
                    'HFLU': {'species_name': 'haemophilus influenzae', 'gram': 'negative', 'shape':'rod', 'formations':[]},
                    'STP': {'species_name': 'streptococcus pneumoniae', 'gram': 'positive', 'shape':'cocci', 'formations':[]},
                    'BSA': {'species_name': 'streptococcus pyogenes', 'gram': 'positive', 'shape':'cocci', 'formations':['chain']},
                    'NMEN': {'species_name': 'streptococcus pyogenes', 'gram': 'negative', 'shape':'cocci', 'formations':['pair']},
                    }
    
    def process_species_info(dat):
        
        species_name = dat["Species"].lower()
        species_code = dat["Code"]
        species_shape = species_dict[species_code]["shape"]
        
        dat["Species"] = species_name
        dat["Shape"] = species_shape
        
        return dat 

    species_info = pd.read_excel("Reference_Clinical_strains_locations.xlsx").iloc[:,:8]

    species_info = species_info.apply(lambda row: process_species_info(row), axis=1)

    columns = species_info.columns.tolist()
    columns.pop(columns.index("Shape"))
    columns.insert(4, "Shape")

    species_info = species_info[columns]
    
    return species_info

def get_ziess_channel_dict(path):
    
    import xmltodict
    from czifile import CziFile

    czi = CziFile(path)
    metadata = czi.metadata()

    metadata = xmltodict.parse(metadata)["ImageDocument"]["Metadata"]

    channels_metadata = metadata["Information"]["Image"]["Dimensions"]["Channels"]["Channel"]

    channel_dict = {}

    for channel_name, channel_meta in enumerate(channels_metadata):
        channel_dict[channel_name] = {}

        for key, value in channel_meta.items():
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

    for index_name in ["S", "T", "M", "Z", "C"]:
        if index_name in img_dims_shape[0].keys():
            index_shape = img_dims_shape[0][index_name][-1]

            dim_list = np.arange(index_shape).tolist()
            dim_list = [{index_name: dim} for dim in dim_list]

            index_dims.append(dim_list)

    dim_list = list(itertools.product(*index_dims))
    dim_list = [dict(ChainMap(*list(dim))) for dim in dim_list]

    for dim in dim_list:
        dim.update({"path": path})

    dim_list = pd.DataFrame(dim_list)

    return dim_list


def get_zeiss_measurements(paths, import_limit="None"):
    
    if type(paths) != list:
        paths = [paths]
    
    czi_measurements = []

    for path in paths:
        if os.path.exists(path):
            dim_list = get_czi_dim_list(path)

            czi_measurements.append(dim_list)

    czi_measurements = pd.concat(czi_measurements)

    groupby_columns = czi_measurements.drop(["C"], axis=1).columns.tolist()

    if len(groupby_columns) == 1:
        groupby_columns = groupby_columns[0]

    czi_fovs = []

    for group, data in czi_measurements.groupby(groupby_columns):
        czi_fovs.append(data)

    if import_limit != "None":
        import_limit = int(import_limit)

        czi_fovs = czi_fovs[:import_limit]
        num_measurements = len(czi_fovs)
        czi_measurements = pd.concat(czi_fovs)

    else:
        num_measurements = len(czi_fovs)
        czi_measurements = pd.concat(czi_fovs)

    channel_names = []

    for path in paths:
        channel_dict = get_ziess_channel_dict(path)

        for key, value in channel_dict.items():
            channel_names.append(value["@Name"])

    channel_names = np.unique(channel_names)

    return czi_measurements, channel_names


def get_hash(img_path=None, img=None):
    
    if img is not None:
        img_path = tempfile.TemporaryFile(suffix=".tif").name
        tifffile.imwrite(img_path, img)

        with open(img_path, "rb") as f:
            bytes = f.read()  # read entire file as bytes
            hash_code = hashlib.sha256(bytes).hexdigest()

        os.remove(img_path)

    else:
        with open(img_path, "rb") as f:
            bytes = f.read()  # read entire file as bytes
            hash_code = hashlib.sha256(bytes).hexdigest()

    return hash_code


def read_zeiss_image_files(zeiss_measurements, channel_names, tile_shape=(500,500), overlap = 10):

    from aicspylibczi import CziFile

    zeiss_images = {}

    num_loaded = 0
    img_index = {}

    for path, dim_list in zeiss_measurements.groupby("path"):
        path = os.path.normpath(path)

        dim_list = dim_list.drop("path", axis=1).dropna(axis=1)

        czi = CziFile(path)
        channel_dict = get_ziess_channel_dict(path)

        key_dim_cols = dim_list.columns.tolist()
        key_dim_cols = dim_list.columns.drop(["C"]).tolist()

        if key_dim_cols == []:
            images, img_shape = czi.read_image()
            
            fov_channels = []
            
            if len(key_dim_cols) == 1:
                key_dim_cols = key_dim_cols[0]

            for channel_index, img_channel in enumerate(images):
                akseg_hash = get_hash(img=img_channel)
                contrast_limit = np.percentile(img_channel, (1, 99))
                contrast_limit = [int(contrast_limit[0] * 0.5), int(contrast_limit[1] * 2), ]

                meta = copy.deepcopy(channel_dict[channel_index])

                image_name = os.path.basename(path).replace(".czi", "")
                image_name = image_name + "_" + meta["@Name"].replace(" ", "")

                meta["akseg_hash"] = akseg_hash
                meta["image_name"] = image_name
                meta["image_path"] = path
                meta["folder"] = path.split(os.sep)[-2]
                meta["mask_name"] = None
                meta["mask_path"] = None
                meta["label_name"] = None
                meta["label_path"] = None
                meta["import_mode"] = "image"
                meta["contrast_limit"] = contrast_limit
                meta["contrast_alpha"] = 0
                meta["contrast_beta"] = 0
                meta["contrast_gamma"] = 0
                meta["dims"] = [img_channel.shape[-1], img_channel.shape[-2]]
                meta["crop"] = [0, img_channel.shape[-2], 0, img_channel.shape[-1], ]

                channel_name = meta["@Name"]

                if channel_name not in img_index.keys():
                    img_index[channel_name] = 0

                fov_channels.append(channel_name)

                if channel_name not in zeiss_images:
                    zeiss_images[channel_name] = dict(images=[img_channel], masks=[], nmasks=[], classes=[], metadata={img_index[channel_name]: meta}, )
                else:
                    zeiss_images[channel_name]["images"].append(img_channel)
                    zeiss_images[channel_name]["metadata"][img_index[channel_name]] = meta

                img_index[channel_name] += 1

            missing_channels = [channel for channel in channel_names if channel not in fov_channels]

            for channel_name in missing_channels:

                img_channel = np.zeros_like(img_channel)

                meta = {}
                meta["image_name"] = "missing image channel"
                meta["image_path"] = "missing image channel"
                meta["folder"] = (None,)
                meta["parent_folder"] = (None,)
                meta["akseg_hash"] = None
                meta["fov_mode"] = None
                meta["import_mode"] = "NIM"
                meta["contrast_limit"] = None
                meta["contrast_alpha"] = None
                meta["contrast_beta"] = None
                meta["contrast_gamma"] = None
                meta["dims"] = [img_channel.shape[-1], img_channel.shape[-2]]
                meta["crop"] = [0, img_channel.shape[-2], 0, img_channel.shape[-1], ]
                meta["light_source"] = channel_name

                if channel_name not in img_index.keys():
                    img_index[channel_name] = 0

                if channel_name not in zeiss_images:
                    zeiss_images[channel_name] = dict(images=[img_channel], masks=[], nmasks=[], classes=[], metadata={img_index[channel_name]: {}}, )
                else:
                    zeiss_images[channel_name]["images"].append(img_channel)
                    zeiss_images[channel_name]["metadata"][img_index[channel_name]] = meta

                img_index[channel_name] += 1
        else:
            iter = 0
            
            if len(key_dim_cols) == 1:
                key_dim_cols = key_dim_cols[0]
            
            for i, (_, data) in enumerate(dim_list.groupby(key_dim_cols)):
                data = data.reset_index(drop=True).dropna().astype(int)

                fov_channels = []

                for channel_index, czi_indeces in data.iterrows():

                    czi_indeces = czi_indeces.to_dict()

                    img, img_shape = czi.read_image(**czi_indeces)
                    
                    img_channel = img.reshape(img.shape[-2:])

                    akseg_hash = get_hash(img=img_channel)
                    contrast_limit = np.percentile(img_channel, (1, 99))
                    contrast_limit = [int(contrast_limit[0] * 0.5), int(contrast_limit[1] * 2), ]

                    meta = copy.deepcopy(channel_dict[channel_index])

                    image_name = os.path.basename(path).replace(".czi", "")

                    for key, value in czi_indeces.items():
                        image_name = image_name + "_" + str(key) + str(value)

                    image_name = (image_name + "_" + meta["@Name"].replace(" ", "") + ".tif")

                    meta["akseg_hash"] = akseg_hash
                    meta["image_name"] = copy.deepcopy(image_name)
                    meta["image_path"] = path
                    meta["folder"] = path.split(os.sep)[-2]
                    meta["mask_name"] = None
                    meta["mask_path"] = None
                    meta["label_name"] = None
                    meta["label_path"] = None
                    meta["import_mode"] = "image"
                    meta["contrast_limit"] = contrast_limit
                    meta["contrast_alpha"] = 0
                    meta["contrast_beta"] = 0
                    meta["contrast_gamma"] = 0
                    meta["dims"] = [img_channel.shape[-1], img_channel.shape[-2], ]
                    meta["crop"] = [0, img_channel.shape[-2], 0, img_channel.shape[-1], ]

                    channel_name = copy.deepcopy(meta["@Name"])

                    if channel_name not in img_index.keys():
                        img_index[channel_name] = 0

                    fov_channels.append(channel_name)

                    if channel_name not in zeiss_images.keys():
                        zeiss_images[channel_name] = dict(images=[img_channel], masks=[], nmasks=[], classes=[], metadata={img_index[channel_name]: meta}, )
                    else:
                        zeiss_images[channel_name]["images"].append(img_channel)
                        zeiss_images[channel_name]["metadata"][img_index[channel_name]] = meta

                    img_index[channel_name] += 1

                missing_channels = [channel for channel in channel_names if channel not in fov_channels]

                for channel_name in missing_channels:
                    img_channel = np.zeros_like(img_channel)

                    meta = {}
                    meta["image_name"] = "missing image channel"
                    meta["image_path"] = "missing image channel"
                    meta["folder"] = (None,)
                    meta["parent_folder"] = (None,)
                    meta["akseg_hash"] = None
                    meta["fov_mode"] = None
                    meta["import_mode"] = "NIM"
                    meta["contrast_limit"] = None
                    meta["contrast_alpha"] = None
                    meta["contrast_beta"] = None
                    meta["contrast_gamma"] = None
                    meta["dims"] = [img_channel.shape[-1], img_channel.shape[-2], ]
                    meta["crop"] = [0, img_channel.shape[-2], 0, img_channel.shape[-1], ]
                    meta["light_source"] = channel_name

                    if channel_name not in img_index.keys():
                        img_index[channel_name] = 0

                    if channel_name not in zeiss_images:
                        zeiss_images[channel_name] = dict(images=[img_channel], masks=[], nmasks=[], classes=[], metadata={img_index[channel_name]: meta}, )
                    else:
                        zeiss_images[channel_name]["images"].append(img_channel)
                        zeiss_images[channel_name]["metadata"][img_index[channel_name]] = meta

                    img_index[channel_name] += 1

    imported_data = dict(imported_images=zeiss_images)

    return imported_data

def tile_imported_data(imported_data, tile_shape=(1024,1024), overlap = 0):

    tiled_zeiss_data = {}
    img_index = {}
    
    for channel, channel_data in imported_data.items():
        
        for img, metadata in zip(channel_data["images"],channel_data["metadata"].values()):
            
            image_name = metadata["image_name"]
            channel_name = metadata["@Name"]
            
            if channel_name not in img_index.keys():
                img_index[channel_name] = 0
            
            tiler_object = Tiler(data_shape=img.shape,
                                  tile_shape=tile_shape,
                                  overlap=overlap)
    
            for tile_id, tile_img in tiler_object.iterate(img):
                
                if tile_img.shape==tile_shape:
                    
                    tile_meta = copy.deepcopy(metadata)
                    
                    akseg_hash = get_hash(img=tile_img)
                    contrast_limit = np.percentile(tile_img, (1, 99))
                    contrast_limit = [int(contrast_limit[0] * 0.5), int(contrast_limit[1] * 2), ]
                
                    tile_name = str(image_name).split(".")[0] + "_tile" + str(tile_id) + ".tif"
                    
                    tile_meta["image_name"] = tile_name
                    tile_meta["akseg_hash"] = akseg_hash
                    tile_meta["contrast_limit"] = contrast_limit
                                    
                    if channel_name not in tiled_zeiss_data:
                        tiled_zeiss_data[channel_name] = dict(images=[tile_img], masks=[], nmasks=[], classes=[], metadata={img_index[channel_name]: tile_meta}, )
                    else:
                        tiled_zeiss_data[channel_name]["images"].append(tile_img)
                        tiled_zeiss_data[channel_name]["metadata"][img_index[channel_name]] = tile_meta
                
                    img_index[channel_name] += 1


    return tiled_zeiss_data

def append_specific_metadata(imported_data, species_info, segmentation_channel = "Phase Contrast"):
    
    for channel, channel_data in imported_data.items():
        
        for i, (img, metadata) in enumerate(zip(channel_data["images"],channel_data["metadata"].values())):
            
            image_name = metadata["image_name"]
            
            channel_name = metadata["@Name"]
            species_code = image_name.split("_")[3]
            plate_name = metadata["folder"].split("_")[2]
            plate_index = int(plate_name.replace("plate",""))
            
            species_data = species_info[(species_info["Code"] == species_code) & (species_info["Set"] == plate_index)]
            
            species_name = species_data["Species"].values[0]
            content = species_name.split(" ")[0][0].capitalize() + "." + species_name.split(" ")[1].capitalize()
            
            imported_data[channel]["metadata"][i]["species_code"] = species_code
            imported_data[channel]["metadata"][i]["species_name"] = species_data["Species"].values[0]
            imported_data[channel]["metadata"][i]["species_shape"] = species_data["Shape"].values[0]
            
            imported_data[channel]["metadata"][i]["strain"] = species_data["Strain"].values[0]
            imported_data[channel]["metadata"][i]["content"] = content
            
            imported_data[channel]["metadata"][i]["user_initial"] = "PT"
            
            imported_data[channel]["metadata"][i]["microscope"] = "Trillian"
            imported_data[channel]["metadata"][i]["mounting method"] = "Agarose Pads"
            
            imported_data[channel]["metadata"][i]["antibiotic"] = "None"
            imported_data[channel]["metadata"][i]["antibiotic concentration"] = ""
            imported_data[channel]["metadata"][i]["treatment time (mins)"] = ""
            imported_data[channel]["metadata"][i]["phenotype"] = "Untreated"
            imported_data[channel]["metadata"][i]["protocol"] = ""
            
            imported_data[channel]["metadata"][i]["user_meta1"] = "Trillian Gram Stain FM143"
            imported_data[channel]["metadata"][i]["user_meta2"] = plate_name
            imported_data[channel]["metadata"][i]["user_meta3"] = ""
            imported_data[channel]["metadata"][i]["user_meta4"] = ""
            imported_data[channel]["metadata"][i]["user_meta5"] = ""
            imported_data[channel]["metadata"][i]["user_meta6"] = ""
            
    return imported_data



def append_generic_metadata(imported_data, akseg_directory, user_initial = "PT", segmentation_channel = "Phase Contrast"):
    
    channel_list_dict = {}

    for channel, channel_data in imported_data.items():
        
        for i, (img, metadata) in enumerate(zip(channel_data["images"],channel_data["metadata"].values())):
            
            image_name = metadata["image_name"]
            channel_name = metadata["@Name"]
            
            if i not in channel_list_dict.keys():
                channel_list_dict[i] = {"channel_list":[], "file_list":[], "segmentation_file":"", "segmentation_channel":""}
                
            if channel_name not in channel_list_dict[i]["channel_list"]:
                channel_list_dict[i]["channel_list"].append(channel_name)
                
            if image_name not in channel_list_dict[i]["file_list"]:
                channel_list_dict[i]["file_list"].append(image_name)
                
            if channel_name == segmentation_channel:
                channel_list_dict[i]["segmentation_file"] = image_name
                channel_list_dict[i]["segmentation_channel"] = channel_name
                
     
    for channel, channel_data in imported_data.items():
        
        for i, (img, metadata) in enumerate(zip(channel_data["images"],channel_data["metadata"].values())):
            
            image_laplacian = cv2.Laplacian(img, cv2.CV_64F).var()
            
            image_name = metadata["image_name"]
            image_path = os.path.normpath(metadata["image_path"])
            
            folder = image_path.split(os.sep)[-2]
            parent_folder = image_path.split(os.sep)[-3]
            
            channel_name = metadata["@Name"]
            
            date_created = datetime.datetime.strptime(image_name.split("_")[0], '%d%m%y').strftime("%d/%m/%y")
             
            file_list = channel_list_dict[i]["file_list"]
            channel_list = channel_list_dict[i]["channel_list"]
            segmentation_file = channel_list_dict[i]["segmentation_file"]
            egmentation_channel = channel_list_dict[i]["segmentation_channel"]
            
            if channel_name == "Bright Field":
                source = 'White Light'
                modality = channel_name
                stain = ""
                stain_target = ""
            if channel_name == "Phase Contrast":
                source = 'White Light'
                modality = channel_name
                stain = ""
                stain_target = ""
            if channel_name == "Nile Red":
                source = 'LED'
                modality = 'Epifluorescence'
                stain = "Nile Red"
                stain_target = "membrane"
            if channel_name == "DAPI":
                stain = "DAPI"
                stain_target = "membrane"
                source = 'LED'
                modality = 'Epifluorescence'
            if channel_name == "AF647":
                source = 'LED'
                modality = 'Epifluorescence'
                stain = "WGA-647"
                stain_target = "membrane"
            if channel_name == "AF488":
                source = 'LED'
                modality = 'Epifluorescence'
                stain = "WGA-647"
                stain_target = "membrane"
            if channel_name == "Fm143":
                source = 'LED'
                modality = 'Epifluorescence'
                stain = "WGA-647"
                stain_target = "membrane"
                
            imported_data[channel]["metadata"][i]["file_name"] = image_name
            imported_data[channel]["metadata"][i]["channel"] = channel
            imported_data[channel]["metadata"][i]["folder"] = folder
            imported_data[channel]["metadata"][i]["parent_folder"] = parent_folder
            
            imported_data[channel]["metadata"][i]["segmentation_file"] = segmentation_file
            imported_data[channel]["metadata"][i]["segmentation_channel"] = segmentation_channel
            imported_data[channel]["metadata"][i]["num_segmentations"] = 0
            
            imported_data[channel]["metadata"][i]["file_list"] = file_list
            imported_data[channel]["metadata"][i]["channel_list"] = channel_list
            
            imported_data[channel]["metadata"][i]["source"] = source
            imported_data[channel]["metadata"][i]["image_laplacian"] = image_laplacian
            imported_data[channel]["metadata"][i]["modality"] = modality
            imported_data[channel]["metadata"][i]["stain"] = stain
            imported_data[channel]["metadata"][i]["stain_target"] = stain_target
            
            imported_data[channel]["metadata"][i]["posX"] = 0
            imported_data[channel]["metadata"][i]["posY"] = 0
            imported_data[channel]["metadata"][i]["posZ"] = 0
            
            imported_data[channel]["metadata"][i]["date_created"] = date_created
            imported_data[channel]["metadata"][i]["date_uploaded"] = datetime.datetime.now().strftime("%d/%m/%y")
            imported_data[channel]["metadata"][i]["date_modified"] = datetime.datetime.now().strftime("%d/%m/%y")
            
           
            imported_data[channel]["metadata"][i]["segmented"] = False
            imported_data[channel]["metadata"][i]["labelled"] = False
            imported_data[channel]["metadata"][i]["segmentation_curated"] = False
            imported_data[channel]["metadata"][i]["label_curated"] = False
            
            imported_data[channel]["metadata"][i]["image_load_path"] = image_path
            imported_data[channel]["metadata"][i]["mask_load_path"] = ""
            imported_data[channel]["metadata"][i]["label_load_path"] = ""
            
            imported_data[channel]["metadata"][i]["image_focus"] = 0
            imported_data[channel]["metadata"][i]["image_debris"] = 0
            
            paths = generate_bacseg_paths(akseg_directory, user_initial, folder, image_name, segmentation_file)
            
            imported_data[channel]["metadata"][i]["image_save_path"] = paths["image_save_path"]
            imported_data[channel]["metadata"][i]["mask_save_path"] = paths["mask_save_path"]
            imported_data[channel]["metadata"][i]["label_save_path"] = paths["label_save_path"]
            imported_data[channel]["metadata"][i]["json_save_path"] = paths["json_save_path"]
            
    return imported_data


    
def generate_bacseg_paths(akseg_directory, user_initial, folder, image_name, segmentation_file):
    
    image_dir = os.path.join(akseg_directory,"Images", user_initial,"images",folder)
    mask_dir = os.path.join(akseg_directory,"Images", user_initial,"masks",folder)
    label_dir = os.path.join(akseg_directory,"Images", user_initial,"labels",folder)
    json_dir = os.path.join(akseg_directory,"Images", user_initial,"json",folder)
    
    segmentation_file_json = pathlib.Path(segmentation_file).with_suffix('.txt')
    
    
    if os.path.exists(image_dir)==False:
        try:
            os.makedirs(image_dir)
        except Exception:
            pass
       
    if os.path.exists(mask_dir)==False:
        try:
            os.makedirs(mask_dir)
        except Exception:
            pass
        
    if os.path.exists(label_dir)==False:
        try:
            os.makedirs(label_dir)
        except Exception:
            pass
       
    if os.path.exists(json_dir)==False:
        try:
            os.makedirs(json_dir)
        except Exception:
            pass

    image_save_path = os.path.join(image_dir, image_name)
    mask_save_path = os.path.join(mask_dir, segmentation_file)
    label_save_path = os.path.join(label_dir, segmentation_file)
    json_save_path = os.path.join(json_dir, segmentation_file_json)
        
    paths = dict(image_save_path=image_save_path, 
                 mask_save_path=mask_save_path, 
                 label_save_path=label_save_path, 
                 json_save_path=json_save_path)

    return paths
    

def upload_files(upload_data):
    
    try:

        file_meta_list = []     
        
        (img, img_metadata, user_metadata_columns) = upload_data
            
        file_meta = {}
    
        for column in user_metadata_columns:
            
            if column in img_metadata.keys():
                
                file_meta[column] = img_metadata[column]
                
        image_name = img_metadata["image_name"]
        image_channel = img_metadata["channel"]
        segmentation_channel = img_metadata["segmentation_channel"]
        
        image_save_path = img_metadata["image_save_path"]
        mask_save_path = img_metadata["mask_save_path"]
        label_save_path = img_metadata["label_save_path"]
        json_save_path = img_metadata["json_save_path"]
        
        mask = np.zeros(img.shape, dtype=np.uint16)
        
        tifffile.imwrite(image_save_path, img, metadata=img_metadata)
    
        if image_channel == segmentation_channel:
            
            export_coco_json(image_name, img, mask, mask, mask, json_save_path)
            
            tifffile.imwrite(mask_save_path, mask, metadata=img_metadata)
            tifffile.imwrite(label_save_path, mask, metadata=img_metadata)
            
        file_meta_list.append(file_meta)
        
    except:
        file_meta_list = None
                
    return file_meta_list


def extract_upload_data(imported_data, user_metadata_columns):
    
    upload_data = []
    
    for channel, channel_data in imported_data.items():
        
        for i, (img, img_metadata) in enumerate(zip(channel_data["images"],channel_data["metadata"].values())):    
            
            upload_data.append([img, img_metadata, user_metadata_columns])
            
    del imported_data
    
    
    return upload_data




if __name__=='__main__':
    
    new_metadata = []

    akseg_directory = r"\\physics\dfs\DAQ\CondensedMatterGroups\AKGroup\Piers\AKSEG" 
    
    user_metadata_path = r"\\physics\dfs\DAQ\CondensedMatterGroups\AKGroup\Piers\AKSEG\Images\PT\PT_file_metadata.txt"
    user_metadata = pd.read_csv(user_metadata_path, converters={'channel_list': lambda x: x.strip("[]").split(", "),
                                                    'file_list': lambda x: x.strip("[]").split(", ")}, low_memory=False)
    
    user_metadata_columns = user_metadata.columns.tolist()
    
    species_info = get_species_info()
    
    paths = glob("*/*.czi")
    paths = [os.path.abspath(path) for path in paths]
    
    for i in range(len(paths)):
        
        try:
        
            print(f"procesing .czi file {os.path.basename(paths[i])}")
        
            zeiss_measurements, channel_names = get_zeiss_measurements(paths[i])
            
            imported_data = read_zeiss_image_files(zeiss_measurements, channel_names)["imported_images"]
            
            imported_data = tile_imported_data(imported_data, tile_shape=(1024,1024), overlap = 0)
            
            imported_data = append_generic_metadata(imported_data, akseg_directory, segmentation_channel="Phase Contrast")
            imported_data = append_specific_metadata(imported_data, species_info)
        
            upload_data = extract_upload_data(imported_data, user_metadata_columns)
            
            with Pool() as p:
                
                d = list(tqdm.tqdm(p.imap(upload_files,upload_data), total=len(upload_data)))
                p.close()
                p.join()
                
                d = [dat for dat in d if dat!=None]
            
            new_metadata.extend(d)
            
        except:
            pass

    with open('new_metadata.pickle', 'wb') as handle:
        pickle.dump(new_metadata, handle, protocol=pickle.HIGHEST_PROTOCOL)

    with open('new_metadata.pickle', 'rb') as handle:
        new_metadata = pickle.load(handle)

    new_metadata = [dat[0] for dat in new_metadata]
    
    new_metadata = pd.DataFrame(new_metadata)
    
    user_metadata = pd.concat((user_metadata,new_metadata))
    
    user_metadata.drop_duplicates(subset=['akseg_hash'], keep="last", inplace=True)  
    
    user_metadata.to_csv(user_metadata_path, sep=",", index = False)
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    