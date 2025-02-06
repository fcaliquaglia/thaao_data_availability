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
import shutil
import zipfile

import pandas as pd

import settings as ts
from single_instr_data_avail import tools as tls

instr = 'dir_rad_trkr'

date_list = pd.date_range(
        ts.instr_metadata[instr]['start_instr'], ts.instr_metadata[instr]['end_instr'], freq='D').tolist()
folder = os.path.join(ts.basefolder, "thaao_" + instr, 'solcom')


def daily_zipping():
    for i in date_list:
        fn = os.path.join(folder, i.strftime('%Y'))
        fn_new = os.path.join(folder, i.strftime('%Y%m%d'))
        files = [j for j in os.listdir(os.path.join(folder, i.strftime('%Y'))) if
                 j.startswith(i.strftime('%Y%m%d'))]
        try:
            if files == []:
                continue
            else:
                for f in files:
                    os.makedirs(fn_new, exist_ok=True)
                    shutil.copy(os.path.join(fn, f), os.path.join(fn_new, f))
                    print(os.path.join(fn_new, f))
        except FileNotFoundError as e:
            print(e)
            continue

        try:
            os.makedirs(os.path.join(folder, i.strftime('%Y')), exist_ok=True)
            with zipfile.ZipFile(
                    os.path.join(folder, i.strftime('%Y'), i.strftime('%Y%m%d') + '.zip'), 'w') as zipf:
                tls.zipdir(fn_new, zipf)
            print(f'zipped {fn_new}')
            try:
                shutil.rmtree(fn_new)
            except FileNotFoundError as e:
                print(e)
        except:
            print(f'error in zipping file {fn_new}')


if __name__ == "__main__":
    # for reordering old files
    # daily_zipping()

    dir_rad_trkr = pd.DataFrame(columns=['dt', 'mask'])
    dir_rad_trkr_missing = pd.DataFrame(columns=['dt', 'mask'])
    for ii, i in enumerate(date_list[:-1]):
        fn = os.path.join(
                folder, i.strftime('%Y'), i.strftime('%Y%m%d'))
        try:
            if os.path.exists(fn + '.zip'):
                print(f'available: {fn}')
                dir_rad_trkr.loc[i] = [i, True]
            else:
                dir_rad_trkr_missing.loc[i] = [i, False]
                print(f'missing: {fn}')

        except (FileNotFoundError, zipfile.BadZipFile) as e:
            print(e)

    tls.save_txt(instr, dir_rad_trkr)
    tls.save_txt(instr, dir_rad_trkr_missing, missing=True)
