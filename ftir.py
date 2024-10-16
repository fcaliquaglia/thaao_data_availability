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
from glob import glob

import numpy as np
import pandas as pd

from utils import thaao_settings as ts

instr = 'ftir'
date_list = pd.date_range(
        ts.instr_na_list[instr]['start_instr'], ts.instr_na_list[instr]['end_instr'], freq='D').tolist()
folder = os.path.join(ts.basefolder, "thaao_" + instr)

if __name__ == "__main__":
    ftir = pd.DataFrame()
    for i in date_list:
        fn = glob(
                os.path.join(folder, 'groundbased_ftir.' + 'c2h6' + '_ncar001_thule_' + i.strftime('%Y%m%d') + '*'))
        try:
            if os.path.exists(fn[0]):
                start = fn[0].split('_')[6]
                end = fn[0].split('_')[7]
                date_list_avail = pd.date_range(
                        dt.datetime.strptime(start[0:8], '%Y%m%d'), dt.datetime.strptime(end[0:8], '%Y%m%d'),
                        freq='D').tolist()
                vals = np.repeat(True, len(date_list_avail))
                ftir_t = pd.concat([pd.Series(date_list_avail), pd.Series(vals)], axis=1)
            ftir = pd.concat([ftir_t, ftir], ignore_index=True)
        except IndexError:
            pass

    ts.save_txt(instr, ftir)
