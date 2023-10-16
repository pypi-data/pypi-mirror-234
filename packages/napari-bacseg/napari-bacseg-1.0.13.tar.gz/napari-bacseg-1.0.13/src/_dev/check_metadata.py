# -*- coding: utf-8 -*-
"""
Created on Thu Nov 17 11:30:52 2022

@author: turnerp
"""

import pandas as pd
import datetime
import numpy as np



metadata_columns = ["date_uploaded",
                    "date_created",
                    "date_modified",
                    "file_name",
                    "channel",
                    "file_list",
                    "channel_list",
                    "segmentation_file",
                    "segmentation_channel",
                    "akseg_hash",
                    "user_initial",
                    "content",
                    "microscope",
                    "modality",
                    "source",
                    "stain",
                    "stain_target",
                    "antibiotic",
                    "treatment time (mins)",
                    "antibiotic concentration",
                    "mounting method",
                    "protocol",
                    "user_meta1",
                    "user_meta2",
                    "user_meta3",
                    "folder",
                    "parent_folder",
                    "segmented",
                    "labelled",
                    "segmentation_curated",
                    "label_curated",
                    "posX",
                    "posY",
                    "posZ",
                    "image_load_path",
                    "image_save_path",
                    "mask_load_path",
                    "mask_save_path",
                    "label_load_path",
                    "label_save_path"]

def check_metadata_format(metadata, expected_columns):

    if "stains" in metadata.columns:
        metadata = metadata.rename(columns={"stains": "stain"})

    missing_columns = list(set(expected_columns) - set(metadata.columns))
    extra_columns = list(set(metadata.columns) - set(expected_columns))
    
    all_columns = expected_columns + extra_columns
    
    metadata[missing_columns] = pd.DataFrame([[None] * len(missing_columns)], index=metadata.index)

    date = datetime.datetime.now()

    metadata['date_uploaded'] = None

    metadata.loc[metadata['date_uploaded'].isin(["None", None, np.nan, 0]),
                  ["date_uploaded", "date_created","date_modified"]] = str(date)
    
    metadata = metadata[all_columns]
    
    metadata = metadata.astype({'segmented': bool,'labelled': bool,
                                'segmentation_curated': bool,'label_curated': bool})
    
    return metadata


user_metadata_path = r"\\physics\dfs\DAQ\CondensedMatterGroups\AKGroup\Piers\AKSEG\Images\DEV\DEV_file_metadata.txt"
# user_metadata_path = r"\\physics\dfs\DAQ\CondensedMatterGroups\AKGroup\Piers\AKSEG\Images\DEV\DEV_file_metadata.txt"
akseg_metadata = pd.read_csv(user_metadata_path, sep = ",", low_memory=False)

akseg_metadata = check_metadata_format(akseg_metadata, metadata_columns)

# akseg_metadata["extra_data1"] = 42

# akseg_metadata = akseg_metadata[akseg_metadata["segmented"]==True]
# akseg_metadata = akseg_metadata[akseg_metadata["content"]=="E.Coli MG1655"]


# akseg_metadata = akseg_metadata.drop(["stain_target"],axis=1)

# # akseg_metadata = akseg_metadata.iloc[:,5:]

# akseg_metadata.to_csv(user_metadata_path, sep=",", index = False)



# meta1 = akseg_metadata.iloc[0:10].copy()
# meta2 = pd.DataFrame(akseg_metadata.iloc[15, 5:])


# meta1.loc[0] = meta1


# meta3 = pd.concat((meta1,meta2), ignore_index=True, axis=0)




# missing_columns = list(set(metadata_columns) - set(akseg_metadata.columns))

















# akseg_metadata = akseg_metadata[metadata_columns]

# akseg_metadata = check_metadata_format(akseg_metadata, metadata_columns)


# xx = akseg_metadata[akseg_metadata["segmented"]is"False"]

# akseg_metadata = akseg_metadata.sort_values(["date_modified"]).reset_index(drop=True)
# akseg_metadata = akseg_metadata.sample(frac=1).reset_index(drop=True)



# if "stains" in akseg_metadata.columns:
#     akseg_metadata = akseg_metadata.rename(columns={"stains": "stain"})


# xx = akseg_metadata.columns

# imported_columns = akseg_metadata.columns

# expected_columns = ["date_uploaded",
#                    "date_created",
#                    "date_modified",
#                    "file_name",
#                    "channel",
#                    "file_list",
#                    "channel_list",
#                    "segmentation_file",
#                    "segmentation_channel",
#                    "akseg_hash",
#                    "user_initial",
#                    "content",
#                    "microscope",
#                    "modality",
#                    "source",
#                    "stain",
#                    "antibiotic",
#                    "treatment time (mins)",
#                    "antibiotic concentration",
#                    "mounting method",
#                    "protocol",
#                    "user_meta1",
#                    "user_meta2",
#                    "user_meta3",
#                    "folder",
#                    "parent_folder",
#                    "segmented",
#                    "labelled",
#                    "segmentation_curated",
#                    "label_curated",
#                    "posX",
#                    "posY",
#                    "posZ",
#                    "image_load_path",
#                    "image_save_path",
#                    "mask_load_path",
#                    "mask_save_path",
#                    "label_load_path",
#                    "label_save_path",
#                    "new_column1",
#                    "new_column2"]


# def check_metadata_format(akseg_metadata,akseg_columns):

#     missing_columns = list(set(expected_columns) - set(imported_columns))
    
#     akseg_metadata[missing_columns] = pd.DataFrame([[None] * len(missing_columns)], index=akseg_metadata.index)
    
#     date = datetime.datetime.now()
    
#     akseg_metadata['date_uploaded'] = None
    
#     akseg_metadata.loc[akseg_metadata['date_uploaded'].isin(["None",None,np.nan,0]), ["date_uploaded","date_created","date_modified"]] = str(date)
    
#     return akseg_metadata


# akseg_metadata = check_metadata_format(akseg_metadata,expected_columns)


# xx = akseg_metadata.iloc[[0]].iloc[0].tolist()

