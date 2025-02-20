# =============================================================
# CREATED:
# AFFILIATION: INGV
# AUTHORS: Filippo Cali' Quaglia
# =============================================================
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

import sys
from tkinter import messagebox, simpledialog

import pandas as pd
from tqdm import tqdm

import plots as plts
import settings as ts
import switches as sw
import tools as tls


def configure_update_data_availability():
    """
    Prompts the user to update a data availability .txt file for a specific instrument.
    If the user opts for an update, the function will process it and then exit the script.
    """
    sw.data_avail_update = tls.get_switch_input('Do you want to update a data availability .txt file?')

    if sw.data_avail_update:
        sw.switch_instr_list = simpledialog.askstring(
                "Instrument Selection for .txt update",
                'For which instrument do you want to update \n the .txt data availability file?')
        tls.update_instr_list()
        tls.update_txt_file(ts.instr_list)
        print(f'Data availability file for {ts.instr_list} updated! Thanks and bye!')
        sys.exit()  # Exit after updating


def configure_plot_settings():
    """
    Configures user-selected parameters for plotting, including rolling and cumulative panels.
    """
    sw.switch_rolling_panels = tls.get_switch_input(
            'Plot rolling panels? \n [Yearly panels: set=12, window=12] ')
    if sw.switch_rolling_panels:
        lag_r = simpledialog.askinteger("Rolling", "Lag (in months):\n [12 for yearly plots]", minvalue=1, maxvalue=120)
        window_size = simpledialog.askinteger(
                "Rolling", "Window size (in months):\n [12 for yearly plots]", minvalue=1, maxvalue=120)
        sw.time_freq_r = pd.DateOffset(months=lag_r)
        sw.time_window_r = pd.DateOffset(months=window_size)

    sw.switch_cumulative_panels = tls.get_switch_input('Plot cumulative panels?')
    if sw.switch_cumulative_panels:
        lag_c = simpledialog.askinteger("Cumulative", "Lag (in months):", minvalue=1, maxvalue=120)
        sw.time_freq_c = pd.DateOffset(months=lag_c)

    # Additional plot options
    sw.switch_campaigns = tls.get_switch_input('Draw field campaigns?', True)
    sw.switch_history = tls.get_switch_input('Draw historical events?', False)
    sw.switch_prog_bar = tls.get_switch_input('Draw progress bar?', False)


def main():
    """
    Main function for instrument selection, data availability update, and plotting.
    """
    root = tls.create_root()

    # Prompt for updating data availability before anything else
    configure_update_data_availability()

    # Instrument list selection
    sw.switch_instr_list = simpledialog.askstring(
            "Instrument Selection for plotting",
            'Which category of instruments (or single instrument)?  \n [thaao, legacy, hyso, all, "single_instr"]')

    tls.update_instr_list()
    tls.set_date_params('Start year: ', 'End year: ')

    # Configure plot settings
    configure_plot_settings()

    # Display selected instruments
    messagebox.showinfo("Selected Instruments", f'These instruments are plotted: {ts.instr_list}')

    # Check and update availability .txt files if needed
    total_steps = len(ts.instr_list)
    with tqdm(
            total=total_steps, desc=f"Check and update availability .txt file", colour='blue',
            bar_format="{l_bar}{bar} {n_fmt}/{total_fmt} [{elapsed}<{remaining}]\n") as tbar:
        for instr in ts.instr_list:
            print(instr)
            tls.check_txt_file_age(instr)
            tbar.update(1)

    # Execute plotting based on user selections
    if sw.switch_rolling_panels:
        plot_type = 'rolling'
        print(f"Generating {plot_type} plots...")
        plts.plot_panels(plot_type)
        print(f"{plot_type.capitalize()} plots completed!")
    if sw.switch_cumulative_panels:
        plot_type = 'cumulative'
        print(f"Generating {plot_type} plots...")
        plts.plot_panels(plot_type)
        print(f"{plot_type.capitalize()} plots completed!")

    print('END')


if __name__ == "__main__":
    main()
