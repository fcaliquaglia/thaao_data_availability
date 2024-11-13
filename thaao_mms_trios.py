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
import zipfile

import pandas as pd

import settings as ts

instr = 'mms_trios'
date_list = pd.date_range(
        ts.instr_metadata[instr]['start_instr'], ts.instr_metadata[instr]['end_instr'], freq='D').tolist()
folder = os.path.join(ts.basefolder, "thaao_" + instr)

if __name__ == "__main__":

    mms_trios = pd.DataFrame(columns=['dt', 'mask'])

    for idx, i in enumerate(date_list):
        print(i)
        # file_list = glob(
        #         os.path.join(
        #                 fol_input, i.strftime('%Y-%m'), i.strftime('%Y-%m-%d') + '.zip'))
        if (os.path.exists(os.path.join(folder, i.strftime('%Y-%m') + '.zip'))) & (i.month != date_list[idx - 1].month):
            try:
                with zipfile.ZipFile(os.path.join(folder, i.strftime('%Y-%m') + '.zip'), 'r') as myzip:
                    file_list = list(set([os.path.dirname(x) for x in myzip.namelist()]))
                    # file_list = [re.split(r'[./]', x)[0] for x in myzip.namelist()]
                    myzip.close()
            except FileNotFoundError:
                continue
        elif os.path.exists(os.path.join(folder, i.strftime('%Y-%m') + '.zip')):
            try:
                if i.strftime('%Y-%m-%d') in file_list:
                    mms_trios.loc[i] = [i, True]
            except IndexError:
                pass

    ts.save_txt(instr, mms_trios)
