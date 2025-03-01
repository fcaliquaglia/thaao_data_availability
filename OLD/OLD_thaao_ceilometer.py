#!/usr/local/bin/python3
# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------------
"""
OK
"""
# -------------------------------------------------------------------------------
__author__ = "Filippo Cali' Quaglia"
__affiliation__ = "UNIVE, INGV"
__credits__ = ["??????"]
__license__ = "GPL"
__version__ = "1.1"
__email__ = "filippo.caliquaglia@ingv.it"
__status__ = "Research"
__lastupdate__ = "February 2025"

import os
import zipfile

import pandas as pd

import settings as ts
from single_instr_data_avail import tools as tls

instr = 'ceilometer'
date_list = pd.date_range(
        ts.instr_metadata[instr]['start_instr'], ts.instr_metadata[instr]['end_instr'], freq='D').tolist()
folder = os.path.join(ts.basefolder, "thaao_" + instr)

if __name__ == "__main__":

    ceilometer = pd.DataFrame(columns=['dt', 'mask'])
    ceilometer_missing = pd.DataFrame(columns=['dt', 'mask'])
    for ii, i in enumerate(date_list[:-1]):
        fn = os.path.join(
                folder, i.strftime('%Y'), i.strftime('%Y%m') + '_Thule_CHM190147.nc')
        date_list_int = pd.date_range(
                date_list[ii], date_list[ii + 1], freq='D', inclusive='left').tolist()
        try:
            with zipfile.ZipFile(f'{fn}.zip', 'r') as myzip:
                file_list = [x.split('_')[0] for x in myzip.namelist()]
                for j in date_list_int:
                    if j.strftime('%Y%m%d') in file_list:
                        ceilometer.loc[j] = [j, True]
                    else:
                        ceilometer_missing.loc[j] = [j, False]
            myzip.close()
            print(fn)
        except (FileNotFoundError, zipfile.BadZipFile) as e:
            print(e)

    tls.save_csv(instr, ceilometer)
    tls.save_csv(instr, ceilometer_missing)
