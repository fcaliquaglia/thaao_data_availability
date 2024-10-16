#!/usr/local/bin/python3
# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------------
#
"""
Plotting radiation preview: LW, SW, PAR, TB, (albedo)
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

import numpy as np
import pandas as pd
import xarray as xr

from prev import radiation_prev as rad_prev
from utils import thaao_settings as ts
from utils.thaao_settings import save_mask_txt

tm_res = '5T'

if __name__ == "__main__":

    var_list_rad = ['SW', 'LW', 'PAR', 'TB']
    var_list_alb = ['ALBEDO_SW', 'SW_UP']
    var_list_cot = ['JDAY_UT', 'JDAY_LOC', 'SZA', 'SW_DOWN', 'SW_UP', 'PAR_DOWN', 'PAR_UP', 'LW_DOWN', 'LW_UP', 'TBP',
                    'ALBEDO_SW', 'ALBEDO_PAR', 'T', 'PE', 'NET_SW', 'NET_LW', 'NET_SW+LW', 'SW_DW_CF', 'SW_UP_CF',
                    'NET_SW_CF', 'LW_DW_CF', 'LW_UP_CF', 'NET_LW_CF', 'NET_SW+LW_CF', 'RF_SW', 'RF_LW', 'RF_SW+LW',
                    'IWV', 'LWP', 'COT', 'REFF']

    variables_rad = {'SW' : {'name': 'SW', 'uom': '[Wm-2]'}, 'LW': {'name': 'LW', 'uom': '[Wm-2]'},
                     'PAR': {'name': 'PAR', 'uom': '[Wm-2]'}, 'TB': {'name': 'TB', 'uom': '[K]'}}

    variables_alb = {'ALBEDO_SW': {'name': 'ALBEDO_SW', 'uom': '[unitless]'},
                     'SW_UP'    : {'name': 'SW_UP', 'uom': '[Wm-2]'}}

    variables_cot = {'JDAY_UT'  : {}, 'JDAY_LOC': {}, 'SZA': {}, 'SW_DOWN': {}, 'SW_UP': {}, 'PAR_DOWN': {},
                     'PAR_UP'   : {}, 'LW_DOWN': {}, 'LW_UP': {}, 'TBP': {}, 'ALBEDO_SW': {}, 'ALBEDO_PAR': {}, 'T': {},
                     'PE'       : {}, 'NET_SW': {}, 'NET_LW': {}, 'NET_SW+LW': {}, 'SW_DW_CF': {}, 'SW_UP_CF': {},
                     'NET_SW_CF': {}, 'LW_DW_CF': {}, 'LW_UP_CF': {}, 'NET_LW_CF': {}, 'NET_SW+LW_CF': {}, 'RF_SW': {},
                     'RF_LW'    : {}, 'RF_SW+LW': {}, 'IWV': {}, 'LWP': {}, 'COT': {}, 'REFF': {}}

    fol_input = os.path.join(ts.basefolder, 'thaao_rad')

    year_ls = [2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023]

    fn_rad_nc = 'radiation_stats_RAD_' + str(tm_res) + '_' + str(year_ls[0]) + '_' + str(year_ls[-1]) + '.nc'
    fn_alb_nc = 'radiation_stats_ALB_' + str(tm_res) + '_' + str(year_ls[0]) + '_' + str(year_ls[-1]) + '.nc'

    tmp_rad = 0
    data_rad = xr.DataArray()
    for yr in year_ls:
        start = dt.datetime(int(yr), 1, 1)
        try:
            data_rad_tmp = rad_prev.read_rad(fol_input, start)
            data_rad = xr.concat([data_rad, data_rad], dim='datetime')
        except FileNotFoundError:
            data_rad_res = None
            print("file radiation " + str(yr) + " not available")

    save_mask_txt(data_rad.to_dataframe()['LW'], 'rad_down_lw')
    save_mask_txt(data_rad.to_dataframe()['SW'], 'rad_down_sw')
    save_mask_txt(data_rad.to_dataframe()['LW_UP'], 'rad_up_lw')
    save_mask_txt(data_rad.to_dataframe()['TB'], 'rad_tb')
    save_mask_txt(data_rad.to_dataframe()['PAR_UP'], 'rad_par_up')
    save_mask_txt(data_rad.to_dataframe()['PAR_DOWN'], 'rad_par_down')

    tmp_alb = 0
    data_alb = xr.DataArray()
    for yr in year_ls:
        start = dt.datetime(int(yr), 1, 1)
        try:
            data_alb_tmp = rad_prev.read_alb(fol_input, start)
            data_alb = xr.concat([data_alb, data_alb_tmp], dim='datetime')
        except FileNotFoundError:
            data_alb_res = None
            print("file albedo " + str(yr) + " not available")

    save_mask_txt(data_alb.to_dataframe()['ALB'], 'rad_up_sw')

    # old rad radiation data DMI availability
    fol_input_rad_old = os.path.join(fol_input, 'rad_dsi_legacy')
    date_list = pd.date_range(dt.datetime(2000, 1, 1), dt.datetime(2011, 12, 31), freq='D').tolist()
    rad_dsi_legacy = pd.DataFrame(columns=['dt', 'mask'])
    for i in date_list:
        fn = os.path.join(fol_input_rad_old, i.strftime('%Y-%m-%d') + '.globirr.thule.txt')
        if os.path.exists(fn):
            rad_dsi_legacy.loc[i] = [i, True]
    np.savetxt(
            os.path.join(fol_input_rad_old, 'rad_dsi_legacy' + '_data_avail_list.txt'), rad_dsi_legacy, fmt='%s')

    fol_input_rad = os.path.join(fol_input, 'rad_hourly')
    uli = pd.read_table(
            os.path.join(fol_input_rad, 'ULI.txt'), comment='#', delim_whitespace=True, usecols=[0, 1, 2],
            parse_dates={'datetime': [0, 1]}, names=['date', 'time', 'rad'], header=0, index_col='datetime')
    dli = pd.read_table(
            os.path.join(fol_input_rad, 'DLI.txt'), comment='#', delim_whitespace=True, usecols=[0, 1, 2],
            parse_dates={'datetime': [0, 1]}, names=['date', 'time', 'rad'], header=0, index_col='datetime')
    usi = pd.read_table(
            os.path.join(fol_input_rad, 'USI.txt'), comment='#', delim_whitespace=True, usecols=[0, 1, 2],
            parse_dates={'datetime': [0, 1]}, names=['date', 'time', 'rad'], header=0, index_col='datetime')
    dsi = pd.read_table(
            os.path.join(fol_input_rad, 'DSI.txt'), comment='#', delim_whitespace=True, usecols=[0, 1, 2],
            parse_dates={'datetime': [0, 1]}, names=['date', 'time', 'rad'], header=0, index_col='datetime')
    rad_dsi_legacy.columns = ['datetime', 'rad']
    rad_dsi_legacy = rad_dsi_legacy.set_index('datetime')
    rad_dsi_legacy = rad_dsi_legacy * 1  # setting a value
    dsi_all = pd.concat([dsi, rad_dsi_legacy])
    dsi_all.sort_index()

    save_mask_txt(usi, 'rad_usi')
    save_mask_txt(uli, 'rad_uli')
    save_mask_txt(dli, 'rad_dli')
    save_mask_txt(dsi_all, 'rad_dsi')
