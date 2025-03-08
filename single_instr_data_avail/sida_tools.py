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
__email__ = "filippo.caliquaglia@gmail.com"
__status__ = "Research"
__lastupdate__ = "February 2025"

import datetime as dt
import os
from datetime import timedelta
from pathlib import Path

import numpy as np
import pandas as pd
import xarray as xr

import settings as ts


def save_m_csv(data_val: pd.DataFrame, fol_out: str, instr_nm: str):
    """
    Saves a text file indicating the availability of data.

    :param data_val: Pandas DataFrame containing data values.
    :param fol_out: Output directory for saving the file.
    :param instr_nm: Instrument name for file naming.
    """

    # Ensure numeric data and round index to seconds
    data_val = data_val.apply(pd.to_numeric, errors='coerce')
    data_val.index = data_val.index.ceil('s').tz_localize(None)  # Remove microseconds

    # Create mask for valid data
    valid_mask = data_val.notnull().sum(axis=1) >= 1

    # Create output DataFrame
    out_file = pd.DataFrame({"timestamp": data_val.index.values, "valid_mask": valid_mask.values})

    # Save file
    output_path = Path(fol_out) / f"{instr_nm}_data_avail_list.csv"
    print(f"Saving: {output_path}")
    np.savetxt(output_path, out_file.values, fmt='%s')
    print(f"Saved: {output_path}")


def save_csv(instr_nm, data_val):
    """

    :param data_val:
    :param instr_nm:
    :return:
    """
    if instr_nm == 'skycam':
        fol_out = os.path.join(ts.basefolder_skycam, f'thaao_{instr_nm}')
    elif instr_nm in ['rad_dli', 'rad_dsi', 'rad_uli', 'rad_usi', 'rad_tbp', 'rad_alb', 'rad_par_up', 'rad_par_down']:
        fol_out = os.path.join(ts.basefolder, f'thaao_rad')
    else:
        fol_out = os.path.join(ts.basefolder, f'thaao_{instr_nm}')

    data_val = data_val.apply(lambda x: x.strip() if isinstance(x, str) else x)
    data_val = data_val.apply(pd.to_numeric, errors='coerce')
    print('Saving: ' + instr_nm)
    flt_fmt = '%.6e' if instr_nm in ['aero_sondes', 'uv-vis_spec', 'ftir', 'lidar_ae', 'o3_sondes'] else '%.2f'
    data_val.to_csv(
            os.path.join(fol_out, f'{instr_nm}_data_avail_list.csv'), sep=',', index=True, index_label='datetime',
            float_format=flt_fmt)
    print('Saved ' + str(os.path.join(fol_out, instr_nm + '_data_avail_list.csv')))
    return


