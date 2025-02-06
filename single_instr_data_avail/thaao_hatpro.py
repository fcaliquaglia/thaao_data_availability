#!/usr/local/bin/python3
# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------------
"""
OK
"""

# =============================================================
# CREATED:
# AFFILIATION: INGV
# AUTHORS: Filippo Cali' Quaglia
# =============================================================
#
# -------------------------------------------------------------------------------
__author__ = "Filippo Cali' Quaglia"
__credits__ = ["??????"]
__license__ = "GPL"
__version__ = "0.1"
__email__ = "filippo.caliquaglia@ingv.it"
__status__ = "Research"
__lastupdate__ = "October 2024"

import os

import pandas as pd

import settings as ts
import tools as tls

instr = 'hatpro'
base_folder = ts.basefolder  # Base folder for efficiency

# Build the file path upfront to avoid repeated path joining
file_path = os.path.join(base_folder, "thaao_hatpro", 'LWP_15_min_all', 'LWP_15_min_all.dat')

if __name__ == "__main__":
    # Read the data with more specific optimizations for file reading
    data_avail_hat = pd.read_csv(
            file_path, skiprows=9, header=0, sep='\s+',  # Using space as delimiter
            parse_dates={'datetime': [0, 1]}, date_parser=lambda x: pd.to_datetime(x, format='%Y-%m-%d %H:%M:%S'),
            index_col='datetime', low_memory=False  # For better performance with large files
    )

    # Saving the specific 'LWP_g/m2' column with the 'save_mask_txt' method
    tls.save_mask_txt(data_avail_hat['LWP_g/m2'], os.path.join(base_folder, "thaao_" + instr), instr)
