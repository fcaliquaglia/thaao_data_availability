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
__version__ = "1.1"
__email__ = "filippo.caliquaglia@gmail.com"
__status__ = "Research"
__lastupdate__ = ""

import datetime as dt
import importlib.util
import os
import sys
import tkinter as tk

import numpy as np
import pandas as pd

import settings as ts
import switches as sw


def check_txt_file_age(instr):
    if instr in ['rad_par_up', 'rad_par_down', 'rad_tb', 'rad_dsi', 'rad_dli', 'rad_usi', 'rad_uli']:
        instr1 = 'rad'
    else:
        instr1 = instr
    if instr == 'skycam':
        basefol=ts.basefolder_skycam
    else:
        basefol=ts.basefolder
    txt_file_path = os.path.join(basefol, f'thaao_{instr1}', f'{instr}_data_avail_list.txt')
    if os.path.exists(txt_file_path):
        # Get the last modified date of the file
        last_modified = dt.datetime.fromtimestamp(os.path.getmtime(txt_file_path))
        current_date = dt.datetime.now()

        # Check if the file is older than n days
        if (current_date - last_modified).days > sw.days_of_an_old_file:
            print(f"{txt_file_path} is older than 6 months. Generating new file...")
            # Call the function to regenerate the .txt file
            update_txt_file(instr)
        else:
            print(f"{txt_file_path} is up-to-date.")
    else:
        print(f"{txt_file_path} does not exist. Generating new file...")
        # Call the function to generate the .txt file if it doesn't exist
        update_txt_file(instr)


def update_txt_file(instr):
    """
    Runs an external script function directly.
    """
    script_path = os.path.join(os.getcwd(), 'single_instr_data_avail', ts.instr_metadata[instr]['data_avail_fn'])

    if not os.path.isfile(script_path):
        print(f"Error: Script not found at {script_path}")
        return

    # Load the script dynamically
    spec = importlib.util.spec_from_file_location("module_name", script_path)
    module = importlib.util.module_from_spec(spec)
    sys.modules["module_name"] = module
    spec.loader.exec_module(module)  # Execute the script

    # Ensure the script has a function to call
    if not hasattr(module, "update_data_avail"):
        print(f"Error: The script {script_path} does not contain 'update_data_avail(instr)' function.")
        return
    else:
        print("Updating .txt file")
        module.update_data_avail(instr)
        print("Update completed successfully.")


# Function to create a Tkinter root window
def create_root():
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    return root


# Function to update the instrument list with pop-up window input
def update_instr_list():
    ts.instr_list = []
    for category in sw.switch_instr_list.split():
        if category in ts.instr_sets:
            ts.instr_list += ts.instr_sets[category]
        elif category in list(ts.metadata_entries.keys()):
            ts.instr_list = category


# Function for getting boolean input through a pop-up window (yes/no)
def get_switch_input(prompt, default=False):
    """ Generic input prompt with default behavior """
    root = create_root()
    user_input = tk.messagebox.askyesno("Input", prompt)  # A simple yes/no dialog box
    return user_input if user_input is not None else default


# Function for getting date range input through pop-up window (start and end years)
def set_date_params(start_prompt, end_prompt):
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
        index_values = pd.date_range(sw.start, dt.datetime.today(), freq='12h')
        return pd.DataFrame(
                {'mask': [np.nan] * len(index_values)}, index=index_values)


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
