


import pandas as pd
from csv import Sniffer
import pathlib
import os
from glob2 import glob
import pickle
import numpy as np

def update_akseg_paths(path, AKSEG_DIRECTORY):
    
    try:
    
        path = pathlib.Path(path.replace("\\","/"))
        AKSEG_DIRECTORY = pathlib.Path(AKSEG_DIRECTORY)
        
        parts = (*AKSEG_DIRECTORY.parts, "Images", *path.parts[-4:])
        path = pathlib.Path('').joinpath(*parts)

    except:
        path = None

    return path


def generate_json_path(dat, AKSEG_DIRECTORY):
    
    AKSEG_DIRECTORY = pathlib.Path(AKSEG_DIRECTORY)
    segmentation_file = dat["segmentation_file"]
    path = pathlib.Path(dat["mask_save_path"])
    
    segmentation_file = pathlib.Path(segmentation_file).with_suffix('.txt')
    
    parts = (*AKSEG_DIRECTORY.parts, "Images", path.parts[-4], "json", path.parts[-2], segmentation_file)
    path = pathlib.Path('').joinpath(*parts)
    
    return path



# path = r"\\physics\dfs\DAQ\CondensedMatterGroups\AKGroup\Piers\AKSEG\Images\PT\PT_file_metadata.txt"
# AKSEG_DIRECTORY = r"\\physics\dfs\DAQ\CondensedMatterGroups\AKGroup\Piers\AKSEG"

# paths = glob(AKSEG_DIRECTORY + r"/Images/*/*.txt")

# akseg_metadata = []
# for path in paths:
#     try:
#         meta = pd.read_csv(path, converters={'channel_list': lambda x: x.strip("[]").split(", "),
#                                                         'file_list': lambda x: x.strip("[]").split(", ")}, low_memory=False)
#         akseg_metadata.append(meta)
#     except:
#         print(path)
        
        
        
# with open('akseg_metadata.pickle', 'wb') as handle:
#     pickle.dump(akseg_metadata, handle, protocol=pickle.HIGHEST_PROTOCOL)
with open('akseg_metadata.pickle', 'rb') as handle:
    akseg_metadata = pickle.load(handle)

akseg_metadata = pd.concat(akseg_metadata)




def get_nile_red_data(akseg_metadata):
    
    user_initials = akseg_metadata.user_initial.dropna().unique().tolist()
    
    nile_red_meta = []
    
    for user in user_initials:
        
        if user == "PT":
        
            meta = akseg_metadata[(akseg_metadata["user_initial"] == user) &
                                  (akseg_metadata["channel"].isin(["532","Nile Red","WGA-488","FM4-64"])) &
                                  (akseg_metadata["content"].isin(["E.Coli MG1655","E.Coli"])) & 
                                  (akseg_metadata["user_meta2"].isin(["short exposure",np.nan])) &
                                  (akseg_metadata["user_meta3"].isin(["focused",np.nan])) &
                                  (akseg_metadata["segmentation_curated"] == True)
                                  ]      
            
            nile_red_meta.append(meta)
            
        if user == "AZ":
            
            meta = akseg_metadata[(akseg_metadata["user_initial"] == user) &
                                    (akseg_metadata["channel"].isin(["532"])) &
                                    (akseg_metadata["content"].isin(['E.Coli MG1655','E.Coli Clinical'])) &
                                    (akseg_metadata["user_meta1"].isin(['2022 DL Paper'])) &
                                    (akseg_metadata["segmentation_curated"] == True)
                                  ]      
            
            nile_red_meta.append(meta)
            
        if user == "CF":
            
                meta = akseg_metadata[(akseg_metadata["user_initial"] == user) &
                                      (akseg_metadata["channel"].isin(["Nile Red"])) &
                                      (akseg_metadata["segmentation_curated"] == True)
                                      ]   
          
                nile_red_meta.append(meta)
    
    
    akseg_metadata = pd.concat(nile_red_meta)
    
    return akseg_metadata


xx = get_nile_red_data(akseg_metadata)





# xx = [pd.read_csv(path) for path in paths]


# akseg_metadata = [pd.read_csv(path, converters={'channel_list': lambda x: x.strip("[]").split(", "),
#                                                 'file_list': lambda x: x.strip("[]").split(", ")}, low_memory=False) for path in paths]


# akseg_metadata = akseg_metadata[
#     (akseg_metadata["user_initial"] == "PT") &
#     (akseg_metadata["segmented"] == True) &
#     (akseg_metadata["user_meta1"] == "TrillianSegDev")
#     # (akseg_metadata["channel"] == "Phase Contrast")
#     ]


# akseg_metadata["image_save_path"] = akseg_metadata["image_save_path"].apply(lambda path: update_akseg_paths(path, AKSEG_DIRECTORY))
# akseg_metadata["mask_save_path"] = akseg_metadata["mask_save_path"].apply(lambda path: update_akseg_paths(path, AKSEG_DIRECTORY))
# akseg_metadata["label_save_path"] = akseg_metadata["label_save_path"].apply(lambda path: update_akseg_paths(path, AKSEG_DIRECTORY))

# akseg_metadata["json_save_path"] = akseg_metadata.apply(lambda dat: generate_json_path(dat, AKSEG_DIRECTORY), axis=1)




# for group, data in akseg_metadata.groupby("segmentation_file"):
    
#     segmentation_channel = data.segmentation_channel.unique()[0]
    
#     mask_save_path = data.mask_save_path
    





# akseg_groups = akseg_metadata.groupby(["user_initial","microscope"])



# for _, data in akseg_groups:
    
#     pass
    
    
    
    
    
    
    
    
    
    