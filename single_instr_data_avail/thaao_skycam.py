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

instr = 'skycam'


def update_data_avail(instr):
    import single_instr_data_avail.sida_tools as sida_tls
    import os
    import pandas as pd
    import settings as ts

    date_list = pd.date_range(
            ts.instr_metadata[instr]['start_instr'], ts.instr_metadata[instr]['end_instr'], freq='D').tolist()
    folder = os.path.join(ts.basefolder_skycam, "thaao_" + instr)

    skycam = pd.DataFrame(columns=['dt', 'mask'])
    skycam_missing = pd.DataFrame(columns=['dt', 'mask'])

    for ii, i in enumerate(date_list[:-1]):
        fn = os.path.join(folder, i.strftime('%Y'), i.strftime('%Y%m%d'))
        date_list_int = pd.date_range(date_list[ii], date_list[ii + 1], freq='5 min', inclusive='left').tolist()

        zip_file_path = f'{fn}.zip'

        # Process the zip file
        found_dates, missing_dates = process_zip_file(zip_file_path, date_list_int)

        # Add found dates to the dataframe
        if found_dates:
            found_df = pd.DataFrame({'dt': found_dates, 'mask': True})
            skycam = pd.concat([skycam, found_df], ignore_index=True)

        # Add missing dates to the missing dataframe
        if missing_dates:
            missing_df = pd.DataFrame({'dt': missing_dates, 'mask': False})
            skycam_missing = pd.concat([skycam_missing, missing_df], ignore_index=True)

        print(fn)

    # Save data to csv files using optimized saving
    sida_tls.save_csv(instr, skycam)


def process_zip_file(zip_file_path, date_list_int):
    import zipfile

    try:
        with zipfile.ZipFile(zip_file_path, 'r') as myzip:
            file_list = set(x.split('/')[1] for x in myzip.namelist())  # Use a set for faster lookups
            found_dates = []
            missing_dates = []
            for j in date_list_int:
                filename = j.strftime('%Y%m%d_%H%M_raw.jpg')
                if filename in file_list:
                    found_dates.append(j)
                else:
                    missing_dates.append(j)
        return found_dates, missing_dates
    except (FileNotFoundError, zipfile.BadZipFile) as e:
        print(f"Error with file {zip_file_path}: {e}")
        return [], []
