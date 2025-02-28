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

instr = 'uv-vis_spec'


def update_data_avail(instr):
    import os
    import pandas as pd
    import single_instr_data_avail.tools as sida_tls

    import settings as ts

    # https://git.nilu.no/ebas/ebas-io/-/wikis/home#downloading-the-software

    date_list = pd.date_range(
            ts.instr_metadata[instr]['start_instr'], ts.instr_metadata[instr]['end_instr'], freq='ME').tolist()
    folder = os.path.join(ts.basefolder, "thaao_" + instr)

    uv_vis_spec = pd.DataFrame()
    for i in date_list:
        fn = os.path.join(folder, 'thtc' + i.strftime('%y%m') + '.erv')
        fn_new = os.path.join(folder, 'thtc' + i.strftime('%y%m') + '_1.erv')
        if not os.path.exists(fn):
            continue
        with open(fn, 'r') as file:
            print(fn)
            lines = file.readlines()
        with open(fn_new, 'w') as file:
            file.writelines(lines[1:])
        #
        # # Open your NASA Ames 1010 file
        # na_file = nappy.openNAFile(fn_new)
        #
        # # Retrieve the NASA Ames dictionary with all header and data information
        # na_dict = na_file.getNADict()
        #
        # # Verify the file format index (should output 1010)
        # print("File Format Index (FFI):", na_dict.get("FFI"))
        #
        # # List available variables and metadata
        # print("Available variables:", na_file.getVariables())
        #
        # data = na_file.readData()
        #
        with open(fn_new, 'r') as file:
            print(fn_new)
            lines = file.readlines()

        # Identify number of header lines to skip (first element in line 1)
        lines_to_skip = int(lines[0].split()[0])

        # Identify where the data begins (after skipping header lines)
        data_start = lines_to_skip

        # Extract metadata (everything before the data start point)
        metadata = lines[:data_start]

        for i, line in enumerate(metadata):
            if "julian day" in line.lower():  # Adjust this condition based on the file content
                column0_names = [line.strip()]

                break
        next_start = 10

        num_columns1 = int(metadata[9].strip())
        if num_columns1 <= 9:
            col1_multiplier = metadata[10].strip()
            col1_nan = metadata[11].strip()
            next_start += 2
        elif num_columns1 > 9:
            col1_multiplier = metadata[10].strip() + metadata[11].strip()
            col1_nan = metadata[12].strip() + metadata[13].strip()
            next_start += 4

        column1_names = []
        column1_uom = []
        for i in range(next_start, next_start + num_columns1):
            column1_names.append(metadata[i].split(";")[0].strip())
            if ";" in metadata[i]:
                column1_uom.append(metadata[i].split(";")[1].strip())

        num_columns2 = int(metadata[next_start + num_columns1].strip())
        col_multiplier2 = metadata[next_start + num_columns1 + 1].strip()
        col_nan1 = metadata[next_start + num_columns1 + 2].strip()
        next_start += 2
        column2_names = []
        column2_uom = []
        for i in range(next_start + num_columns1 + 1, next_start + num_columns1 + num_columns2 + 1):
            column2_names.append(metadata[i].split(";")[0].strip())
            if ";" in metadata[i]:
                column2_uom.append(metadata[i].split(";")[1].strip())

        df = pd.DataFrame(columns=column0_names + column2_names + column1_names)

        for i in range(data_start, len(lines) - 1):
            first_line = lines[i].split()
            combined_lines = lines[i + 1].split()

            # Ensure combined_lines has the correct number of columns
            k = 1  # Start at the next line
            while len(combined_lines) < num_columns1 and i + k + 1 < len(lines):
                combined_lines.extend(lines[i + k + 1].split())
                k += 1

            if len(combined_lines) != num_columns1:
                continue  # Skip if still incorrect

            full_line = first_line + combined_lines

            if len(full_line) == len(df.columns):  # Ensure correct shape before adding
                df.loc[len(df)] = full_line
            else:
                print(f"Skipping row due to incorrect column count: {full_line}")
        df['datetime'] = pd.to_datetime(df['year'].astype(str)) + pd.to_timedelta(
                df[column0_names[0]].astype(float) - 1, unit='D')

        try:
            df['O3_vertical density (510 nm)'] = df['O3 vertical ednsity (510 nm)']
            df.drop(columns=['O3 vertical ednsity (510 nm)'], inplace=True)
        except KeyError as e:
            pass
        try:
            df['NO2 vertical column density (430 nm)'] = df['NO2 vertical column_density (430 nm']
            df.drop(columns=['NO2 vertical column density (430 nm'], inplace=True)
        except KeyError as e:
            pass
        try:
            df['Fractional julian day of the current year'] = df['Julian day of the current year']
            df.drop(columns=['Fractional julian day of the current year'], inplace=True)
        except KeyError as e:
            pass

        # Strip extra spaces from column names to avoid issues
        df.columns = df.columns.str.strip()
        # df.columns = df.columns.str.replace(' ', '_', regex=False)

        # First, reset index to avoid index conflicts during concatenation
        uv_vis_spec = uv_vis_spec.reset_index(drop=True)
        df = df.reset_index(drop=True)

        df.index = df.index + len(uv_vis_spec)
        uv_vis_spec = uv_vis_spec.join(df, how='outer', rsuffix='_duplicate')

    uv_vis_spec.columns = uv_vis_spec.columns.str.rstrip('_duplicate')
    uv_vis_spec.columns = uv_vis_spec.columns.str.replace("color", "colour")
    uv_vis_spec.columns = uv_vis_spec.columns.str.replace(" : ", ": ")
    uv_vis_spec.columns = uv_vis_spec.columns.str.replace("O3_vertical", "O3 vertical")
    uv_vis_spec.columns = uv_vis_spec.columns.str.replace("(430 nm)", "(430 nm)")
    uv_vis_spec.columns = uv_vis_spec.columns.str.replace("O3_vertical", "O3 vertical")
    uv_vis_spec.columns = uv_vis_spec.columns.str.replace("datetim", "datetime")
    uv_vis_spec.columns = uv_vis_spec.columns.str.replace("air temperatur", "air temperature")

    for col in uv_vis_spec.columns:
        col_df2 = col + '_duplicate'
        if col_df2 in uv_vis_spec.columns:
            # Merge: take values from df1, and if NaN then use values from df2
            uv_vis_spec[col] = uv_vis_spec[col].combine_first(uv_vis_spec[col_df2])
            # Drop the extra column after merging
            uv_vis_spec.drop(columns=[col_df2], inplace=True)

    # uv_vis_spec = uv_vis_spec.groupby(axis=1, level=0).first()
    uv_vis_spec = uv_vis_spec[uv_vis_spec.columns[~uv_vis_spec.columns.str.startswith('type of observation')]]
    uv_vis_spec.set_index('datetime', inplace=True)

    for elem in ['Julian day of the current year', 'Julian day of the current year', 'year', 'day of month', 'hour',
                 'min', 'month number']:
        try:
            uv_vis_spec.drop(columns=[elem], inplace=True)
        except KeyError as e:
            print(e)

    import matplotlib.pyplot as plt
    plt.plot(uv_vis_spec['air temperature'])
    sida_tls.save_mask_txt(uv_vis_spec, os.path.join(folder, "thaao_" + instr), instr)
