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
from glob import glob

import pandas as pd

import settings as ts

instr = 'o3_sondes'
date_list = pd.date_range(
        ts.instr_metadata[instr]['start_instr'], ts.instr_metadata[instr]['end_instr'], freq='D').tolist()
folder = os.path.join(ts.basefolder, "thaao_" + instr)

if __name__ == "__main__":

    o3_sondes = pd.DataFrame(columns=['dt', 'mask'])

    for i in date_list:
        fn = glob(os.path.join(folder, 'th' + i.strftime('%y%m%d') + '.*'))
        try:
            if fn[0]:
                o3_sondes.loc[i] = [i, True]
        except IndexError:
            pass

    ts.save_txt(instr, o3_sondes)