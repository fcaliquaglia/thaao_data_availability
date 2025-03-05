#!/usr/local/bin/python3
# -*- coding: utf-8 -*-


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
from pathlib import Path

import numpy as np
import pandas as pd
import xarray as xr

import settings as ts


def update_data_avail(instr):
    """
    Updates the availability of LIDAR temperature data by checking for existing
    zip files and matching file patterns in the specified directory.
    """

    folder = Path(ts.basefolder) / f"thaao_{instr}"

    filenames = glob.glob(os.path.join(folder, "thte*"))

    lidar_temp = []
    for filename in filenames[0:10]:
        try:
            lidar_temp_tmp = nasa_ames_parser_2110(filename)
            lidar_temp.append(lidar_temp_tmp)
        except:
            print(filename)
            continue

    lidar_temp_list_tmp = [item for sublist in lidar_temp for item in sublist]
    # lidar_temp_list = [elem.sel(pressure_levels=~elem.coords['pressure_levels'].duplicated()) for elem in lidar_temp_list_tmp]

    stacked_blocks = xr.concat(lidar_temp_list_tmp, dim='timestamps')
    stacked_blocks.to_netcdf(os.path.join(ts.basefolder, 'thaao_lidar_temp', 'test.nc'))

    # Save the DataFrame using sida_tls module  # sida_tls.save_csv(instr, lidar_temp)


def nasa_ames_parser_2110(fn):
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
        line_parts = metadata[next_start].split('(')
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
        line_parts = metadata[next_start].split('(')
        extra_vars.append(line_parts[0].strip())
        extra_units.append(line_parts[1].strip()[:-1] if len(line_parts) > 1 else np.nan)
        next_start += 1

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
            print(f'this is a new block at line: {i}')
            block_metadata = {key: value for key, value in zip([independent_vars[1]] + extra_vars, elements)}
            print(block_metadata['Day'] + ' ' + block_metadata['Month'] + ' ' + block_metadata['Year'])
            new_date = dt.datetime.strptime(
                    block_metadata['Year'] + block_metadata['Month'] + block_metadata['Day'] + block_metadata['Hour'] +
                    block_metadata['Minutes'], '%Y%m%d%H%M')
            block_metadata['datetime'] = new_date

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

            timestamps = np.array(pd.to_datetime([block_metadata['datetime']]))  # Ensure a single timestamp per block
            height_levels = data_block_fmt[:, 0]
            pressure_levels = data_block_fmt[:, 3]
            # Create an empty temperature array with shape (102, 102)

            height_levels = np.unique(data_block_fmt[:, 0])  # Unique height levels (should be 102)
            pressure_levels = np.unique(data_block_fmt[:, 3])  # Unique pressure levels (should be 102)

            print(f"Height levels: {len(height_levels)}, Pressure levels: {len(pressure_levels)}")
            temperature_grid = np.full((len(height_levels), len(pressure_levels)), np.nan)

            # Populate the grid by matching height and pressure levels
            for row in data_block_fmt:
                height = row[0]  # Height value
                pressure = row[3]  # Pressure value
                temp_value = row[5]  # Temperature value

                # Find the correct index for height and pressure
                height_idx = np.where(height_levels == height)[0][0]
                pressure_idx = np.where(pressure_levels == pressure)[0][0]

                # Assign temperature to correct position
                temperature_grid[height_idx, pressure_idx] = temp_value
            temperatures = temperature_grid.reshape(1, len(height_levels), len(pressure_levels))

            temp = xr.DataArray(
                    temperatures, coords={"timestamps"     : timestamps, "height_levels": height_levels,
                                          "pressure_levels": pressure_levels},
                    dims=["timestamps", "height_levels", "pressure_levels"], name="temperatures")

            # Attach the metadata as attributes to the DataArray
            keys_to_keep = ['Altitude of aperture of the mechanical shutter', 'Latitude', 'Longitude',
                            'Laser wavelength']  # List of keys to keep

            # Remove all keys not in keys_to_keep
            for key in list(block_metadata.keys()):  # Convert to list to avoid modifying the dictionary while iterating
                if key not in keys_to_keep:
                    del block_metadata[key]

            temp.attrs = block_metadata

            # Add the xarray to the list of all blocks
            all_blocks.append(temp)

    # Stack all blocks into a single xarray (assuming you want a single xarray with multiple blocks)
    return all_blocks

    import matplotlib.pyplot as plt
    plt.figure(figsize=(10, 6))
    temp_da = stacked_blocks.transpose("timestamps", "height_levels")
    stacked_blocks.plot(
            x="timestamps", y="height_levels", cmap="coolwarm", cbar_kwargs={"label": "Temperature (K)"})
    plt.title("Vertical Temperature Profiles (Contour)")
    plt.xlabel("Time")
    plt.ylabel("Height (m)")
    plt.show()

    # Apply multipliers
    for col in df.columns:
        df[col] *= metadata_dict[col]['mult']

    df.set_index('datetime', inplace=True)
    lidar_temp = pd.concat([lidar_temp, df])

    lidar_temp = lidar_temp.sort_index()

    return lidar_temp
