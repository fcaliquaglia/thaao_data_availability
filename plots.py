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

import matplotlib.dates as mdates
import matplotlib.patches as patches
import numpy as np
from matplotlib.lines import Line2D
from matplotlib.pyplot import cm
from PIL import Image, ImageDraw

import settings as ts
import switches as sw
import tools as tls

dpi_fac = 2  # if increased, dpi resolution increases
dpi = 300 * dpi_fac

import numpy as np
import pandas as pd
import matplotlib.cm as cm
import matplotlib.pyplot as plt


def plot_data_avail(ax, inp, yy1, yy2, idx):
    """Optimized function to plot data availability"""

    # Try reading the data
    try:
        data_val = pd.read_table(inp, sep=' ')
        data_val.columns = ['date', 'time', 'mask']
        data_val['datetime'] = pd.to_datetime(data_val['date'] + ' ' + data_val['time'])
        data_val.set_index('datetime', inplace=True)
        data_val.drop(columns=['date', 'time'], inplace=True)
        missing_switch = 0
    except FileNotFoundError:
        print(f'{inp} not found or corrupted!')
        missing_switch = 1
        data_val = pd.DataFrame({'mask': [True] * 0})  # Empty DataFrame
        data_val['datetime'] = pd.date_range(dt.datetime(1900, 1, 1), dt.datetime.today(), freq='720min')
        data_val.set_index('datetime', inplace=True)

    # Filter data within specified range (yy1, yy2)
    if missing_switch == 0:
        data_val = data_val[(data_val.index >= yy1) & (data_val.index <= yy2)]

    # Initialize 'data_na' for missing data mask
    data_na = pd.DataFrame(index=pd.date_range(yy1, yy2, freq='720min'), columns=['mask'], data=False)

    # Excluding seasonal unavailability using vectorized operations
    instr_metadata = ts.instr_metadata.get(ts.instr_list[idx])
    start_seas = pd.Timestamp(instr_metadata['start_seas']).month
    end_seas = pd.Timestamp(instr_metadata['end_seas']).month
    start_instr = pd.Timestamp(instr_metadata['start_instr'])
    end_instr = pd.Timestamp(instr_metadata['end_instr'])

    data_na['mask'] = np.where(
        (data_na.index.month < start_seas) | (data_na.index.month > end_seas) |
        (data_na.index < start_instr) | (data_na.index > end_instr), True, False)

    # Plotting: Error bars for missing data
    ys_1 = np.repeat(idx, len(data_na.index[data_na['mask']]))
    ax.errorbar(
            data_na.index[data_na['mask']], ys_1, xerr=None, yerr=0.3, fmt='.', color='lightgrey', capsize=0,
            markersize=0)

    # Plotting actual data availability
    if missing_switch == 0:
        color = cm.rainbow(np.linspace(0, 1, 40))[idx]
    else:
        color = 'black'

    try:
        data_val = data_val['mask'].astype(int)
        ys = np.repeat(idx, len(data_val.index[data_val == 1]))
        ax.errorbar(data_val.index[data_val == 1], ys, xerr=None, yerr=0.3, fmt='.', color=color, capsize=0, markersize=0)
    except pd.errors.IntCastingNaNError:
        print(f'{ts.instr_list[idx]} -  all data are NAN')
    return


