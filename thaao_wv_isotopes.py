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

import numpy as np
import pandas as pd
import tools as tls
import settings as ts

instr = 'wv_isotopes'
folder = os.path.join(ts.basefolder, "thaao_" + instr)

if __name__ == "__main__":
    fn = os.path.join(folder, 'wv_isotopes.xlsx')
    wv_isotopes_tmp = pd.read_excel(fn)
    vals = np.repeat(True, len(wv_isotopes_tmp))

    wv_isotopes = pd.concat([pd.Series(wv_isotopes_tmp.values[:, 0]), pd.Series(vals)], axis=1)

    tls.save_mask_txt(wv_isotopes, folder, instr)
