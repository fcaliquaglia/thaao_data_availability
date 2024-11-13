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

instr = 'ecapac_mrr'
date_list = pd.date_range(
        ts.instr_metadata[instr]['start_instr'], ts.instr_metadata[instr]['end_instr'], freq='D').tolist()
folder = os.path.join(ts.basefolder, "thaao_" + instr)

if __name__ == "__main__":

    ecapac_mrr = pd.DataFrame(columns=['dt', 'mask'])

    # # currently no real date, only estimate
    # for i in date_list:
    #     ecapac_mrr.loc[i] = [i, True]

    for i in date_list:
        fn = os.path.join(
                folder, 'RawSpectra', i.strftime('%Y%m'), i.strftime('%m%d') + ".raw")
        if os.path.exists(fn):
            ecapac_mrr.loc[i] = [i, True]

    tls.save_txt(instr, ecapac_mrr)
