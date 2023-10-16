# -*- coding: utf-8 -*-
"""
Created on Wed Mar 22 14:35:20 2023

@author: turnerp
"""


import pandas as pd
import pathlib
import numpy as np


path = r"\\physics\dfs\DAQ\CondensedMatterGroups\AKGroup\Piers\AKSEG\Images\CF\CF_file_metadata.txt"


meta = pd.read_csv(path, sep= ",", dtype=object)


meta.loc[meta["user_meta3"] == "BioRepet1", "user_meta3"] = "BioRepeat1"

meta.loc[meta["user_meta3"].isin(["BioRepeat1","BioRepeat2"]), "user_meta6"] = "L48480"
meta.loc[meta["user_meta3"].isin(["BioRepeat3","BioRepeat4"]), "user_meta6"] = "L11037"

meta.loc[meta["user_meta4"] == "TechRepeat1", "user_meta5"] = "TechRepeat1"
meta.loc[meta["user_meta4"] == "TechRepeat2", "user_meta5"] = "TechRepeat2"
meta.loc[meta["user_meta3"] == "BioRepeat1", "user_meta4"] = "BioRepeat1"
meta.loc[meta["user_meta3"] == "BioRepeat2", "user_meta4"] = "BioRepeat2"
meta.loc[meta["user_meta3"] == "BioRepeat3", "user_meta4"] = "BioRepeat1"
meta.loc[meta["user_meta3"] == "BioRepeat4", "user_meta4"] = "BioRepeat2"
meta.loc[meta["user_meta6"] == "L48480", "user_meta3"] = "L48480"
meta.loc[meta["user_meta6"] == "L11037", "user_meta3"] = "L11037"
meta.loc[meta["user_meta6"] == "L48480", "user_meta6"] = ""
meta.loc[meta["user_meta6"] == "L11037", "user_meta6"] = ""


# xx = meta[["file_name", "user_meta1","user_meta2","user_meta3","user_meta4","user_meta5"]]
# xx = xx[xx["user_meta1"] =]


for column in meta.columns:
    if "user_meta" in column:
        column_values = meta[column].unique().tolist()
        
        column_values = [value for value in column_values if value not in [None, np.nan, "", " "]]
        
        print(column,column_values)
        


# meta = meta[(meta["user_meta1"] == "Direct From Plate GASKET") &
#             (meta["user_meta2"] == "plate1")]                     
                        

# meta = meta[["file_name", "user_meta1","user_meta2","user_meta3","user_meta4","user_meta5"]]  


# meta = meta.sort_values(["user_meta2"])        
        

# meta.to_csv(path, sep=",", index=False)





# meta = meta[(meta["user_meta1"] == "Direct From Plate GASKET") &
#             (meta["user_meta2"] == "plate1") &
#             (meta["user_meta3"] == "BioRepet1")]



# user_meta = {column: meta[column].unique().tolist() for column in meta.columns if "meta" in column}



# user_initial = "PT"
# database_name = "AKSEG"
# database_directory = "\\physics\dfs\DAQ\CondensedMatterGroups\AKGroup\Piers\AKSEG"


# txt_meta_path = r"\\physics\dfs\DAQ\CondensedMatterGroups\AKGroup\Piers\AKSEG\Metadata\AKSEG User Metadata [PT].txt"

# print(txt_meta_path)

# txt_meta = f"# {database_name} User Metadata: {user_initial}\n"

# for key, value in user_meta.items():
    
#     txt_meta += f"\n# User Meta [{key.replace('user_meta', '')}] (add new entries below):"

#     for item in value:
#         txt_meta += f"\n{item}"

#     txt_meta += "\n"


#     with open(txt_meta_path, "w") as f:
#         f.write(txt_meta)
