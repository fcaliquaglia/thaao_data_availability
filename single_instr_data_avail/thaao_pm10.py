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

from pathlib import Path
import pandas as pd
import settings as ts
import single_instr_data_avail.sida_tools as sida_tls


def update_data_avail(instr):
    folder = Path(ts.basefolder) / f"thaao_{instr}"
    file_path = folder / "Thule_2010_sampling_3mag23_modificato_per_data_availability.xls"

    # Read Excel file directly
    pm10_tmp = pd.read_excel(file_path, index_col=0)

    # Create a DataFrame with True values for each date in pm10_tmp
    pm10 = pd.DataFrame({"datetime": pd.to_datetime(pm10_tmp.index), "PM10": pm10_tmp['PM10']})
    pm10.set_index('datetime', inplace=True)

    # Save data
    sida_tls.save_csv(instr, pm10)

