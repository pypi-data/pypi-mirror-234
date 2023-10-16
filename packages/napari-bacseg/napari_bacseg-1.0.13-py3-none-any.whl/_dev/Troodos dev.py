# -*- coding: utf-8 -*-
"""
Created on Thu May 26 12:27:28 2022

@author: turnerp
"""

from astropy.io import fits
from glob2 import glob
import os


directory = r"\\CMDAQ4.physics.ox.ac.uk\AKGroup\Piers\First rough test of Troodos nucleoid imaging"


paths = glob(directory + "\*.fits")

file_names = [os.path.basename(path) for path in paths]

with fits.open(paths[0]) as hdul:
    print(hdul.info())
    header = dict(hdul[0].header)
    data = hdul[0].data