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
__version__ = "1.1"
__email__ = "filippo.caliquaglia@gmail.com"
__status__ = "Research"
__lastupdate__ = "February 2025"

import os
from pathlib import Path

import numpy as np
import pandas as pd

import settings as ts


def save_m_csv(data_val: pd.DataFrame, fol_out: str, instr_nm: str):
    """
    Saves a text file indicating the availability of data.

    :param data_val: Pandas DataFrame containing data values.
    :param fol_out: Output directory for saving the file.
    :param instr_nm: Instrument name for file naming.
    """

    # Ensure numeric data and round index to seconds
    data_val = data_val.apply(pd.to_numeric, errors='coerce')
    data_val.index = data_val.index.ceil('s').tz_localize(None)  # Remove microseconds

    # Create mask for valid data
    valid_mask = data_val.notnull().sum(axis=1) >= 1

    # Create output DataFrame
    out_file = pd.DataFrame({"timestamp": data_val.index.values, "valid_mask": valid_mask.values})

    # Save file
    output_path = Path(fol_out) / f"{instr_nm}_data_avail_list.csv"
    print(f"Saving: {output_path}")
    np.savetxt(output_path, out_file.values, fmt='%s')
    print(f"Saved: {output_path}")


def save_csv(instr_nm, data_val):
    """

    :param data_val:
    :param instr_nm:
    :return:
    """
    if instr_nm == 'skycam':
        fol_out = os.path.join(ts.basefolder_skycam, f'thaao_{instr_nm}')
    elif instr_nm in ['rad_dli', 'rad_dsi', 'rad_uli', 'rad_usi', 'rad_tb', 'rad_alb']:
        fol_out = os.path.join(ts.basefolder, f'thaao_rad')
    else:
        fol_out = os.path.join(ts.basefolder, f'thaao_{instr_nm}')

    data_val = data_val.apply(lambda x: x.strip() if isinstance(x, str) else x)
    data_val = data_val.apply(pd.to_numeric, errors='coerce')
    print('Saving: ' + instr_nm)
    flt_fmt = '%.6e' if instr_nm in ['uv-vis_spec', 'ftir'] else '%.2f'
    data_val.to_csv(
        os.path.join(fol_out, f'{instr_nm}_data_avail_list.csv'), sep=',', index=True, index_label='datetime',
        float_format=flt_fmt)
    print('Saved ' + str(os.path.join(fol_out, instr_nm + '_data_avail_list.csv')))
    return
