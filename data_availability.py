#!/usr/local/bin/python3
# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------------
#
"""
Brief description
"""

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
__lastupdate__ = "October 2024"

from plots import *
import settings as ts

if __name__ == "__main__":

    # instrument list selection
    switch_instr_list = input(
            'Which category of instruments (Default to : all. Otherwise chose one or more among: current, legacy, macmap, separated by space)\n')
    if 'all' in switch_instr_list.split():
        ts.instr_list = ts.instr_list_current + ts.instr_list_legacy + ts.instr_list_macmap
    if 'macmap' in switch_instr_list.split():
        ts.instr_list += ts.instr_list_macmap
    if 'legacy' in switch_instr_list.split():
        ts.instr_list += ts.instr_list_legacy
    if 'current' in switch_instr_list.split():
        ts.instr_list += ts.instr_list_current

    # panel for rolling (for gifs, by i years)
    switch_rolling_panels = input('Plot rolling panels (yes/no)\n')
    if switch_rolling_panels == 'no':
        sw.switch_rolling_panels = False
    elif switch_rolling_panels == 'yes':
        sw.switch_rolling_panels = True
        window_size = int(input('window size (in months): '))
        lag_c = int(input('lag (in months): '))
        sw.time_window_c = pd.DateOffset(months=window_size)
        sw.time_freq_c = pd.DateOffset(months=lag_c)
        strt_y = int(input('start year: '))
        sw.start_c = dt.datetime(strt_y, 1, 1) + sw.time_window_c
        sw.end_c = dt.datetime.today() + dt.timedelta(minutes=500000)

    # yearly panels
    switch_yearly_panels = input('Plot yearly panels? (yes/no)\n')
    if switch_yearly_panels == 'no':
        sw.switch_yearly_panels = False
    elif switch_yearly_panels == 'yes':
        sw.switch_yearly_panels = True
        strt_y = int(input('start year: '))
        sw.start_y = dt.datetime(strt_y, 1, 1)
        nd_y = int(input('end year: '))
        sw.end_y = dt.datetime(nd_y, 12, 31)

    # Full panels
    switch_cumulative_panels = input('Plot cumulative panels? (yes/no)\n')
    if switch_cumulative_panels == 'no':
        sw.switch_cumulative_panels = False
    elif switch_cumulative_panels == 'yes':
        sw.switch_cumulative_panels = True
        strt_y = int(input('start year: '))
        sw.start_a = dt.datetime(strt_y, 1, 1)
        nd_y = int(input('end year: '))
        sw.end_a = dt.datetime(nd_y, 12, 31)
        # window_size = int(input('window size (in years):'))
        # time_window = pd.DateOffset(years=window_size)
        lag_a = int(input('lag (in months): '))
        sw.time_freq_a = pd.DateOffset(months=lag_a)

    # Field Campaigns
    switch_campaigns = input('Draw field campaigns? (yes/no)\n')
    if switch_campaigns == 'yes':
        sw.switch_campaigns = True
    elif switch_campaigns == 'no':
        sw.switch_campaigns = False

    # Historical events
    switch_history = input('Draw historical events? (yes/no)\n')
    if switch_history == 'yes':
        sw.switch_history = True
    elif switch_history == 'no':
        sw.switch_history = False

    # Time-progress bar
    switch_prog_bar = input('Draw progress bar? (yes/no)\n')
    if switch_prog_bar == 'yes':
        sw.switch_prog_bar = True
    elif switch_prog_bar == 'no':
        sw.switch_prog_bar = False

    print(f'These instruments are plotted (hard-coded): {ts.instr_list}')

    # rolling panels
    if sw.switch_rolling_panels:
        plot_rolling_panels()

    # yearly panels
    if sw.switch_yearly_panels:
        plot_yearly_panels()

    # cumulative panels
    if sw.switch_cumulative_panels:
        plot_cumulative_panels()

    # TODO: develop composition of different pngs into a gif.  #  Until now, I did it manually externally from pyhton using ffmpeg from Unix terminal. See below  # os.system("cd " + os.path.join(fol_out, 'gif'))  # import ffmpeg  # os.system("ffmpeg -f image2 -framerate 1 -pattern_type glob -i 'data_avail_*-*_*_p.png' data_avail_p.mp4")

    # # create animation  # import matplotlib.pyplot as plt  # from matplotlib.animation import FuncAnimation  #  # nframes = 30  # plt.subplots_adjust(top=1, bottom=0, left=0, right=1)  #  # def animate(i):  #     im = plt.imread(os.path.join(fol_out, 'data_avail_1990-' + str(1990 + i) + '.png'))  #     plt.imshow(im)  #  #  # anim = FuncAnimation(plt.gcf(), animate, frames=nframes, interval=(2000.0 / nframes))  # anim.save(os.path.join(fol_out, 'data_avail_1990-' + str(2020) + '.gif'), writer='imagemagick')

    # ffmpeg -f image2 -i image%d.png output.mp4  # ffmpeg -f image2 -framerate 1 -pattern_type glob -i 'data_avail_*-*_*_p.png' output1_p.mp4  # ffmpeg -i output.mp4 -vf "fps=10,scale=320:-1:flags=lanczos" -c:v pam -f image2pipe - | convert -delay 10 - -loop 0 -layers optimize output.gif

    # if switch_yp:  #     print('YEARLY')  #     range_lab =  #     print()  #     images = os.listdir(os.path.join(fol_out, 'yearly'))  #     img_arr = []  #     for image in images:  #         img = Image.open(os.path.join(fol_out, 'yearly', image)).convert('RGB')  #         img = np.asarray(img)  #         img_arr.append(img)  #   #     fig, ax = plt.subplots(figsize=(18, 18))  #     fig.suptitle("THAAO datasets")  #   #     grid = ImageGrid(fig, 111, (6, 6), axes_pad=0, share_all=True, aspect=False, direction='row')  #   #     for (ax, im) in zip(grid, img_arr):  #         ax.imshow(im)  #         ax.xaxis.set_visible(False)  #         ax.yaxis.set_visible(False)  #   #     plt.savefig(  #             os.path.join(fol_out, 'yearly', 'data_avail_yearly_panel_' + range_lab + '.png'),  #             dpi=600)  #     plt.gca()  #     plt.cla()  #     plt.close('all')