# def plot_data_avail(ax, inp, yy1, yy2, idx):
#     """
#
#     :param ax:
#     :param idx:
#     :param inp:
#     :param yy1:
#     :param yy2:
#     :return:
#     """
#
#     # data
#     try:
#         data_val = pd.read_table(inp, sep=' ')
#         data_val.columns = ['date', 'time', 'mask']
#         data_val = data_val.set_index(pd.DatetimeIndex(data_val['date'] + 'T' + data_val['time']))
#         data_val = data_val.drop(columns=['date', 'time'])
#         missing_switch = 0
#     except FileNotFoundError:
#         print(f'{inp} not found or corrupted!')
#         missing_switch = 1
#         data_val = pd.DataFrame(data=np.empty((0, 2)))
#         data_val.columns = ['datetime', 'mask']
#         data_val['datetime'] = pd.date_range(dt.datetime(1900, 1, 1), dt.datetime.today(), freq='720min')
#         data_val = data_val.set_index(pd.DatetimeIndex(data_val['datetime']))
#         data_val = data_val.drop(columns=['datetime'])
#         data_val['mask'] = True
#
#     if missing_switch == 0:
#         data_val = data_val[(data_val.index >= yy1) & (data_val.index <= yy2)]
#
#     # data na
#     data_na = pd.DataFrame()
#     data_na['date'] = pd.date_range(yy1, yy2, freq='720min')
#     data_na['mask'] = np.empty(data_na['date'].shape)
#     data_na['mask'] = False
#     data_na.index = data_na['date']
#     data_na.drop(columns=['date'], inplace=True)
#
#     # excluding seasonal unavailability
#     for i, ii in enumerate(data_na.index):
#         if (ii.month > pd.Timestamp(ts.instr_metadata.get(ts.instr_list[idx])['end_seas']).month) | (
#                 ii.month < pd.Timestamp(ts.instr_metadata.get(ts.instr_list[idx])['start_seas']).month):
#             if data_na['mask'].iloc[i] != True:
#                 data_na.loc[ii, 'mask'] = True
#         else:
#             data_na.loc[ii, 'mask'] = False
#
#     # excluding instrument missing or not installed
#     for i, ii in enumerate(data_na.index):
#         if (ii < pd.Timestamp(ts.instr_metadata.get(ts.instr_list[idx])['start_instr'])) | (
#                 ii > pd.Timestamp(ts.instr_metadata.get(ts.instr_list[idx])['end_instr'])):
#             data_na.loc[ii, 'mask'] = True
#         else:
#             pass
#
#     data_na = data_na['mask'].astype('int')
#     ys_1 = np.repeat(idx, len(data_na.index[data_na == 1].values))
#     ax.errorbar(
#             data_na.index[data_na == 1].values, ys_1, xerr=None, yerr=0.3, fmt='.', color='lightgrey', capsize=0,
#             markersize=0)
#
#     # plot data
#     if missing_switch == 0:
#         color = cm.rainbow(np.linspace(0, 1, 40))
#         color = color[idx]
#     else:
#         color = 'black'
#     data_val = data_val['mask'].astype('int')
#     ys = np.repeat(idx, len(data_val.index[data_val == 1].values))
#     ax.errorbar(
#             data_val.index[data_val == 1].values, ys, xerr=None, yerr=0.3, fmt='.', color=color, capsize=0,
#             markersize=0)
#
#     return


def ax_style(axx, yy1, yy2, i_labs, i_length):
    """
    Customizes the axis appearance, including setting limits, formatting date ticks,
    and styling y-ticks based on instrument metadata.

    :param axx: The axis to style.
    :param yy1: Start date for the x-axis.
    :param yy2: End date for the x-axis.
    :param i_labs: List of labels for the y-axis.
    :param i_length: The length of the y-axis.
    :return: None
    """
    # Set the x and y axis limits
    axx.set_xlim(yy1, yy2)
    axx.set_ylim(-1, i_length)

    # Set the date format for x-axis
    if yy2.year - yy1.year > 10:
        myFmt = mdates.DateFormatter('%Y')
    else:
        myFmt = mdates.DateFormatter('%b-%Y')
    axx.xaxis.set_major_formatter(myFmt)

    # Set the y-axis ticks and labels
    axx.set_yticks(np.arange(i_length))  # Directly using numpy for range
    axx.set_yticklabels(i_labs)

    # Style the y-ticks based on instrument metadata
    for ytick in axx.get_yticklabels():
        label_text = ytick.get_text()
        instr_metadata = ts.instr_metadata.get(label_text)

        # Skip ytick if metadata is not available
        if instr_metadata is None:
            continue

        # Check if the instrument's end/start date is out of the range
        if instr_metadata['end_instr'] < yy1 or instr_metadata['start_instr'] > yy2:
            ytick.set_color('grey')
        else:
            institution_color = ts.institution_colors.get(instr_metadata['institution'], 'black')
            ytick.set_color(institution_color)
            ytick.set_fontweight('bold')

    return


