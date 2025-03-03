#!/usr/local/bin/python3
# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------------
#
"""
Optimized code for updating data availability for isotopic data.
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

import os
import pandas as pd
import settings as ts
import single_instr_data_avail.sida_tools as sida_tls

# Helper function to load and process each file
def load_isotope_data(file_path, datetime_col, date_format, data_col):
    data = pd.read_csv(file_path)
    data['datetime'] = pd.to_datetime(data[datetime_col], format=date_format)
    data.set_index('datetime', inplace=True)
    data['d18O'] = data[data_col]  # Add the isotopic data
    return data[['d18O']]

def update_data_avail(instr):
    folder = os.path.join(ts.basefolder, "thaao_" + instr)

    # Load all isotope data using the helper function
    wv_isotopes1 = load_isotope_data(
        os.path.join(folder, 'BGK_MOSAiC_ADC_finaldataset.csv'),
        'DateTime_UTC', '%m/%d/%Y %H:%M', 'BAR_d18O'
    )

    wv_isotopes2 = load_isotope_data(
        os.path.join(folder, 'thule_isotope_wx_10min_2017_2019.csv'),
        'min10break', '%d-%m-%y %H:%M', None  # No 'd18O' column for this file
    )

    wv_isotopes3 = load_isotope_data(
        os.path.join(folder, 'Thule_water_vapor_isotopes_16.csv'),
        'Date', '%Y-%m-%d %H:%M:%S', 'd18o'
    )

    wv_isotopes4 = load_isotope_data(
        os.path.join(folder, 'ThuleAFB_ppt_isotopes.csv'),
        'Date ', '%m/%d/%y', 'd18O (per mil)'
    )

    # Concatenate all dataframes and sort by datetime index
    wv_isotopes = pd.concat([wv_isotopes1, wv_isotopes2, wv_isotopes3, wv_isotopes4])
    wv_isotopes.sort_index(inplace=True)

    # Save the processed data
    sida_tls.save_csv(instr, wv_isotopes)
