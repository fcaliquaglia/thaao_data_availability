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
from single_instr_data_avail import tools as tls

instr = 'ecapac_aws_snow'
date_list = pd.date_range(
        ts.instr_metadata[instr]['start_instr'], ts.instr_metadata[instr]['end_instr'], freq='D').tolist()
folder = os.path.join(ts.basefolder, "thaao_" + instr)

if __name__ == "__main__":

    ecapac_aws_snow = pd.DataFrame(columns=['dt', 'mask'])
    # # currently no real date, only estimates
    # for i in date_list:
    #     ecapac_aws_snow.loc[i] = [i, True]

    for i in date_list:
        fn = os.path.join(
                folder, "AWS_ECAPAC", i.strftime('%Y'), "AWS_THAAO_" + i.strftime('%Y_%m_%d') + '_00_00' + ".dat")
        if os.path.exists(fn):
            ecapac_aws_snow.loc[i] = [i, True]

    tls.save_txt(instr, ecapac_aws_snow)
