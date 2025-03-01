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
    Prompts the user to update a data availability .csv file for a specific instrument.
    If the user opts for an update, the function will process it and then exit the script.
    """
    sw.data_avail_update = tls.get_switch_input('Do you want to update data availability .csv files?')

    if sw.data_avail_update:
        ts.update_threshold = simpledialog.askinteger(
            "Update threshold", 'Update all data availability .csv files older than? \n (days)', minvalue=1)
        tls.update_instr_list('all')
        tls.update_csv_file()
        print(f'Data availability files updated! Thanks and bye!')
        sys.exit()  # Exit after updating


def configure_plot_settings():
    """
    Configures user-selected parameters for plotting, including rolling and cumulative panels.
    """

    sw.switch_summary_panel = tls.get_switch_input('Plot data summary?')

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

    # Execute plotting based on user selection
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
    if sw.switch_summary_panel:
        plot_type = 'summary'
        print(f"Generating {plot_type} plots...")
        plts.plot_panels(plot_type)
        print(f"{plot_type.capitalize()} plots completed!")

    print('END')


if __name__ == "__main__":
    main()
