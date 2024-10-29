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

import copy as cp
import datetime as dt
import gc
import os

import matplotlib.dates as mdates
import matplotlib.patches as patches
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.lines import Line2D
from matplotlib.pyplot import cm
from PIL import Image, ImageDraw

import thaao_settings as ts

dpi_fac = 2  # if increased, dpi resolution increases
dpi = 300 * dpi_fac


def plot_data_avail(ax, inp, yy1, yy2, idx):
    """

    :param ax:
    :param idx:
    :param inp:
    :param yy1:
    :param yy2:
    :return:
    """

    # data
    try:
        data_val = pd.read_table(inp, sep=' ')
        data_val.columns = ['date', 'time', 'mask']
        data_val = data_val.set_index(pd.DatetimeIndex(data_val['date'] + 'T' + data_val['time']))
        data_val = data_val.drop(columns=['date', 'time'])
        missing_switch = 0
    except FileNotFoundError:
        missing_switch = 1
        data_val = pd.DataFrame(data=np.empty((0, 2)))
        data_val.columns = ['datetime', 'mask']
        data_val['datetime'] = pd.date_range(dt.datetime(1900, 1, 1), dt.datetime.today(), freq='720min')
        data_val = data_val.set_index(pd.DatetimeIndex(data_val['datetime']))
        data_val = data_val.drop(columns=['datetime'])
        data_val['mask'] = True

    if missing_switch == 0:
        data_val = data_val[(data_val.index >= yy1) & (data_val.index <= yy2)]

        # data na
        data_na = pd.DataFrame()
        data_na['date'] = pd.date_range(yy1, yy2, freq='720min')
        data_na['mask'] = np.empty(data_na['date'].shape)
        data_na['mask'] = False
        data_na.index = data_na['date']
        data_na.drop(columns=['date'], inplace=True)

        # excluding seasonal unavailability
        for i, ii in enumerate(data_na.index):
            if (ii.month > pd.Timestamp(ts.instr_metadata.get(instr_list[idx])['end_seas']).month) | (
                    ii.month < pd.Timestamp(ts.instr_metadata.get(instr_list[idx])['start_seas']).month):
                if data_na['mask'].iloc[i] != True:
                    data_na.loc[ii, 'mask'] = True
            else:
                data_na.loc[ii, 'mask'] = False

        # excluding instrument missing or not installed
        for i, ii in enumerate(data_na.index):
            if (ii < pd.Timestamp(ts.instr_metadata.get(instr_list[idx])['start_instr'])) | (
                    ii > pd.Timestamp(ts.instr_metadata.get(instr_list[idx])['end_instr'])):
                data_na.loc[ii, 'mask'] = True
            else:
                pass

        data_na = data_na['mask'].astype('int')
        ys_1 = np.repeat(idx, len(data_na.index[data_na == 1].values))
        ax.errorbar(
                data_na.index[data_na == 1].values, ys_1, xerr=None, yerr=0.3, fmt='.', color='lightgrey', capsize=0,
                markersize=0)

        # plot data
    if missing_switch == 0:
        color = cm.rainbow(np.linspace(0, 1, 40))
        color = color[idx]
    else:
        color = 'black'
    data_val = data_val['mask'].astype('int')
    ys = np.repeat(idx, len(data_val.index[data_val == 1].values))
    ax.errorbar(
            data_val.index[data_val == 1].values, ys, xerr=None, yerr=0.3, fmt='.', color=color, capsize=0,
            markersize=0)

    del data_val

    return


