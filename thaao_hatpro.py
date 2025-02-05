#!/usr/local/bin/python3
# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------------
#
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
folder = os.path.join(ts.basefolder, "thaao_" + instr)

if __name__ == "__main__":

    data_avail_hat = pd.read_table(
            os.path.join(ts.basefolder, "thaao_hatpro", 'LWP_15_min_all', 'LWP_15_min_all.dat'), skiprows=9, header=0,
            sep='\s+', parse_dates={'datetime': [0, 1]}, date_format='%Y-%m-%d %H:%M:%S', index_col='datetime')

    tls.save_mask_txt(data_avail_hat['LWP_g/m2'], folder, instr)
