
import pandas as pd
import numpy as np





def metadata(path):

    metadata_columns = ["date_uploaded", "date_created", "date_modified", "file_name", "channel", "file_list", "channel_list", "segmentation_file", "segmentation_channel", "akseg_hash",
        "user_initial", "content", "microscope", "modality", "source", "strain", "phenotype", "stain", "stain_target", "antibiotic", "treatment time (mins)", "antibiotic concentration",
        "mounting method", "protocol", "folder", "parent_folder", "num_segmentations", "image_laplacian", "image_focus", "image_debris", "segmented", "labelled", "segmentation_curated",
        "label_curated", "posX", "posY", "posZ", "image_load_path", "image_save_path", "mask_load_path", "mask_save_path", "label_load_path", "label_save_path", ]
    
    user_key_list = np.arange(1, 6 + 1).tolist()
    user_key_list.reverse()
    
    for key in user_key_list:
        user_key = f"user_meta{key}"
        metadata_columns.insert(22, str(user_key))

    user_metadata = pd.read_csv(path, sep=",")

    return user_metadata
    
    
    
path = r"\\physics\dfs\DAQ\CondensedMatterGroups\AKGroup\Piers\AKSEG\Images\AF\AF_file_metadata.txt"


user_initial = "AF"
upload_segmentation_combo = 0
upload_label_combo = 0
download_sort_order_1 = 1
download_sort_order_2 = 0
download_sort_direction_1 = 0
download_sort_direction_2 = 0
import_limit = 10

database_metadata = {"user_initial": "AF", "content": "", 
                     "microscope": "", "phenotype": "",
                     "strain": "", "antibiotic": "", 
                     "antibiotic concentration": "", 
                     "treatment time (mins)": "", "mounting method": "", 
                     "protocol": "", }


database_metadata = {key: val for key, val in database_metadata.items() if val not in ["", "Required for upload", "example_item1", "example_item2", "example_item3", ]}

user_metadata = metadata(path)

print(user_metadata.user_meta1.unique())


# user_metadata["segmentation_channel"] = user_metadata["segmentation_channel"].astype(str)
# user_metadata["treatment time (mins)"] = user_metadata["treatment time (mins)"].astype(str)

# for key, value in database_metadata.items():
#     if key in user_metadata.columns:
#         user_metadata = user_metadata[user_metadata[key] == value]

# if upload_segmentation_combo == 1:
#     user_metadata = user_metadata[user_metadata["segmented"] == False]
# if upload_segmentation_combo == 2:
#     user_metadata = user_metadata[user_metadata["segmented"] == True & (user_metadata["segmentation_curated"] == False)]
# if upload_segmentation_combo == 3:
#     user_metadata = user_metadata[(user_metadata["segmented"] == True) & (user_metadata["segmentation_curated"] == True)]
# if upload_label_combo == 1:
#     user_metadata = user_metadata[user_metadata["labelled"] == False]
# if upload_label_combo == 2:
#     user_metadata = user_metadata[user_metadata["labelled"] == True & (user_metadata["label_curated"] == False)]
# if upload_label_combo == 3:
#     user_metadata = user_metadata[(user_metadata["labelled"] == True) & (user_metadata["label_curated"] == True)]

# user_metadata.sort_values(by=["posX", "posY", "posZ"], ascending=True)

# sort_names = []
# sort_directions = []

# if download_sort_order_1 > 1:
#     if download_sort_direction_1 == 1:
#         sort_directions.append(True)
#     if download_sort_direction_1 == 2:
#         sort_directions.append(False)

# if download_sort_order_2 > 1:
#     if download_sort_direction_2 == 1:
#         sort_directions.append(True)
#     if download_sort_direction_2 == 2:
#         sort_directions.append(False)

