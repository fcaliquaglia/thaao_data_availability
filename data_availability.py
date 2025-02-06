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

import tkinter as tk
from tkinter import messagebox, simpledialog

from plots import *


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
    user_input = messagebox.askyesno("Input", prompt)  # A simple yes/no dialog box
    return user_input if user_input is not None else default


# Function for getting date range input through pop-up window (start and end years)
def set_date_params(start_prompt, end_prompt, date_type):
    """ Generic date input handling """
    root = create_root()

    start_year = simpledialog.askinteger("Input", start_prompt, minvalue=1900, maxvalue=2100)
    start_date = dt.datetime(start_year, 1, 1)

    end_year = simpledialog.askinteger("Input", end_prompt, minvalue=1900, maxvalue=2100)
    end_date = dt.datetime(end_year, 12, 31)

    if date_type == 'rolling':
        sw.start_c = start_date + sw.time_window_c
        sw.end_c = dt.datetime.today() + dt.timedelta(minutes=500000)
    elif date_type == 'yearly':
        sw.start_y = start_date
        sw.end_y = end_date
    elif date_type == 'cumulative':
        sw.start_a = start_date
        sw.end_a = end_date


# Main execution code (optimized)
def main():
    # Create root for dialog boxes
    root = create_root()

    # Instrument list selection
    sw.switch_instr_list = simpledialog.askstring(
            "Instrument Category",
            'Which category of instruments (Default to: all. Otherwise choose one or more among: current, legacy, macmap, separated by space)?')
    if not sw.switch_instr_list:
        sw.switch_instr_list = 'all'  # Default to 'all' if the user doesn't provide input
    update_instr_list()

    # Panel selections with boolean logic and defaulting to 'n' (False)
    sw.switch_rolling_panels = get_switch_input('Plot rolling panels? (y/n)')
    if sw.switch_rolling_panels:
        window_size = simpledialog.askinteger("Input", "Window size (in months):", minvalue=1, maxvalue=120)
        lag_c = simpledialog.askinteger("Input", "Lag (in months):", minvalue=1, maxvalue=120)
        sw.time_window_c = pd.DateOffset(months=window_size)
        sw.time_freq_c = pd.DateOffset(months=lag_c)
        set_date_params('Start year: ', 'End year: ', 'rolling')

    sw.switch_yearly_panels = get_switch_input('Plot yearly panels? (y/n)')
    if sw.switch_yearly_panels:
        set_date_params('Start year: ', 'End year: ', 'yearly')

    sw.switch_cumulative_panels = get_switch_input('Plot cumulative panels? (y/n)')
    if sw.switch_cumulative_panels:
        lag_a = simpledialog.askinteger("Input", "Lag (in months):", minvalue=1, maxvalue=120)
        sw.time_freq_a = pd.DateOffset(months=lag_a)
        set_date_params('Start year: ', 'End year: ', 'cumulative')

    # Field Campaigns and Historical events (y/n)
    sw.switch_campaigns = get_switch_input('Draw field campaigns? (y/n)', True)
    sw.switch_history = get_switch_input('Draw historical events? (y/n)', False)
    sw.switch_prog_bar = get_switch_input('Draw progress bar? (y/n)', False)

    # Displaying the selected instruments
    messagebox.showinfo("Selected Instruments", f'These instruments are plotted: {ts.instr_list}')

    # Plot the panels based on the switches
    if sw.switch_rolling_panels:
        plot_rolling_panels()

    if sw.switch_yearly_panels:
        plot_yearly_panels()

    if sw.switch_cumulative_panels:
        plot_cumulative_panels()

    print('END')


# Running the main function
if __name__ == "__main__":
    main()

