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
__version__ = "0.1"
__email__ = "filippo.caliquaglia@ingv.it"
__status__ = "Research"
__lastupdate__ = "February 2025"

from tkinter import messagebox, simpledialog

import pandas as pd

import plots as plts
import settings as ts
import switches as sw
import tools as tls


# Main execution code
def main():
    # Create root for dialog boxes
    root = tls.create_root()

    # Instrument list selection
    sw.switch_instr_list = simpledialog.askstring(
            "Instrument Category",
            'Which category of instruments (or single instrument)?  \n [thaao, legacy, hyso, all, "single_instr"]')

    tls.update_instr_list()

    # Force update of the availability .txt files for each instrument
    if ts.instr_list in list(ts.metadata_entries.keys()):
        for instr in ts.instr_list:
            tls.update_txt_file(instr)
            return

    tls.set_date_params('Start year: ', 'End year: ')

    # Panel selections with boolean logic and defaulting to 'n' (False)
    sw.switch_rolling_panels = tls.get_switch_input(
            'Plot rolling panels? (y/n) \n [Yearly panels: set=12, window=12] ')
    if sw.switch_rolling_panels:
        lag_r = simpledialog.askinteger("Rolling", "Lag (in months):\n [12 for yearly plots]", minvalue=1, maxvalue=120)
        window_size = simpledialog.askinteger(
                "Rolling", "Window size (in months):\n [12 for yearly plots]", minvalue=1, maxvalue=120)
        sw.time_freq_r = pd.DateOffset(months=lag_r)
        sw.time_window_r = pd.DateOffset(months=window_size)

    sw.switch_cumulative_panels = tls.get_switch_input('Plot cumulative panels? (y/n)')
    if sw.switch_cumulative_panels:
        lag_c = simpledialog.askinteger("Cumulative", "Lag (in months):", minvalue=1, maxvalue=120)
        sw.time_freq_c = pd.DateOffset(months=lag_c)

    # Field Campaigns and Historical events (y/n)
    sw.switch_campaigns = tls.get_switch_input('Draw field campaigns? (y/n)', True)
    sw.switch_history = tls.get_switch_input('Draw historical events? (y/n)', False)
    sw.switch_prog_bar = tls.get_switch_input('Draw progress bar? (y/n)', False)

    # Displaying the selected instruments
    messagebox.showinfo("Selected Instruments", f'These instruments are plotted: {ts.instr_list}')

    # Check and update the availability .txt files for each instrument
    for instr in ts.instr_list:
        tls.check_txt_file_age(instr)

    # Plot the panels based on the switches
    if sw.switch_rolling_panels:
        plts.plot_panels('rolling')
    if sw.switch_cumulative_panels:
        plts.plot_panels('cumulative')

    print('END')


# Running the main function
if __name__ == "__main__":
    main()
