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

import glob
import os

import numpy as np
import pandas as pd
import xarray as xr

import settings as ts
import single_instr_data_avail.sida_tools as sida_tls


def update_data_avail(instr):
    folder = os.path.join(ts.basefolder, 'thaao_' + instr)

    filenames = glob.glob(os.path.join(folder, "th*"))

    varname = ['Ozone partial pressure']  # , 'Scattering ratio for red channel', 'Scattering ratio for blue channel']
    vert_var = ['Geopotential height']
    aero_sondes = []
    for filename in filenames:
        try:
            aero_sondes_tmp = sida_tls.nasa_ames_parser_2110(filename, instr, vert_var=vert_var, varnames=varname)
            aero_sondes.append(aero_sondes_tmp)
        except:
            print(f'Error {filename}')
            continue

    aero_sondes_list_tmp = [item for sublist in aero_sondes for item in sublist]

    all_heights = np.unique(np.concatenate([ds.height_levels.values for ds in aero_sondes_list_tmp]))
    reindexed_datasets = [ds.reindex(height_levels=all_heights) for ds in aero_sondes_list_tmp]
    stacked_blocks = xr.concat(reindexed_datasets, dim='timestamps')
    stacked_blocks = stacked_blocks.sortby('timestamps')
    stacked_blocks.to_netcdf(os.path.join(folder, instr + '.nc'))

    height_targets = [15000, 20000, 25000]  # Altitude in meters
    # Create an empty DataFrame to store results (with timestamps as the index)
    data = pd.DataFrame()

    for height_target in height_targets:
        try:
            # Loop over each timestamp in the data
            for timestamp in stacked_blocks.timestamps.values:
                # Select the data for the current timestamp
                data_at_timestamp = stacked_blocks.sel(timestamps=timestamp)

                # Mask out NaN values along the 'height_levels' dimension
                data_at_timestamp_non_nan = data_at_timestamp.where(~np.isnan(data_at_timestamp), drop=True)

                if not data_at_timestamp_non_nan.isnull().all():
                    # Select the nearest value at the specified height
                    data_sel = data_at_timestamp_non_nan.sel(
                            height_levels=height_target, method="nearest", tolerance=100)

                    # Ensure the selected data is a single value
                    if not data_sel.isnull():
                        # Extract the scalar value from data_sel (it's a single value)
                        ozone_value = data_sel.values

                        # Get the timestamp and height_level (these are already in data_sel's coordinates)
                        timestamp = data_sel.timestamps.values

                        # Create a DataFrame with the ozone value and timestamp
                        data_sel_df = pd.DataFrame(
                                {f'Ozone partial pressure_at_{height_target}m': [ozone_value]},
                                index=[pd.to_datetime(timestamp, unit='s')]  # Convert timestamp to datetime
                        )
                        data = pd.concat([data_sel_df, data])
            # Convert the index to datetime (if needed)
            data.index = pd.to_datetime(data.index, unit="s")
        except Exception as e:
            print(f"Error extracting ozone at {height_target}m: {e}")

    # Save the data to a CSV or further processing
    data = data.drop_duplicates(keep='first')
    data.sort_index(inplace=True)
    sida_tls.save_csv(instr, data)