def input_file_selection(i_idx, i_list, i_name):
    """

    :param i_idx:
    :param i_list:
    :param i_name:
    :return:
    """
    try:
        print(f'{i_idx:02}' + ' ' + i_name)
        # if i_name[0:3] == 'rad':
        #     inp_file = os.path.join(fol_input, 'thaao_rad', i_name + '_data_avail_list.txt')
        if i_name[0:3] == 'aws':
            inp_file = os.path.join(ts.basefolder, 'thaao_meteo', i_name + '_data_avail_list.txt')
        # elif i_name[0:5] == 'lidar':
        #     inp_file = os.path.join(fol_input, 'thaao_lidar', i_name + '_data_avail_list.txt')
        # elif i_name[0:5] == 'metar':
        #     inp_file = os.path.join(fol_input, i_name + '_data_avail_list.txt')
        # elif i_name[0:13] == 'macmap_seismometers':
        #     inp_file = os.path.join(fol_input, 'thaao_macmap_seismometers', i_name + '_data_avail_list.txt')
        # elif (i_name[0:11] == 'ecapac_snow') | (i_name[0:10] == 'ecapac_aws'):
        #     inp_file = os.path.join(fol_input, 'thaao_ecapac_aws_snow', i_name + '_data_avail_list.txt')
        else:
            inp_file = os.path.join(ts.basefolder, 'thaao_' + i_name, i_name + '_data_avail_list.txt')
        i_list.append(i_name)
    except FileNotFoundError:
        inp_file = None
        print('file for ' + i_name + ' was not found')

    return inp_file, i_list


def ax_style(axx, yy1, yy2, i_labs, i_length):
    """

    :param axx:
    :param i_length:
    :param i_labs:
    :param yy1:
    :param yy2:
    :return:
    """

    axx.set_xlim(yy1, yy2)
    axx.set_ylim(-1, i_length)
    if yy2.year - yy1.year > 10:
        myFmt = mdates.DateFormatter('%Y')
    else:
        myFmt = mdates.DateFormatter('%b-%Y')
    axx.xaxis.set_major_formatter(myFmt)
    axx.set_xticklabels(axx.get_xticklabels(), fontsize=14)
    axx.set_yticks(list(np.arange(0, i_length)))
    axx.set_yticklabels(i_labs)
    for ytick in axx.get_yticklabels():
        if ts.instr_metadata.get(ytick.get_text())['end_instr'] < yy1:
            ytick.set_color('grey')
        elif ts.instr_metadata.get(ytick.get_text())['start_instr'] > yy2:
            ytick.set_color('grey')
        else:
            ytick.set_color(
                    ts.institution_colors[ts.instr_metadata.get(ytick.get_text())['institution']])
            ytick.set_fontweight('bold')
    return


def draw_events(ax, a1, a2):
    """

    :param ax:
    :param a1:
    :param a2:
    :return:
    """
    for event, event_idx in zip(ts.events_dict.values(), ts.events_dict.keys()):
        if event['date'] in pd.date_range(a1, a2):
            mx = len(instr_list) + 1
            ax.vlines(x=event['date'], ymin=-1., ymax=mx, color='grey', ls='dotted')
            np.random.seed(event_idx)
            ax.text(
                    event['date'], np.random.randint(0, mx), event['label'], fontweight='bold', bbox=dict(
                            facecolor='white', edgecolor='black', boxstyle='round,pad=1', alpha=0.8), zorder=10)

    return


def draw_campaigns(ax, a1, a2):
    """

    :param ax:
    :param a1:
    :param a2:
    :return:
    """
    for campaign_idx, campaign in enumerate(ts.campaigns_dict.values()):
        if campaign['start'] in pd.date_range(a1, a2):
            ax.axvspan(
                    campaign['start'], campaign['end'], alpha=0.3, color='cyan', label='Field campaign', zorder=10)

    return


def draw_data_avail(a1, a2, i_list):
    """

    :param a1:
    :param a2:
    :param i_list:
    :return:
    """
    # with plt.xkcd():
    # fig, ax = plt.subplots(figsize=(15, 10))
    fig = plt.figure(figsize=(15, 10))
    ax = fig.add_axes([0.15, 0.1, 0.7, 0.8])
    ax2 = ax.twinx()
    i_labs = []
    for instr_idx, instr_name in enumerate(i_list):
        inp_file, i_labs = input_file_selection(instr_idx, i_labs, instr_name)
        plot_data_avail(ax, inp_file, a1, a2, instr_idx)
    if switch_history:
        draw_events(ax, a1, a2)
    if switch_campaigns:
        draw_campaigns(ax, a1, a2)
    ax_style(ax, a1, a2, i_labs, len(i_labs))
    ax_style(ax2, a1, a2, i_labs, len(i_labs))
    # legend of institutions
    legend_elements = []
    legend_colors = []
    for idx, elem in enumerate(ts.institution_colors.keys()):
        legend_elements.append(
                Line2D(
                        [0], [0], marker='', markersize=0, lw=0, color=ts.institution_colors.get(elem), label=elem))
        legend_colors.append(ts.institution_colors.get(elem))
    # N/A legend
    # campaign legend
    rect1 = patches.Rectangle((0, 0), 1, 1, facecolor='cyan', label='Field Campaign')
    rect2 = patches.Rectangle((0, 0), 1, 1, facecolor='black', label='N/A')
    legend_elements.append(rect1)
    legend_colors.append('cyan')
    legend_elements.append(rect2)
    legend_colors.append('black')
    ax.legend(
            handles=legend_elements, loc='upper center', bbox_to_anchor=(0.5, -0.05), fancybox=True, shadow=True,
            ncol=6, labelcolor=legend_colors, prop={'weight': 'bold'})
    return fig


