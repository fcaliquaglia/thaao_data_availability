#!/usr/local/bin/python3
# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------------
#
"""
Brief description
"""

# =============================================================
# CREATED: 
# AFFILIATION: UNIVE, INGV
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

import datetime as dt
import os
import tkinter as tk

import pandas as pd

import settings as ts
import switches as sw


# Function to create a Tkinter root window
def create_root():
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    return root


# Function to update the instrument list with pop-up window input
def update_instr_list():
    for category in sw.switch_instr_list.split():
        if category in ts.instr_sets:
            ts.instr_list += ts.instr_sets[category]


# Function for getting boolean input through a pop-up window (yes/no)
def get_switch_input(prompt, default=False):
    """ Generic input prompt with default behavior """
    root = create_root()
    user_input = tk.messagebox.askyesno("Input", prompt)  # A simple yes/no dialog box
    return user_input if user_input is not None else default


# Function for getting date range input through pop-up window (start and end years)
def set_date_params(start_prompt, end_prompt, date_type):
    """ Generic date input handling """
    root = create_root()

    start_year = tk.simpledialog.askinteger("Input", start_prompt, minvalue=1920, maxvalue=dt.datetime.today().year)
    start_date = dt.datetime(start_year, 1, 1)

    end_year = tk.simpledialog.askinteger("Input", end_prompt, minvalue=1920, maxvalue=dt.datetime.today().year)
    end_date = dt.datetime(end_year, 12, 31)

    sw.start = start_date
    sw.end = end_date

    return


def load_data_file(inp):
    """
    Loads the data from the input file. Returns a DataFrame with 'datetime' as the index
    and 'mask' column indicating data availability.
    """
    try:
        data_val = pd.read_table(inp, sep=' ')
        data_val.columns = ['date', 'time', 'mask']
        data_val['datetime'] = pd.to_datetime(data_val['date'] + ' ' + data_val['time'])
        data_val.set_index('datetime', inplace=True)
        data_val.drop(columns=['date', 'time'], inplace=True)
        return data_val
    except FileNotFoundError:
        print(f'{inp} not found or corrupted!')
        # Return an empty DataFrame for missing data
        return pd.DataFrame(
                {'mask': []}, index=pd.date_range(dt.datetime(1900, 1, 1), dt.datetime.today(), freq='720min'))


def input_file_selection(i_list, i_name):
    """Select the appropriate input file for each instrument."""
    try:
        if i_name == 'skycam':
            inp_file = os.path.join(ts.basefolder_skycam, 'thaao_skycam', i_name + '_data_avail_list.txt')
        elif i_name.startswith('rad'):
            inp_file = os.path.join(ts.basefolder, 'thaao_rad', i_name + '_data_avail_list.txt')
        else:
            inp_file = os.path.join(ts.basefolder, 'thaao_' + i_name, i_name + '_data_avail_list.txt')
        i_list.append(i_name)
    except FileNotFoundError:
        inp_file = None
        print(f'File for {i_name} was not found')

    return inp_file, i_name
