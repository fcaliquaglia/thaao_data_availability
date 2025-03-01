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
__version__ = "1.1"
__email__ = "filippo.caliquaglia@ingv.it"
__status__ = "Research"
__lastupdate__ = "February 2025"

import datetime as dt
import os

instr = 'rad'


def update_data_avail(instr):
    import single_instr_data_avail.sida_tools as sida_tls
    import os
    import pandas as pd

    import settings as ts

    folder = os.path.join(ts.basefolder, "thaao_rad")
    year_ls = [2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024]

    data_rad = pd.DataFrame()
    for yr in year_ls:
        start = dt.datetime(int(yr), 1, 1)
        try:
            data_rad_tmp = read_rad(start, folder)
            data_rad = pd.concat([data_rad, data_rad_tmp])
        except FileNotFoundError:
            data_rad_tmp = None
            print("file radiation " + str(yr) + " not available")

    try:
        sida_tls.save_m_csv(data_rad['SW_DOWN'], folder, 'rad_dsi')
        sida_tls.save_m_csv(data_rad['LW_DOWN'], folder, 'rad_dli')
        sida_tls.save_m_csv(data_rad['PAR_DOWN'], folder, 'rad_par_down')
        sida_tls.save_m_csv(data_rad['SW_UP'], folder, 'rad_usi')
        sida_tls.save_m_csv(data_rad['LW_UP'], folder, 'rad_uli')
        sida_tls.save_m_csv(data_rad['PAR_UP'], folder, 'rad_par_up')
        sida_tls.save_m_csv(data_rad['TBP'], folder, 'rad_tb')
    except IndexError:
        print('error in var')

    # TODO: the legacy data part is not working  # # old rad radiation data from DMI  # try:  #     fol_input_rad_old = os.path.join(folder, 'rad_dsi_legacy')  #     date_list = pd.date_range(dt.datetime(2000, 1, 1), dt.datetime(2011, 12, 31), freq='D').tolist()  #     rad_dsi_legacy = pd.DataFrame(columns=['dt', 'mask'])  #     for i in date_list:  #         fn = os.path.join(fol_input_rad_old, i.strftime('%Y-%m-%d') + '.globirr.thule.csv')  #         if os.path.exists(fn):  #             rad_dsi_legacy.loc[i] = [i, True]  #     np.savecsv(  #             os.path.join(fol_input_rad_old, 'rad_dsi_legacy' + '_data_avail_list.csv'), rad_dsi_legacy, fmt='%s')

    # old radiation data  # TODO: files missing --> ask Giorgio di Sarra??

    #     fol_input_rad = os.path.join(folder, 'rad_hourly')  #     uli = pd.read_table(  #             os.path.join(fol_input_rad, 'ULI.csv'), comment='#', sep='\s+', usecols=[0, 1, 2],  #             parse_dates={'datetime': [0, 1]}, names=['date', 'time', 'rad'], header=0, index_col='datetime')  #     dli = pd.read_table(  #             os.path.join(fol_input_rad, 'DLI.csv'), comment='#', sep='\s+', usecols=[0, 1, 2],  #             parse_dates={'datetime': [0, 1]}, names=['date', 'time', 'rad'], header=0, index_col='datetime')  #     usi = pd.read_table(  #             os.path.join(fol_input_rad, 'USI.csv'), comment='#', sep='\s+', usecols=[0, 1, 2],  #             parse_dates={'datetime': [0, 1]}, names=['date', 'time', 'rad'], header=0, index_col='datetime')  #     dsi = pd.read_table(  #             os.path.join(fol_input_rad, 'DSI.csv'), comment='#', sep='\s+', usecols=[0, 1, 2],  #             parse_dates={'datetime': [0, 1]}, names=['date', 'time', 'rad'], header=0, index_col='datetime')  #     rad_dsi_legacy.columns = ['datetime', 'rad']  #     rad_dsi_legacy = rad_dsi_legacy.set_index('datetime')  #     rad_dsi_legacy = rad_dsi_legacy * 1  # setting a value  #     dsi_all = pd.concat([dsi, rad_dsi_legacy])  #     dsi_all.sort_index()  #  #     tls.save_m_csv(usi, folder, 'rad_usi')  #     tls.save_m_csv(uli, folder, 'rad_uli')  #     tls.save_m_csv(dli, folder, 'rad_dli')  #     tls.save_m_csv(dsi_all, folder, 'rad_dsi')  # except:  #     print('error with legacy data 1')


def read_rad(date_f, fol):
    """
    Function for reading radiation data and formatting data strings.
    :param date_f: (YYYY)
    :return: radiation data as DataFrame (pandas). Index is datetime and columns are: ['SZA', 'SW', 'LW', 'PAR', 'TB']
    """
    import pandas as pd
    print('Reading RADIATION data for year ', date_f.strftime('%Y'))
    file_rad = os.path.join(fol, 'MERGED_SW_LW_UP_DW_METEO_' + date_f.strftime('%Y') + '_5MIN.DAT')
    rad = pd.read_table(file_rad, skiprows=None, header=0, decimal='.', sep='\s+')

    rad.index = pd.DatetimeIndex(
            pd.to_datetime(date_f.strftime('%Y') + '-1-1') + pd.to_timedelta(rad['JDAY_UT'], unit='D'))
    rad.index.name = 'datetime'

    data = rad.drop(
            labels=['JDAY_UT', 'JDAY_LOC', 'SZA', 'ALBEDO_SW', 'ALBEDO_LW', 'ALBEDO_PAR', 'P', 'T', 'RH', 'PE', 'RR2'],
            axis=1)

    return data
