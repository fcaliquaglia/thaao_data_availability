#!/usr/local/bin/python3
# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------------
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
__version__ = "0.1"
__email__ = "filippo.caliquaglia@ingv.it"
__status__ = "Research"
__lastupdate__ = "October 2024"

import os

import pandas as pd

import settings as ts
import tools as tls

instr = 'ecapac_aws_snow'
date_list = pd.date_range(
        ts.instr_metadata[instr]['start_instr'], ts.instr_metadata[instr]['end_instr'], freq='D').tolist()
folder = os.path.join(ts.basefolder, "thaao_" + instr)


def generate_file_path(date):
    """Generate the file path for the given date."""
    year_dir = os.path.join(folder, "AWS_ECAPAC", date.strftime('%Y'))
    file_name = f"AWS_THAAO_{date.strftime('%Y_%m_%d')}_00_00.dat"
    return os.path.join(year_dir, file_name)


def main():
    ecapac_aws_snow = []  # List to accumulate results

    for date in date_list:
        file_path = generate_file_path(date)
        if os.path.exists(file_path):
            ecapac_aws_snow.append({'dt': date, 'mask': True})

    # Convert the accumulated results into a DataFrame
    ecapac_aws_snow_df = pd.DataFrame(ecapac_aws_snow)

    # Save the DataFrame to a text file
    tls.save_txt(instr, ecapac_aws_snow_df)


if __name__ == "__main__":
    main()
