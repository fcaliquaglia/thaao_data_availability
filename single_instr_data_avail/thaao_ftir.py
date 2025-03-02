#!/usr/local/bin/python3
# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------------
#
"""
Optimized version of the update_data_avail function
"""

# =============================================================
# CREATED:
# AFFILIATION: INGV
# AUTHORS: Filippo Cali' Quaglia
# =============================================================
#
# -------------------------------------------------------------------------------
__author__ = "Filippo Cali' Quaglia, Monica Tosco"
__credits__ = ['??????']
__license__ = 'GPL'
__version__ = '0.1'
__email__ = 'filippo.caliquaglia@ingv.it'
__status__ = 'Research'
__lastupdate__ = "February 2025"

import os
from datetime import datetime, timedelta

import pandas as pd

import settings as ts
import single_instr_data_avail.sida_tools as sida_tls


def mjd2k_to_date(mjd2k):
    """
    Convert Modified Julian Date 2K (MJD2K) to standard datetime.
    MJD2K is the number of days since Jan. 1, 2000, 00:00:00 UTC.

    Args:
    mjd2k: Number of days since Jan. 1, 2000

    Returns:
    A datetime object representing the corresponding UTC date and time.
    """
    # Reference date (Jan 1, 2000, 00:00:00 UTC)
    mjd2k_ref = datetime(2000, 1, 1, 0, 0, 0)

    # Add the MJD2K days to the reference date
    converted_date = mjd2k_ref + timedelta(days=mjd2k)

    return converted_date


def convert_mjd2k_list_to_date(mjd2k_list):
    """
    Convert a list of MJD2K values to standard datetime objects.

    Args:
    mjd2k_list: List of MJD2K values (number of days since Jan 1, 2000)

    Returns:
    List of corresponding datetime objects.
    """
    return [mjd2k_to_date(mjd2k) for mjd2k in mjd2k_list]


def update_data_avail(instr):
    folder = os.path.join(ts.basefolder, 'thaao_' + instr)
    gas_species = ['ch4']  # , 'c2h6', 'co', 'clono2', 'h2co', 'hcl', 'hcn', 'hf', 'hno3', 'n20', 'nh3', 'o3', 'ocs']

    # Initialize an empty list to store DataFrames

    for gas in gas_species:
        # Find all relevant files for this gas
        files = [file for file in os.listdir(folder) if file.startswith(f'groundbased_ftir.{gas}_ncar001_thule_')]

        from pyhdf.SD import SD, SDC
        gas_data = pd.DataFrame()
        for file in files:
            print(file)
            hdf = SD(os.path.join(folder, file), SDC.READ)

            # Access a specific dataset
            gas_data_sel = hdf.select(gas.upper() + '.COLUMN_ABSORPTION.SOLAR')[:]
            gas_time_tmp = hdf.select('DATETIME')[:]
            gas_time = convert_mjd2k_list_to_date(gas_time_tmp)

            gas_data_tmp = pd.DataFrame(gas_data_sel, index=gas_time)
            gas_data = pd.concat([gas_data_tmp, gas_data])
        gas_data.columns = [gas.lower()]

    gas_data.sort_index(inplace=True)

    # Save the resulting DataFrame as a CSV
    gas_data = gas_data.apply(pd.to_numeric, errors='coerce')

    sida_tls.save_csv(instr, gas_data)
    # needed for format purpose
    ftir = pd.read_csv(
            os.path.join(folder, 'ftir_data_avail_list.csv'), parse_dates=['datetime'], index_col='datetime')
    sida_tls.save_csv(instr, gas_data)