# def ax_style(axx, yy1, yy2, i_labs, i_length):
#     """
#
#     :param axx:
#     :param i_length:
#     :param i_labs:
#     :param yy1:
#     :param yy2:
#     :return:
#     """
#
#     axx.set_xlim(yy1, yy2)
#     axx.set_ylim(-1, i_length)
#     if yy2.year - yy1.year > 10:
#         myFmt = mdates.DateFormatter('%Y')
#     else:
#         myFmt = mdates.DateFormatter('%b-%Y')
#     axx.xaxis.set_major_formatter(myFmt)
#
#     # axx.set_xticks(list(np.arange(0, i_length)))
#     # axx.set_xticklabels(axx.get_xticklabels(), fontsize=14)
#     axx.set_yticks(list(np.arange(0, i_length)))
#     axx.set_yticklabels(i_labs)
#     for ytick in axx.get_yticklabels():
#         if ts.instr_metadata.get(ytick.get_text())['end_instr'] < yy1:
#             ytick.set_color('grey')
#         elif ts.instr_metadata.get(ytick.get_text())['start_instr'] > yy2:
#             ytick.set_color('grey')
#         else:
#             ytick.set_color(
#                     ts.institution_colors[ts.instr_metadata.get(ytick.get_text())['institution']])
#             ytick.set_fontweight('bold')
#     return


def draw_events(ax, a1, a2):
    """
    Draw events on the given axis within the date range [a1, a2].

    :param ax: The axis to plot on.
    :param a1: Start date of the plotting range.
    :param a2: End date of the plotting range.
    :return: None
    """
    # Precompute the date range for efficiency
    event_range = pd.date_range(a1, a2)

    # Prepare random positions for event labels to avoid calling np.random multiple times
    max_y = len(ts.instr_list) + 1
    random_positions = np.random.randint(0, max_y, size=len(ts.events_dict))

    # Iterate over events and plot
    for event_idx, event in enumerate(ts.events_dict.values()):
        # Only plot events within the date range
        if event['date'] in event_range:
            # Plot vertical line for the event
            ax.vlines(x=event['date'], ymin=-1., ymax=max_y, color='grey', ls='dotted')

            # Use a random position from pre-generated positions for text
            ax.text(
                    event['date'], random_positions[event_idx], event['label'], fontweight='bold',
                    bbox=dict(facecolor='white', edgecolor='black', boxstyle='round,pad=1', alpha=0.8), zorder=10)

    return


#
# def draw_events(ax, a1, a2):
#     """
#
#     :param ax:
#     :param a1:
#     :param a2:
#     :return:
#     """
#     for event, event_idx in zip(ts.events_dict.values(), ts.events_dict.keys()):
#         if event['date'] in pd.date_range(a1, a2):
#             mx = len(ts.instr_list) + 1
#             ax.vlines(x=event['date'], ymin=-1., ymax=mx, color='grey', ls='dotted')
#             np.random.seed(event_idx)
#             ax.text(
#                     event['date'], np.random.randint(0, mx), event['label'], fontweight='bold', bbox=dict(
#                             facecolor='white', edgecolor='black', boxstyle='round,pad=1', alpha=0.8), zorder=10)
#
#     return


def draw_campaigns(ax, a1, a2):
    """
    Draw campaign periods on the given axis.

    :param ax: The axis to plot on.
    :param a1: Start date of the plotting range.
    :param a2: End date of the plotting range.
    :return: None
    """
    # Precompute the date range for efficiency
    campaign_range = pd.date_range(a1, a2)

    # Iterate over campaigns and draw the campaign periods within the given range
    for campaign in ts.campaigns_dict.values():
        if campaign['start'] in campaign_range:
            ax.axvspan(campaign['start'], campaign['end'], alpha=0.3, color='cyan', zorder=10)

    return


