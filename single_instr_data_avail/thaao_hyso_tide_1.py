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

import numpy as np
import pandas as pd

import settings as ts
import single_instr_data_avail.sida_tools as sida_tls


def update_data_avail(instr):
    date_list = pd.date_range(
            ts.instr_metadata[instr]['start_instr'], ts.instr_metadata[instr]['end_instr'], freq='D').tolist()
    folder = os.path.join(ts.basefolder, "thaao_" + instr)

    hyso_tide_1 = pd.DataFrame()
    for i in date_list:
        fn = os.path.join(folder, i.strftime('%Y'), "Thule_1_2_" + i.strftime('%y%m%d') + "_corr.dat")
        if os.path.exists(fn):
            hyso_tide_1_tmp = pd.read_table(fn, header=None)
            hyso_tide_1_tmp.loc[1, hyso_tide_1_tmp.iloc[1] == 9999.00] = np.nan
            for j, date_str in enumerate(hyso_tide_1_tmp[0]):  # adjusting dates with hour 24:00 which raise errors!
                if "24:00:00" in date_str:
                    date_part, _ = date_str.split("|")  # Extract the date part
                    new_date = pd.to_datetime(date_part, format="%d/%m/%Y") + pd.Timedelta(days=1)
                    hyso_tide_1_tmp.at[j, 0] = new_date.strftime("%d/%m/%Y|00:00:00")
                else:
                    continue

            hyso_tide_1_tmp.index = pd.DatetimeIndex(pd.to_datetime(hyso_tide_1_tmp[0], format='%d/%m/%Y|%H:%M:%S'))
            hyso_tide_1_tmp.drop(columns=[0], inplace=True)
            hyso_tide_1_tmp.columns = ['sea_level', 'unk', 'unk']
            hyso_tide_1_tmp = hyso_tide_1_tmp[['sea_level']].resample('1min').mean()
            hyso_tide_1_tmp['sea_level'] = hyso_tide_1_tmp['sea_level'].replace(9999., np.nan)
            hyso_tide_1 = pd.concat([hyso_tide_1_tmp, hyso_tide_1])
            print('file ' + str(fn) + ' FOUND')
        else:
            print('file ' + str(fn) + ' not found')

    sida_tls.save_csv(instr, hyso_tide_1)
