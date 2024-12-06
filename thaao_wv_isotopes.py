#!/usr/local/bin/python3
# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------------
#
"""
# TODO:
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
import tools as tls
import settings as ts
import datetime as dt

instr = 'wv_isotopes'
date_list = pd.date_range(
        ts.instr_metadata[instr]['start_instr'], ts.instr_metadata[instr]['end_instr'], freq='H').tolist()
folder = os.path.join(ts.basefolder, "thaao_" + instr)

if __name__ == "__main__":
    wv_isotopes = pd.DataFrame(columns=['dt', 'mask'])
    wv_isotopes_missing = pd.DataFrame(columns=['dt', 'mask'])
    fn = os.path.join(folder, 'wv_isotopes.txt')
    wv_isotopes_dt = pd.read_table(fn)
    wv_isotopes_dt.index = pd.to_datetime(wv_isotopes_dt.values.flatten(), format='%m-%d-%y %H:%M') # .round('h')

    for i in date_list:
        if i in wv_isotopes_dt.index:
            wv_isotopes.loc[i] = [i, True]
        else:
            wv_isotopes_missing.loc[i] = [i, True]

    tls.save_txt(instr, wv_isotopes)
    tls.save_txt(instr, wv_isotopes_missing, missing=True)

