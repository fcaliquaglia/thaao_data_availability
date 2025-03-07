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

import numpy as np
import pandas as pd
import xarray as xr

import settings as ts
import single_instr_data_avail.sida_tools as sida_tls


def update_data_avail(instr):
    folder = os.path.join(ts.basefolder, "thaao_" + instr)

    filenames = glob.glob(os.path.join(folder, "thae*"))
    varname = ['Aerosol backscattering coefficient',
               'Backscattering coefficient']  # multiple for differnt names in files
    vert_var = ['Geometric altitude', 'Altitude']
    # varname = 'Backscatter ratio'
    lidar_ae = []
    for filename in filenames:
        try:
            lidar_ae_tmp = sida_tls.nasa_ames_parser_2110(filename, instr, vert_var=vert_var, varnames=varname)
            lidar_ae.append(lidar_ae_tmp)
        except FileNotFoundError:
            print(f'Error {filename}')
            continue

    lidar_ae_list_tmp = [item for sublist in lidar_ae for item in sublist]

    stacked_blocks = xr.concat(lidar_ae_list_tmp, dim='timestamps')
    stacked_blocks = stacked_blocks.sortby('timestamps')
    stacked_blocks.to_netcdf(os.path.join(folder, instr + '.nc'))

    height_targets = [10000, 15000, 20000]  # Altitude in meters
    # Create an empty DataFrame to store results (with timestamps as the index)
    data = pd.DataFrame()

    # Loop through each height target
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

                        # Get the timestamp (this is already in data_sel's coordinates)
                        timestamp = data_sel.timestamps.values

                        # Convert the timestamp to datetime
                        timestamp = pd.to_datetime(timestamp, unit='s')

                        # Create a DataFrame with the ozone value for the specific height level and timestamp
                        data_sel_df = pd.DataFrame(
                                {f'backscatter_at_{height_target}m': [ozone_value]}, index=[timestamp]
                                # Use the timestamp as the index
                        )

                        # Check if the timestamp already exists in the DataFrame
                        if timestamp in data.index:
                            # If it exists, update the value in the corresponding column (don't add a new row)
                            data.loc[timestamp, f'backscatter_at_{height_target}m'] = ozone_value
                        else:
                            # Otherwise, add a new row with the value for that timestamp
                            data = pd.concat([data, data_sel_df])

            # Sort the DataFrame by index (timestamps) to ensure it's ordered
            data.sort_index(inplace=True)

        except Exception as e:
            print(f"Error extracting backscatter at {height_target}m: {e}")
