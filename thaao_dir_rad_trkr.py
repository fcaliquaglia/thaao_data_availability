#!/usr/local/bin/python3
# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------------
"""
OK
"""
# -------------------------------------------------------------------------------
__author__ = "Filippo Cali' Quaglia"
__credits__ = ["??????"]
__license__ = "GPL"
__version__ = "0.1"
__email__ = "filippo.caliquaglia@ingv.it"
__status__ = "Research"
__lastupdate__ = "October 2024"

import os
import shutil
import zipfile
import pandas as pd
import settings as ts
import tools as tls

instr = 'dir_rad_trkr'
date_list = pd.date_range(ts.instr_metadata[instr]['start_instr'], ts.instr_metadata[instr]['end_instr'], freq='D').tolist()
folder = os.path.join(ts.basefolder, "thaao_" + instr, 'solcom')


def daily_zipping():
    for i in date_list:
        fn = os.path.join(folder, i.strftime('%Y'))
        fn_new = os.path.join(folder, i.strftime('%Y%m%d'))
        files = [f for f in os.listdir(fn) if f.startswith(i.strftime('%Y%m%d'))]

        if not files:
            continue

        # Ensure the directory exists before copying files
        os.makedirs(fn_new, exist_ok=True)

        for f in files:
            try:
                shutil.copy(os.path.join(fn, f), os.path.join(fn_new, f))
                print(f"Copied: {os.path.join(fn_new, f)}")
            except FileNotFoundError as e:
                print(f"Error copying {f}: {e}")

        try:
            os.makedirs(os.path.join(folder, i.strftime('%Y')), exist_ok=True)
            with zipfile.ZipFile(os.path.join(folder, i.strftime('%Y'), i.strftime('%Y%m%d') + '.zip'), 'w') as zipf:
                tls.zipdir(fn_new, zipf)
            print(f"Zipped: {fn_new}")
        except Exception as e:
            print(f"Error zipping file {fn_new}: {e}")

        try:
            shutil.rmtree(fn_new)
        except FileNotFoundError as e:
            print(f"Error deleting {fn_new}: {e}")


def main():
    dir_rad_trkr = []
    dir_rad_trkr_missing = []

    for ii, i in enumerate(date_list[:-1]):
        fn = os.path.join(folder, i.strftime('%Y'), i.strftime('%Y%m%d'))

        try:
            if os.path.exists(fn + '.zip'):
                print(f"Available: {fn}")
                dir_rad_trkr.append([i, True])
            else:
                dir_rad_trkr_missing.append([i, False])
                print(f"Missing: {fn}")
        except (FileNotFoundError, zipfile.BadZipFile) as e:
            print(f"Error with file {fn}: {e}")

    # Convert lists to DataFrames after processing
    dir_rad_trkr_df = pd.DataFrame(dir_rad_trkr, columns=['dt', 'mask'])
    dir_rad_trkr_missing_df = pd.DataFrame(dir_rad_trkr_missing, columns=['dt', 'mask'])

    # Save the results
    tls.save_txt(instr, dir_rad_trkr_df)
    tls.save_txt(instr, dir_rad_trkr_missing_df, missing=True)


if __name__ == "__main__":
    main()
