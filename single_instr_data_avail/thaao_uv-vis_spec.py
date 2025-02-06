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

instr = 'uv-vis_spec'
date_list = pd.date_range(
        ts.instr_metadata[instr]['start_instr'], ts.instr_metadata[instr]['end_instr'], freq='D').tolist()
folder = os.path.join(ts.basefolder, "thaao_" + instr)

if __name__ == "__main__":
    uv_vis_spec = pd.DataFrame(columns=['dt', 'mask'])
    uv_vis_spec_missing = pd.DataFrame(columns=['dt', 'mask'])

    for i in date_list:
        fn = os.path.join(folder, 'thtc' + i.strftime('%y%m') + '.erv')
        if os.path.exists(fn):
            uv_vis_spec.loc[i] = [i, True]
        else:
            uv_vis_spec_missing.loc[i] = [i, True]

    tls.save_txt(instr, uv_vis_spec)
    tls.save_txt(instr, uv_vis_spec_missing, missing=True)
