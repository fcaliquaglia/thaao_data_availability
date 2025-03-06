#!/usr/local/bin/python3
# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------------
#
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

import os
import glob

import pandas as pd
import xarray as xr

import settings as ts
import single_instr_data_avail.sida_tools as sida_tls


def update_data_avail(instr):
    folder = os.path.join(ts.basefolder, 'thaao_' + instr)

    filenames = glob.glob(os.path.join(folder, "th*"))

    varname = ['Ozone partial pressure']  # , 'Scattering ratio for red channel', 'Scattering ratio for blue channel']
    aero_sondes = []
    for filename in filenames:
        try:
            aero_sondes_tmp = sida_tls.nasa_ames_parser_2110(filename, instr, varnames=varname)
            aero_sondes.append(aero_sondes_tmp)
        except:
            print(f'Error {filename}')
            continue

    aero_sondes_list_tmp = [item for sublist in aero_sondes for item in sublist]

    stacked_blocks = xr.concat(aero_sondes_list_tmp, dim='timestamps')
    stacked_blocks = stacked_blocks.sortby('timestamps')
    stacked_blocks.to_netcdf(os.path.join(folder, instr + '.nc'))

    altitude_targets = [15000, 20000, 25000]  # Altitude in meters
    data = pd.DataFrame()
    for altitude_target in altitude_targets:
        try:
            data_sel = stacked_blocks.sel(height_levels=altitude_target, method="nearest")
        except Exception as e:
            print(f"Error extracting ozone at {altitude_target}m: {e}")
        data_sel = data_sel.to_dataframe()
        data_sel.columns = ['height_levels', f'Ozone partial pressure_at_{altitude_target}m']
        data = pd.concat([data, data_sel[f'Ozone partial pressure_at_{altitude_target}m']], axis=0)
    data.index = pd.to_datetime(data.index, unit="s")
    sida_tls.save_csv(instr, data)
