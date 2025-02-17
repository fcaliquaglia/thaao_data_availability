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
import subprocess
import tkinter as tk

import numpy as np
import pandas as pd

import settings as ts
import switches as sw


# Function to check if the .txt file is older than 6 months
def check_txt_file_age(instr):
    txt_file_path = os.path.join(ts.basefolder, f'thaao_{instr}', f'{instr}_data_avail_list.txt')
    if os.path.exists(txt_file_path):
        # Get the last modified date of the file
        last_modified = dt.datetime.fromtimestamp(os.path.getmtime(txt_file_path))
        current_date = dt.datetime.now()

        # Check if the file is older than 6 months (180 days)
        if (current_date - last_modified).days > 180:
            print(f"{txt_file_path} is older than 6 months. Generating new file...")
            # Call the function to regenerate the .txt file
            update_txt_file(instr)
        else:
            print(f"{txt_file_path} is up-to-date.")
    else:
        print(f"{txt_file_path} does not exist. Generating new file...")
        # Call the function to generate the .txt file if it doesn't exist
        update_txt_file(instr)


# Function to invoke the external script to update the .txt file
def update_txt_file(instr):
    # Path to the external Python script that updates the .txt file
    specific_script_path = os.getcwd() + ts.instr_metadata[instr]['data_avail_fn']
    try:
        print("Running the external Python script to update the .txt file...")
        subprocess.run(['python', specific_script_path], check=True)
        print("External script executed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error occurred while running the external script: {e}")


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
