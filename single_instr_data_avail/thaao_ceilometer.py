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

instr = 'ceilometer'


def update_data_avail(instr):
    import os
    import pandas as pd

    import settings as ts
    import single_instr_data_avail.tools as sida_tls

    date_list = pd.date_range(
            ts.instr_metadata[instr]['start_instr'], ts.instr_metadata[instr]['end_instr'], freq='D').tolist()
    folder = os.path.join(ts.basefolder, "thaao_" + instr)

    ceilometer = pd.DataFrame(columns=['dt', 'mask'])
    ceilometer_missing = pd.DataFrame(columns=['dt', 'mask'])

    for ii, i in enumerate(date_list[:-1]):
        fn = os.path.join(folder, i.strftime('%Y'), i.strftime('%Y%m') + '_Thule_CHM190147.nc')
        date_list_int = pd.date_range(date_list[ii], date_list[ii + 1], freq='D', inclusive='left').tolist()

        zip_file_path = f'{fn}.zip'

        # Process the zip file and collect found and missing dates
        found_dates, missing_dates = process_zip_file(zip_file_path, date_list_int)

        # Add found dates to the dataframe
        if found_dates:
            found_df = pd.DataFrame({'dt': found_dates, 'mask': True})
            ceilometer = pd.concat([ceilometer, found_df], ignore_index=True)

        # Add missing dates to the missing dataframe
        if missing_dates:
            missing_df = pd.DataFrame({'dt': missing_dates, 'mask': False})
            ceilometer_missing = pd.concat([ceilometer_missing, missing_df], ignore_index=True)

        print(fn)

    # Save data to txt files using optimized saving
    sida_tls.save_txt(instr, ceilometer)
    sida_tls.save_txt(instr, ceilometer_missing, missing=True)


def process_zip_file(zip_file_path, date_list_int):
    import zipfile
    try:
        with zipfile.ZipFile(zip_file_path, 'r') as myzip:
            file_list = set(x.split('_')[0] for x in myzip.namelist())  # Use set for faster lookups
            found_dates = []
            missing_dates = []
            for j in date_list_int:
                filename = j.strftime('%Y%m%d')
                if filename in file_list:
                    found_dates.append(j)
                else:
                    missing_dates.append(j)
        return found_dates, missing_dates
    except (FileNotFoundError, zipfile.BadZipFile) as e:
        print(f"Error with file {zip_file_path}: {e}")
        return [], []
