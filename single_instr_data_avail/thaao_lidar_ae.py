#!/usr/local/bin/python3
# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------------
#
"""
Brief description
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

instr = 'lidar_ae'


def update_data_avail(instr):
    import single_instr_data_avail.tools as sida_tls

    import settings as ts

    import os
    import pandas as pd
    import glob

    date_list = pd.date_range(
            ts.instr_metadata[instr]['start_instr'], ts.instr_metadata[instr]['end_instr'], freq='ME').tolist()
    folder = os.path.join(ts.basefolder, "thaao_" + instr)

    # Initialize an empty list to hold the rows before concatenating
    rows = []

    for i in date_list:
        # Create the pattern for file matching
        fn_pattern = os.path.join(folder, 'WWW-AIR_1685207569988', 'thae' + i.strftime('%y%m') + '.*')
        files = glob.glob(fn_pattern)  # Use glob to find files that match the pattern

        if files:  # If files exist that match the pattern
            # Append the data as a dictionary to the list
            rows.append({'dt': i, 'mask': True})

    # Convert the list of dictionaries into a DataFrame
    lidar_ae = pd.DataFrame(rows)

    # Ensure tls.save_txt is implemented correctly to save the DataFrame
    sida_tls.save_txt(instr, lidar_ae)
