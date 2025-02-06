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

#     # TODO: develop composition of different pngs into a gif.  #  Until now, I did it manually externally from pyhton using ffmpeg from Unix terminal. See below  # os.system("cd " + os.path.join(fol_out, 'gif'))  # import ffmpeg  # os.system("ffmpeg -f image2 -framerate 1 -pattern_type glob -i 'data_avail_*-*_*_p.png' data_avail_p.mp4")
#
#     # # create animation  # import matplotlib.pyplot as plt  # from matplotlib.animation import FuncAnimation  #  # nframes = 30  # plt.subplots_adjust(top=1, bottom=0, left=0, right=1)  #  # def animate(i):  #     im = plt.imread(os.path.join(fol_out, 'data_avail_1990-' + str(1990 + i) + '.png'))  #     plt.imshow(im)  #  #  # anim = FuncAnimation(plt.gcf(), animate, frames=nframes, interval=(2000.0 / nframes))  # anim.save(os.path.join(fol_out, 'data_avail_1990-' + str(2020) + '.gif'), writer='imagemagick')
#
#     # ffmpeg -f image2 -i image%d.png output.mp4  # ffmpeg -f image2 -framerate 1 -pattern_type glob -i 'data_avail_*-*_*_p.png' output1_p.mp4  # ffmpeg -i output.mp4 -vf "fps=10,scale=320:-1:flags=lanczos" -c:v pam -f image2pipe - | convert -delay 10 - -loop 0 -layers optimize output.gif
#
#     # if switch_yp:  #     print('YEARLY')  #     range_lab =  #     print()  #     images = os.listdir(os.path.join(fol_out, 'yearly'))  #     img_arr = []  #     for image in images:  #         img = Image.open(os.path.join(fol_out, 'yearly', image)).convert('RGB')  #         img = np.asarray(img)  #         img_arr.append(img)  #   #     fig, ax = plt.subplots(figsize=(18, 18))  #     fig.suptitle("THAAO datasets")  #   #     grid = ImageGrid(fig, 111, (6, 6), axes_pad=0, share_all=True, aspect=False, direction='row')  #   #     for (ax, im) in zip(grid, img_arr):  #         ax.imshow(im)  #         ax.xaxis.set_visible(False)  #         ax.yaxis.set_visible(False)  #   #     plt.savefig(  #             os.path.join(fol_out, 'yearly', 'data_avail_yearly_panel_' + range_lab + '.png'),  #             dpi=600)  #     plt.gca()  #     plt.cla()  #     plt.close('all')
