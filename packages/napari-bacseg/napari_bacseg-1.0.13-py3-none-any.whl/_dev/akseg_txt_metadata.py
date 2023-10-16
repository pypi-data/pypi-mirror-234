import pandas as pd
import numpy as np
from glob2 import glob
import pickle
import os
import tifffile
import cv2

from shapely.geometry import LineString, LinearRing, Point
from shapely.geometry import Polygon
from shapely.geometry.polygon import orient
from shapely.ops import nearest_points
import matplotlib.path as mpltPath
from scipy.spatial.distance import cdist
from scipy.spatial import Voronoi
import warnings
import math
import matplotlib.pyplot as plt
from shapely.ops import nearest_points
from shapely.ops import linemerge, unary_union, polygonize
from shapely.geometry import LineString, Polygon
from shapely.geometry import mapping
from shapely.ops import split
import traceback
import scipy
import pathlib



def generate_txt_metadata(database_directory):
    
    database_name = pathlib.Path(database_directory).parts[-1].replace("_Database","")
    
    path = pathlib.PurePath(database_directory,"Metadata",f"{database_name} Metadata.xlsx")

    akmeta = pd.read_excel(path, usecols="B:M", header=2)
    
    akmeta = dict(user_initial=akmeta["User Initial"].dropna().astype(str).tolist(),
                  content=akmeta["Image Content"].dropna().astype(str).tolist(),
                  microscope=akmeta["Microscope"].dropna().astype(str).tolist(),
                  modality=akmeta["Modality"].dropna().astype(str).tolist(),
                  source=akmeta["Light Source"].dropna().astype(str).tolist(),
                  antibiotic=akmeta["Antibiotic"].dropna().astype(str).tolist(),
                  abxconcentration=akmeta["Antibiotic Concentration"].dropna().astype(str).tolist(),
                  treatment_time=akmeta["Treatment Time (mins)"].dropna().astype(str).tolist(),
                  stain=akmeta["Stains"].dropna().astype(str).tolist(),
                  stain_target=akmeta["Stain Target"].dropna().astype(str).tolist(),
                  mount=akmeta["Mounting Method"].dropna().astype(str).tolist(),
                  protocol=akmeta["Protocol"].dropna().astype(str).tolist())
    
    #generate file metadata
    
    for key, value in akmeta.items():
        
        txt_meta = f"# {database_name} Image Metadata: {key} (Add new entries below):"
        
        txt_meta_path = pathlib.PurePath(database_directory,"Metadata", f"{database_name} Image Metadata [{key}].txt")
        
        for item in value:
            
            txt_meta += f"\n{item.lstrip().rstrip()}"
        
        with open(txt_meta_path, "w") as f:
            f.write(txt_meta)
        
    #generate user metadata
    
    user_metadata = pd.read_excel(path, sheet_name="User Metadata", usecols="B:E", header=2)
    users = user_metadata[user_metadata["User Initial"]!="example"]["User Initial"].unique().tolist()
        
    for user in users:
        
        txt_meta = f"# {database_name} User Metadata: {user}\n"
        
        txt_meta_path = pathlib.PurePath(database_directory,"Metadata", f"{database_name} User Metadata [{user}].txt")
        
        for i in range(1,4):
            
            txt_meta += f"\n# User Meta [{i}] (add new entries below):"
            
            item_list = user_metadata[(user_metadata["User Initial"]==user)][f"User Meta #{i}"].dropna().tolist()
            
            if len(item_list)==0:
                txt_meta += "\n"
            else:
                for item in item_list:
                    if item not in ["", " ", None]:
                        txt_meta += f"\n{item.lstrip().rstrip()}"
            txt_meta += "\n"
                    
        with open(txt_meta_path, "w") as f:
            f.write(txt_meta)
    
  
