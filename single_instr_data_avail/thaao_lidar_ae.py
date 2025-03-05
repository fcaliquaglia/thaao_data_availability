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

import glob
import os

import pandas as pd
import xarray as xr

import settings as ts
import single_instr_data_avail.sida_tools as sida_tls


def update_data_avail(instr):
    folder = os.path.join(ts.basefolder, "thaao_" + instr)

    filenames = glob.glob(os.path.join(folder, "thae*"))
    varname = ['Aerosol backscattering coefficient',
               'Backscattering coefficient']  # multiple for differnt names in files
    # varname = 'Backscatter ratio'
    lidar_ae = []
    for filename in filenames:
        try:
            lidar_ae_tmp = sida_tls.nasa_ames_parser_2110(filename, instr, varnames=varname)
            lidar_ae.append(lidar_ae_tmp)
        except FileNotFoundError:
            print(f'Error {filename}')
            continue

    lidar_ae_list_tmp = [item for sublist in lidar_ae for item in sublist]

    stacked_blocks = xr.concat(lidar_ae_list_tmp, dim='timestamps')
    stacked_blocks = stacked_blocks.sortby('timestamps')
    stacked_blocks.to_netcdf(os.path.join(folder, instr + '.nc'))

    altitude_target = 25000  # Altitude in meters

    try:
        # Select the closest altitude level to 25000m
        data_sel = stacked_blocks.sel(height_levels=altitude_target, method="nearest")
    except Exception as e:
        print(f"Error extracting temperature at {altitude_target}m: {e}")
    sida_tls.save_csv(instr, data_sel.to_dataframe())

    import matplotlib.pyplot as plt

    # Ensure that timestamps are in datetime format
    stacked_blocks["timestamps"] = pd.to_datetime(stacked_blocks["timestamps"], unit="s", origin="1970-01-01")

    # stacked_blocks_filtered = stacked_blocks.sel(timestamps=slice(start_date, end_date))

    # Resample data by month and compute the monthly averages
    stacked_blocks_monthly_avg = stacked_blocks.resample(timestamps="ME").mean()  # '1MS' means monthly start

    plt.figure(figsize=(10, 6))
    stacked_blocks_monthly_avg.plot(
            x="timestamps", y="height_levels", cmap="coolwarm", cbar_kwargs={"label": "Aerosols "}, vmin=1e-7,
            vmax=7.35e-7)

    plt.title("Vertical AE Profiles - Monthly Averages (Sept 1991 - Feb 1996) - di Sarra et al., 1998")
    plt.xlabel("Time")
    plt.ylabel("Height (m)")
    plt.savefig(os.path.join(folder, 'disarraetal1998_7D.png'))
