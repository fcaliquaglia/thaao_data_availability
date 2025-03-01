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
    import single_instr_data_avail.sida_tools as sida_tls
    import settings as ts

    # https://git.nilu.no/ebas/ebas-io/-/wikis/home#downloading-the-software

    date_list = pd.date_range(
            ts.instr_metadata[instr]['start_instr'], ts.instr_metadata[instr]['end_instr'], freq='ME').tolist()
    folder = os.path.join(ts.basefolder, "thaao_" + instr)

    uv_vis_spec = nasa_ames_parser(date_list, folder)
    # uv_vis_spec = pd.read_csv(
    #         os.path.join(folder, 'uv-vis_spec.csv'), parse_dates=['datetime'], index_col='datetime')
    sida_tls.save_m_csv(uv_vis_spec, folder, instr)


def nasa_ames_parser(date_list, folder):
    import os
    import pandas as pd
    import numpy as np

    uv_vis_spec = pd.DataFrame()
    for i in date_list:
        fn = os.path.join(folder, 'thtc' + i.strftime('%y%m') + '.erv')
        if not os.path.exists(fn):
            continue

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
        with open(fn, 'r') as file:
            print(fn)
            lines = file.readlines()
            lines = lines[1:]

        # Identify number of header lines to skip (first element in line 1)
        lines_to_skip = int(lines[0].split()[0])

        # Identify where the data begins (after skipping header lines)
        data_start = lines_to_skip

        # Extract metadata (everything before the data start point)
        metadata = lines[:data_start]

        # COL 0
        col0_nan = ['np.nan']
        col0_uom = ['np.nan']
        col0_mult = [1]
        for i, line in enumerate(metadata):
            if "julian" in line.lower():  # Adjust this condition based on the file content
                col0_names = [line.strip()]
        next_start = 10

        col1_num = int(metadata[9].strip())
        if col1_num <= 9:
            col1_mult = metadata[10].strip().split()
            col1_mult = [float(x) for x in col1_mult]
            col1_nan = metadata[11].strip().split()
            col1_nan = [float(x) for x in col1_nan]
            next_start += 2
        elif col1_num > 9:
            col1_mult = metadata[10].strip().split() + metadata[11].strip().split()
            col1_mult = [float(x) for x in col1_mult]
            col1_nan = metadata[12].strip().split() + metadata[13].strip().split()
            col1_nan = [float(x) for x in col1_nan]
            next_start += 4

        col1_names = []
        col1_uom = []
        for i in range(next_start, next_start + col1_num):
            col1_names.append(metadata[i].split(";")[0].strip())
            if ";" in metadata[i]:
                col1_uom.append(metadata[i].split(";")[1].strip())
            else:
                col1_uom.append(np.nan)

        col2_num = int(metadata[next_start + col1_num].strip())
        col2_mult = metadata[next_start + col1_num + 1].strip()
        col2_mult = [float(x) for x in col2_mult.split()]
        col2_nan = metadata[next_start + col1_num + 2].strip()
        col2_nan = [float(x) for x in col2_nan.split()]
        next_start += 2
        col2_names = []
        col2_uom = []
        for i in range(next_start + col1_num + 1, next_start + col1_num + col2_num + 1):
            col2_names.append(metadata[i].split(";")[0].strip())
            if ";" in metadata[i]:
                col2_uom.append(metadata[i].split(";")[1].strip())
            else:
                col2_uom.append(np.nan)

        # check col metadata
        if not len(col0_uom) == len(col0_names) == len(col0_nan) == len(col0_mult):
            print('Error in column0 metadata')
        if not len(col1_uom) == len(col1_names) == len(col1_nan) == len(col1_mult):
            print('Error in column1 metadata')
        if not len(col2_uom) == len(col2_names) == len(col2_nan) == len(col2_mult):
            print('Error in column2 metadata')

        metadata_dict0 = {col0_names[0]: {"mult": 1, "nanval": np.nan, "uom": 'fractional julian day'}}
        metadata_dict1 = {key: {"mult": mult, "nanval": nan, "uom": uom} for key, mult, nan, uom, in
                          zip(col1_names, col1_mult, col1_nan, col1_uom)}
        metadata_dict2 = {key: {"mult": mult, "nanval": nan, "uom": uom} for key, mult, nan, uom, in
                          zip(col2_names, col2_mult, col2_nan, col2_uom)}
        metadata_dict2.update(metadata_dict0)
        metadata_dict2.update(metadata_dict1)
        metadata_dict = metadata_dict2

        df = pd.DataFrame(columns=col0_names + col2_names + col1_names)

        for ijk in range(data_start, len(lines) - 1):
            first_line = lines[ijk].split()
            combined_lines = lines[ijk + 1].split()

            # Ensure combined_lines has the correct number of columns
            k = 1  # Start at the next line
            while len(combined_lines) < col1_num and ijk + k + 1 < len(lines):
                combined_lines.extend(lines[ijk + k + 1].split())
                k += 1

            if len(combined_lines) != col1_num:
                continue

            full_line = first_line + combined_lines

            # cast to float

            full_line = [float(x) for x in full_line]

            # nan check
            nan_vals = col0_nan + col2_nan + col1_nan
            for jj_index, jj_val in enumerate(full_line):
                if jj_val == nan_vals[jj_index]:
                    full_line[jj_index] = np.nan

                # if not icol.startswith('type'):  #     try:  #         df[icol] = df[icol].replace(metadata_dict[icol]['nanval'], pd.NA)  #     except KeyError as e:  #         print(e)  # print(full_line)

            if len(full_line) == len(df.columns):
                try:
                    df.loc[len(df)] = full_line
                except:
                    pass

        for icol in df.columns:
            if (icol.startswith('type')) or ('error bar' in icol) or ('index' in icol):
                pass
            else:
                try:
                    df[icol] *= metadata_dict[icol]['mult']
                except KeyError as e:
                    print(e)

        df['datetime'] = pd.to_datetime(df['year'], format='%Y') + pd.to_timedelta(
                df[col0_names[0]].astype(float) - 1, unit='D')

        if 'O3 vertical ednsity (510 nm)' in df.columns:
            df['O3_vertical density (510 nm)'] = df['O3 vertical ednsity (510 nm)']
            df.drop(columns=['O3 vertical ednsity (510 nm)'], inplace=True)

        if 'NO2 vertical column_density (430 nm' in df.columns:
            df['NO2 vertical column density (430 nm)'] = df['NO2 vertical column_density (430 nm']
            df.drop(columns=['NO2 vertical column density (430 nm'], inplace=True)

        if 'Julian day of the current year' in df.columns:
            df['Fractional julian day of the current year'] = df['Julian day of the current year']
            df.drop(columns=['Fractional julian day of the current year'], inplace=True)
        if 'solar zenith ang' in df.columns:
            df['solar zenith angle'] = df['solar zenith ang']
            df.drop(columns=['solar zenith ang'], inplace=True)

        # Strip extra spaces from column names to avoid issues
        df.columns = df.columns.str.strip()

        # First, reset index to avoid index conflicts during concatenation
        uv_vis_spec = uv_vis_spec.reset_index(drop=True)
        df = df.reset_index(drop=True)

        df.index = df.index + len(uv_vis_spec)
        uv_vis_spec = uv_vis_spec.join(df, how='outer', rsuffix='_duplicate')
    uv_vis_spec.columns = uv_vis_spec.columns.str.rstrip('_duplicate')
    uv_vis_spec.columns = uv_vis_spec.columns.str.replace("color", "colour")
    uv_vis_spec.columns = uv_vis_spec.columns.str.replace(" : ", ": ")
    uv_vis_spec.columns = uv_vis_spec.columns.str.replace("O3_vertical", "O3 vertical")
    uv_vis_spec.columns = uv_vis_spec.columns.str.replace("(430 nm)", "(430 nm")
    uv_vis_spec.columns = uv_vis_spec.columns.str.replace("(430 nm", "(430 nm)")
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
    uv_vis_spec = uv_vis_spec.T.groupby(level=0).first().T
    uv_vis_spec = uv_vis_spec[uv_vis_spec.columns[~uv_vis_spec.columns.str.startswith('type of observation')]]
    uv_vis_spec.set_index('datetime', inplace=True)
    for elem in ['Julian day of the current year', 'Fractional julian day of the current year', 'year', 'day of month',
                 'hour', 'min', 'month number']:
        try:
            uv_vis_spec.drop(columns=[elem], inplace=True)
        except KeyError:
            print(f"Column {elem} not found")
    uv_vis_spec = uv_vis_spec.sort_index()
    uv_vis_spec = uv_vis_spec.apply(pd.to_numeric, errors='coerce')
    uv_vis_spec.to_csv(os.path.join(folder, 'uv-vis_spec.csv'), sep=',', index=True, float_format='%.2f')

    return uv_vis_spec