def nasa_ames_parser_2160(fn, instr, vert_var, varnames):
    with open(fn, 'r') as file:
        lines = file.readlines()
        lines = lines[1:]

    # Identify number of header lines to skip (first element in line 1)
    lines_to_skip = int(lines[0].split()[0])
    data_start = lines_to_skip
    metadata = lines[:data_start]

    # Extract independent variable count for 2110 format
    num_independent_vars = len(metadata[5].split())
    datetime = dt.datetime(int(metadata[6].split()[0]), int(metadata[6].split()[1]), int(metadata[6].split()[2]))
    # Extract independent variable metadata
    independent_vars = []
    independent_uom = []
    next_start = 7 + num_independent_vars

    dependent_mult = []
    dependent_nan = []
    dependent_mult.extend([float(x) for x in metadata[next_start + 1 + num_independent_vars].strip().split()])
    dependent_nan.extend([float(x) for x in metadata[next_start + 2 + num_independent_vars].strip().split()])
    for _ in range(num_independent_vars):
        if '(' in metadata[next_start]:
            independent_vars.append(metadata[next_start].strip().split('(')[0].strip())
            independent_uom.append(metadata[next_start].strip().split('(')[1])
        else:
            independent_vars.append(metadata[next_start].strip())
            independent_uom.append(np.nan)
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
        dependent_vars.append(line_parts[0].strip().capitalize())
        dependent_units.append(line_parts[1].strip()[:-1] if len(line_parts) > 1 else np.nan)
        next_start += 1

    num_extra_vars = int(metadata[next_start].split()[0])
    skip = int(metadata[next_start + 1].split()[0])
    extra_vars = []
    extra_units = []
    extra_nan = []
    extra_mult = [float(x) for x in metadata[next_start + 2].split()]
    [extra_mult.append(1.) for i in range(skip)]
    while len(extra_nan) < num_extra_vars:
        extra_nan = extra_nan + [float(x) for x in metadata[next_start + 3].split()]
        next_start += 1

    next_start += 3 + skip
    for _ in range(num_extra_vars):
        if '(' in metadata[next_start]:
            line_parts = metadata[next_start].strip().split('(')
            extra_vars.append(line_parts[0].strip().capitalize())
            extra_units.append(line_parts[1].strip()[:-1] if len(line_parts) > 1 else np.nan)
        elif ';' in metadata[next_start]:
            line_parts = metadata[next_start].strip().split(';')
            extra_vars.append(line_parts[0].strip().capitalize())
            extra_units.append(line_parts[1].strip()[:-1] if len(line_parts) > 1 else np.nan)
        else:
            line_parts = metadata[next_start].strip()
            extra_vars.append(line_parts.strip().capitalize())
            extra_units.append(np.nan)

        next_start += 1

    comment_lines = []

    nr_comment_lines1 = int(metadata[next_start].strip())
    [comment_lines.append(elem.strip()) for elem in metadata[next_start + 1:next_start + 1 + nr_comment_lines]]

    next_start += 1 + nr_comment_lines1
    nr_comment_lines2 = int(metadata[next_start].strip())
    [comment_lines.append(elem.strip()) for elem in metadata[next_start + 1:next_start + 1 + nr_comment_lines]]
    next_start += 1 + nr_comment_lines2

    # Check metadata consistency
    if not (len(dependent_nan) == len(dependent_mult) == len(dependent_units) == len(dependent_vars)):
        print('Error in dependent variable metadata')
    if not (len(extra_vars) == len(extra_mult) == len(extra_nan) == len(extra_units)):
        print('Error in extra variable metadata')

    # Create metadata dictionary
    metadata_dict = {var: {'mult': mult, 'nanval': nan} for var, mult, nan in zip(extra_vars, extra_mult, extra_nan)}
    metadata_dict.update(
            {var: {'mult': mult, 'nanval': nan, 'uom': uom} for var, mult, nan, uom in
             zip(dependent_vars, dependent_mult, dependent_nan, dependent_units)})

    independent_vars_vals = lines[next_start].strip()

    extra_vars_vals = [independent_vars_vals]
    while len(extra_vars_vals) < num_extra_vars - skip + 1:
        extra_vars_vals += [float(x) for x in lines[next_start + 1].split()]
        next_start += 1

    while len(extra_vars_vals) < num_extra_vars + 1:
        extra_vars_vals += [lines[next_start + 1].strip()]
        next_start += 1

    # block_metadata = {key: value for key, value in zip([independent_vars[0]] + dependent_vars, elements)}
    extra_metadata = {key: value for key, value in zip([independent_vars[1]] + extra_vars, extra_vars_vals)}

    def cast_hour_to_datetime(dtt, decimal_hour):
        newdate = dtt.replace(hour=0, minute=0, second=0, microsecond=0)
        return newdate + timedelta(hours=decimal_hour)

    if instr in ['o3_sondes']:
        try:
            extra_metadata['datetime'] = cast_hour_to_datetime(datetime, extra_metadata['launch time'])
        except KeyError:
            extra_metadata['datetime'] = cast_hour_to_datetime(datetime, extra_metadata['Launch time'])

    data_start = next_start + 2

    timestamps = pd.to_datetime([extra_metadata['datetime']])  # Ensure a single timestamp per block
    # Define the correct reference time (e.g., "1970-01-01 00:00:00")
    reference_time = pd.Timestamp('1970-01-01 00:00:00')
    # Calculate the time difference in seconds since the reference time
    time_diff_in_seconds = np.array((timestamps - reference_time).total_seconds())

    try:
        vert_var_idx = ([independent_vars[0]] + dependent_vars).index(vert_var[0].capitalize())
    except ValueError:
        vert_var_idx = ([independent_vars[0]] + dependent_vars).index(vert_var[1].capitalize())
    data_grid = np.full((len(lines[data_start:])), np.nan)

    v_var_levels = []

    [v_var_levels.append(list(filter(None, lines[data_start:][k].strip().split()))) for k in
     range(len(lines[data_start:]))]
    v_var_levels = np.array(v_var_levels).astype(float)

    for row in lines[data_start:]:
        el = row.strip().split()
        elements = np.array(el).astype(float)
        elements[np.isin(elements, np.array([np.nan] + dependent_nan))] = np.nan
        elements *= np.array([1] + dependent_mult)  # applying multiplication factors
        v_var = elements[vert_var_idx]  # vert value
        for varn in varnames:
            data_value = elements[dependent_vars.index(varn.capitalize())]

        # Find the correct index for v_var

        v_var_idx = np.where(v_var_levels[:, vert_var_idx] == v_var)[0][0]

        data_grid[v_var_idx] = data_value
    data = data_grid.reshape(1, len(lines[data_start:]))

    if any(word in vert_var[0].lower() for word in ['geopotential', 'height', 'altitude']):
        ver_var_lab = 'height_levels'
    if any(word in vert_var[0].lower() for word in ['pressure']):
        ver_var_lab = 'pressure_levels'
    data_tmp = xr.DataArray(
            data, coords={"timestamps": time_diff_in_seconds, ver_var_lab: v_var_levels[:, vert_var_idx]},
            dims=["timestamps", ver_var_lab], name=varn)

    data_tmp.coords["timestamps"].attrs[
        "units"] = "seconds since 1970-01-01 00:00:00"  # Adjust this to your preferred format

    # data_tmp = data_tmp.sortby(ver_var_lab)
    data_tmp = data_tmp.sortby("timestamps")

    # Attach the metadata as attributes to the DataArray
    if instr == 'o3_sondes':
        keys_to_keep = ['east longitude of station', 'latitude of station']  # List of keys to keep

    # Remove all keys not in keys_to_keep
    for key in list(extra_metadata.keys()):  # Convert to list to avoid modifying the dictionary while iterating
        if key not in keys_to_keep:
            del extra_metadata[key]

    data_tmp.attrs = extra_metadata

    return data_tmp


