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

import datetime as dt
from tkinter import messagebox, simpledialog

import pandas as pd

import plots as plts
import settings as ts
import switches as sw
import tools as tls




def main():
    """
    Main function for instrument selection, data availability update, and plotting.
    """
    root = tls.create_root()

    # Instrument list selection
    sw.switch_instr_list = simpledialog.askstring(
            "Instrument Selection for operations",
            'Which category of instruments (or single instrument, separated by white space)?  \n [thaao, legacy, hyso, all, "single_instr"]')
    tls.update_instr_list()
    tls.csv_filename_creation()
    # Prompt for updating data availability before anything else
    tls.update_data_availability()

    # time resolution
    ts.time_res = simpledialog.askstring("Time resolution", 'What time resolution?  \n [H, D, ME]', initialvalue='ME')

    start_year = simpledialog.askinteger(
            "Input", 'Start year: ', minvalue=1900, maxvalue=dt.datetime.today().year, initialvalue=sw.start)
    sw.start_date = dt.datetime(start_year, 1, 1)

    end_year = simpledialog.askinteger(
            "Input", 'End year: ', minvalue=1900, maxvalue=dt.datetime.today().year, initialvalue=sw.end)
    sw.end_date = dt.datetime(end_year, 12, 31)

    # Configure plot settings
    tls.configure_plot_settings()

    # Display selected instruments
    messagebox.showinfo("Selected Instruments", f'These instruments are plotted: {ts.instr_list}')
    print(f'These instruments are plotted: {ts.instr_list}')

    # Execute plotting based on user selection
    if sw.switch_summary_panel:
        plot_type = 'summary'
        print(f"Generating {plot_type} plot...")
        plts.plot_panels(plot_type)
        print(f"{plot_type.capitalize()} plot completed!")
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
