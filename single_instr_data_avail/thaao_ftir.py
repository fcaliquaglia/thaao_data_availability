#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

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
    gas_species = ['ch4', 'c2h6', 'co', 'h2co', 'hcn', 'hf', 'hno3', 'nh3', 'o3', 'ocs']
    # 'clono2' 'hcl' not working

    # Initialize an empty DataFrame for appending all gas data
    all_gas_data = pd.DataFrame()

    # Loop over each gas species
    for gas in gas_species:
        # Find all relevant files for this gas
        files = [file for file in os.listdir(folder) if file.startswith(f'groundbased_ftir.{gas}_ncar001_thule_')]

        from pyhdf.SD import SD, SDC
        gas_data = pd.DataFrame()

        # Process each file for the current gas species
        for file in files:
            print(f"Processing file: {file}")
            hdf = SD(os.path.join(folder, file), SDC.READ)

            # Access the specific dataset for the current gas
            gas_data_sel = hdf.select(gas.upper() + '.COLUMN_ABSORPTION.SOLAR')[:]
            gas_time_tmp = hdf.select('DATETIME')[:]
            gas_time = convert_mjd2k_list_to_date(gas_time_tmp)

            # Create a temporary DataFrame for the current gas data
            gas_data_tmp = pd.DataFrame(gas_data_sel, index=gas_time)
            gas_data_tmp.columns = [gas.lower()]

            # Append the data for the current gas to the main gas data DataFrame
            gas_data = pd.concat([gas_data, gas_data_tmp], axis=1)

        # Concatenate the gas data to the main DataFrame `all_gas_data` column-wise, aligning by the index
        all_gas_data = pd.concat([all_gas_data, gas_data], axis=1)

    # Sort the resulting DataFrame by index (datetime)
    all_gas_data.sort_index(inplace=True)

    # Convert data to numeric and handle errors (e.g., NaN for invalid data)
    all_gas_data = all_gas_data.apply(pd.to_numeric, errors='coerce')
    all_gas_data = all_gas_data.T.groupby(level=0).first().T
    # Save the resulting DataFrame as a CSV
    sida_tls.save_csv(instr, all_gas_data)

    # # Optionally, load the additional CSV file if needed
    # ftir = pd.read_csv(
    #     os.path.join(folder, 'ftir_data_avail_list.csv'), parse_dates=['datetime'], index_col='datetime')
    #
    # # Save or process ftir DataFrame if necessary
    # sida_tls.save_csv(instr, ftir)
