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


def update_data_avail(instr):
    import os

    import pandas as pd

    import settings as ts

    import single_instr_data_avail.sida_tools as sida_tls

    date_list = pd.date_range(
            ts.instr_metadata[instr]['start_instr'], ts.instr_metadata[instr]['end_instr'], freq='D').tolist()
    folder = os.path.join(ts.basefolder, "thaao_" + instr)

    hyso_tide_1 = pd.DataFrame(columns=['dt', 'mask'])
    hyso_tide_1_missing = pd.DataFrame(columns=['dt', 'mask'])
    for i in date_list:
        fn = os.path.join(folder, i.strftime('%Y'), "Thule_1_2_" + i.strftime('%y%m%d') + "_corr.dat")
        if os.path.exists(fn):
            hyso_tide_1.loc[i] = [i, True]
            print('file ' + str(fn) + ' FOUND')
        else:
            hyso_tide_1_missing.loc[i] = [i, True]
            print('file ' + str(fn) + ' not found')

    sida_tls.save_csv(instr, hyso_tide_1)
