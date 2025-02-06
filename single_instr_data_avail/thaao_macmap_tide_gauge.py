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

instr = 'macmap_tide_gauge'
date_list = pd.date_range(
        ts.instr_metadata[instr]['start_instr'], ts.instr_metadata[instr]['end_instr'], freq='D').tolist()
folder = os.path.join(ts.basefolder, "thaao_" + instr)

if __name__ == "__main__":

    macmap_tide_gauge = pd.DataFrame(columns=['dt', 'mask'])
    macmap_tide_gauge_missing = pd.DataFrame(columns=['dt', 'mask'])
    for i in date_list:
        fn = os.path.join(folder, i.strftime('%Y'), "Thule_1_2_" + i.strftime('%y%m%d') + "_corr.dat")
        if os.path.exists(fn):
            macmap_tide_gauge.loc[i] = [i, True]
        else:
            macmap_tide_gauge_missing.loc[i] = [i, True]
            print('file ' + str(fn) + ' not found')

    tls.save_txt(instr, macmap_tide_gauge)
    tls.save_txt(instr, macmap_tide_gauge_missing, missing=True)
