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

import datetime as dt
import os

# import julian
# import numpy as np
import pandas as pd

import settings as ts
import tools as tls

instr = 'rad'
folder = os.path.join(ts.basefolder, "thaao_" + instr)


def read_rad(date_f):
    """
    Function for reading radiation data and formatting data strings.
    :param date_f: (YYYY)
    :return: radiation data as DataFrame (pandas). Index is datetime and columns are: ['SZA', 'SW', 'LW', 'PAR', 'TB']
    """

    print('Reading RADIATION data for year ', date_f.strftime('%Y'))
    file_rad = os.path.join(folder, 'MERGED_SW_LW_UP_DW_METEO_' + date_f.strftime('%Y') + '_5MIN.DAT')
    rad = pd.read_table(file_rad, skiprows=None, header=0, decimal='.', sep='\s+')

    rad.index = pd.DatetimeIndex(
        pd.to_datetime(date_f.strftime('%Y') + '-1-1') + pd.to_timedelta(rad['JDAY_UT'], unit='D'))
    rad.index.name = 'datetime'

    data = rad.drop(
            labels=['JDAY_UT', 'JDAY_LOC', 'SZA', 'ALBEDO_SW', 'ALBEDO_LW', 'ALBEDO_PAR', 'P', 'T', 'RH', 'PE', 'RR2'],
            axis=1)

    return data


# def read_alb(date_f):
#     """
#     Function for reading albedo data and formatting data strings.
#     :param date_f: (YYYY)
#     :return: radiation data as DataFrame (pandas).
#     """
#
#     print('Reading ALBEDO data for year ', date_f.strftime('%Y'))
#     file_rad = os.path.join(folder, 'ALBEDO_SW_' + date_f.strftime('%Y') + '_5MIN.DAT')
#     alb = pd.read_table(file_rad, skiprows=None, header=0, decimal='.', sep='\s+')
#     tmp = np.empty(alb['JDAY_UT'].shape, dtype=dt.datetime)
#     for ii, el in enumerate(alb['JDAY_UT']):
#         new_jd_ass = el + julian.to_jd(dt.datetime(int(date_f.strftime('%Y')) - 1, 12, 31, 0, 0), fmt='jd')
#         tmp[ii] = julian.from_jd(new_jd_ass, fmt='jd')
#         tmp[ii] = tmp[ii].replace(microsecond=0)
#
#     alb.index = pd.DatetimeIndex(tmp)
#     alb.index.name = 'datetime'
#
#     data = alb.drop(['JDAY_UT', 'JDAY_LOC', 'SZA', 'SW_DOWN'], axis=1)
#
#     return data


if __name__ == "__main__":

    year_ls = [2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024]

    tmp_rad = 0
    data_rad = pd.DataFrame()
    for yr in year_ls:
        start = dt.datetime(int(yr), 1, 1)
        try:
            data_rad_tmp = read_rad(start)
            data_rad = pd.concat([data_rad, data_rad_tmp])
        except FileNotFoundError:
            data_rad_res = None
            print("file radiation " + str(yr) + " not available")

    try:
        tls.save_mask_txt(data_rad['SW_DOWN'], folder, 'rad_dsi')
        tls.save_mask_txt(data_rad['LW_DOWN'], folder, 'rad_dli')
        tls.save_mask_txt(data_rad['PAR_DOWN'], folder, 'rad_par_down')
        tls.save_mask_txt(data_rad['SW_UP'], folder, 'rad_usi')
        tls.save_mask_txt(data_rad['LW_UP'], folder, 'rad_uli')
        tls.save_mask_txt(data_rad['PAR_UP'], folder, 'rad_par_up')
        tls.save_mask_txt(data_rad['TBP'], folder, 'rad_tb')
    except IndexError:
        print('error in var')

    # TODO: the legacy data part is not working  # # old rad radiation data from DMI  # try:  #     fol_input_rad_old = os.path.join(folder, 'rad_dsi_legacy')  #     date_list = pd.date_range(dt.datetime(2000, 1, 1), dt.datetime(2011, 12, 31), freq='D').tolist()  #     rad_dsi_legacy = pd.DataFrame(columns=['dt', 'mask'])  #     for i in date_list:  #         fn = os.path.join(fol_input_rad_old, i.strftime('%Y-%m-%d') + '.globirr.thule.txt')  #         if os.path.exists(fn):  #             rad_dsi_legacy.loc[i] = [i, True]  #     np.savetxt(  #             os.path.join(fol_input_rad_old, 'rad_dsi_legacy' + '_data_avail_list.txt'), rad_dsi_legacy, fmt='%s')

    # old radiation data  # TODO: files missing --> ask Giorgio di Sarra??

    #     fol_input_rad = os.path.join(folder, 'rad_hourly')  #     uli = pd.read_table(  #             os.path.join(fol_input_rad, 'ULI.txt'), comment='#', sep='\s+', usecols=[0, 1, 2],  #             parse_dates={'datetime': [0, 1]}, names=['date', 'time', 'rad'], header=0, index_col='datetime')  #     dli = pd.read_table(  #             os.path.join(fol_input_rad, 'DLI.txt'), comment='#', sep='\s+', usecols=[0, 1, 2],  #             parse_dates={'datetime': [0, 1]}, names=['date', 'time', 'rad'], header=0, index_col='datetime')  #     usi = pd.read_table(  #             os.path.join(fol_input_rad, 'USI.txt'), comment='#', sep='\s+', usecols=[0, 1, 2],  #             parse_dates={'datetime': [0, 1]}, names=['date', 'time', 'rad'], header=0, index_col='datetime')  #     dsi = pd.read_table(  #             os.path.join(fol_input_rad, 'DSI.txt'), comment='#', sep='\s+', usecols=[0, 1, 2],  #             parse_dates={'datetime': [0, 1]}, names=['date', 'time', 'rad'], header=0, index_col='datetime')  #     rad_dsi_legacy.columns = ['datetime', 'rad']  #     rad_dsi_legacy = rad_dsi_legacy.set_index('datetime')  #     rad_dsi_legacy = rad_dsi_legacy * 1  # setting a value  #     dsi_all = pd.concat([dsi, rad_dsi_legacy])  #     dsi_all.sort_index()  #  #     tls.save_mask_txt(usi, folder, 'rad_usi')  #     tls.save_mask_txt(uli, folder, 'rad_uli')  #     tls.save_mask_txt(dli, folder, 'rad_dli')  #     tls.save_mask_txt(dsi_all, folder, 'rad_dsi')  # except:  #     print('error with legacy data 1')
