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

import datetime as dt
import glob
import os

import numpy as np
import pandas as pd
import xarray as xr

import settings as ts


def update_data_avail(instr):
    date_list = pd.date_range(
            ts.instr_metadata[instr]['start_instr'], ts.instr_metadata[instr]['end_instr'], freq='ME').tolist()
    folder = os.path.join(ts.basefolder, "thaao_" + instr)

    filenames = glob.glob(os.path.join(folder, "thae*"))
    varname = 'Aerosol backscattering coefficient'
    lidar_temp = []
    for filename in filenames:
        try:

            lidar_temp_tmp = nasa_ames_parser_2110(filename, instr, varname=varname)
            lidar_temp.append(lidar_temp_tmp)
        except:
            print(f'Error {filename}')
            continue

    lidar_temp_list_tmp = [item for sublist in lidar_temp for item in sublist]

    stacked_blocks = xr.concat(lidar_temp_list_tmp, dim='timestamps')
    stacked_blocks = stacked_blocks.sortby('timestamps')
    stacked_blocks.to_netcdf(os.path.join(folder, instr + '.nc'))

    import matplotlib.pyplot as plt

    # Ensure that timestamps are in datetime format
    stacked_blocks["timestamps"] = pd.to_datetime(stacked_blocks["timestamps"], unit="s", origin="1970-01-01")

    # Filter data for the specific date range (September 1991 to February 1996)
    start_date = "1991-09-01"
    end_date = "1996-02-28"
    stacked_blocks_filtered = stacked_blocks.sel(timestamps=slice(start_date, end_date))

    # Resample data by month and compute the monthly averages
    stacked_blocks_monthly_avg = stacked_blocks_filtered.resample(timestamps="1MS").mean()  # '1MS' means monthly start

    plt.figure(figsize=(10, 6))
    stacked_blocks_monthly_avg.plot(
            x="timestamps", y="height_levels", cmap="coolwarm", cbar_kwargs={"label": "Aerosols "}, vmin=1e-7,
            vmax=7.35e-7)

    plt.title("Vertical AE Profiles - Monthly Averages (Sept 1991 - Feb 1996) - di Sarra et al., 1998")
    plt.xlabel("Time")
    plt.ylabel("Height (m)")
    plt.ylim(5000, 25000)
    plt.savefig(os.path.join(folder, 'disarraetal1998.png'))


