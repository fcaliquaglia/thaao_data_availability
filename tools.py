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
import gc
import importlib.util
import os
import sys
import tkinter as tk
from tkinter import messagebox, simpledialog

import numpy as np
import pandas as pd

import settings as ts
import switches as sw


def check_csv_file_age():
    for instr in ts.instr_list:
        if instr in ts.instr_sets['legacy']:
            print(f'{instr} is not active anymore. Skipping data update. Manually delete it for forced update.')
            continue

        csv_file_path = ts.instr_metadata[instr]['csv_path']
        if os.path.exists(csv_file_path):
            # Get the last modified date of the file
            last_modified = dt.datetime.fromtimestamp(os.path.getmtime(csv_file_path))
            current_date = dt.datetime.now()

            # Check if the file is older than n days
            if (current_date - last_modified).days > sw.days_of_an_old_file:
                print(f"{csv_file_path} is older than {sw.days_of_an_old_file} days. Updating the file...")
                update_csv_file(instr)
                print(f"{csv_file_path} has been updated! Great!")
            else:
                print(f"{csv_file_path} is up-to-date. Nothing to do.")
        else:
            print(f"{csv_file_path} does not exist. Generating new file...")
            update_csv_file(instr)
            print(f"{csv_file_path} has been created! Great!")


def update_csv_file(instr):
    """
    Runs an external script function directly.
    """

    script_path = os.path.join(os.getcwd(), 'single_instr_data_avail', ts.instr_metadata[instr]['data_avail_py'])

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
        print("Updating .csv file")
        module.update_data_avail(instr)
        print("Update completed successfully.")
        gc.collect()


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
        elif category in list(ts.instr_metadata.keys()):
            ts.instr_list.append(category)
        else:
            print(f'{category} is wrong!')
    return


def configure_plot_settings():
    """
    Configures user-selected parameters for plotting, including rolling and cumulative panels.
    """

    sw.switch_summary_panel = get_switch_input('Plot data summary?', False)

    ts.fig_size = get_figure_size()

    sw.switch_rolling_panels = get_switch_input(
            'Plot rolling panels? \n [Yearly panels: set=12, window=12]', False)

    if sw.switch_rolling_panels:
        # Get lag value with default fallback
        lag_r = simpledialog.askinteger(
                "Rolling", "Lag (in months):\n [12 for yearly plots]", minvalue=1, maxvalue=120,
                initialvalue=sw.time_freq_r)
        sw.time_freq_r = pd.DateOffset(months=lag_r)

        # Get window size with default fallback
        window_size = simpledialog.askinteger(
                "Rolling", "Window size (in months):\n [12 for yearly plots]", minvalue=1, maxvalue=120,
                initialvalue=sw.time_window_r)
        sw.time_window_r = pd.DateOffset(months=window_size)

    sw.switch_cumulative_panels = get_switch_input('Plot cumulative panels?', False)
    if sw.switch_cumulative_panels:
        lag_c = simpledialog.askinteger(
                "Cumulative", "Lag (in months):", minvalue=1, maxvalue=120, initialvalue=sw.time_freq_c)
        sw.time_freq_c = pd.DateOffset(months=lag_c)

    # Additional plot options
    sw.switch_campaigns = get_switch_input('Draw field campaigns?', True)
    sw.switch_history = get_switch_input('Draw historical events?', False)
    sw.switch_prog_bar = get_switch_input('Draw progress bar?', False)


def update_data_availability():
    """
    Prompts the user to update a data availability .csv file for a specific instrument.
    If the user opts for an update, the function will process it and then exit the script.
    """
    sw.data_avail_update = get_switch_input(
            'Do you want to update the data availability .csv files for the selected instruments?')

    if sw.data_avail_update:
        ts.update_threshold = simpledialog.askinteger(
                "Update threshold", 'Update the data availability .csv files older than? \n (days)', minvalue=1,
                initialvalue=ts.update_threshold)
        check_csv_file_age()


def get_figure_size():
    root = create_root()
    user_input = tk.simpledialog.askstring(
            "Figure format", "Figure size (choose among A4, A3, A2, A1, or A0)", initialvalue='A3')

    return user_input


def get_switch_input(prompt, default=False):
    """Get boolean input through a pop-up window with a default value."""
    root = create_root()
    user_input = tk.messagebox.askyesno("Input", prompt)
    return user_input if user_input is not None else default


def load_data_file(instr):
    """Load the data from the input file and return a DataFrame with 'datetime' as the index."""
    print(f'Loading csv file for {instr}')

    if not os.path.exists(ts.instr_metadata[instr]['csv_path']):
        update_csv_file(instr)

    inp = ts.instr_metadata[instr]['csv_path']
    try:
        date_format = lambda x: pd.to_datetime(x, format='mixed')
        data_val = pd.read_csv(inp, index_col='datetime', date_format=date_format)
        data_val.index = pd.DatetimeIndex(data_val.index)
        return data_val
    except (FileNotFoundError, pd.errors.ParserError):
        print(f'{inp} not found or corrupted! Returning empty DataFrame.')
        index_values = pd.date_range(sw.start, dt.datetime.today(), freq='12h')
        return pd.DataFrame({'mask': [np.nan] * len(index_values)}, index=index_values)


def csv_filename_creation():
    """Create the appropriate file path for each instrument."""
    for instr in ts.instr_list:
        try:
            if instr == 'skycam':
                ts.instr_metadata[instr]['csv_path'] = os.path.join(
                        ts.basefolder_skycam, 'thaao_skycam', f'{instr}_data_avail_list.csv')
            elif instr.startswith('rad'):
                ts.instr_metadata[instr]['csv_path'] = os.path.join(
                        ts.basefolder, 'thaao_rad', f'{instr}_data_avail_list.csv')
            else:
                ts.instr_metadata[instr]['csv_path'] = os.path.join(
                        ts.basefolder, f'thaao_{instr}', f'{instr}_data_avail_list.csv')
        except FileNotFoundError:
            ts.instr_metadata[instr]['csv_path'] = ''
            print(f'File for {instr} not found')

    return
