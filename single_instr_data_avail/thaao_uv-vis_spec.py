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

    date_list = pd.date_range(
            ts.instr_metadata[instr]['start_instr'], ts.instr_metadata[instr]['end_instr'], freq='ME').tolist()
    folder = os.path.join(ts.basefolder, "thaao_" + instr)

    uv_vis_spec = pd.DataFrame()
    for i in date_list:
        fn = os.path.join(folder, 'thtc' + i.strftime('%y%m') + '.erv')
        if not os.path.exists(fn):
            continue
        with open(fn, 'r') as file:
            print(fn)
            lines = file.readlines()

        # Identify number of header lines to skip (first element in line 1)
        lines_to_skip = int(lines[1].split()[0])

        # Identify where the data begins (after skipping header lines)
        data_start = lines_to_skip + 1

        # Extract metadata (everything before the data start point)
        metadata = lines[:data_start]

        column0_names = [lines[9].strip()]
        next_start = 11

        num_columns1 = int(lines[10].strip())
        if num_columns1 <= 9:
            col1_multiplier = lines[11].strip()
            col1_nan = lines[12].strip()
            next_start += 2
        elif num_columns1 > 9:
            col1_multiplier = lines[11].strip() + lines[12].strip()
            col1_nan = lines[13].strip() + lines[14].strip()
            next_start += 4

        column1_names = []
        column1_uom = []
        for i in range(next_start, next_start + num_columns1):
            column1_names.append(lines[i].split(";")[0].strip())
            if ";" in lines[i]:
                column1_uom.append(lines[i].split(";")[1].strip())

        num_columns2 = int(lines[next_start + num_columns1].strip())
        col_multiplier2 = lines[next_start + num_columns1 + 1].strip()
        col_nan1 = lines[next_start + num_columns1 + 2].strip()
        next_start += 2
        column2_names = []
        column2_uom = []
        for i in range(next_start + num_columns1 + 1, next_start + num_columns1 + num_columns2 + 1):
            column2_names.append(lines[i].split(";")[0].strip())
            if ";" in lines[i]:
                column2_uom.append(lines[i].split(";")[1].strip())

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

        df.columns = df.columns.str.replace('/', '-', regex=False)
        df.columns = df.columns.str.replace(' ', '_', regex=False)
        try:
            df['O3_vertical_density_(510_nm)'] = df['O3_vertical_ednsity_(510_nm)']
            df.drop(columns=['O3_vertical_ednsity_(510_nm)'], inplace=True)
        except KeyError as e:
            pass
        uv_vis_spec = pd.concat([uv_vis_spec, df], ignore_index=True)

    uv_vis_spec.set_index('datetime', inplace=True)
    uv_vis_spec.drop(
            columns=[column0_names[0], 'year', 'month number', 'day of month', 'hour', 'minute', 'datetime'],
            inplace=True)

    sida_tls.save_mask_txt(uv_vis_spec, os.path.join(folder, "thaao_" + instr), instr)
