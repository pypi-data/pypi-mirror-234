# -*- coding: utf-8 -*-
"""
Created on Mon Nov 14 14:44:09 2022

@author: turnerp
"""

import pandas as pd
import tifffile
import numpy as np


species_dict = {'BSB': {'species_name': 'streptococcus agalactiae', 'gram': 'positive', 'shape':'cocci', 'formations':['chain']},
                'ECOLI': {'species_name': 'escherichia coli', 'gram': 'negative', 'shape':'rod', 'formations':[]},
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
                'STCA': {'species_name': 'staphylococcus capitis', 'gram': 'positive', 'shape':'cocci', 'formations':['cluster']}}




species_info = []

for key,value in species_dict.items():
    
    species_info.append({"species_name":value["species_name"].capitalize(),
                         "gram":value["gram"],
                         "shape":value["shape"]})


species_info = pd.DataFrame(species_info)

species_info = species_info.sort_values(["gram","shape"])

path = r"\\CMWT188.nat.physics.ox.ac.uk\C\Users\turnerp\PycharmProjects\AMR_GramStain\A1--W00001--P00005--Z00000--T00000--WGA-488_tile3_AKSEG.tif"

mask = tifffile.imread(path)

print(np.unique(mask))