# if download_sort_order_1 == 1:
#     user_metadata = user_metadata.sample(frac=1).reset_index(drop=True)
# if download_sort_order_1 == 2:
#     sort_names.append("date_uploaded")
# if download_sort_order_1 == 3:
#     sort_names.append("date_modified")
# if download_sort_order_1 == 4:
#     if "image_laplacian" in user_metadata.columns:
#         sort_names.append("image_laplacian")
# if download_sort_order_1 == 5:
#     if "num_segmentations" in user_metadata.columns:
#         sort_names.append("num_segmentations")
# if download_sort_order_1 == 6:
#     if "image_focus" in user_metadata.columns:
#         sort_names.append("image_focus")
# if download_sort_order_1 == 7:
#     if "image_debris" in user_metadata.columns:
#         sort_names.append("image_debris")

# if download_sort_order_2 == 1:
#     user_metadata = user_metadata.sample(frac=1).reset_index(drop=True)
# if download_sort_order_2 == 2:
#     sort_names.append("date_uploaded")
# if download_sort_order_2 == 3:
#     sort_names.append("date_modified")
# if download_sort_order_2 == 4:
#     if "image_laplacian" in user_metadata.columns:
#         sort_names.append("image_laplacian")
# if download_sort_order_2 == 5:
#     if "num_segmentations" in user_metadata.columns:
#         sort_names.append("num_segmentations")
# if download_sort_order_2 == 6:
#     if "image_focus" in user_metadata.columns:
#         sort_names.append("image_focus")
# if download_sort_order_2 == 7:
#     if "image_debris" in user_metadata.columns:
#         sort_names.append("image_debris")

# if len(sort_names) > 0:
#     if len(sort_names) != len(sort_directions):
#         sort_directions = [False] * len(sort_names)
#     user_metadata = user_metadata.sort_values(sort_names, ascending=sort_directions).reset_index(drop=True)

# sort_columns = []

# user_metadata = user_metadata.drop_duplicates()

# if "folder" in user_metadata.columns:
#     sort_columns.append("folder")
#     user_metadata.loc[user_metadata["folder"].isna(), "folder"] = "None"
# if "segmentation_file" in user_metadata.columns:
#     sort_columns.append("segmentation_file")
#     user_metadata.loc[user_metadata["segmentation_file"].isna(), "segmentation_file",] = "None"
# if "posX" in user_metadata.columns:
#     sort_columns.append("posX")
#     user_metadata['posX'] = user_metadata['posX'].fillna(0, inplace=True)
#     user_metadata.loc[user_metadata["posX"].isna(), "posX"] = 0
# if "posY" in user_metadata.columns:
#     sort_columns.append("posY")
#     user_metadata['posY'] = user_metadata['posY'].fillna(0, inplace=True)
#     user_metadata.loc[user_metadata["posY"].isna(), "posY"] = 0
# if "posZ" in user_metadata.columns:
#     sort_columns.append("posZ")
#     user_metadata['posZ'] = user_metadata['posZ'].fillna(0, inplace=True)
#     user_metadata.loc[user_metadata["posZ"].isna(), "posZ"] = 0


# segmentation_files = user_metadata["segmentation_file"].unique()
# num_measurements = len(segmentation_files)

# if import_limit == "All":
#     import_limit = num_measurements
# else:
#     if int(import_limit) > num_measurements:
#         import_limit = num_measurements

# segmentation_file_filter = segmentation_files[: int(import_limit)]

# user_metadata = user_metadata[user_metadata["segmentation_file"].isin(segmentation_files[: int(import_limit)])]



# measurements = user_metadata.groupby(sort_columns)

# for group,measurement in measurements:
    
#     segmentation_channel = measurement["segmentation_channel"].unique()[0]
    
#     segmentation_file_data = measurement[measurement["channel"] == segmentation_channel]
    
#     segmentation_file = segmentation_file_data["file_name"].unique().tolist()
#     user_initial = segmentation_file_data["user_initial"].unique().tolist()
#     folder = segmentation_file_data["folder"]
    
#     print(segmentation_file)
    





# show_info(f"Found {len(file_paths) // len(channels)} matching database files.")