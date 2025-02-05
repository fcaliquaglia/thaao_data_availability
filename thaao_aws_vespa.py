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

import glob
import os

import pandas as pd
import xarray as xr

import settings as ts
import tools as tls

instr = 'aws_vespa'
date_list = pd.date_range(
        ts.instr_metadata[instr]['start_instr'], ts.instr_metadata[instr]['end_instr'], freq='h').tolist()
folder = os.path.join(ts.basefolder, "thaao_" + instr)


def create_netcdf_file():
    # merge together all the weekly files from Giovanni
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
    return


if __name__ == "__main__":
    # create netcdf file from all weekly files
    create_netcdf_file()

    all_weekly = xr.open_dataset(os.path.join(folder, 'Meteo_weekly_all.nc'))
    tls.save_mask_txt(all_weekly['Air_K'].to_dataframe(), folder, instr)
