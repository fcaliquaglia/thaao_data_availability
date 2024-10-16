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

import pandas as pd

from utils import thaao_settings as ts

instr = 'macmap_tide_gauge'
date_list = pd.date_range(
        ts.instr_na_list[instr]['start_instr'], ts.instr_na_list[instr]['end_instr'], freq='D').tolist()
folder = os.path.join(ts.basefolder, "thaao_" + instr)

if __name__ == "__main__":

    dateparse = lambda x: dt.datetime.strptime(x, ' %d/%m/%Y')
    date_converted = pd.DataFrame()
    for i in date_list:
        try:
            fn = os.path.join(folder, "Thule_" + i.strftime('%y%m') + ".dat")
            list_file = pd.read_table(fn, sep='|', parse_dates={'datetime': [0]}, date_parser=dateparse)
            date_converted = pd.concat([date_converted, list_file['datetime'].drop_duplicates()])
        except FileNotFoundError:
            print('file ' + str(fn) + ' not found')

    macmap_tide_gauge = pd.DataFrame(columns=['dt', 'mask'])
    for i in date_list:
        if i.strftime('%Y-%m-%d') in pd.to_datetime(date_converted.values.flatten()):
            macmap_tide_gauge.loc[i] = [i, True]
    ts.save_txt(instr, macmap_tide_gauge)
