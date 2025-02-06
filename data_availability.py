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
import switches as sw
import tools as tls
import settings as ts


# Main execution code
def main():
    # Create root for dialog boxes
    root = tls.create_root()

    # Instrument list selection
    sw.switch_instr_list = simpledialog.askstring(
            "Instrument Category",
            'Which category of instruments (Default to: all. Otherwise choose one or more among: current, legacy, macmap, separated by space)?')
    tls.update_instr_list()

    # Panel selections with boolean logic and defaulting to 'n' (False)
    sw.switch_rolling_panels = tls.get_switch_input('Plot rolling panels? (y/n)')
    if sw.switch_rolling_panels:
        window_size = simpledialog.askinteger("Input", "Window size (in months):", minvalue=1, maxvalue=120)
        lag_c = simpledialog.askinteger("Input", "Lag (in months):", minvalue=1, maxvalue=120)
        sw.time_window_c = pd.DateOffset(months=window_size)
        sw.time_freq_c = pd.DateOffset(months=lag_c)
        tls.set_date_params('Start year: ', 'End year: ', 'rolling')

    sw.switch_yearly_panels = tls.get_switch_input('Plot yearly panels? (y/n)')
    if sw.switch_yearly_panels:
        tls.set_date_params('Start year: ', 'End year: ', 'yearly')

    sw.switch_cumulative_panels = tls.get_switch_input('Plot cumulative panels? (y/n)')
    if sw.switch_cumulative_panels:
        lag_a = simpledialog.askinteger("Input", "Lag (in months):", minvalue=1, maxvalue=120)
        sw.time_freq_a = pd.DateOffset(months=lag_a)
        tls.set_date_params('Start year: ', 'End year: ', 'cumulative')

    # Field Campaigns and Historical events (y/n)
    sw.switch_campaigns = tls.get_switch_input('Draw field campaigns? (y/n)', True)
    sw.switch_history = tls.get_switch_input('Draw historical events? (y/n)', False)
    sw.switch_prog_bar = tls.get_switch_input('Draw progress bar? (y/n)', False)

    # Displaying the selected instruments
    messagebox.showinfo("Selected Instruments", f'These instruments are plotted: {ts.instr_list}')

    # Plot the panels based on the switches
    if sw.switch_rolling_panels:
        plts.plot_panels('rolling')
    if sw.switch_yearly_panels:
        plts.plot_panels('yearly')
    if sw.switch_cumulative_panels:
        plts.plot_panels('cumulative')

    print('END')


# Running the main function
if __name__ == "__main__":
    main()