# import numpy as np
# import pandas as pd
# import datetime as dt
# import xarray as xr
#
#
# import numpy as np
# import pandas as pd
# import datetime as dt
# import xarray as xr
#
# def nasa_ames_parser_2110(fn, instr, varname):
#     try:
#         with open(fn, 'r') as file:
#             lines = file.readlines()[1:]  # Skip the first line
#     except Exception as e:
#         print(f"Error reading file {fn}: {e}")
#         return []
#
#     try:
#         # Identify number of header lines to skip
#         data_start = int(lines[0].split()[0])
#         metadata = lines[:data_start]
#     except Exception as e:
#         print(f"Error parsing header lines: {e}")
#         return []
#
#     try:
#         # Extract independent variable count and metadata
#         num_independent_vars = len(metadata[5].split())
#         independent_vars = [metadata[8 + i].strip() for i in range(num_independent_vars)]
#     except Exception as e:
#         print(f"Error extracting independent variables: {e}")
#         return []
#
#     try:
#         # Extract dependent variable metadata
#         next_start = 8 + num_independent_vars
#         dependent_mult = list(map(float, metadata[next_start + 1].split()))
#         dependent_nan = list(map(float, metadata[next_start + 2].split()))
#
#         num_dependent_vars = int(metadata[next_start].strip())
#         dependent_vars, dependent_units = [], []
#
#         next_start += 3
#         for _ in range(num_dependent_vars):
#             line_parts = metadata[next_start].strip().replace(';', '(').split('(')
#             dependent_vars.append(line_parts[0].strip())
#             dependent_units.append(line_parts[1].strip()[:-1] if len(line_parts) > 1 else np.nan)
#             next_start += 1
#     except Exception as e:
#         print(f"Error extracting dependent variables: {e}")
#         return []
#
#     try:
#         # Extract extra variables metadata
#         num_extra_vars = int(metadata[next_start].split()[0])
#         extra_mult = list(map(float, metadata[next_start + 1].split()))
#         extra_nan = list(map(float, metadata[next_start + 2].split()))
#
#         extra_vars, extra_units = [], []
#         next_start += 3
#         for _ in range(num_extra_vars):
#             line_parts = metadata[next_start].strip().replace(';', '(').split('(')
#             extra_vars.append(line_parts[0].strip())
#             extra_units.append(line_parts[1].strip()[:-1] if len(line_parts) > 1 else np.nan)
#             next_start += 1
#     except Exception as e:
#         print(f"Error extracting extra variables: {e}")
#         return []
#
#     try:
#         # Extract comment lines
#         nr_comment_lines = int(metadata[next_start + 1].strip())
#         comment_lines = metadata[next_start + 2:next_start + 2 + nr_comment_lines]
#     except Exception as e:
#         print(f"Error extracting comment lines: {e}")
#         return []
#
#     try:
#         # Check metadata consistency
#         if not (len(dependent_nan) == len(dependent_mult) == len(dependent_units)):
#             raise ValueError("Mismatch in dependent variable metadata lengths.")
#         if not (len(extra_vars) == len(extra_mult) == len(extra_nan)):
#             raise ValueError("Mismatch in extra variable metadata lengths.")
#
#         # Create metadata dictionary
#         metadata_dict = {
#             var: {'mult': mult, 'nanval': nan, 'uom': uom}
#             for var, mult, nan, uom in zip(dependent_vars, dependent_mult, dependent_nan, dependent_units)
#         }
#         metadata_dict.update({
#             var: {'mult': mult, 'nanval': nan}
#             for var, mult, nan in zip(extra_vars, extra_mult, extra_nan)
#         })
#     except Exception as e:
#         print(f"Error in metadata dictionary creation: {e}")
#         return []
#
#     all_blocks = []
#     lines_data = lines[data_start:]
#
#     try:
#         i = 0
#         while i < len(lines_data) - 1:
#             try:
#                 elements = np.array(lines_data[i].split(), dtype=float)
#                 elements1 = np.array(lines_data[i + 1].split(), dtype=float)
#             except Exception as e:
#                 print(f"Error parsing line {i}: {e}")
#                 i += 1
#                 continue
#
#             if len(elements) == num_extra_vars + 1 and len(elements1) == num_dependent_vars + 1:
#                 try:
#                     elements[elements == extra_nan] = np.nan
#                     elements *= np.array([1] + extra_mult)
#
#                     block_metadata = dict(zip([independent_vars[1]] + extra_vars, elements))
#
#                     new_date = dt.datetime.strptime(
#                         f"{int(block_metadata['Year']):04d}{int(block_metadata['Month']):02d}"
#                         f"{int(block_metadata['Day']):02d}{int(block_metadata['Hour']):02d}"
#                         f"{int(block_metadata['Minutes']):02d}", '%Y%m%d%H%M'
#                     )
#                     block_metadata['datetime'] = new_date
#                 except Exception as e:
#                     print(f"Error processing metadata at line {i}: {e}")
#                     i += 1
#                     continue
#
#                 try:
#                     j = 1
#                     while i + 1 + j < len(lines_data) and len(lines_data[i + 1 + j].split()) == num_dependent_vars + 1:
#                         j += 1
#                 except Exception as e:
#                     print(f"Error finding data block end at line {i}: {e}")
#                     i += j
#                     continue
#
#                 try:
#                     data_block = np.array([line.split() for line in lines_data[i + 1:i + j]], dtype=float)
#                     data_block[data_block == dependent_nan] = np.nan
#                     data_block *= np.array([1] + dependent_mult)
#
#                     timestamps = pd.to_datetime([block_metadata['datetime']])
#                     reference_time = pd.Timestamp('1970-01-01 00:00:00')
#                     time_diff_in_seconds = np.array((timestamps - reference_time).total_seconds())
#
#                     height_levels = np.unique(data_block[:, 0])
#                     data_grid = np.full(len(height_levels), np.nan)
#
#                     for row in data_block:
#                         height_idx = np.where(height_levels == row[0])[0][0]
#                         data_grid[height_idx] = row[dependent_vars.index(varname) + 1]
#
#                     temp = xr.DataArray(
#                         data_grid.reshape(1, -1),
#                         coords={"timestamps": time_diff_in_seconds, "height_levels": height_levels},
#                         dims=["timestamps", "height_levels"],
#                         name='data'
#                     )
#
#                     temp.coords["timestamps"].attrs["units"] = "seconds since 1970-01-01 00:00:00"
#                     temp = temp.sortby("height_levels").sortby("timestamps")
#
#                     keys_to_keep = {
#                         'lidar_ae': ['Altitude of aperture of the mechanical shutter', 'Averaging time of presented data',
#                                      'Latitude', 'Longitude', 'Laser wavelength'],
#                         'lidar_temp': ['Altitude of aperture of the mechanical shutter', 'Latitude', 'Longitude',
#                                        'Laser wavelength']
#                     }.get(instr, [])
#
#                     block_metadata = {key: block_metadata[key] for key in keys_to_keep if key in block_metadata}
#                     temp.attrs = block_metadata
#                     all_blocks.append(temp)
#                 except Exception as e:
#                     print(f"Error processing data block at line {i}: {e}")
#
#                 i += j  # Skip processed lines
#             else:
#                 i += 1
#     except Exception as e:
#         print(f"Unexpected error in main loop: {e}")
#         return []
#
#     return all_blocks