def draw_progress_bar(n_dir, range_lab_f, strt_ff, end_ff, jj):
    # create image or load your existing image with out=Image.open(path)
    out = Image.open(os.path.join(n_dir, 'data_avail_' + range_lab_f + '.png')).convert('RGBA')
    d = ImageDraw.Draw(out)
    # draw the progress bar to given location, width, progress and color
    progress = (jj.year - strt_ff.year) / (end_ff.year - strt_ff.year)
    d = drawProgressBar(d, 50 * dpi_fac, 180 * dpi_fac, 4300 * dpi_fac, 60 * dpi_fac, progress, 'grey', 'blue')
    out.save(os.path.join(n_dir, f'data_avail_{range_lab_f}_p.png'))


def drawProgressBar(d, x, y, w, h, progress_func, bg="black", fg="red"):
    # draw background
    d.ellipse((x + w, y, x + h + w, y + h), fill=bg)
    d.ellipse((x, y, x + h, y + h), fill=bg)
    d.rectangle((x + (h / 2), y, x + w + (h / 2), y + h), fill=bg)

    # draw progress bar
    w *= progress_func
    d.ellipse((x + w, y, x + h + w, y + h), fill=fg)
    d.ellipse((x, y, x + h, y + h), fill=fg)
    d.rectangle((x + (h / 2), y, x + w + (h / 2), y + h), fill=fg)

    return d


def plot_cumulative(fol, strt_f, end_f, tm_win_f, tm_freq_f, instr_l):
    """

    :param fol:
    :param strt_f:
    :param end_f:
    :param tm_win_f:
    :param tm_freq_f:
    :param instr_l:
    :return:
    """
    print('CUMULATIVE')
    newdir = os.path.join(fol, 'gif', f'{strt_f.year}-{end_f.year}')
    os.makedirs(newdir, exist_ok=True)
    j = cp.copy(strt_f)
    while j + tm_win_f <= end_f + tm_win_f:
        yyyy1, yyyy2 = (j - tm_win_f, j)
        range_lab = dt.datetime.strftime(yyyy1, '%Y%m') + '_' + dt.datetime.strftime(yyyy2, '%Y%m')
        print(range_lab)
        ffig = draw_data_avail(yyyy1, yyyy2, instr_l)
        plt.suptitle(
                dt.datetime.strftime(yyyy1, '%b %Y') + ' to ' + dt.datetime.strftime(yyyy2, '%b %Y'), fontsize=20)
        # plt.gcf().autofmt_xdate()
        plt.savefig(os.path.join(newdir, 'data_avail_' + range_lab + '.png'), dpi=dpi, transparent=True)
        plt.gca()
        plt.cla()
        gc.collect()
        plt.close(ffig)

        if switch_prog_bar:
            draw_progress_bar(newdir, range_lab, strt_f, end_f, j)

        j += tm_freq_f
    return


def plot_yearly(fol, strt_f, end_f, instr_l):
    """

    :param fol:
    :param strt_f:
    :param end_f:
    :param instr_l:
    :return:
    """
    print('YEARLY')
    j = cp.copy(strt_f)
    j1 = j + pd.DateOffset(years=1)
    while j1 <= end_f:
        print(j1)
        range_lab = dt.datetime.strftime(j, '%Y-%m')
        ffig = draw_data_avail(j, j1, instr_l)
        plt.suptitle(dt.datetime.strftime(j, '%b-%Y') + ' to ' + dt.datetime.strftime(j1, '%b-%Y'))
        plt.gcf().autofmt_xdate()
        plt.savefig(os.path.join(fol, 'yearly', 'data_avail_' + range_lab + '.png'), dpi=dpi)
        plt.gca()
        plt.cla()
        gc.collect()
        plt.close(ffig)

        j += pd.DateOffset(years=1)
        j1 += pd.DateOffset(years=1)

    return


