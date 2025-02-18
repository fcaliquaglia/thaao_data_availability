#!/usr/local/bin/python3
# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------------
#
"""
Optimized version without parallel processing.
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

instr = 'aws_vespa'


def update_data_avail(instr):
    import os
    import pandas as pd
    import single_instr_data_avail.tools as sida_tls

    import settings as ts
    # Create NetCDF file from all weekly files
    date_list = pd.date_range(
            ts.instr_metadata[instr]['start_instr'], ts.instr_metadata[instr]['end_instr'], freq='h').tolist()
    folder = os.path.join(ts.basefolder, "thaao_" + instr)

    create_netcdf_file(folder)

    # Load the NetCDF dataset and save the data to text file
    all_weekly = xr.open_dataset(os.path.join(folder, 'Meteo_weekly_all.nc'))
    sida_tls.save_mask_txt(all_weekly['Air_K'].to_dataframe(), folder, instr)


def read_and_process_file(f):
    """Reads a file, processes it, and returns the processed DataFrame."""
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
    return file


def create_netcdf_file(fol):
    """Merge all weekly files and save them as a single NetCDF file."""
    ls_f = glob.glob(os.path.join(fol, 'weekly', 'DatiMeteoThule*'))

    # Initialize a list to hold all processed DataFrames
    all_files = []

    for f in ls_f:
        print(f)
        # Read and process each file, adding it to the list
        processed_file = read_and_process_file(f)
        all_files.append(processed_file)

    # Combine all processed files into one DataFrame
    all_weekly = pd.concat(all_files)
    all_weekly.sort_index(inplace=True)
    all_weekly = all_weekly[~all_weekly.index.duplicated(keep='first')]

    # Convert to xarray and save as NetCDF
    all_weekly_xr = all_weekly.to_xarray()
    all_weekly_xr.to_netcdf(os.path.join(fol, 'Meteo_weekly_all.nc'))