#
# def draw_campaigns(ax, a1, a2):
#     """
#
#     :param ax:
#     :param a1:
#     :param a2:
#     :return:
#     """
#     for campaign_idx, campaign in enumerate(ts.campaigns_dict.values()):
#         if campaign['start'] in pd.date_range(a1, a2):
#             ax.axvspan(
#                     campaign['start'], campaign['end'], alpha=0.3, color='cyan', label='Field campaign', zorder=10)
#
#     return


def draw_data_avail(a1, a2):
    """
    Draws data availability with legends for instruments and campaigns.
    :param a1: Start date
    :param a2: End date
    :return: Matplotlib figure
    """

    fig, ax = plt.subplots(figsize=(15, 10))
    ax2 = ax.twinx()

    i_labs = []

    # Precompute instrument inputs
    instrument_data = [tls.input_file_selection(i_labs, instr_name) for instr_idx, instr_name in
                       enumerate(ts.instr_list)]

    for instr_idx, (inp_file, _) in enumerate(instrument_data):
        print(f'{instr_idx:02}')
        plot_data_avail(ax, inp_file, a1, a2, instr_idx)

    # Check switches
    if sw.switch_history:
        draw_events(ax, a1, a2)
    if sw.switch_campaigns:
        draw_campaigns(ax, a1, a2)

    # Compute labels length once
    num_labs = len(i_labs)
    ax_style(ax, a1, a2, i_labs, num_labs)
    ax_style(ax2, a1, a2, i_labs, num_labs)

    # Optimize legend creation using list comprehension
    legend_elements = [Line2D([0], [0], marker='', lw=0, color=ts.institution_colors[elem], label=elem) for elem in
                       ts.institution_colors]

    # Add additional legend elements
    legend_elements.extend(
            [patches.Rectangle((0, 0), 1, 1, facecolor='cyan', label='Field Campaign'),
             patches.Rectangle((0, 0), 1, 1, facecolor='black', label='N/A')])

    ax.legend(
            handles=legend_elements, loc='upper center', bbox_to_anchor=(0.5, -0.05), fancybox=True, shadow=True,
            ncol=6, labelcolor=[ts.institution_colors[elem] for elem in ts.institution_colors], prop={'weight': 'bold'})

    return fig


# def draw_data_avail(a1, a2):
#     """
#
#     :param a1:
#     :param a2:
#     :return:
#     """
#     # with plt.xkcd():
#     fig = plt.figure(figsize=(15, 10))
#     ax = fig.add_axes([0.15, 0.1, 0.7, 0.8])
#     ax2 = ax.twinx()
#     i_labs = []
#     for instr_idx, instr_name in enumerate(ts.instr_list):
#         inp_file, i_labs = tls.input_file_selection(instr_idx, i_labs, instr_name)
#         plot_data_avail(ax, inp_file, a1, a2, instr_idx)
#     if sw.switch_history:
#         draw_events(ax, a1, a2)
#     if sw.switch_campaigns:
#         draw_campaigns(ax, a1, a2)
#     num_labs=len(i_labs)
#     ax_style(ax, a1, a2, i_labs, num_labs)
#     ax_style(ax2, a1, a2, i_labs, num_labs)
#     # legend of institutions
#     legend_elements = []
#     legend_colors = []
#     for idx, elem in enumerate(ts.institution_colors.keys()):
#         legend_elements.append(
#                 Line2D(
#                         [0], [0], marker='', markersize=0, lw=0, color=ts.institution_colors.get(elem), label=elem))
#         legend_colors.append(ts.institution_colors.get(elem))
#     # N/A legend
#     # campaign legend
#     rect1 = patches.Rectangle((0, 0), 1, 1, facecolor='cyan', label='Field Campaign')
#     rect2 = patches.Rectangle((0, 0), 1, 1, facecolor='black', label='N/A')
#     legend_elements.append(rect1)
#     legend_colors.append('cyan')
#     legend_elements.append(rect2)
#     legend_colors.append('black')
#     ax.legend(
#             handles=legend_elements, loc='upper center', bbox_to_anchor=(0.5, -0.05), fancybox=True, shadow=True,
#             ncol=6, labelcolor=legend_colors, prop={'weight': 'bold'})
#     return fig


