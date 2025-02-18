#!/usr/local/bin/python3
# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------------
#
"""
# TODO:
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

instr = 'lidar_temp'


def update_data_avail(instr):
    import single_instr_data_avail.tools as sida_tls

    import settings as ts

    import os
    import pandas as pd
    import glob

    date_list = pd.date_range(
            ts.instr_metadata[instr]['start_instr'], ts.instr_metadata[instr]['end_instr'], freq='D').tolist()
    folder = os.path.join(ts.basefolder, "thaao_" + instr)

    # Initialize an empty list to hold the rows before concatenating
    rows = []

    for i in date_list:
        try:
            # Create the pattern for file matching
            fn_pattern = os.path.join(folder, i.strftime('%y%m%d') + '.zip')
            files = glob.glob(fn_pattern)  # Use glob to find files that match the pattern
            if os.path.exists(fn_pattern):
                rows.append({'dt': i, 'mask': True})
        except:
            fn_pattern = os.path.join(folder, 'LIDAR_' + i.strftime('%Y%m%d') + '.zip')
            if os.path.exists(fn_pattern):
                rows.append({'dt': i, 'mask': True})

    # Convert the list of dictionaries into a DataFrame
    lidar_temp = pd.DataFrame(rows)

    # Ensure tls.save_txt is implemented correctly to save the DataFrame
    sida_tls.save_txt(instr, lidar_temp)
