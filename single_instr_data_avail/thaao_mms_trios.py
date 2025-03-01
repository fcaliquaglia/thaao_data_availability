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

instr = 'mms_trios'


def update_data_avail(instr):
    import os

    import pandas as pd

    import settings as ts
    import single_instr_data_avail.sida_tools as sida_tls

    date_list = pd.date_range(
            ts.instr_metadata[instr]['start_instr'], ts.instr_metadata[instr]['end_instr'], freq='D').tolist()
    folder = os.path.join(ts.basefolder, "thaao_" + instr)

    mms_trios = pd.DataFrame(columns=['dt', 'mask'])
    mms_trios_missing = pd.DataFrame(columns=['dt', 'mask'])

    for i in date_list:
        fn = os.path.join(
                folder, i.strftime('%Y'), i.strftime('%Y%m%d'))
        if os.path.exists(fn + '.zip'):
            print(i)
            mms_trios.loc[i] = [i, True]
        else:
            mms_trios_missing.loc[i] = [i, False]

    sida_tls.save_csv(instr, mms_trios)
