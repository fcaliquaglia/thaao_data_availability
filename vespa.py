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

import pandas as pd

import thaao_settings as ts
import tools as tls

instr = 'vespa'
folder = os.path.join(ts.basefolder, "thaao_" + instr)
if __name__ == "__main__":
    vespa = pd.read_table(os.path.join(folder, 'vespaIWV_July2016-Sept2022_v3.txt'), delimiter='\s+')
    vespa['dt'] = vespa['yyyy-mm-dd'].values + ' ' + vespa['HH:MM:SS'].values
    vespa.index = pd.DatetimeIndex(vespa['dt'])

    tls.save_mask_txt(vespa['PWV'], folder, instr)