def draw_progress_bar(n_dir, range_lab_f, strt_ff, end_ff, jj):
    """
    Draw the progress bar on the image.

    :param n_dir: Directory containing the image.
    :param range_lab_f: Label for the range (used in filenames).
    :param strt_ff: Start datetime for the range.
    :param end_ff: End datetime for the range.
    :param jj: Current datetime, used for progress calculation.
    :return: None
    """
    # Load the image and prepare for drawing (open once and reuse)
    img_path = os.path.join(n_dir, f'thaao_data_avail_{range_lab_f}.png')
    out = Image.open(img_path).convert('RGBA')

    # Draw the progress bar on the image
    progress = (jj.year - strt_ff.year) / (end_ff.year - strt_ff.year)
    d = ImageDraw.Draw(out)
    progress_width = 50 * dpi_fac
    progress_height = 60 * dpi_fac
    drawProgressBar(d, 180 * dpi_fac, 4300 * dpi_fac, progress_width, progress_height, progress, 'grey', 'blue')

    # Save the image with the progress bar
    progress_img_path = os.path.join(n_dir, f'thaao_data_avail_{range_lab_f}_p.png')
    out.save(progress_img_path)
    return


def drawProgressBar(d, x, y, w, h, progress_func, bg="black", fg="red"):
    """
    Draw the actual progress bar.

    :param d: Drawing object.
    :param x: X position for the bar.
    :param y: Y position for the bar.
    :param w: Width of the bar.
    :param h: Height of the bar.
    :param progress_func: Progress percentage (0 to 1).
    :param bg: Background color.
    :param fg: Foreground (progress) color.
    :return: Updated drawing object.
    """
    # Draw background
    d.ellipse((x + w, y, x + h + w, y + h), fill=bg)
    d.ellipse((x, y, x + h, y + h), fill=bg)
    d.rectangle((x + (h / 2), y, x + w + (h / 2), y + h), fill=bg)

    # Draw the progress bar itself
    w *= progress_func
    d.ellipse((x + w, y, x + h + w, y + h), fill=fg)
    d.ellipse((x, y, x + h, y + h), fill=fg)
    d.rectangle((x + (h / 2), y, x + w + (h / 2), y + h), fill=fg)

    return d


# def draw_progress_bar(n_dir, range_lab_f, strt_ff, end_ff, jj):
#     """
#
#     :param n_dir:
#     :param range_lab_f:
#     :param strt_ff:
#     :param end_ff:
#     :param jj:
#     :return:
#     """
#     # create image or load your existing image with out=Image.open(path)
#     out = Image.open(os.path.join(n_dir, 'thaao_data_avail_' + range_lab_f + '.png')).convert('RGBA')
#     d = ImageDraw.Draw(out)
#     # draw the progress bar to given location, width, progress and color
#     progress = (jj.year - strt_ff.year) / (end_ff.year - strt_ff.year)
#     d = drawProgressBar(d, 50 * dpi_fac, 180 * dpi_fac, 4300 * dpi_fac, 60 * dpi_fac, progress, 'grey', 'blue')
#     out.save(os.path.join(n_dir, f'thaao_data_avail_{range_lab_f}_p.png'))
#     return
#
#
# def drawProgressBar(d, x, y, w, h, progress_func, bg="black", fg="red"):
#     """
#
#     :param d:
#     :param x:
#     :param y:
#     :param w:
#     :param h:
#     :param progress_func:
#     :param bg:
#     :param fg:
#     :return:
#     """
#     # draw background
#     d.ellipse((x + w, y, x + h + w, y + h), fill=bg)
#     d.ellipse((x, y, x + h, y + h), fill=bg)
#     d.rectangle((x + (h / 2), y, x + w + (h / 2), y + h), fill=bg)
#
#     # draw progress bar
#     w *= progress_func
#     d.ellipse((x + w, y, x + h + w, y + h), fill=fg)
#     d.ellipse((x, y, x + h, y + h), fill=fg)
#     d.rectangle((x + (h / 2), y, x + w + (h / 2), y + h), fill=fg)
#
#     return d
#

