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
import tools as tls

import settings as ts

instr = 'meteo'
folder = os.path.join(ts.basefolder, "thaao_" + instr)

if __name__ == "__main__":

    start = dt.datetime(2016, 3, 8, 0, 0, 0)
    days = 2000

    # merge together all the weekly files from Giovanni
    import glob

    ls_f = glob.glob(os.path.join(folder, 'weekly', 'DatiMeteoThule*'))
    all_weekly = pd.DataFrame()
    for f in ls_f:
        print(f)
        try:
            file = pd.read_table(f, skiprows=4, header=None, delimiter=',')
            file[2] *= 10  # conversion to hPa
            file.columns = ["TIMESTAMP", "RECORD", "BP_hPa", "Air_K", "RH_%", "Angle_X", "Angle_Y"]
            file.index = pd.DatetimeIndex(file['TIMESTAMP'])
            file.drop(columns=["RECORD", "TIMESTAMP", "Angle_X", "Angle_Y"], inplace=True)
        except ValueError:
            file = pd.read_table(f, skiprows=4, header=None, delimiter=',')
            file[2] *= 10  # conversion to hPa
            file.columns = ["TIMESTAMP", "RECORD", "BP_hPa", "Air_K", "RH_%"]
            file.index = pd.DatetimeIndex(file['TIMESTAMP'])
            file.drop(columns=["RECORD", "TIMESTAMP"], inplace=True)

        all_weekly = pd.concat([all_weekly, file])

    all_weekly.sort_index(inplace=True)
    all_weekly = all_weekly[~all_weekly.index.duplicated(keep='first')]
    all_weekly_xr = all_weekly.to_xarray()
    all_weekly_xr.to_netcdf(os.path.join(folder, 'Meteo_weekly_all.nc'))

    tls.save_mask_txt(all_weekly['Air_K'], folder, 'aws_vespa')
