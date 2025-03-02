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

import os

import pandas as pd

import settings as ts
import single_instr_data_avail.sida_tools as sida_tls


def update_data_avail(instr):
    folder = os.path.join(ts.basefolder, "thaao_rad")
    date_list = pd.date_range(
            ts.instr_metadata[instr]['start_instr'], ts.instr_metadata[instr]['end_instr'], freq='Y').tolist()

    data_rad = pd.DataFrame()

    for i in date_list:
        try:
            data_tmp = read_rad(i.year, folder)
            data_rad = pd.concat([data_rad, data_tmp])
        except FileNotFoundError:
            continue

    sida_tls.save_csv(instr, data_rad[list(ts.instr_metadata[instr]['plot_vars'].keys())[0]])


def read_rad(year, fol):
    """
    Function for reading radiation data and formatting data strings.
    :param fol:
    :param year: (YYYY)
    :return: radiation data as DataFrame (pandas). Index is datetime and columns are: ['SZA', 'SW', 'LW', 'PAR', 'TB']
    """
    print('Reading RADIATION data for year ', str(year))
    file_rad = os.path.join(fol, 'MERGED_SW_LW_UP_DW_METEO_' + str(year) + '_5MIN.DAT')
    rad = pd.read_table(file_rad, skiprows=None, header=0, decimal='.', sep='\s+')

    rad.index = pd.DatetimeIndex(
            pd.to_datetime( str(year) + '-1-1') + pd.to_timedelta(rad['JDAY_UT'], unit='D'))
    rad.index.name = 'datetime'

    data = rad.drop(
            labels=['JDAY_UT', 'JDAY_LOC', 'SZA', 'ALBEDO_LW', 'ALBEDO_PAR', 'P', 'T', 'RH', 'PE', 'RR2'],
            axis=1)

    return data