def plot_rolling_panels():
    """
    Generate and save rolling data availability plots.
    """
    print('ROLLING')

    # Define the output directory
    newdir = os.path.join(ts.da_folder, 'rolling', f'{sw.start_c.year}-{sw.end_c.year}')
    os.makedirs(newdir, exist_ok=True)

    # Loop over rolling windows, from start to end
    for j in pd.date_range(sw.start_c, sw.end_c, freq=sw.time_freq_c):
        yyyy1 = j - sw.time_window_c
        yyyy2 = j

        # Define range label
        range_lab = f'{yyyy1.strftime("%Y%m")}_{yyyy2.strftime("%Y%m")}'
        print(range_lab)

        # Draw the figure and save it
        ffig = draw_data_avail(yyyy1, yyyy2)
        plt.suptitle(f'{yyyy1.strftime("%b %Y")} to {yyyy2.strftime("%b %Y")}', fontsize=20)

        # Save the figure as PNG
        plt.savefig(
            os.path.join(newdir, f'thaao_data_avail_{range_lab}_{sw.switch_instr_list}.png'), dpi=dpi, transparent=True)
        plt.close(ffig)  # Close the figure to free resources

        # Optional progress bar update
        if sw.switch_prog_bar:
            draw_progress_bar(newdir, range_lab, sw.start_c, sw.end_c, j)

    return


# def plot_rolling_panels():
#     """
#
#     :return:
#     """
#     print('ROLLING')
#     newdir = os.path.join(ts.da_folder, 'rolling', f'{sw.start_c.year}-{sw.end_c.year}')
#     os.makedirs(newdir, exist_ok=True)
#     j = cp.copy(sw.start_c)
#     while j + sw.time_window_c <= sw.end_c + sw.time_window_c:
#         yyyy1, yyyy2 = (j - sw.time_window_c, j)
#         range_lab = dt.datetime.strftime(yyyy1, '%Y%m') + '_' + dt.datetime.strftime(yyyy2, '%Y%m')
#         print(range_lab)
#         ffig = draw_data_avail(yyyy1, yyyy2)
#         plt.suptitle(
#                 dt.datetime.strftime(yyyy1, '%b %Y') + ' to ' + dt.datetime.strftime(yyyy2, '%b %Y'), fontsize=20)
#
#         plt.savefig(os.path.join(newdir, 'thaao_data_avail_' + range_lab + '.png'), dpi=dpi, transparent=True)
#         # plt.gca()
#         # plt.cla()
#         # gc.collect()
#         plt.close(ffig)
#
#         if sw.switch_prog_bar:
#             draw_progress_bar(newdir, range_lab, sw.start_c, sw.end_c, j)
#
#         j += sw.time_freq_c
#     return


def plot_yearly_panels():
    """
    Generate and save yearly data availability plots.
    """
    print('YEARLY')

    # Define the output directory
    newdir = os.path.join(ts.da_folder, 'yearly')
    os.makedirs(newdir, exist_ok=True)  # Ensure the directory exists

    # Loop over years from start to end, inclusive
    for current_year in pd.date_range(sw.start_y, sw.end_y, freq='YS'):
        print(current_year.strftime('%Y'))
        range_lab = current_year.strftime('%Y')

        # Draw the figure and save it
        yyyy1 = current_year
        yyyy2 = current_year + pd.DateOffset(years=1)
        ffig = draw_data_avail(yyyy1, yyyy2)
        plt.suptitle(current_year.strftime('%Y'))

        # Save the figure as PNG
        plt.savefig(os.path.join(newdir, f'thaao_data_avail_{range_lab}_{sw.switch_instr_list}.png'), dpi=dpi)
        plt.close(ffig)  # Close the figure to free resources

    return


