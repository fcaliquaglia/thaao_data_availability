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

instr = 'vespa'


def update_data_avail(instr):
    import single_instr_data_avail.tools as sida_tls
    import os

    import pandas as pd

    import settings as ts

    date_list = pd.date_range(
            ts.instr_metadata[instr]['start_instr'], ts.instr_metadata[instr]['end_instr'], freq='h').tolist()
    folder = os.path.join(ts.basefolder, "thaao_" + instr)

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

    sida_tls.save_csv(instr, vespa)
