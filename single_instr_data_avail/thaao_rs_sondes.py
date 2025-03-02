#!/usr/local/bin/python3
# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------------
"""
OK
Reading and plotting data from EDT radiosounding.
ATTENTION! Before plotting data you need to format the data file using the script
C:\\Users\\FCQ\\iCloudDrive\\Documents\\bin\\thaao_rs_raw\\rs_1_convert_2022-on.py -- from 2022 onward
C:\\Users\\FCQ\\iCloudDrive\\Documents\\bin\\thaao_rs_raw\\rs_1_convert_2021.py -- for 2021
C:\\Users\\FCQ\\iCloudDrive\\Documents\\bin\\thaao_rs_raw\\rs_1_convert_2005-2020.py -- from 2006 to 2020
C:\\Users\\FCQ\\iCloudDrive\\Documents\\bin\\thaao_rs_raw\\rs_1_convert_wyo.py -- from 1973 to 2005
"""
#
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
from metpy.calc import dewpoint_from_relative_humidity, precipitable_water
from metpy.units import units

import settings as ts
import datetime as dt
import single_instr_data_avail.sida_tools as sida_tls


def convert_rs_to_iwv(df, tp):
    """
    Convertito concettualmente in python da codice di Giovanni: PWV_Gio.m
    :param tp: % of the max pressure value up to which calculate the iwv. it is necessary because interpolation fails.
    :param df:
    :return:
    """

    td = dewpoint_from_relative_humidity(
            df['temp'].to_xarray() * units("degC"), df['rh'].to_xarray() / 100)
    iwv = precipitable_water(
            df['pres'].to_xarray() * units("hPa"), td, bottom=None, top=np.nanmin(df['pres']) * tp * units('hPa'))

    return iwv


def update_data_avail(instr):
    date_list = pd.date_range(
            ts.instr_metadata[instr]['start_instr'], ts.instr_metadata[instr]['end_instr'], freq='Y').tolist()
    folder = os.path.join(ts.basefolder, "thaao_" + instr, 'txt')

    rs_sondes = pd.DataFrame()
    for yy, date in enumerate(date_list):
        try:
            fol_input = os.path.join(folder, f'{date.year}')
            file_l = os.listdir(fol_input)
            file_l.sort()
            for i in file_l:
                print(i)
                try:
                    file_date = dt.datetime.strptime(i[9:22], '%Y%m%d_%H%M')
                    kw = dict(
                            skiprows=17, skipfooter=1, header=None, delimiter=" ", na_values="nan", na_filter=True,
                            skipinitialspace=False, decimal=".", names=['height', 'pres', 'temp', 'rh'],
                            engine='python', usecols=[0, 1, 2, 3])
                    dfs = pd.read_table(os.path.join(fol_input, i), **kw)
                    # unphysical values checks
                    dfs.loc[(dfs['pres'] > 1013) | (dfs['pres'] < 0), 'pres'] = np.nan
                    dfs.loc[(dfs['height'] < 0), 'height'] = np.nan
                    dfs.loc[(dfs['temp'] < -100) | (dfs['temp'] > 30), 'temp'] = np.nan
                    dfs.loc[(dfs['rh'] < 1.) | (dfs['rh'] > 120), 'rh'] = np.nan
                    dfs.dropna(subset=['temp', 'pres', 'rh'], inplace=True)
                    dfs.drop_duplicates(subset=['height'], inplace=True)
                    # min_pres_ind exclude values recorded during descent
                    min_pres = np.nanmin(dfs['pres'])
                    min_pres_ind = np.nanmin(np.where(dfs['pres'] == min_pres)[0])
                    dfs1 = dfs.iloc[:min_pres_ind]
                    dfs2 = dfs1.set_index(['height'])
                    rs_iwv = convert_rs_to_iwv(dfs2, 1.01)
                    t2_tmp = pd.DataFrame(index=pd.DatetimeIndex([file_date]), data=[rs_iwv.magnitude])
                    rs_sondes = pd.concat([rs_sondes, t2_tmp], axis=0)
                except ValueError:
                    print('issue with ' + i)
            print(f'OK: year {date.year}')
        except FileNotFoundError:
            print(f'NOT FOUND: year {date.year}')
    rs_sondes.columns = ['iwv']

    sida_tls.save_csv(instr, rs_sondes)
