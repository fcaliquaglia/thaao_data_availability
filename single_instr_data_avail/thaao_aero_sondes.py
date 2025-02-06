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
from glob import glob

import pandas as pd

import settings as ts
import tools as tls

instr = 'aero_sondes'
date_list = pd.date_range(
        ts.instr_metadata[instr]['start_instr'], ts.instr_metadata[instr]['end_instr'], freq='D').tolist()
folder = os.path.join(ts.basefolder, 'thaao_' + instr)

if __name__ == "__main__":
    aero_sondes = pd.DataFrame(columns=['dt', 'mask'])

    for i in date_list:
        fn = glob(os.path.join(folder, 'th' + i.strftime('%y%m%d') + '.*'))
        try:
            if fn[0]:
                aero_sondes.loc[i] = [i, True]
        except IndexError:
            pass

    tls.save_txt(instr, aero_sondes)
