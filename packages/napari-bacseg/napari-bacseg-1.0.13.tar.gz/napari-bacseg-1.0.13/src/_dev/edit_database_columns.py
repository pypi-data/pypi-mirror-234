# -*- coding: utf-8 -*-
"""
Created on Wed Mar 22 11:43:58 2023

@author: turnerp
"""


import pandas as pd


path = r"C:\Users\turnerp\Desktop\database_test4\BacSeg_Database\Images\PT\PT_file_metadata.txt"
path = r"\\physics\dfs\DAQ\CondensedMatterGroups\AKGroup\Piers\AKSEG\Images\PT\PT_file_metadata.txt"


meta = pd.read_csv(path, sep= ",")

# cols = meta.columns.tolist()

# meta_index = cols.index("protocol") + 1


# meta["xxx"] = ""
# meta.drop(["xxx"], axis=1, inplace=True)

# # meta.drop(["user_meta4","user_meta5", "image_laplacian", "image_focus","image_blur"], axis=1, inplace=True)

# meta.to_csv(path, sep=",", index=False)