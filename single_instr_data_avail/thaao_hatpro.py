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

instr = 'hatpro'


def update_data_avail(instr):
    import os
    import numpy as np
    import pandas as pd
    import julian
    import datetime as dt

    import settings as ts
    import single_instr_data_avail.sida_tools as sida_tls
    base_folder = ts.basefolder  # Base folder for efficiency

    year_ls = np.arange(2017, 2025)

    data_avail_hat = pd.DataFrame()
    for year in year_ls:
        file_path1 = os.path.join(
                base_folder, "thaao_hatpro", 'LWP_2019_20_21', f'LWP_QUAD_Ka_allKa_OFFS_1_min_{year}.dat')

        try:
            hatpro_tmp = pd.read_table(file_path1, sep='\s+', low_memory=False)
            tmp = np.empty(hatpro_tmp['JD_rif'].shape, dtype=dt.datetime)
            for ii, el in enumerate(hatpro_tmp['JD_rif']):
                new_jd_ass = el + julian.to_jd(dt.datetime(year - 1, 12, 31, 0, 0), fmt='jd')
                tmp[ii] = julian.from_jd(new_jd_ass, fmt='jd')
                tmp[ii] = tmp[ii].replace(microsecond=0)
            hatpro_tmp['datetime'] = tmp
            data_avail_hat = pd.concat([data_avail_hat, hatpro_tmp[['datetime', 'LWP_gm-2']]])
        except FileNotFoundError as e:
            print(e)

    file_path2 = os.path.join(base_folder, "thaao_hatpro", 'LWP_ARCSIX_1_min_2024.dat')
    hatpro_tmp = pd.read_table(file_path2, sep='\s+', low_memory=False)
    tmp = np.empty(hatpro_tmp['JD_rif'].shape, dtype=dt.datetime)
    for ii, el in enumerate(hatpro_tmp['JD_rif']):
        new_jd_ass = el + julian.to_jd(dt.datetime(year - 1, 12, 31, 0, 0), fmt='jd')
        tmp[ii] = julian.from_jd(new_jd_ass, fmt='jd')
        tmp[ii] = tmp[ii].replace(microsecond=0)
    hatpro_tmp['datetime'] = tmp
    data_avail_hat = pd.concat([data_avail_hat, hatpro_tmp[['datetime', 'LWP_gm-2']]])

    data_avail_hat = data_avail_hat.set_index('datetime').sort_index()
    # Saving the specific 'LWP_gm-2' column with the 'save_m_csv' method
    sida_tls.save_m_csv(data_avail_hat, os.path.join(base_folder, "thaao_" + instr), instr)
