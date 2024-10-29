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

if __name__ == "__main__":
    # panel for cumulative (for gifs, by i years)
    ts.switch_cumulative = input('Plot panels for gif? (yes/no)')
    if ts.switch_cumulative == 'no':
        ts.switch_cumulative = False
    elif ts.switch_cumulative == 'yes':
        ts.switch_cumulative = True
        window_size = int(input('window size (in years):'))  # 5  # in years
        lag_c = int(input('lag (in months):'))  # 3  # in months
        ts.time_window_c = pd.DateOffset(years=window_size)
        ts.time_freq_c = pd.DateOffset(months=lag_c)
        strt_y = int(input('start year:'))
        ts.start_c = dt.datetime(strt_y, 1, 1) + ts.time_window_c  # dt.datetime(1900, 1, 1) + time_window
        ts.end_c = dt.datetime.today() + dt.timedelta(minutes=500000)

    # single-year panels
    ts.switch_yearly = input('Plot single-year panels? (yes/no)')
    if ts.switch_yearly == 'no':
        ts.switch_yearly = False
    elif ts.switch_yearly == 'yes':
        strt_y = int(input('start year:'))
        ts.start_y = dt.datetime(strt_y, 1, 1)
        nd_y = int(input('end year:'))
        ts.end_y = dt.datetime(nd_y, 12, 31)

    # complete plot
    ts.switch_all = input('Plot full panels? (yes/no)')
    if ts.switch_all == 'no':
        ts.switch_all = False
    elif ts.switch_all == 'yes':
        strt_y = int(input('start year:'))
        ts.start_a = dt.datetime(strt_y, 1, 1)
        nd_y = int(input('end year:'))
        ts.end_a = dt.datetime(nd_y, 12, 31)
        window_size = int(input('window size (in years):'))  # 5  # in years
        lag_a = int(input('lag (in months):'))  # 6
        time_window = pd.DateOffset(years=window_size)
        ts.time_freq_a = pd.DateOffset(months=lag_a)

    # Field Campaigns
    switch_campaigns = input('Draw field campaigns? (yes/no)')
    if ts.switch_campaigns == 'yes':
        ts.switch_campaigns = True
    elif ts.switch_campaigns == 'no':
        ts.switch_campaigns = False

    # Historical events
    ts.switch_history = input('Draw historical events? (yes/no)')
    if ts.switch_history == 'yes':
        ts.switch_history = True
    elif ts.switch_history == 'no':
        ts.switch_history = False

    # Time-progress bar
    ts.switch_prog_bar = input('Draw progress bar? (yes/no)')
    if ts.switch_prog_bar == 'yes':
        ts.switch_prog_bar = True
    elif ts.switch_prog_bar == 'no':
        ts.switch_prog_bar = False

    # TODO: instrument selection from input
    # instr_list = input(
    # 'insert list of instruments separated by comma (choosing from: '
    # '\n uv-vis_spec, lidar_ae, o3_sondes, aero_sondes, wv_isotopes, gbms, hatpro,'
    # '\n ftir, aeronet, metar,'
    # '\n rs_sondes, vespa, ceilometer, dir_rad_trkr, pm10, aws(p,T,RH), mms_trios, lidar_temp, skycam, gnss, '
    # '\n ecapac_aws_snow, ecapac_disdro_precip, ecapac_aws, ecapac_mrr, '
    # '\n macmap_tide_gauge, macmap_seismometer_1, macmap_seismometer_2, macmap_seismometer_3, macmap_seismometer_4, '
    # '\n rad_uli, rad_usi,rad_dli, rad_dsi, rad_tb, rad_par_up, rad_par_dow):')

    print(f'These instruments are plotted (hard-coded): {ts.instr_list}')

    # cumulative
    if ts.switch_cumulative:
        plot_cumulative()

    # yearly
    if ts.switch_yearly:
        plot_yearly()

    # all
    if ts.switch_all:
        plot_all()

    # os.system("cd " + os.path.join(fol_out, 'gif'))  # import ffmpeg  # os.system("ffmpeg -f image2 -framerate 1 -pattern_type glob -i 'data_avail_*-*_*_p.png' data_avail_p.mp4")

    # # create animation  # import matplotlib.pyplot as plt  # from matplotlib.animation import FuncAnimation  #  # nframes = 30  # plt.subplots_adjust(top=1, bottom=0, left=0, right=1)  #  # def animate(i):  #     im = plt.imread(os.path.join(fol_out, 'data_avail_1990-' + str(1990 + i) + '.png'))  #     plt.imshow(im)  #  #  # anim = FuncAnimation(plt.gcf(), animate, frames=nframes, interval=(2000.0 / nframes))  # anim.save(os.path.join(fol_out, 'data_avail_1990-' + str(2020) + '.gif'), writer='imagemagick')

    # ffmpeg -f image2 -i image%d.png output.mp4  # ffmpeg -f image2 -framerate 1 -pattern_type glob -i 'data_avail_*-*_*_p.png' output1_p.mp4  # ffmpeg -i output.mp4 -vf "fps=10,scale=320:-1:flags=lanczos" -c:v pam -f image2pipe - | convert -delay 10 - -loop 0 -layers optimize output.gif

    # if switch_yp:  #     print('YEARLY')  #     range_lab =  #     print()  #     images = os.listdir(os.path.join(fol_out, 'yearly'))  #     img_arr = []  #     for image in images:  #         img = Image.open(os.path.join(fol_out, 'yearly', image)).convert('RGB')  #         img = np.asarray(img)  #         img_arr.append(img)  #   #     fig, ax = plt.subplots(figsize=(18, 18))  #     fig.suptitle("THAAO datasets")  #   #     grid = ImageGrid(fig, 111, (6, 6), axes_pad=0, share_all=True, aspect=False, direction='row')  #   #     for (ax, im) in zip(grid, img_arr):  #         ax.imshow(im)  #         ax.xaxis.set_visible(False)  #         ax.yaxis.set_visible(False)  #   #     plt.savefig(  #             os.path.join(fol_out, 'yearly', 'data_avail_yearly_panel_' + range_lab + '.png'),  #             dpi=600)  #     plt.gca()  #     plt.cla()  #     plt.close('all')