def nasa_ames_parser_2110(fn, instr, varname):
    with open(fn, 'r') as file:
        lines = file.readlines()
        lines = lines[1:]

    # Identify number of header lines to skip (first element in line 1)
    lines_to_skip = int(lines[0].split()[0])
    data_start = lines_to_skip
    metadata = lines[:data_start]

    # Extract independent variable count for 2110 format
    num_independent_vars = len(metadata[5].split())

    # Extract independent variable metadata
    independent_vars = []
    next_start = 8

    dependent_mult = []
    dependent_nan = []
    dependent_mult.extend([float(x) for x in metadata[next_start + 1 + num_independent_vars].strip().split()])
    dependent_nan.extend([float(x) for x in metadata[next_start + 2 + num_independent_vars].strip().split()])
    for _ in range(num_independent_vars):
        independent_vars.append(metadata[next_start].strip())
        next_start += 1

    # Extract dependent variables metadata
    num_dependent_vars = int(metadata[next_start].strip())
    dependent_vars = []
    dependent_units = []

    next_start += 3
    for _ in range(num_dependent_vars):
        if '(' in metadata[next_start]:
            line_parts = metadata[next_start].strip().split('(')
        if ';' in metadata[next_start]:
            line_parts = metadata[next_start].strip().split(';')
        dependent_vars.append(line_parts[0].strip())
        dependent_units.append(line_parts[1].strip()[:-1] if len(line_parts) > 1 else np.nan)
        next_start += 1

    num_extra_vars = int(metadata[next_start].split()[0])
    extra_vars = []
    extra_units = []
    extra_mult = [float(x) for x in metadata[next_start + 1].split()]
    extra_nan = [float(x) for x in metadata[next_start + 2].split()]

    next_start += 3
    for _ in range(num_extra_vars):
        if '(' in metadata[next_start]:
            line_parts = metadata[next_start].strip().split('(')
        if ';' in metadata[next_start]:
            line_parts = metadata[next_start].strip().split(';')
        extra_vars.append(line_parts[0].strip())
        extra_units.append(line_parts[1].strip()[:-1] if len(line_parts) > 1 else np.nan)
        next_start += 1

    nr_comment_lines = int(metadata[next_start + 1].strip())
    comment_lines = metadata[next_start + 2:next_start + 2 + nr_comment_lines]

    # Check metadata consistency
    if not (len(dependent_nan) == len(dependent_mult) == len(dependent_units)):
        print('Error in independent variable metadata')
    if not (len(extra_vars) == len(extra_mult) == len(extra_nan)):
        print('Error in dependent variable metadata')

    # Create metadata dictionary
    metadata_dict = {var: {'mult': mult, 'nanval': nan} for var, mult, nan in zip(extra_vars, extra_mult, extra_nan)}
    metadata_dict.update(
            {var: {'mult': mult, 'nanval': nan, 'uom': uom} for var, mult, nan, uom in
             zip(dependent_vars, dependent_mult, dependent_nan, dependent_units)})

    all_blocks = []
    for i, _ in enumerate(lines[data_start:-1]):
        # Split the line by spaces and filter out empty strings
        elements = list(filter(None, lines[data_start:][i].strip().split()))
        elements1 = list(filter(None, lines[data_start:][i + 1].strip().split()))

        # If the row has more than a threshold number of elements, it's a new block
        if (len(elements) == num_extra_vars + 1) & (len(elements1) == num_dependent_vars + 1):
            try:
                elements = np.array(elements).astype(float)
                elements[np.isin(elements, np.array([np.nan] + extra_nan))] = np.nan
                elements *= np.array([1] + extra_mult)  # applying multiplication factors

                block_metadata = {key: value for key, value in zip([independent_vars[1]] + extra_vars, elements)}
                if block_metadata['Hour'].astype(int) == 24:
                    block_metadata['Hour'] = 0
                    new_date = dt.datetime(
                            block_metadata['Year'].astype(int), block_metadata['Month'].astype(int),
                            block_metadata['Day'].astype(int), block_metadata['Hour'].astype(int),
                            block_metadata['Minutes'].astype(int)) + dt.timedelta(days=1)
                else:
                    new_date = dt.datetime(
                            block_metadata['Year'].astype(int), block_metadata['Month'].astype(int),
                            block_metadata['Day'].astype(int), block_metadata['Hour'].astype(int),
                            block_metadata['Minutes'].astype(int))
                print(new_date)
                block_metadata['datetime'] = new_date
            except:
                print('errror')
            j = 1
            elements1 = list(filter(None, lines[data_start:][i + 1].strip().split()))
            while len(elements1) == num_dependent_vars + 1:
                try:
                    elements1 = list(filter(None, lines[data_start:][i + 1 + j].strip().split()))
                    j += 1
                except IndexError:
                    j -= 1
                    break

            data_block = lines[data_start:][i + 1:i + j]
            data_block_fmt = []
            [data_block_fmt.append(list(filter(None, data_block[k].strip().split()))) for k in range(len(data_block))]
            data_block_fmt = np.array(data_block_fmt).astype(float)
            data_block_fmt[np.isin(data_block_fmt, np.array([np.nan] + dependent_nan))] = np.nan
            data_block_fmt *= np.array([1] + dependent_mult)  # applying multiplication factors
            timestamps = pd.to_datetime([block_metadata['datetime']])  # Ensure a single timestamp per block
            # Define the correct reference time (e.g., "1970-01-01 00:00:00")
            reference_time = pd.Timestamp('1970-01-01 00:00:00')
            # Calculate the time difference in seconds since the reference time
            time_diff_in_seconds = np.array((timestamps - reference_time).total_seconds())

            height_levels = np.unique(data_block_fmt[:, 0])
            # pressure_levels = np.unique(data_block_fmt[:, 3])  # Unique pressure levels (should be 102)
            # temperature_grid = np.full((len(height_levels), len(pressure_levels)), np.nan)
            data_grid = np.full((len(height_levels)), np.nan)

            # Populate the grid by matching height and pressure levels
            for row in data_block_fmt:
                height = row[0]  # Height value
                # pressure = row[3]  # Pressure value
                temp_value = row[dependent_vars.index(varname) + 1]  # Temperature value

                # Find the correct index for height and pressure
                height_idx = np.where(height_levels == height)[0][0]
                # pressure_idx = np.where(pressure_levels == pressure)[0][0]

                # Assign temperature to correct position
                data_grid[height_idx] = temp_value  # temperature_grid[height_idx, pressure_idx] = temp_value
            data = data_grid.reshape(1, len(height_levels))
            # temperatures = temperature_grid.reshape(1, len(height_levels), len(pressure_levels))

            temp = xr.DataArray(
                    data, coords={"timestamps": time_diff_in_seconds, "height_levels": height_levels},
                    dims=["timestamps", "height_levels"], name='data')

            temp.coords["timestamps"].attrs[
                "units"] = "seconds since 1970-01-01 00:00:00"  # Adjust this to your preferred format

            temp = temp.sortby("height_levels")
            temp = temp.sortby("timestamps")

            # Attach the metadata as attributes to the DataArray
            if instr == 'lidar_ae':
                keys_to_keep = ['Altitude of aperture of the mechanical shutter', 'Averaging time of presented data',
                                'Latitude', 'Longitude', 'Laser wavelength']  # List of keys to keep
            if instr == 'lidar_temp':
                keys_to_keep = ['Altitude of aperture of the mechanical shutter', 'Latitude', 'Longitude',
                                'Laser wavelength']  # List of keys to keep

            # Remove all keys not in keys_to_keep
            for key in list(block_metadata.keys()):  # Convert to list to avoid modifying the dictionary while iterating
                if key not in keys_to_keep:
                    del block_metadata[key]

            temp.attrs = block_metadata

            # Add the xarray to the list of all blocks
            all_blocks.append(temp)

    return all_blocks
