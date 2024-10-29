#!/usr/local/bin/python3
# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------------
"""
Brief description
"""
# -------------------------------------------------------------------------------
__author__ = "Filippo Cali' Quaglia"
__affiliation__ = "UNIVE, INGV"
__credits__ = ["??????"]
__license__ = "GPL"
__version__ = "0.1"
__email__ = "filippo.caliquaglia@ingv.it"
__status__ = "Research"
__lastupdate__ = "October 2024"

import os

import pandas as pd

import thaao_settings as ts

instr = 'ceilometer'
date_list = pd.date_range(
        ts.instr_metadata[instr]['start_instr'], ts.instr_metadata[instr]['end_instr'], freq='D').tolist()
folder = os.path.join(ts.basefolder, "thaao_" + instr)

if __name__ == "__main__":

    ceilometer = pd.DataFrame(columns=['dt', 'mask'])

    for i in date_list:
        fn = os.path.join(
                folder, i.strftime('%Y%m') + "_Thule_CHM190147.nc", i.strftime('%Y%m%d') + "_Thule_CHM190147_000.nc")
        if os.path.exists(fn):
            ceilometer.loc[i] = [i, True]

    ts.save_txt(instr, ceilometer)