#
# def plot_yearly_panels():
#     """
#     :return:
#     """
#     print('YEARLY')
#     newdir = os.path.join(ts.da_folder, 'yearly')
#     j = cp.copy(sw.start_y)
#     j1 = j + pd.DateOffset(years=1)
#     while j1 <= sw.end_y:
#         print(j)
#         range_lab = dt.datetime.strftime(j, '%Y')
#         ffig = draw_data_avail(j, j1)
#         plt.suptitle(dt.datetime.strftime(j, '%Y'))
#         # plt.gcf().autofmt_xdate()
#         plt.savefig(os.path.join(newdir, 'thaao_data_avail_' + range_lab + '.png'), dpi=dpi)
#         # plt.gca()
#         # plt.cla()
#         # gc.collect()
#         plt.close(ffig)
#
#         j += pd.DateOffset(years=1)
#         j1 += pd.DateOffset(years=1)
#
#     return

import os
import pandas as pd
import matplotlib.pyplot as plt
import datetime as dt


def plot_cumulative_panels():
    """
    Generate and save cumulative data availability plots.
    """
    print('CUMULATIVE')

    # Define the output directory
    newdir = os.path.join(ts.da_folder, 'cumulative', f'{sw.start_a.year}-{sw.end_a.year}')
    os.makedirs(newdir, exist_ok=True)

    # Loop over cumulative periods from start to end, based on frequency
    for current_date in pd.date_range(sw.start_a, sw.end_a, freq=sw.time_freq_a):
        # Define the range labels for the plot
        range_lab = f'{current_date.strftime("%Y%m")}_{(current_date + sw.time_freq_a).strftime("%Y%m")}'
        print(range_lab)

        # Draw the figure and save it
        yyyy1 = sw.start_a
        yyyy2 = current_date + sw.time_freq_a
        ffig = draw_data_avail(yyyy1, yyyy2)
        plt.suptitle(f'{sw.start_a.strftime("%b-%Y")} to {current_date.strftime("%b-%Y")}')

        # Save the figure as PNG
        plt.savefig(os.path.join(newdir, f'thaao_data_avail_{range_lab}_{sw.switch_instr_list}.png'), dpi=dpi)
        plt.close(ffig)  # Close the figure to free resources

    return

#
# def plot_cumulative_panels():
#     """
#
#     :return:
#     """
#     print('CUMULATIVE')
#     newdir = os.path.join(ts.da_folder, 'cumulative', str(sw.start_a.year) + '-' + str(sw.end_a.year))
#     os.makedirs(newdir, exist_ok=True)
#     j = cp.copy(sw.start_a) + sw.time_freq_a
#     while j <= sw.end_a:
#         yyyy1, yyyy2 = (sw.start_a, j)
#         range_lab = dt.datetime.strftime(yyyy1, '%Y%m') + '_' + dt.datetime.strftime(yyyy2, '%Y%m')
#         print(range_lab)
#         ffig = draw_data_avail(sw.start_a, j)
#         plt.suptitle(dt.datetime.strftime(sw.start_a, '%b-%Y') + ' to ' + dt.datetime.strftime(j, '%b-%Y'))
#         # plt.gcf().autofmt_xdate()
#         plt.savefig(os.path.join(newdir, f'thaao_data_avail_{range_lab}.png'), dpi=dpi)
#         # plt.gca()
#         # plt.cla()
#         # gc.collect()
#         plt.close(ffig)
#         j += sw.time_freq_a
#
#     return
