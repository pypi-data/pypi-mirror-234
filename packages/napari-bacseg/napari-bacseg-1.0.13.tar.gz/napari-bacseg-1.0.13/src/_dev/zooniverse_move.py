# # -*- coding: utf-8 -*-
# """
# Created on Fri Jan 27 16:41:44 2023
#
# @author: turnerp
# """
#
#
# import json
# import pandas as pd
# import numpy as np
# import tifffile
# import matplotlib.pyplot as plt
# import cv2
# import scipy
# from skimage.registration import phase_cross_correlation
# from skimage.registration._phase_cross_correlation import _upsampled_dft
# from skimage import exposure
# from skimage import data
# # from imgaug import augmenters as iaa
# import os
# import tqdm
# from multiprocessing import Pool
# from glob2 import glob
# import pickle
#
# # new_zooniverse_path = r"C:\Users\turnerp\Documents\ZooniverseTest_treated"
# # old_zooniverse_path = r"C:\Users\turnerp\Documents\ZooniverseTest"
#
# # old_zooniverse_files = glob(old_zooniverse_path + "*/**/*.tif")
# # new_zooniverse_files = glob(new_zooniverse_path + "*/**/*.tif")
#
# # with open('zooniverse_files.pkl', 'wb') as f:  # Python 3: open(..., 'wb')
# #     pickle.dump([old_zooniverse_files, new_zooniverse_files],f)
#
# with open('zooniverse_files.pkl','rb') as f:  # Python 3: open(..., 'rb')
#     old_zooniverse_files, new_zooniverse_files = pickle.load(f)
#
#
# def generate_file_name(row):
#
#     index = row.name
#
#     path = row.read_path
#
#     file_name = os.path.basename(path)
#
#     file_name = f"ID{index}.tif"
#
#     return file_name
#
# def generate_export_path(row, export_directory):
#
#     file_name = row["zooniverse_file_name"]
#
#     export_path = os.path.join(export_directory,file_name)
#
#     return export_path
#
# def export_zooniverse_file(data):
#
#     try:
#
#         import_path = data["read_path"]
#         export_path = data["export_path"]
#
#         img = tifffile.imread(import_path)
#         tifffile.imwrite(export_path, img)
#
#     except Exception:
#         pass
#
#
# def process_df(df, export_directory):
#
#     df = df.copy().sample(frac=1, random_state=42).reset_index(drop=True)
#
#     df["file_name"] = df["read_path"].str.split("\\").str[-1]
#
#     # df["raw_file_name"] = df["file_name"].str.split("_cell").str[0] + ".tif"
#
#     df["label"] = df["read_path"].str.split("\\").str[-2]
#     df["strain"]  = df["read_path"].str.split("\\").str[-1].str.split("_").str[2]
#     df["zooniverse_file_name"] = df.apply(lambda row: generate_file_name(row), axis=1)
#     df["export_path"] = df.apply(lambda row: generate_export_path(row,export_directory), axis=1)
#
#     return df
#
#
#
#
# old_df_path = r"\\physics\dfs\DAQ\CondensedMatterGroups\AKGroup\Piers\Zooniverse\dataset2022\zooniverse_file_names.txt"
# old_file_names = pd.read_csv(old_df_path).iloc[:5000].file_name.tolist()
#
#
#
# # old_file_paths = glob(r"\\physics\dfs\DAQ\CondensedMatterGroups\AKGroup\Piers\Zooniverse\dataset2022" + "*/**/*.tif")
#
#
#
#
# export_directory = r"\\physics\dfs\DAQ\CondensedMatterGroups\AKGroup\Piers\Zooniverse\dataset2023_treated"
#
#
# old_df = pd.DataFrame(old_zooniverse_files, columns=["read_path"])
# new_df = pd.DataFrame(new_zooniverse_files, columns=["read_path"])
#
# old_df = process_df(old_df, export_directory)
# new_df = process_df(new_df, export_directory)
#
# old_df_sorted = []
#
# for file_name in old_file_names:
#
#     old_df_sorted.append(old_df[old_df["file_name"]isfile_name].iloc[-1])
#
# old_df = pd.DataFrame(old_df_sorted).reset_index(drop=True)
#
#
# new_df = new_df[~new_df["file_name"].isin(old_file_names)]
# df = pd.concat([old_df,new_df]).reset_index(drop=True)
# df["zooniverse_file_name"] = df.apply(lambda row: generate_file_name(row), axis=1)
# df["export_path"] = df.apply(lambda row: generate_export_path(row,export_directory), axis=1)
#
# df.drop_duplicates(["file_name"], inplace=True)
#
# # old_df = old_df.iloc[:5000]
# # old_file_names = old_df.file_name.tolist()
#
# # old_import_path = old_df.read_path[0]
# # old_export_path = old_df.export_path[0]
#
# # plt.imshow(tifffile.imread(old_import_path))
#
#
# # new_df = new_df[~new_df["file_name"].isin(old_file_names)]
#
#
# # df = pd.concat([old_df,new_df]).reset_index(drop=True)
# # df["zooniverse_file_name"] = df.apply(lambda row: generate_file_name(row), axis=1)
# # df["export_path"] = df.apply(lambda row: generate_export_path(row,export_directory), axis=1)
#
#
#
#
#
# # df = pd.DataFrame(zooniverse_files, columns=["read_path"])
#
# # df = df.copy().sample(frac=1, random_state=42).reset_index(drop=True)
#
# # df["file_name"] = df["read_path"].str.split("\\").str[-1]
#
# # df["raw_file_name"] = df["file_name"].str.split("_cell").str[0] + ".tif"
#
# # df = df[~df["file_name"].str.split("_cell")[0].isin(old_file_names)]
#
# # df["label"] = df["read_path"].str.split("\\").str[-2]
# # df["strain"]  = df["read_path"].str.split("\\").str[-1].str.split("_").str[2]
# # df["zooniverse_file_name"] = df.apply(lambda row: generate_file_name(row), axis=1)
# # df["export_path"] = df.apply(lambda row: generate_export_path(row,export_directory), axis=1)
#
# # df = pd.concat([old_df,df])
#
#
#
#
#
# df.iloc[:,1:-1].to_csv(os.path.join(export_directory,"zooniverse_file_names.txt"), sep=",", index=False)
#
#
# files = [df.iloc[i] for i in range(len(df))]
#
# if __name__=='__main__':
#
#     with Pool() as p:
#
#         d = list(tqdm.tqdm(p.imap(export_zooniverse_file,files), total=len(files)))
#         p.close()
#         p.join()
#
#         # new_metadata = pd.concat(d)
#
#
# # export_zooniverse_file(files[0])
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#