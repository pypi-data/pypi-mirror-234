# -*- coding: utf-8 -*-
"""
Created on Tue Feb 14 15:25:53 2023

@author: turnerp
"""

import pandas as pd
import pickle



with open('metadev.pickle', 'rb') as handle:
    file_metadata = pickle.load(handle)



file_metadata = pd.DataFrame.from_dict(file_metadata, dtype=object)

columns = file_metadata.columns.tolist()
column_dict = {col:"first" for col in columns if col not in ["file_list","channel_list"]}

df = (file_metadata.groupby(['file_name']).agg({**{'file_list': lambda x: x.tolist(),
                                                   "channel_list": lambda x: x.tolist()}, **column_dict})).reset_index(drop=True)

file_metadata = df[columns]

