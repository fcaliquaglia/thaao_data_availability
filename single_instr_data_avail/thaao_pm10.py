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

import numpy as np
import pandas as pd

import settings as ts
import tools as tls

instr = 'pm10'
date_list = pd.date_range(
        ts.instr_metadata[instr]['start_instr'], ts.instr_metadata[instr]['end_instr'], freq='D').tolist()
folder = os.path.join(ts.basefolder, 'thaao_' + instr)

if __name__ == "__main__":
    pm10_tmp = pd.DataFrame(columns=['dt', 'mask'])

    fn = os.path.join(folder, 'Thule_2010_sampling_3mag23_modificato_per_data_availability.xls')
    pm10_tmp = pd.read_excel(fn, index_col=0)
    vals = np.repeat(True, len(pm10_tmp))

    pm10 = pd.concat([pd.Series(pd.DatetimeIndex(pm10_tmp.index)), pd.Series(vals)], axis=1)

    tls.save_txt(instr, pm10)