def nasa_ames_parser_2110(fn, instr, vert_var, varnames):
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
    independent_uom = []
    next_start = 8

    dependent_mult = []
    dependent_nan = []
    dependent_mult.extend([float(x) for x in metadata[next_start + 1 + num_independent_vars].strip().split()])
    dependent_nan.extend([float(x) for x in metadata[next_start + 2 + num_independent_vars].strip().split()])
    for _ in range(num_independent_vars):
        if '(' in metadata[next_start]:
            independent_vars.append(metadata[next_start].strip().split('(')[0].strip())
            independent_uom.append(metadata[next_start].strip().split('(')[1])
        else:
            independent_vars.append(metadata[next_start].strip())
            independent_uom.append(np.nan)
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
            extra_vars.append(line_parts[0].strip())
            extra_units.append(line_parts[1].strip()[:-1] if len(line_parts) > 1 else np.nan)
        elif ';' in metadata[next_start]:
            line_parts = metadata[next_start].strip().split(';')
            extra_vars.append(line_parts[0].strip())
            extra_units.append(line_parts[1].strip()[:-1] if len(line_parts) > 1 else np.nan)
        else:
            line_parts = metadata[next_start].strip()
            extra_vars.append(line_parts.strip())
            extra_units.append(np.nan)

        next_start += 1

    comment_lines = []
    nr_comment_lines = int(metadata[next_start].strip())
    [comment_lines.append(elem.strip()) for elem in metadata[next_start + 1:next_start + 1 + nr_comment_lines]]

    # for aero_sondes
    next_start += 1 + nr_comment_lines
    nr_comment_lines = int(metadata[next_start].strip())
    [comment_lines.append(elem.strip()) for elem in metadata[next_start + 1:next_start + 1 + nr_comment_lines]]

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
                if instr in ['lidar_temp', 'lidar_ae']:
                    if block_metadata['Hour'].astype(int) == 24:
                        block_metadata['Hour'] = 0
                        new_date = dt.datetime(
                                block_metadata['Year'].astype(int), block_metadata['Month'].astype(int),
                                block_metadata['Day'].astype(int), block_metadata['Hour'],
                                block_metadata['Minutes'].astype(int)) + dt.timedelta(days=1)
                    else:
                        new_date = dt.datetime(
                                block_metadata['Year'].astype(int), block_metadata['Month'].astype(int),
                                block_metadata['Day'].astype(int), block_metadata['Hour'].astype(int),
                                block_metadata['Minutes'].astype(int))
                    print(new_date)
                    block_metadata['datetime'] = new_date
                if instr in ['aero_sondes', 'o3_sondes']:
                    timedelta = pd.to_timedelta(block_metadata['Launch time'], unit="h")
                    new_date = dt.datetime(
                            block_metadata['Year of launch'].astype(int), block_metadata['Month of launch'].astype(int),
                            block_metadata['Day of launch'].astype(int), timedelta.components.hours,
                            timedelta.components.minutes)
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

            if len(vert_var) > 1:
                try:
                    vert_var_idx = ([independent_vars[0]] + dependent_vars).index(vert_var[0])
                except ValueError:
                    vert_var_idx = ([independent_vars[0]] + dependent_vars).index(vert_var[1])
            v_var_levels = np.unique(
                    data_block_fmt[:, vert_var_idx])
            data_grid = np.full((len(v_var_levels)), np.nan)

            for row in data_block_fmt:
                v_var = row[vert_var_idx]  # vert value
                for varn in varnames:
                    try:
                        data_value = row[dependent_vars.index(varn) + 1]
                        break
                    except ValueError:
                        continue

                # Find the correct index for v_var
                v_var_idx = np.where(v_var_levels == v_var)[0][0]

                # Assign temperature to correct position
                # data_grid[height_idx] = temp_value
                data_grid[v_var_idx] = data_value
            data = data_grid.reshape(1, len(v_var_levels))
            # temperatures = temperature_grid.reshape(1, len(height_levels), len(pressure_levels))

            if any(word in vert_var[0].lower() for word in ['geopotential', 'height', 'altitude']):
                ver_var_lab = 'height_levels'
            if any(word in vert_var[0].lower() for word in ['pressure']):
                ver_var_lab = 'pressure_levels'
            data_tmp = xr.DataArray(
                    data, coords={"timestamps": time_diff_in_seconds, ver_var_lab: v_var_levels},
                    dims=["timestamps", ver_var_lab], name=varn)

            data_tmp.coords["timestamps"].attrs[
                "units"] = "seconds since 1970-01-01 00:00:00"  # Adjust this to your preferred format

            # data_tmp = data_tmp.sortby(ver_var_lab)
            data_tmp = data_tmp.sortby("timestamps")

            # Attach the metadata as attributes to the DataArray
            if instr == 'lidar_ae':
                keys_to_keep = ['Altitude of aperture of the mechanical shutter', 'Averaging time of presented data',
                                'Latitude', 'Longitude', 'Laser wavelength']  # List of keys to keep
            if instr == 'lidar_temp':
                keys_to_keep = ['Altitude of aperture of the mechanical shutter', 'Latitude',
                                'Longitude']  # List of keys to keep
            if instr == 'aero_sondes':
                keys_to_keep = ['East longitude of station', 'Latitude of station',
                                'Laser wavelength']  # List of keys to keep
            # TODO:
            if instr == 'o3_sondes':
                keys_to_keep = []  # List of keys to keep

            # Remove all keys not in keys_to_keep
            for key in list(block_metadata.keys()):  # Convert to list to avoid modifying the dictionary while iterating
                if key not in keys_to_keep:
                    del block_metadata[key]

            data_tmp.attrs = block_metadata

            # Add the xarray to the list of all blocks
            all_blocks.append(data_tmp)

    return all_blocks
