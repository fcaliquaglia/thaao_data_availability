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

instr = 'vespa'
date_list = pd.date_range(
        ts.instr_metadata[instr]['start_instr'], ts.instr_metadata[instr]['end_instr'], freq='H').tolist()
folder = os.path.join(ts.basefolder, "thaao_" + instr)

if __name__ == "__main__":
    vespa = pd.DataFrame(columns=['dt', 'mask'])
    vespa_missing = pd.DataFrame(columns=['dt', 'mask'])

    vespa_dt = pd.read_table(os.path.join(folder, 'vespaPWVClearSky.txt'), delimiter='\s+')
    vespa_dt['dt'] = vespa_dt['yyyy-mm-dd'].values + ' ' + vespa_dt['HH:MM:SS'].values
    # rounding datetime index to hour
    vespa_dt.index = pd.DatetimeIndex(vespa_dt['dt']).round('h')

    for i in date_list:
        if i in vespa_dt.index:
            vespa.loc[i] = [i, True]
        else:
            vespa_missing.loc[i] = [i, True]

    tls.save_txt(instr, vespa)
    tls.save_txt(instr, vespa_missing, missing=True)
