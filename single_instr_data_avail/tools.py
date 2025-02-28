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

import numpy as np
import pandas as pd

import settings as ts


def save_mask_txt(data_val, fol_out, instr_nm):
    """

    :param fol_out:
    :param data_val:
    :param instr_nm:
    :return:
    """

    # Make sure interesting data fields are numeric (i.e. floats)
    data_val = data_val.apply(pd.to_numeric, errors='coerce')
    data_val.index = data_val.index.ceil('s').tz_localize(None)  # remove microseconds

    # Create masks
    try:
        valid_mask = np.sum(data_val.notnull(), axis=1) >=1
    except:
        valid_mask = data_val.notnull()

    out_file = pd.concat([pd.Series(data_val.index.values), pd.Series(valid_mask.values)], axis=1)

    print(f'Saving: {instr_nm}')
    np.savetxt(os.path.join(fol_out, f'{instr_nm}_data_avail_list.txt'), out_file, fmt='%s')
    print('Saved ' + os.path.join(fol_out, f'{instr_nm}_data_avail_list.txt'))
    return


def save_txt(instr_nm, data_val, missing=False):
    """

    :param missing:
    :param data_val:
    :param instr_nm:
    :return:
    """
    if instr_nm == 'skycam':
        fol_out = os.path.join(ts.basefolder_skycam, f'thaao_{instr_nm}')
    else:
        fol_out = os.path.join(ts.basefolder, f'thaao_{instr_nm}')

    if missing:
        print('Saving missing: ' + instr_nm)
        np.savetxt(os.path.join(fol_out, f'{instr_nm}_data_missing_list.txt'), data_val, fmt='%s')
        print('Saved ' + str(os.path.join(fol_out, instr_nm + '_data_missing_list.txt')))
    else:
        print('Saving: ' + instr_nm)
        np.savetxt(os.path.join(fol_out, f'{instr_nm}_data_avail_list.txt'), data_val, fmt='%s')
        print('Saved ' + str(os.path.join(fol_out, instr_nm + '_data_avail_list.txt')))
    return
