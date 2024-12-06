#!/usr/local/bin/python3
# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------------
#
"""
Brief description
"""

# =============================================================
# CREATED: 
# AFFILIATION: UNIVE, INGV
# AUTHORS: Filippo Cali' Quaglia
# =============================================================
#
# -------------------------------------------------------------------------------
__author__ = "Filippo Cali' Quaglia"
__credits__ = ["??????"]
__license__ = "GPL"
__version__ = "0.1"
__email__ = "filippo.caliquaglia@gmail.com"
__status__ = "Research"
__lastupdate__ = ""

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

import settings as ts
import switches as sw
import tools as tls

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
        if (ii.month > pd.Timestamp(ts.instr_metadata.get(ts.instr_list[idx])['end_seas']).month) | (
                ii.month < pd.Timestamp(ts.instr_metadata.get(ts.instr_list[idx])['start_seas']).month):
            if data_na['mask'].iloc[i] != True:
                data_na.loc[ii, 'mask'] = True
        else:
            data_na.loc[ii, 'mask'] = False

    # excluding instrument missing or not installed
    for i, ii in enumerate(data_na.index):
        if (ii < pd.Timestamp(ts.instr_metadata.get(ts.instr_list[idx])['start_instr'])) | (
                ii > pd.Timestamp(ts.instr_metadata.get(ts.instr_list[idx])['end_instr'])):
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

    # axx.set_xticks(list(np.arange(0, i_length)))
    # axx.set_xticklabels(axx.get_xticklabels(), fontsize=14)
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
            mx = len(ts.instr_list) + 1
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


def draw_data_avail(a1, a2):
    """

    :param a1:
    :param a2:
    :return:
    """
    # with plt.xkcd():
    # fig, ax = plt.subplots(figsize=(15, 10))
    fig = plt.figure(figsize=(15, 10))
    ax = fig.add_axes([0.15, 0.1, 0.7, 0.8])
    ax2 = ax.twinx()
    i_labs = []
    for instr_idx, instr_name in enumerate(ts.instr_list):
        inp_file, i_labs = tls.input_file_selection(instr_idx, i_labs, instr_name)
        plot_data_avail(ax, inp_file, a1, a2, instr_idx)
    if sw.switch_history:
        draw_events(ax, a1, a2)
    if sw.switch_campaigns:
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
    """

    :param n_dir:
    :param range_lab_f:
    :param strt_ff:
    :param end_ff:
    :param jj:
    :return:
    """
    # create image or load your existing image with out=Image.open(path)
    out = Image.open(os.path.join(n_dir, 'thaao_data_avail_' + range_lab_f + '.png')).convert('RGBA')
    d = ImageDraw.Draw(out)
    # draw the progress bar to given location, width, progress and color
    progress = (jj.year - strt_ff.year) / (end_ff.year - strt_ff.year)
    d = drawProgressBar(d, 50 * dpi_fac, 180 * dpi_fac, 4300 * dpi_fac, 60 * dpi_fac, progress, 'grey', 'blue')
    out.save(os.path.join(n_dir, f'thaao_data_avail_{range_lab_f}_p.png'))
    return


def drawProgressBar(d, x, y, w, h, progress_func, bg="black", fg="red"):
    """

    :param d:
    :param x:
    :param y:
    :param w:
    :param h:
    :param progress_func:
    :param bg:
    :param fg:
    :return:
    """
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


def plot_cumulative_panels():
    """

    :return:
    """
    print('CUMULATIVE')
    newdir = os.path.join(ts.da_folder, 'gif', f'{ts.start_c.year}-{ts.end_c.year}')
    os.makedirs(newdir, exist_ok=True)
    j = cp.copy(ts.start_c)
    while j + ts.time_window_c <= ts.end_c + ts.time_window_c:
        yyyy1, yyyy2 = (j - ts.time_window_c, j)
        range_lab = dt.datetime.strftime(yyyy1, '%Y%m') + '_' + dt.datetime.strftime(yyyy2, '%Y%m')
        print(range_lab)
        ffig = draw_data_avail(yyyy1, yyyy2)
        plt.suptitle(
                dt.datetime.strftime(yyyy1, '%b %Y') + ' to ' + dt.datetime.strftime(yyyy2, '%b %Y'), fontsize=20)

        plt.savefig(os.path.join(newdir, 'thaao_data_avail_' + range_lab + '.png'), dpi=dpi, transparent=True)
        plt.gca()
        plt.cla()
        gc.collect()
        plt.close(ffig)

        if sw.switch_prog_bar:
            draw_progress_bar(newdir, range_lab, ts.start_c, ts.end_c, j)

        j += ts.time_freq_c
    return


def plot_yearly_panels():
    """
    :return:
    """
    print('YEARLY')
    newdir = os.path.join(ts.da_folder, 'yearly')
    j = cp.copy(ts.start_y)
    j1 = j + pd.DateOffset(years=1)
    while j1 <= ts.end_y:
        print(j)
        range_lab = dt.datetime.strftime(j, '%Y')
        ffig = draw_data_avail(j, j1)
        plt.suptitle(dt.datetime.strftime(j, '%b-%Y') + ' to ' + dt.datetime.strftime(j1, '%b-%Y'))
        plt.gcf().autofmt_xdate()
        plt.savefig(os.path.join(newdir, 'thaao_data_avail_' + range_lab + '.png'), dpi=dpi)
        plt.gca()
        plt.cla()
        gc.collect()
        plt.close(ffig)

        j += pd.DateOffset(years=1)
        j1 += pd.DateOffset(years=1)

    return


def plot_full_panels():
    """

    :return:
    """
    print('FULL')
    newdir = os.path.join(ts.da_folder, 'full', str(ts.start_a.year) + '-' + str(ts.end_a.year))
    os.makedirs(newdir, exist_ok=True)
    j = cp.copy(ts.start_a) + ts.time_freq_a
    while j <= ts.end_a:
        yyyy1, yyyy2 = (ts.start_a, j)
        range_lab = dt.datetime.strftime(yyyy1, '%Y%m') + '_' + dt.datetime.strftime(yyyy2, '%Y%m')
        print(range_lab)
        ffig = draw_data_avail(ts.start_a, j)
        plt.suptitle(dt.datetime.strftime(ts.start_a, '%b-%Y') + ' to ' + dt.datetime.strftime(j, '%b-%Y'))
        plt.gcf().autofmt_xdate()
        plt.savefig(os.path.join(newdir, f'thaao_data_avail_{range_lab}.png'), dpi=dpi)
        plt.gca()
        plt.cla()
        gc.collect()
        plt.close(ffig)
        j += ts.time_freq_a

    return