# #!/usr/local/bin/python3
# # -*- coding: utf-8 -*-
# # -------------------------------------------------------------------------------
# #
# """
# Brief description
# """
#
# # =============================================================
# # CREATED:
# # AFFILIATION: INGV
# # AUTHORS: Filippo Cali' Quaglia
# # =============================================================
# # =============================================================
# #
# # -------------------------------------------------------------------------------
# __author__ = "Filippo Cali' Quaglia"
# __credits__ = ["??????"]
# __license__ = "GPL"
# __version__ = "0.1"
# __email__ = "filippo.caliquaglia@ingv.it"
# __status__ = "Research"
# __lastupdate__ = "February 2025"
#
# import settings as ts
# from plots import *
#
#
# def update_instr_list(switch_instr_list):
#     # Start with an empty list
#     ts.instr_list = []
#
#     # For each valid category in the input, update the instrument list
#     for category in switch_instr_list.split():
#         if category in ts.instr_sets:
#             ts.instr_list += ts.instr_sets[category]
#
#
# def get_switch_input(prompt, default=False):
#     """ Generic input prompt with default behavior """
#     user_input = input(prompt).strip().lower()
#     if user_input == 'y':
#         return True
#     elif user_input == 'n':
#         return False
#     return default
#
#
# def set_date_params(start_prompt, end_prompt, date_type):
#     """ Generic date input handling """
#     start_year = int(input(start_prompt))
#     start_date = dt.datetime(start_year, 1, 1)
#     end_year = int(input(end_prompt))
#     end_date = dt.datetime(end_year, 12, 31)
#
#     if date_type == 'rolling':
#         sw.start_c = start_date + sw.time_window_c
#         sw.end_c = dt.datetime.today() + dt.timedelta(minutes=500000)
#     elif date_type == 'yearly':
#         sw.start_y = start_date
#         sw.end_y = end_date
#     elif date_type == 'cumulative':
#         sw.start_a = start_date
#         sw.end_a = end_date
#
#
# # Main execution code (optimized)
# def main():
#     # Instrument list selection
#     switch_instr_list = input(
#             'Which category of instruments (Default to: all. Otherwise choose one or more among: current, legacy, macmap, separated by space)\n')
#     update_instr_list(switch_instr_list)
#
#     # Panel selections with boolean logic and defaulting to 'n' (False)
#     sw.switch_rolling_panels = get_switch_input('Plot rolling panels (y/n)\n')
#     if sw.switch_rolling_panels:
#         window_size = int(input('window size (in months): '))
#         lag_c = int(input('lag (in months): '))
#         sw.time_window_c = pd.DateOffset(months=window_size)
#         sw.time_freq_c = pd.DateOffset(months=lag_c)
#         set_date_params('start year: ', 'end year: ', 'rolling')
#
#     sw.switch_yearly_panels = get_switch_input('Plot yearly panels? (y/n)\n')
#     if sw.switch_yearly_panels:
#         set_date_params('start year: ', 'end year: ', 'yearly')
#
#     sw.switch_cumulative_panels = get_switch_input('Plot cumulative panels? (y/n)\n')
#     if sw.switch_cumulative_panels:
#         lag_a = int(input('lag (in months): '))
#         sw.time_freq_a = pd.DateOffset(months=lag_a)
#         set_date_params('start year: ', 'end year: ', 'cumulative')
#
#     # Field Campaigns and Historical events (y/n)
#     sw.switch_campaigns = get_switch_input('Draw field campaigns? (y/n)\n', True)
#     sw.switch_history = get_switch_input('Draw historical events? (y/n)\n', False)
#     sw.switch_prog_bar = get_switch_input('Draw progress bar? (y/n)\n', False)
#
#     # Displaying the selected instruments
#     print(f'These instruments are plotted: {ts.instr_list}')
#
#     # Plot the panels based on the switches
#     if sw.switch_rolling_panels:
#         plot_rolling_panels()
#
#     if sw.switch_yearly_panels:
#         plot_yearly_panels()
#
#     if sw.switch_cumulative_panels:
#         plot_cumulative_panels()
#
#     print('END')
#
#
# # Running the main function
# if __name__ == "__main__":
#     main()

