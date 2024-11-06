#!/usr/local/bin/python3
# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------------
#
"""
Brief description
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

import datetime as dt
import os

import pandas as pd

import thaao_settings as ts

instr = 'hatpro'
folder = os.path.join(ts.basefolder, "thaao_" + instr)

if __name__ == "__main__":
    dateparse = lambda x: dt.datetime.strptime(x, '%Y-%m-%d %H:%M:%S')
    data_avail_hat = pd.read_table(
            os.path.join(ts.basefolder, "thaao_hatpro", 'IWV_20170101_20220919.txt'), skiprows=10, header=None,
            sep='\s+', parse_dates={'datetime': [0, 1]}, date_parser=dateparse, index_col='datetime')
    data_avail_hat.columns = ['IWV[kg/m2]', 'STD_IWV[kg/m2]', 'Num']

    ts.save_mask_txt(data_avail_hat['IWV[kg/m2]'], instr)
