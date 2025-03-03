# =============================================================
# CREATED:
# AFFILIATION: INGV
# AUTHOR: Filippo Cali' Quaglia
# =============================================================
__author__ = "Filippo Cali' Quaglia"
__credits__ = ["??????"]
__license__ = "GPL"
__version__ = "1.1"
__email__ = "filippo.caliquaglia@ingv.it"
__status__ = "Research"
__lastupdate__ = "February 2025"

import datetime as dt
from tkinter import messagebox, simpledialog

import plots as plts
import settings as ts
import switches as sw
import tools as tls


def main():
    """ Main function for instrument selection, data availability update, and plotting. """
    root = tls.create_root()
    current_year = dt.datetime.today().year  # Avoid multiple calls

    # Instrument list selection
    sw.switch_instr_list = simpledialog.askstring(
        "Instrument Selection for operations",
        'Which category of instruments (or single instrument, separated by white space)?\n'
        '[thaao, legacy, hyso, all, "single_instr"]'
    )

    # Update instrument list and data availability
    tls.update_instr_list()
    tls.csv_filename_creation()
    tls.update_data_availability()

    # Time resolution selection
    ts.time_res = simpledialog.askstring("Time resolution", "What time resolution? [H, D, ME]", initialvalue=ts.time_res)

    # Start and end year selection
    sw.start_date = dt.datetime(simpledialog.askinteger(
        "Input", "Start year:", minvalue=1900, maxvalue=current_year, initialvalue=sw.DEFAULT_START_YEAR
    ), 1, 1)

    sw.end_date = dt.datetime(simpledialog.askinteger(
        "Input", "End year:", minvalue=1900, maxvalue=current_year, initialvalue=sw.DEFAULT_END_YEAR
    ), 12, 31)

    # Configure plot settings
    tls.configure_plot_settings()

    # Display selected instruments
    messagebox.showinfo("Selected Instruments", f'These instruments are plotted: {ts.instr_list}')
    print(f'These instruments are plotted: {ts.instr_list}')

    # Execute plotting based on user selections
    plot_types = {
        "summary": sw.switch_summary_panel,
        "rolling": sw.switch_rolling_panels,
        "cumulative": sw.switch_cumulative_panels,
    }

    for plot_type, is_enabled in plot_types.items():
        if is_enabled:
            print(f"Generating {plot_type} plot...")
            plts.plot_panels(plot_type)
            print(f"{plot_type.capitalize()} plot completed!")

    print("END")


if __name__ == "__main__":
    main()