# if __name__ == "__main__":
#
#     # instrument list selection
#     switch_instr_list = input(
#             'Which category of instruments (Default to : all. Otherwise chose one or more among: current, legacy, macmap, separated by space)\n')
#     if 'all' in switch_instr_list.split():
#         ts.instr_list = ts.instr_list_current + ts.instr_list_legacy + ts.instr_list_macmap
#     if 'macmap' in switch_instr_list.split():
#         ts.instr_list += ts.instr_list_macmap
#     if 'legacy' in switch_instr_list.split():
#         ts.instr_list += ts.instr_list_legacy
#     if 'current' in switch_instr_list.split():
#         ts.instr_list += ts.instr_list_current
#
#     # panel for rolling (for gifs, by i years)
#     switch_rolling_panels = input('Plot rolling panels (y/n)\n')
#     if switch_rolling_panels == 'n':
#         sw.switch_rolling_panels = False
#     elif switch_rolling_panels == 'y':
#         sw.switch_rolling_panels = True
#         window_size = int(input('window size (in months): '))
#         lag_c = int(input('lag (in months): '))
#         sw.time_window_c = pd.DateOffset(months=window_size)
#         sw.time_freq_c = pd.DateOffset(months=lag_c)
#         strt_y = int(input('start year: '))
#         sw.start_c = dt.datetime(strt_y, 1, 1) + sw.time_window_c
#         sw.end_c = dt.datetime.today() + dt.timedelta(minutes=500000)
#
#     # yearly panels
#     switch_yearly_panels = input('Plot yearly panels? (y/n)\n')
#     if switch_yearly_panels == 'n':
#         sw.switch_yearly_panels = False
#     elif switch_yearly_panels == 'y':
#         sw.switch_yearly_panels = True
#         strt_y = int(input('start year: '))
#         sw.start_y = dt.datetime(strt_y, 1, 1)
#         nd_y = int(input('end year: '))
#         sw.end_y = dt.datetime(nd_y, 12, 31)
#
#     # Full panels
#     switch_cumulative_panels = input('Plot cumulative panels? (y/n)\n')
#     if switch_cumulative_panels == 'n':
#         sw.switch_cumulative_panels = False
#     elif switch_cumulative_panels == 'y':
#         sw.switch_cumulative_panels = True
#         strt_y = int(input('start year: '))
#         sw.start_a = dt.datetime(strt_y, 1, 1)
#         nd_y = int(input('end year: '))
#         sw.end_a = dt.datetime(nd_y, 12, 31)
#         # window_size = int(input('window size (in years):'))
#         # time_window = pd.DateOffset(years=window_size)
#         lag_a = int(input('lag (in months): '))
#         sw.time_freq_a = pd.DateOffset(months=lag_a)
#
#     # Field Campaigns
#     switch_campaigns = input('Draw field campaigns? (y/n)\n')
#     if switch_campaigns == 'y':
#         sw.switch_campaigns = True
#     elif switch_campaigns == 'n':
#         sw.switch_campaigns = False
#
#     # Historical events
#     switch_history = input('Draw historical events? (y/n)\n')
#     if switch_history == 'y':
#         sw.switch_history = True
#     elif switch_history == 'n':
#         sw.switch_history = False
#
#     # Time-progress bar
#     switch_prog_bar = input('Draw progress bar? (y/n)\n')
#     if switch_prog_bar == 'y':
#         sw.switch_prog_bar = True
#     elif switch_prog_bar == 'n':
#         sw.switch_prog_bar = False
#
#     print(f'These instruments are plotted: {ts.instr_list}')
#
#     # rolling panels
#     if sw.switch_rolling_panels:
#         plot_rolling_panels()
#
#     # yearly panels
#     if sw.switch_yearly_panels:
#         plot_yearly_panels()
#
#     # cumulative panels
#     if sw.switch_cumulative_panels:
#         plot_cumulative_panels()
#
#     print('END')
#
#     # TODO: develop composition of different pngs into a gif.  #  Until now, I did it manually externally from pyhton using ffmpeg from Unix terminal. See below  # os.system("cd " + os.path.join(fol_out, 'gif'))  # import ffmpeg  # os.system("ffmpeg -f image2 -framerate 1 -pattern_type glob -i 'data_avail_*-*_*_p.png' data_avail_p.mp4")
#
#     # # create animation  # import matplotlib.pyplot as plt  # from matplotlib.animation import FuncAnimation  #  # nframes = 30  # plt.subplots_adjust(top=1, bottom=0, left=0, right=1)  #  # def animate(i):  #     im = plt.imread(os.path.join(fol_out, 'data_avail_1990-' + str(1990 + i) + '.png'))  #     plt.imshow(im)  #  #  # anim = FuncAnimation(plt.gcf(), animate, frames=nframes, interval=(2000.0 / nframes))  # anim.save(os.path.join(fol_out, 'data_avail_1990-' + str(2020) + '.gif'), writer='imagemagick')
#
#     # ffmpeg -f image2 -i image%d.png output.mp4  # ffmpeg -f image2 -framerate 1 -pattern_type glob -i 'data_avail_*-*_*_p.png' output1_p.mp4  # ffmpeg -i output.mp4 -vf "fps=10,scale=320:-1:flags=lanczos" -c:v pam -f image2pipe - | convert -delay 10 - -loop 0 -layers optimize output.gif
#
#     # if switch_yp:  #     print('YEARLY')  #     range_lab =  #     print()  #     images = os.listdir(os.path.join(fol_out, 'yearly'))  #     img_arr = []  #     for image in images:  #         img = Image.open(os.path.join(fol_out, 'yearly', image)).convert('RGB')  #         img = np.asarray(img)  #         img_arr.append(img)  #   #     fig, ax = plt.subplots(figsize=(18, 18))  #     fig.suptitle("THAAO datasets")  #   #     grid = ImageGrid(fig, 111, (6, 6), axes_pad=0, share_all=True, aspect=False, direction='row')  #   #     for (ax, im) in zip(grid, img_arr):  #         ax.imshow(im)  #         ax.xaxis.set_visible(False)  #         ax.yaxis.set_visible(False)  #   #     plt.savefig(  #             os.path.join(fol_out, 'yearly', 'data_avail_yearly_panel_' + range_lab + '.png'),  #             dpi=600)  #     plt.gca()  #     plt.cla()  #     plt.close('all')
