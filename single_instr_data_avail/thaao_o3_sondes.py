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
__version__ = "1.1"
__email__ = "filippo.caliquaglia@ingv.it"
__status__ = "Research"
__lastupdate__ = "February 2025"

import os

import pandas as pd

import settings as ts
import single_instr_data_avail.sida_tools as sida_tls


def update_data_avail(instr):
    date_list = pd.date_range(
            ts.instr_metadata[instr]['start_instr'], ts.instr_metadata[instr]['end_instr'], freq='D').tolist()
    folder = os.path.join(ts.basefolder, "thaao_" + instr)
    o3_sondes = pd.DataFrame(columns=['datetime', 'mask'])
    for i in date_list:
        fn = os.path.join(folder, 'th' + i.strftime('%y%m') + '.erv')
        if os.path.exists(fn):
            o3_sondes.loc[i] = [i, True]

    o3_sondes = pd.DataFrame(columns=['dt', 'mask'])

    sida_tls.save_csv(instr, o3_sondes)
