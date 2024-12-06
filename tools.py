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
__email__ = "filippo.caliquaglia@gmail.com"
__status__ = "Research"
__lastupdate__ = ""

import os

import numpy as np
import pandas as pd

import settings as ts


def input_file_selection(i_idx, i_list, i_name):
    """

    :param i_idx:
    :param i_list:
    :param i_name:
    :return:
    """
    try:
        print(f'{i_idx:02}' + ' ' + i_name)
        # if i_name[0:3] == 'rad':
        #     inp_file = os.path.join(fol_input, 'thaao_rad', i_name + '_data_avail_list.txt')
        if i_name[0:3] == 'aws':
            inp_file = os.path.join(ts.basefolder, 'thaao_meteo', i_name + '_data_avail_list.txt')
        if i_name[0:7] == 'skycam':
            inp_file = os.path.join(ts.basefolder_skycam, 'thaao_skycam', i_name + '_data_avail_list.txt')
        # elif i_name[0:5] == 'lidar':
        #     inp_file = os.path.join(fol_input, 'thaao_lidar', i_name + '_data_avail_list.txt')
        # elif i_name[0:5] == 'metar':
        #     inp_file = os.path.join(fol_input, i_name + '_data_avail_list.txt')
        # elif i_name[0:13] == 'macmap_seismometers':
        #     inp_file = os.path.join(fol_input, 'thaao_macmap_seismometers', i_name + '_data_avail_list.txt')
        # elif (i_name[0:11] == 'ecapac_snow') | (i_name[0:10] == 'ecapac_aws'):
        #     inp_file = os.path.join(fol_input, 'thaao_ecapac_aws_snow', i_name + '_data_avail_list.txt')
        else:
            inp_file = os.path.join(ts.basefolder, 'thaao_' + i_name, i_name + '_data_avail_list.txt')
        i_list.append(i_name)
    except FileNotFoundError:
        inp_file = None
        print('file for ' + i_name + ' was not found')

    return inp_file, i_list


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
        valid_mask = np.sum(data_val.notnull(), axis=1) == data_val.shape[1]
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


def zipdir(path, ziph):
    # ziph is zipfile handle
    # for root, dirs, files in os.walk(path):
    files = os.listdir(path)
    for file in files:
        ziph.write(
                os.path.join(path, file), os.path.relpath(os.path.join(path, file), os.path.join(path, '..')))