def read_txt_metadata(database_directory):

    database_name = pathlib.Path(database_directory).parts[-1].replace("_Database","")

    metadata_directory = str(pathlib.PurePath(database_directory,"Metadata"))
    
    metadata_files = glob(metadata_directory + "\*.txt")
        
    if len(metadata_files)==0:

        generate_txt_metadata(database_directory)
        metadata_files = glob(metadata_directory + "\*.txt")
        
    image_metadata_files = [path for path in metadata_files if f"{database_name} Database Metadata" in path]
    user_metadata_fies =   [path for path in metadata_files if f"{database_name} User Metadata" in path]  
      
    image_metadata = {}
    
    for file in image_metadata_files:
        
        key = strip_brackets(file)
        
        with open(file,"r") as f:
            lines = f.readlines()
            
            lines = [line for line in lines if line[0]!="#"]
            
        image_metadata[key] = lines      
      
    user_metadata = {}
    
    for file in user_metadata_fies:
        
        user = strip_brackets(file)
    
        with open(file,"r") as f:
            lines = f.readlines()
             
        metakey = None
        
        user_dict = {"User Initial":user}
    
        for i,line in enumerate(lines):
            
            line = line.lstrip().rstrip()
            
            if "User Meta" in line and i!=0:
                
                metakey = f"User Meta #{strip_brackets(line)}"
                
                if metakey not in user_dict.keys():
                    
                    user_dict[metakey] = []
                
            else:
                
                if metakey!=None and line.strip() not in ["",","," ", None]:
                    
                    user_dict[metakey].append(line)
                    
        user_metadata[user] = user_dict
        
    return image_metadata, user_metadata
        

def strip_brackets(string):
    
    value = string[string.find("[")+1:string.find("]")]
    
    return value

def create_database(path, database_name = "BacSeg"):

    if os.path.isdir(path):
    
        path = os.path.abspath(path)
        database_directory =  str(pathlib.PurePath(path,f"{database_name}_Database"))
        
        if os.path.exists(database_directory)==True:
            
            print(f"{database_name} Database already exists at location {database_directory}")
            
        else:
            
            print(f"Creating {database_name} Database at location {database_directory}")
    
            if os.path.isdir(database_directory)==False:
                os.mkdir(database_directory)
        
            folders = ["Images", "Metadata", "Models"]
            
            folder_paths = [str(pathlib.PurePath(database_directory,folder)) for folder in folders]
        
            for folder_path in folder_paths:
                if os.path.exists(folder_path)==False:
                    os.mkdir(folder_path)
                
            image_metadata_list = ['abxconcentration',
                                   'antibiotic',
                                   'content',
                                   'microscope',
                                   'modality',
                                   'mount',
                                   'protocol',
                                   'source',
                                   'stain',
                                   'treatment_time',
                                   'user_initial']
            
            user_metadata_list = ["example_user"]
            
            for meta_item in image_metadata_list:
                
                txt_meta = f"# {database_name} Image Metadata: {meta_item} (Add new entries below):"
                
                txt_meta_path = pathlib.PurePath(database_directory,"Metadata", f"{database_name} Image Metadata [{meta_item}].txt")
            
                with open(txt_meta_path, "w") as f:
                    f.write(txt_meta)
            
            for user in user_metadata_list:
                
                 txt_meta = f"# {database_name} User Metadata: {user}\n"
                 txt_meta +="# Replace 'example_user' with your intial\n"
                 
                 txt_meta_path = pathlib.PurePath(database_directory,"Metadata", f"{database_name} User Metadata [{user}].txt")
                 
                 for i in range(1,4):
                   
                    txt_meta += f"\n# User Meta [{i}] (add new entries below):"
                    txt_meta += "\nexample_item1"
                    txt_meta += "\nexample_item2"
                    txt_meta += "\nexample_item3"
                    txt_meta += "\n"
                    
                 with open(txt_meta_path, "w") as f:
                     f.write(txt_meta)
                     
    return database_directory




database_directory = r"\\physics\dfs\DAQ\CondensedMatterGroups\AKGroup\Piers\AKSEG"

# path = r"C:\Users\turnerp\Desktop\DatabaseTest"

# database_directory = create_database(path, database_name = "DevDev")

# database_directory = r"C:\Users\turnerp\Desktop\DatabaseTest\DevDev_Database"

image_metadata, user_metadata = read_txt_metadata(database_directory)
            


# active_database_folders = [folder.split("\\")[-1] for folder in glob(database_directory + "*/*")]

           
# active_database_folders = [os.path.basename(path) for path in glob(database_directory + "/*", recursive = True)]   
    


# print(image_metadata.keys())
    
# control_dict = {'abxconcentration':'upload_abxconcentration',
#                 'antibiotic':'upload_antibiotic',
#                 'content':'upload_content',
#                 'microscope':'upload_microscope',
#                 'modality':'label_modality',
#                 'mount':'upload_mount',
#                 'protocol':'upload_protocol',
#                 'source':'label_light_source',
#                 'stain':'label_stain',
#                 'stain_target':'label_stain_target',
#                 'treatment_time':'upload_treatmenttime',
#                 'user_initial':'upload_initial'}    
    

    
    
    
    
    
    
    