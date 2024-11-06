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

import julian
import numpy as np
import pandas as pd
import xarray as xr

import thaao_settings as ts
import tools as tls

instr = 'rad'
tm_res = '5min'

var_list_rad = ['SW', 'LW', 'PAR', 'TB']
var_list_alb = ['ALBEDO_SW', 'SW_UP']

variables_rad = {'SW' : {'name': 'SW', 'uom': '[Wm-2]'}, 'LW': {'name': 'LW', 'uom': '[Wm-2]'},
                 'PAR': {'name': 'PAR', 'uom': '[Wm-2]'}, 'TB': {'name': 'TB', 'uom': '[K]'}}

variables_alb = {'ALBEDO_SW': {'name': 'ALBEDO_SW', 'uom': '[unitless]'}, 'SW_UP': {'name': 'SW_UP', 'uom': '[Wm-2]'}}

folder = os.path.join(ts.basefolder, "thaao_" + instr)


def read_rad(date_f):
    """
    Function for reading radiation data and formatting data strings.
    :param date_f: (YYYY)
    :return: radiation data as DataFrame (pandas). Index is datetime and columns are: ['SZA', 'SW', 'LW', 'PAR', 'TB']
    """

    print('Reading RADIATION data for year ', date_f.strftime('%Y'))
    file_rad = os.path.join(folder, 'IRR_' + date_f.strftime('%y') + '001_' + date_f.strftime('%y') + '365_FIN.DAT')
    rad = pd.read_table(file_rad, skiprows=None, header=0, decimal='.', sep='\s+')

    tmp = np.empty(rad['JDAY_ASS'].shape, dtype=dt.datetime)
    for ii, el in enumerate(rad['JDAY_ASS']):
        tmp[ii] = julian.from_jd(el, fmt='jd')
        tmp[ii].replace(microsecond=0)

    rad.index = pd.DatetimeIndex(tmp)
    rad.index.name = 'datetime'

    data = rad.drop(['JDAY_ASS', 'YEAR_FR', 'JDAY_UT', 'TIME_UT', 'JDAY_LOC', 'TIME_LOC'], axis=1)

    return data


def read_alb(date_f):
    """
    Function for reading albedo data and formatting data strings.
    :param date_f: (YYYY)
    :return: radiation data as DataFrame (pandas). Index is datetime and columns are: ['SZA', 'SW', 'LW', 'PAR', 'TB']
    """

    print('Reading ALBEDO data for year ', date_f.strftime('%Y'))
    file_rad = os.path.join(folder, 'ALBEDO_SW_' + date_f.strftime('%Y') + '_5MIN.DAT')
    alb = pd.read_table(file_rad, skiprows=None, header=0, decimal='.', sep='\s+')
    tmp = np.empty(alb['JDAY_UT'].shape, dtype=dt.datetime)
    for ii, el in enumerate(alb['JDAY_UT']):
        new_jd_ass = el + julian.to_jd(dt.datetime(int(date_f.strftime('%Y')) - 1, 12, 31, 0, 0), fmt='jd')
        tmp[ii] = julian.from_jd(new_jd_ass, fmt='jd')
        tmp[ii] = tmp[ii].replace(microsecond=0)

    alb.index = pd.DatetimeIndex(tmp)
    alb.index.name = 'datetime'

    data = alb.drop(['JDAY_UT', 'JDAY_LOC', 'SZA', 'SW_DOWN'], axis=1)

    return data


if __name__ == "__main__":

    year_ls = [2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024]

    # fn_rad_nc = 'radiation_stats_RAD_' + str(tm_res) + '_' + str(year_ls[0]) + '_' + str(year_ls[-1]) + '.nc'
    # fn_alb_nc = 'radiation_stats_ALB_' + str(tm_res) + '_' + str(year_ls[0]) + '_' + str(year_ls[-1]) + '.nc'

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

    tls.save_mask_txt(data_rad['LW'], 'rad_down_lw')
    tls.save_mask_txt(data_rad['SW'], 'rad_down_sw')
    tls.save_mask_txt(data_rad['LW_UP'], 'rad_up_lw')
    tls.save_mask_txt(data_rad['TB'], 'rad_tb')
    tls.save_mask_txt(data_rad['PAR_UP'], 'rad_par_up')
    tls.save_mask_txt(data_rad['PAR_DOWN'], 'rad_par_down')

    tmp_alb = 0
    data_alb = pd.DataFrame()
    for yr in year_ls:
        start = dt.datetime(int(yr), 1, 1)
        try:
            data_alb_tmp = read_alb(start)
            data_alb = pd.concat([data_alb, data_alb_tmp])
        except FileNotFoundError:
            data_alb_res = None
            print("file albedo " + str(yr) + " not available")

    tls.save_mask_txt(data_alb['ALB'], 'rad_up_sw')

    # old rad radiation data DMI availability
    fol_input_rad_old = os.path.join(folder, 'rad_dsi_legacy')
    date_list = pd.date_range(dt.datetime(2000, 1, 1), dt.datetime(2011, 12, 31), freq='D').tolist()
    rad_dsi_legacy = pd.DataFrame(columns=['dt', 'mask'])
    for i in date_list:
        fn = os.path.join(fol_input_rad_old, i.strftime('%Y-%m-%d') + '.globirr.thule.txt')
        if os.path.exists(fn):
            rad_dsi_legacy.loc[i] = [i, True]
    np.savetxt(
            os.path.join(fol_input_rad_old, 'rad_dsi_legacy' + '_data_avail_list.txt'), rad_dsi_legacy, fmt='%s')

    fol_input_rad = os.path.join(folder, 'rad_hourly')
    uli = pd.read_table(
            os.path.join(fol_input_rad, 'ULI.txt'), comment='#', sep='\s+', usecols=[0, 1, 2],
            parse_dates={'datetime': [0, 1]}, names=['date', 'time', 'rad'], header=0, index_col='datetime')
    dli = pd.read_table(
            os.path.join(fol_input_rad, 'DLI.txt'), comment='#', sep='\s+', usecols=[0, 1, 2],
            parse_dates={'datetime': [0, 1]}, names=['date', 'time', 'rad'], header=0, index_col='datetime')
    usi = pd.read_table(
            os.path.join(fol_input_rad, 'USI.txt'), comment='#', sep='\s+', usecols=[0, 1, 2],
            parse_dates={'datetime': [0, 1]}, names=['date', 'time', 'rad'], header=0, index_col='datetime')
    dsi = pd.read_table(
            os.path.join(fol_input_rad, 'DSI.txt'), comment='#', sep='\s+', usecols=[0, 1, 2],
            parse_dates={'datetime': [0, 1]}, names=['date', 'time', 'rad'], header=0, index_col='datetime')
    rad_dsi_legacy.columns = ['datetime', 'rad']
    rad_dsi_legacy = rad_dsi_legacy.set_index('datetime')
    rad_dsi_legacy = rad_dsi_legacy * 1  # setting a value
    dsi_all = pd.concat([dsi, rad_dsi_legacy])
    dsi_all.sort_index()

    tls.save_mask_txt(usi, 'rad_usi')
    tls.save_mask_txt(uli, 'rad_uli')
    tls.save_mask_txt(dli, 'rad_dli')
    tls.save_mask_txt(dsi_all, 'rad_dsi')
