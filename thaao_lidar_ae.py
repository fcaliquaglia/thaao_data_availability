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

import os
from glob import glob

import pandas as pd

import settings as ts
import tools as tls

instr = 'lidar_ae'
date_list = pd.date_range(
        ts.instr_metadata[instr]['start_instr'], ts.instr_metadata[instr]['end_instr'], freq='D').tolist()
folder = os.path.join(ts.basefolder, "thaao_" + instr)

if __name__ == "__main__":

    lidar_ae = pd.DataFrame(columns=['dt', 'mask'])

    for i in date_list:
        fn = os.path.join(folder, 'WWW-AIR_1685207569988', 'thae' + i.strftime('%y%m') + '.*')
        if os.path.exists(fn):
            lidar_ae.loc[i] = [i, True]

    tls.save_txt(instr, lidar_ae)
