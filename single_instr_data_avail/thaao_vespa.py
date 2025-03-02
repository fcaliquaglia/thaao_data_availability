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
    folder = os.path.join(ts.basefolder, "thaao_" + instr)

    vespa = pd.read_table(os.path.join(folder, 'vespaPWVClearSky.txt'), delimiter='\s+')
    vespa['datetime'] = vespa['yyyy-mm-dd'].values + ' ' + vespa['HH:MM:SS'].values
    # rounding datetime index to hour
    vespa.set_index('datetime', inplace=True)
    vespa.drop(columns=['yyyy-mm-dd', 'HH:MM:SS', 'Tout', 'Tatm', 'RH'], inplace=True)

    sida_tls.save_csv(instr, vespa)