def plot_all(fol, strt_f, end_f, tm_freq_f, instr_l):
    """

    :param end_f:
    :param fol:
    :param strt_f:
    :param tm_freq_f:
    :param instr_l:
    :return:
    """
    print('ALL')
    newdir = os.path.join(fol, 'all', str(strt_f.year) + '-' + str(end_f.year))
    os.makedirs(newdir, exist_ok=True)
    j = cp.copy(strt_f) + tm_freq_f
    while j <= end_f:
        yyyy1, yyyy2 = (strt_f, j)
        range_lab = dt.datetime.strftime(yyyy1, '%Y%m') + '_' + dt.datetime.strftime(yyyy2, '%Y%m')
        print(range_lab)
        ffig = draw_data_avail(strt_f, j, instr_l)
        plt.suptitle(dt.datetime.strftime(strt_f, '%b-%Y') + ' to ' + dt.datetime.strftime(j, '%b-%Y'))
        plt.gcf().autofmt_xdate()
        plt.savefig(os.path.join(newdir, f'data_avail_{range_lab}.png'), dpi=dpi)
        plt.gca()
        plt.cla()
        gc.collect()
        plt.close(ffig)
        j += tm_freq_f

    return


if __name__ == "__main__":

    folder = os.path.join(ts.basefolder, 'thaao_data_availability')

    # INPUTS

    # panel for gifs (by i years)
    switch_gif = input('Plot panels for gif? (yes/no)')
    if switch_gif == 'no':
        switch_gif = False
    elif switch_gif == 'yes':
        switch_gif = True
        window_size = int(input('window size (in years):'))  # 5  # in years
        lag_g = int(input('lag (in months):'))  # 3  # in months
        time_window_g = pd.DateOffset(years=window_size)
        time_freq_g = pd.DateOffset(months=lag_g)
        strt_y = int(input('start year:'))
        start_g = dt.datetime(strt_y, 1, 1) + time_window_g  # dt.datetime(1900, 1, 1) + time_window
        end_g = dt.datetime.today() + dt.timedelta(minutes=500000)

    # single-year panels
    switch_yearly = input('Plot single-year panels? (yes/no)')
    if switch_yearly == 'no':
        switch_yearly = False
    elif switch_yearly == 'yes':
        strt_y = int(input('start year:'))
        start_y = dt.datetime(strt_y, 1, 1)
        nd_y = int(input('end year:'))
        end_y = dt.datetime(nd_y, 12, 31)

    # complete plot
    switch_all = input('Plot full panels? (yes/no)')
    if switch_all == 'no':
        switch_all = False
    elif switch_all == 'yes':
        strt_y = int(input('start year:'))
        start_a = dt.datetime(strt_y, 1, 1)
        nd_y = int(input('end year:'))
        end_a = dt.datetime(nd_y, 12, 31)
        window_size = int(input('window size (in years):'))  # 5  # in years
        lag_a = int(input('lag (in months):'))  # 6
        time_window = pd.DateOffset(years=window_size)
        time_freq_a = pd.DateOffset(months=lag_a)

    # Field Campaigns
    switch_campaigns = input('Draw field campaigns? (yes/no)')
    if switch_campaigns == 'yes':
        switch_campaigns = True
    elif switch_campaigns == 'no':
        switch_campaigns = False

    # Historical events
    switch_history = input('Draw historical events? (yes/no)')
    if switch_history == 'yes':
        switch_history = True
    elif switch_history == 'no':
        switch_history = False

    # Time-progress bar
    switch_prog_bar = input('Draw historical events? (yes/no)')
    if switch_prog_bar == 'yes':
        switch_prog_bar = True
    elif switch_prog_bar == 'no':
        switch_prog_bar = False

    # instr_list = input(
    #         'insert list of instruments separated by comma (choosing from: '
    #         '\n uv-vis_spec, lidar_ae, o3_sondes, aero_sondes, wv_isotopes, gbms, hatpro,'
    #         '\n ftir, aeronet, metar,'
    #         '\n rs_sondes, vespa, ceilometer, dir_rad_trkr, pm10, aws(p,T,RH), mms_trios, lidar_temp, skycam, gnss, '
    #         '\n ecapac_aws_snow, ecapac_disdro_precip, ecapac_aws, ecapac_mrr, '
    #         '\n macmap_tide_gauge, macmap_seismometer_1, macmap_seismometer_2, macmap_seismometer_3, macmap_seismometer_4, '
    #         '\n rad_uli, rad_usi,rad_dli, rad_dsi, rad_tb, rad_par_up, rad_par_dow):')

    instr_list = ['uv-vis_spec', 'lidar_ae', 'o3_sondes', 'aero_sondes', 'rs_sondes', 'gbms', 'wv_isotopes', 'metar',
                  'vespa', 'ceilometer', 'hatpro', 'dir_rad_trkr', 'pm10', 'ftir', 'aeronet', 'ecapac_mrr',
                  # 'ecapac_aws_snow', 'ecapac_disdro_precip', 'ecapac_aws', 'aws(p,T,RH)', 'mms_trios', 'lidar_temp',
                  # 'skycam', 'gnss', 'macmap_seismometer_1', 'macmap_seismometer_2', 'macmap_seismometer_3',
                  # 'macmap_seismometer_4', 'macmap_tide_gauge', 'rad_uli', 'rad_usi', 'rad_dli', 'rad_dsi', 'rad_tb',
                  'rad_par_up', 'rad_par_down']
    print(f'These instruments are plotted (hard-coded): {instr_list}')

    # cumulative
    if switch_gif:
        plot_cumulative(folder, start_g, end_g, time_window_g, time_freq_g, instr_list)

    # yearly
    if switch_yearly:
        plot_yearly(folder, start_y, end_y, instr_list)

    # all
    if switch_all:
        plot_all(folder, start_a, end_a, time_freq_a, instr_list)

    # os.system("cd " + os.path.join(fol_out, 'gif'))  # import ffmpeg  # os.system("ffmpeg -f image2 -framerate 1 -pattern_type glob -i 'data_avail_*-*_*_p.png' data_avail_p.mp4")

    # # create animation  # import matplotlib.pyplot as plt  # from matplotlib.animation import FuncAnimation  #  # nframes = 30  # plt.subplots_adjust(top=1, bottom=0, left=0, right=1)  #  # def animate(i):  #     im = plt.imread(os.path.join(fol_out, 'data_avail_1990-' + str(1990 + i) + '.png'))  #     plt.imshow(im)  #  #  # anim = FuncAnimation(plt.gcf(), animate, frames=nframes, interval=(2000.0 / nframes))  # anim.save(os.path.join(fol_out, 'data_avail_1990-' + str(2020) + '.gif'), writer='imagemagick')

    # ffmpeg -f image2 -i image%d.png output.mp4  # ffmpeg -f image2 -framerate 1 -pattern_type glob -i 'data_avail_*-*_*_p.png' output1_p.mp4  # ffmpeg -i output.mp4 -vf "fps=10,scale=320:-1:flags=lanczos" -c:v pam -f image2pipe - | convert -delay 10 - -loop 0 -layers optimize output.gif

    # if switch_yp:  #     print('YEARLY')  #     range_lab =  #     print()  #     images = os.listdir(os.path.join(fol_out, 'yearly'))  #     img_arr = []  #     for image in images:  #         img = Image.open(os.path.join(fol_out, 'yearly', image)).convert('RGB')  #         img = np.asarray(img)  #         img_arr.append(img)  #   #     fig, ax = plt.subplots(figsize=(18, 18))  #     fig.suptitle("THAAO datasets")  #   #     grid = ImageGrid(fig, 111, (6, 6), axes_pad=0, share_all=True, aspect=False, direction='row')  #   #     for (ax, im) in zip(grid, img_arr):  #         ax.imshow(im)  #         ax.xaxis.set_visible(False)  #         ax.yaxis.set_visible(False)  #   #     plt.savefig(  #             os.path.join(fol_out, 'yearly', 'data_avail_yearly_panel_' + range_lab + '.png'),  #             dpi=600)  #     plt.gca()  #     plt.cla()  #     plt.close('all')
