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

instr = 'ecapac_mrr'
date_list = pd.date_range(
        ts.instr_metadata[instr]['start_instr'], ts.instr_metadata[instr]['end_instr'], freq='D').tolist()
folder = os.path.join(ts.basefolder, "thaao_" + instr)

if __name__ == "__main__":

    ecapac_mrr = pd.DataFrame(columns=['dt', 'mask'])

    # currently no real date, only estimate
    for i in date_list:
        ecapac_mrr.loc[i] = [i, True]

    # for i in date_list:
    #     fn = os.path.join(
    #             folder, "mrr_improtoo_0.107_Thule_" + i.strftime('%Y%m%d') + ".nc")
    #     if os.path.exists(fn):
    #         ecapac_mrr.loc[i] = [i, True]

    ts.save_txt(instr, ecapac_mrr)
