


import pandas as pd
from csv import Sniffer
import pathlib
import os

path = r"\\physics\dfs\DAQ\CondensedMatterGroups\AKGroup\Piers\AKSEG\Images\PT\PT_file_metadata.txt"
AKSEG_DIRECTORY = r"\\physics\dfs\DAQ\CondensedMatterGroups\AKGroup\Piers\AKSEG"

# sniffer = Sniffer()

# print(user_metadata_path)

# # checks the delimiter of the metadata file

# with open(user_metadata_path) as f:
#     line = next(f).strip()
#     delim = sniffer.sniff(line)

# df = pd.read_csv(user_metadata_path, sep=",")

# AKSEG_DIRECTORY = r"/home/turnerp/.cache/gvfs/smb-share:server=physics.ox.ac.uk,share=dfs/DAQ/CondensedMatterGroups/AKGroup/Piers/AKSEG"
# # # AKSEG_DIRECTORY = r"\\physics\dfs\DAQ\CondensedMatterGroups\AKGroup\Piers\AKSEG"
# #
# akseg_metadata = glob(AKSEG_DIRECTORY + "*/Images/PT/*.txt")



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





akseg_metadata = pd.read_csv(path, converters={'channel_list': lambda x: x.strip("[]").split(", "),
                                                'file_list': lambda x: x.strip("[]").split(", ")}, low_memory=False)


akseg_metadata = akseg_metadata[
    (akseg_metadata["user_initial"] == "PT") &
    (akseg_metadata["segmented"] == True) &
    (akseg_metadata["user_meta1"] == "TrillianSegDev")
    # (akseg_metadata["channel"] == "Phase Contrast")
    ]


akseg_metadata["image_save_path"] = akseg_metadata["image_save_path"].apply(lambda path: update_akseg_paths(path, AKSEG_DIRECTORY))
akseg_metadata["mask_save_path"] = akseg_metadata["mask_save_path"].apply(lambda path: update_akseg_paths(path, AKSEG_DIRECTORY))
akseg_metadata["label_save_path"] = akseg_metadata["label_save_path"].apply(lambda path: update_akseg_paths(path, AKSEG_DIRECTORY))

akseg_metadata["json_save_path"] = akseg_metadata.apply(lambda dat: generate_json_path(dat, AKSEG_DIRECTORY), axis=1)




# for group, data in akseg_metadata.groupby("segmentation_file"):
    
#     segmentation_channel = data.segmentation_channel.unique()[0]
    
#     mask_save_path = data.mask_save_path
    





# akseg_groups = akseg_metadata.groupby(["user_initial","microscope"])



# for _, data in akseg_groups:
    
#     pass
    
    
    
    
    
    
    
    
    
    