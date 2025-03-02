#!/usr/local/bin/python3
# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------------
"""
OK
"""
# -------------------------------------------------------------------------------
__author__ = "Filippo Cali' Quaglia"
__affiliation__ = "UNIVE, INGV"
__credits__ = ["??????"]
__license__ = "GPL"
__version__ = "1.1"
__email__ = "filippo.caliquaglia@ingv.it"
__status__ = "Research"
__lastupdate__ = "February 2025"

import os

import numpy as np
import pandas as pd

import settings as ts
import single_instr_data_avail.sida_tools as sida_tls


def update_data_avail(instr):
    date_list = pd.date_range(
            ts.instr_metadata[instr]['start_instr'], ts.instr_metadata[instr]['end_instr'], freq='D')
    folder = os.path.join(ts.basefolder, "thaao_" + instr)
    formatted_dates = date_list.strftime('%Y%m%d_Thule_CHM190147_000_0060cloud')

    # Initialize an empty list to collect DataFrames
    dfs = []

    # Loop through formatted dates and read data
    for i_fmt in formatted_dates:
        try:
            file_path = os.path.join(folder, 'medie_tat_rianalisi', f'{i_fmt}.txt')
            # Read the file into a DataFrame
            t_tmp = pd.read_table(
                    file_path, skipfooter=0, sep='\s+', header=0, skiprows=9, engine='python')

            # Replace 9999 with NaN
            t_tmp[t_tmp == -9999.9] = np.nan

            # Append the DataFrame to the list
            dfs.append(t_tmp)
        except FileNotFoundError:
            print(f'NOT FOUND: {i_fmt}.txt')

    # Concatenate all DataFrames at once (much more efficient than using pd.concat in a loop)
    if dfs:
        ceilometer = pd.concat(dfs, axis=0)

        ceilometer['datetime'] = pd.to_datetime(
                ceilometer['#'] + ' ' + ceilometer['date[y-m-d]time[h:m:s]'], format='%Y-%m-%d %H:%M:%S')
        ceilometer.set_index('datetime', inplace=True)
    else:
        ceilometer = pd.DataFrame()  # If no data was found, return an empty DataFrame

    ceilometer = ceilometer[['CBH_L1[m]', 'TCC[okt]']]

    sida_tls.save_csv(instr, ceilometer)

    # for ii, i in enumerate(date_list[:-1]):  #     fn = os.path.join(folder, i.strftime('%Y'), i.strftime('%Y%m') + '_Thule_CHM190147.nc')  #     date_list_int = pd.date_range(date_list[ii], date_list[ii + 1], freq='D', inclusive='left').tolist()  #   #     zip_file_path = f'{fn}.zip'  #   #     # Process the zip file and collect found and missing dates  #     found_dates, missing_dates = process_zip_file(zip_file_path, date_list_int)  #   #     # Add found dates to the dataframe  #     if found_dates:  #         found_df = pd.DataFrame({'dt': found_dates, 'mask': True})  #         ceilometer = pd.concat([ceilometer, found_df], ignore_index=True)  #   #     print(fn)  #  #  # def process_zip_file(zip_file_path, date_list_int):  #     import zipfile
#     try:
#         with zipfile.ZipFile(zip_file_path, 'r') as myzip:
#             file_list = set(x.split('_')[0] for x in myzip.namelist())  # Use set for faster lookups
#             found_dates = []
#             missing_dates = []
#             for j in date_list_int:
#                 filename = j.strftime('%Y%m%d')
#                 if filename in file_list:
#                     found_dates.append(j)
#                 else:
#                     missing_dates.append(j)
#         return found_dates, missing_dates
#     except (FileNotFoundError, zipfile.BadZipFile) as e:
#         print(f"Error with file {zip_file_path}: {e}")
#         return [], []
