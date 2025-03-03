#!/usr/local/bin/python3
# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------------
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

import datetime as dt
import os

import julian
import numpy as np
import pandas as pd

import settings as ts
import single_instr_data_avail.sida_tools as sida_tls


def update_data_avail(instr):
    folder = os.path.join(ts.basefolder, "thaao_" + instr)
    date_list = pd.date_range(
            ts.instr_metadata[instr]['start_instr'], ts.instr_metadata[instr]['end_instr'], freq='YE').tolist()

    hatpro_lwp = pd.DataFrame()
    for date in date_list:
        file_path1 = os.path.join(
                folder, 'LWP_2019_20_21', f'LWP_QUAD_Ka_allKa_OFFS_1_min_{date.year}.dat')

        try:
            hatpro_tmp = pd.read_table(file_path1, sep='\s+', low_memory=False)
            tmp = np.empty(hatpro_tmp['JD_rif'].shape, dtype=dt.datetime)
            for ii, el in enumerate(hatpro_tmp['JD_rif']):
                new_jd_ass = el + julian.to_jd(dt.datetime(date.year - 1, 12, 31, 0, 0), fmt='jd')
                tmp[ii] = julian.from_jd(new_jd_ass, fmt='jd')
                tmp[ii] = tmp[ii].replace(microsecond=0)
            hatpro_tmp['datetime'] = tmp
            hatpro_lwp = pd.concat([hatpro_lwp, hatpro_tmp[['datetime', 'LWP_gm-2']]])
        except FileNotFoundError as e:
            print(e)

    YEAR = 2024
    file_path2 = os.path.join(folder, f'LWP_ARCSIX_1_min_{YEAR}.dat')
    hatpro_tmp = pd.read_table(file_path2, sep='\s+', low_memory=False)
    tmp = np.empty(hatpro_tmp['JD_rif'].shape, dtype=dt.datetime)
    for ii, el in enumerate(hatpro_tmp['JD_rif']):
        new_jd_ass = el + julian.to_jd(dt.datetime(YEAR - 1, 12, 31, 0, 0), fmt='jd')
        tmp[ii] = julian.from_jd(new_jd_ass, fmt='jd')
        tmp[ii] = tmp[ii].replace(microsecond=0)
    hatpro_tmp['datetime'] = tmp
    hatpro_lwp = pd.concat([hatpro_lwp, hatpro_tmp[['datetime', 'LWP_gm-2']]])

    hatpro_lwp = hatpro_lwp.set_index('datetime').sort_index()

    hatpro_iwv = pd.DataFrame()
    for date in date_list:
        file_path3 = os.path.join(
                folder, 'IWV_2019_20_21', f'QC_1min_IWV_{date.year}_STD_09_RF_BACK_20min.DAT')
        try:
            hatpro_tmp = pd.read_table(file_path3, sep='\s+', low_memory=False)
            tmp = np.empty(hatpro_tmp['JD_rif'].shape, dtype=dt.datetime)
            for ii, el in enumerate(hatpro_tmp['JD_rif']):
                new_jd_ass = el + julian.to_jd(dt.datetime(date.year - 1, 12, 31, 0, 0), fmt='jd')
                tmp[ii] = julian.from_jd(new_jd_ass, fmt='jd')
                tmp[ii] = tmp[ii].replace(microsecond=0)
            hatpro_tmp['datetime'] = tmp
            hatpro_iwv = pd.concat([hatpro_iwv, hatpro_tmp[['datetime', 'IWV']]])
        except FileNotFoundError as e:
            print(e)
    hatpro_iwv = hatpro_iwv.set_index('datetime').sort_index()

    hatpro = pd.concat([hatpro_iwv, hatpro_lwp])
    sida_tls.save_csv(instr, hatpro)
