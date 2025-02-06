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
# # AFFILIATION: UNIVE, INGV
# # AUTHORS: Filippo Cali' Quaglia
# # =============================================================
# #
# # -------------------------------------------------------------------------------
# __author__ = "Filippo Cali' Quaglia"
# __credits__ = ["??????"]
# __license__ = "GPL"
# __version__ = "0.1"
# __email__ = "filippo.caliquaglia@gmail.com"
# __status__ = "Research"
# __lastupdate__ = ""
#
# import datetime as dt
# import os
#
# import matplotlib.cm as cm
# import matplotlib.dates as mdates
# import matplotlib.patches as patches
# import matplotlib.pyplot as plt
# import numpy as np
# import pandas as pd
# from matplotlib.lines import Line2D
# from PIL import Image, ImageDraw
#
# import settings as ts
# import switches as sw
# import tools as tls
#
# dpi_fac = 2  # if increased, dpi resolution increases
# dpi = 300 * dpi_fac
#
#
# def plot_data_avail(ax, inp, yy1, yy2, idx):
#     """Optimized function to plot data availability"""
#
#     # Try reading the data
#     try:
#         data_val = pd.read_table(inp, sep=' ')
#         data_val.columns = ['date', 'time', 'mask']
#         data_val['datetime'] = pd.to_datetime(data_val['date'] + ' ' + data_val['time'])
#         data_val.set_index('datetime', inplace=True)
#         data_val.drop(columns=['date', 'time'], inplace=True)
#         missing_switch = 0
#     except FileNotFoundError:
#         print(f'{inp} not found or corrupted!')
#         missing_switch = 1
#         data_val = pd.DataFrame({'mask': [True] * 0})  # Empty DataFrame
#         data_val['datetime'] = pd.date_range(dt.datetime(1900, 1, 1), dt.datetime.today(), freq='720min')
#         data_val.set_index('datetime', inplace=True)
#
#     # Filter data within specified range (yy1, yy2)
#     if missing_switch == 0:
#         data_val = data_val[(data_val.index >= yy1) & (data_val.index <= yy2)]
#
#     # Initialize 'data_na' for missing data mask
#     data_na = pd.DataFrame(index=pd.date_range(yy1, yy2, freq='720min'), columns=['mask'], data=False)
#
#     # Excluding seasonal unavailability using vectorized operations
#     instr_metadata = ts.instr_metadata.get(ts.instr_list[idx])
#     start_seas = pd.Timestamp(instr_metadata['start_seas']).month
#     end_seas = pd.Timestamp(instr_metadata['end_seas']).month
#     start_instr = pd.Timestamp(instr_metadata['start_instr'])
#     end_instr = pd.Timestamp(instr_metadata['end_instr'])
#
#     data_na['mask'] = np.where(
#             (data_na.index.month < start_seas) | (data_na.index.month > end_seas) | (data_na.index < start_instr) | (
#                     data_na.index > end_instr), True, False)
#
#     # Plotting missing data
#     ys_1 = np.repeat(idx, len(data_na.index[data_na['mask']]))
#     ax.errorbar(
#             data_na.index[data_na['mask']], ys_1, xerr=None, yerr=0.3, fmt='.', color='lightgrey', capsize=0,
#             markersize=0)
#
#     # Plotting actual data availability
#     if missing_switch == 0:
#         color = cm.rainbow(np.linspace(0, 1, 40))[idx]
#     else:
#         color = 'black'
#
#     try:
#         data_val = data_val['mask'].astype(int)
#         ys = np.repeat(idx, len(data_val.index[data_val == 1]))
#         ax.errorbar(
#                 data_val.index[data_val == 1], ys, xerr=None, yerr=0.3, fmt='.', color=color, capsize=0, markersize=0)
#     except pd.errors.IntCastingNaNError:
#         print(f'{ts.instr_list[idx]} -  all data are NAN')
#     return
#
#
# def ax_style(axx, yy1, yy2, i_labs, i_length):
#     """
#     Customizes the axis appearance, including setting limits, formatting date ticks,
#     and styling y-ticks based on instrument metadata.
#
#     :param axx: The axis to style.
#     :param yy1: Start date for the x-axis.
#     :param yy2: End date for the x-axis.
#     :param i_labs: List of labels for the y-axis.
#     :param i_length: The length of the y-axis.
#     :return: None
#     """
#     # Set the x and y axis limits
#     axx.set_xlim(yy1, yy2)
#     axx.set_ylim(-1, i_length)
#
#     # Set the date format for x-axis
#     if yy2.year - yy1.year > 10:
#         myFmt = mdates.DateFormatter('%Y')
#     else:
#         myFmt = mdates.DateFormatter('%b-%Y')
#     axx.xaxis.set_major_formatter(myFmt)
#
#     # Set the y-axis ticks and labels
#     axx.set_yticks(np.arange(i_length))  # Directly using numpy for range
#     axx.set_yticklabels(i_labs)
#
#     # Style the y-ticks based on instrument metadata
#     for ytick in axx.get_yticklabels():
#         label_text = ytick.get_text()
#         instr_metadata = ts.instr_metadata.get(label_text)
#
#         # Skip ytick if metadata is not available
#         if instr_metadata is None:
#             continue
#
#         # Check if the instrument's end/start date is out of the range
#         if instr_metadata['end_instr'] < yy1 or instr_metadata['start_instr'] > yy2:
#             ytick.set_color('grey')
#         else:
#             institution_color = ts.institution_colors.get(instr_metadata['institution'], 'black')
#             ytick.set_color(institution_color)
#             ytick.set_fontweight('bold')
#
#     return
#
#
# def draw_events(ax, a1, a2):
#     """
#     Draw events on the given axis within the date range [a1, a2].
#
#     :param ax: The axis to plot on.
#     :param a1: Start date of the plotting range.
#     :param a2: End date of the plotting range.
#     :return: None
#     """
#     # Precompute the date range for efficiency
#     event_range = pd.date_range(a1, a2)
#
#     # Prepare random positions for event labels to avoid calling np.random multiple times
#     max_y = len(ts.instr_list) + 1
#     random_positions = np.random.randint(0, max_y, size=len(ts.events_dict))
#
#     # Iterate over events and plot
#     for event_idx, event in enumerate(ts.events_dict.values()):
#         # Only plot events within the date range
#         if event['date'] in event_range:
#             # Plot vertical line for the event
#             ax.vlines(x=event['date'], ymin=-1., ymax=max_y, color='grey', ls='dotted')
#
#             # Use a random position from pre-generated positions for text
#             ax.text(
#                     event['date'], random_positions[event_idx], event['label'], fontweight='bold',
#                     bbox=dict(facecolor='white', edgecolor='black', boxstyle='round,pad=1', alpha=0.8), zorder=10)
#
#     return
#
#
# def draw_campaigns(ax, a1, a2):
#     """
#     Draw campaign periods on the given axis.
#
#     :param ax: The axis to plot on.
#     :param a1: Start date of the plotting range.
#     :param a2: End date of the plotting range.
#     :return: None
#     """
#     # Precompute the date range for efficiency
#     campaign_range = pd.date_range(a1, a2)
#
#     # Iterate over campaigns and draw the campaign periods within the given range
#     for campaign in ts.campaigns_dict.values():
#         if campaign['start'] in campaign_range:
#             ax.axvspan(campaign['start'], campaign['end'], alpha=0.3, color='cyan', zorder=10)
#
#     return
#
#
# def draw_data_avail(a1, a2):
#     """
#     Draws data availability with legends for instruments and campaigns.
#     :param a1: Start date
#     :param a2: End date
#     :return: Matplotlib figure
#     """
#
#     fig, ax = plt.subplots(figsize=(15, 10))
#     ax2 = ax.twinx()
#
#     i_labs = []
#
#     # Precompute instrument inputs
#     instrument_data = [tls.input_file_selection(i_labs, instr_name) for instr_idx, instr_name in
#                        enumerate(ts.instr_list)]
#
#     for instr_idx, (inp_file, _) in enumerate(instrument_data):
#         print(f'{instr_idx:02}')
#         plot_data_avail(ax, inp_file, a1, a2, instr_idx)
#
#     # Check switches
#     if sw.switch_history:
#         draw_events(ax, a1, a2)
#     if sw.switch_campaigns:
#         draw_campaigns(ax, a1, a2)
#
#     # Compute labels length once
#     num_labs = len(i_labs)
#     ax_style(ax, a1, a2, i_labs, num_labs)
#     ax_style(ax2, a1, a2, i_labs, num_labs)
#
#     # Optimize legend creation using list comprehension
#     legend_elements = [Line2D([0], [0], marker='', lw=0, color=ts.institution_colors[elem], label=elem) for elem in
#                        ts.institution_colors]
#
#     # Add additional legend elements
#     legend_elements.extend(
#             [patches.Rectangle((0, 0), 1, 1, facecolor='cyan', label='Field Campaign'),
#              patches.Rectangle((0, 0), 1, 1, facecolor='black', label='N/A')])
#
#     ax.legend(
#             handles=legend_elements, loc='upper center', bbox_to_anchor=(0.5, -0.05), fancybox=True, shadow=True,
#             ncol=6, labelcolor=[ts.institution_colors[elem] for elem in ts.institution_colors], prop={'weight': 'bold'})
#
#     return fig
#
#
# def draw_progress_bar(n_dir, range_lab_f, strt_ff, end_ff, jj):
#     """
#     Draw the progress bar on the image.
#
#     :param n_dir: Directory containing the image.
#     :param range_lab_f: Label for the range (used in filenames).
#     :param strt_ff: Start datetime for the range.
#     :param end_ff: End datetime for the range.
#     :param jj: Current datetime, used for progress calculation.
#     :return: None
#     """
#     # Load the image and prepare for drawing (open once and reuse)
#     img_path = os.path.join(n_dir, f'thaao_data_avail_{range_lab_f}.png')
#     out = Image.open(img_path).convert('RGBA')
#
#     # Draw the progress bar on the image
#     progress = (jj.year - strt_ff.year) / (end_ff.year - strt_ff.year)
#     d = ImageDraw.Draw(out)
#     progress_width = 50 * dpi_fac
#     progress_height = 60 * dpi_fac
#     drawProgressBar(d, 180 * dpi_fac, 4300 * dpi_fac, progress_width, progress_height, progress, 'grey', 'blue')
#
#     # Save the image with the progress bar
#     progress_img_path = os.path.join(n_dir, f'thaao_data_avail_{range_lab_f}_p.png')
#     out.save(progress_img_path)
#     return
#
#
# def drawProgressBar(d, x, y, w, h, progress_func, bg="black", fg="red"):
#     """
#     Draw the actual progress bar.
#
#     :param d: Drawing object.
#     :param x: X position for the bar.
#     :param y: Y position for the bar.
#     :param w: Width of the bar.
#     :param h: Height of the bar.
#     :param progress_func: Progress percentage (0 to 1).
#     :param bg: Background color.
#     :param fg: Foreground (progress) color.
#     :return: Updated drawing object.
#     """
#     # Draw background
#     d.ellipse((x + w, y, x + h + w, y + h), fill=bg)
#     d.ellipse((x, y, x + h, y + h), fill=bg)
#     d.rectangle((x + (h / 2), y, x + w + (h / 2), y + h), fill=bg)
#
#     # Draw the progress bar itself
#     w *= progress_func
#     d.ellipse((x + w, y, x + h + w, y + h), fill=fg)
#     d.ellipse((x, y, x + h, y + h), fill=fg)
#     d.rectangle((x + (h / 2), y, x + w + (h / 2), y + h), fill=fg)
#
#     return d
#
#
# def plot_rolling_panels():
#     """
#     Generate and save rolling data availability plots.
#     """
#     print('ROLLING')
#
#     # Define the output directory
#     newdir = os.path.join(ts.da_folder, 'rolling', f'{sw.start_c.year}-{sw.end_c.year}')
#     os.makedirs(newdir, exist_ok=True)
#
#     # Loop over rolling windows, from start to end
#     for j in pd.date_range(sw.start_c, sw.end_c, freq=sw.time_freq_c):
#         yyyy1 = j - sw.time_window_c
#         yyyy2 = j
#
#         # Define range label
#         range_lab = f'{yyyy1.strftime("%Y%m")}_{yyyy2.strftime("%Y%m")}'
#         print(range_lab)
#
#         # Draw the figure and save it
#         ffig = draw_data_avail(yyyy1, yyyy2)
#         plt.suptitle(f'{yyyy1.strftime("%b %Y")} to {yyyy2.strftime("%b %Y")}', fontsize=20)
#
#         # Save the figure as PNG
#         plt.savefig(
#                 os.path.join(newdir, f'thaao_data_avail_{range_lab}_{sw.switch_instr_list}.png'), dpi=dpi,
#                 transparent=True)
#         plt.close(ffig)  # Close the figure to free resources
#
#         # Optional progress bar update
#         if sw.switch_prog_bar:
#             draw_progress_bar(newdir, range_lab, sw.start_c, sw.end_c, j)
#
#     return
#
#
# def plot_yearly_panels():
#     """
#     Generate and save yearly data availability plots.
#     """
#     print('YEARLY')
#
#     # Define the output directory
#     newdir = os.path.join(ts.da_folder, 'yearly')
#     os.makedirs(newdir, exist_ok=True)  # Ensure the directory exists
#
#     # Loop over years from start to end, inclusive
#     for current_year in pd.date_range(sw.start_y, sw.end_y, freq='YS'):
#         print(current_year.strftime('%Y'))
#         range_lab = current_year.strftime('%Y')
#
#         # Draw the figure and save it
#         yyyy1 = current_year
#         yyyy2 = current_year + pd.DateOffset(years=1)
#         ffig = draw_data_avail(yyyy1, yyyy2)
#         plt.suptitle(current_year.strftime('%Y'))
#
#         # Save the figure as PNG
#         plt.savefig(os.path.join(newdir, f'thaao_data_avail_{range_lab}_{sw.switch_instr_list}.png'), dpi=dpi)
#         plt.close(ffig)  # Close the figure to free resources
#
#     return
#
#
# def plot_cumulative_panels():
#     """
#     Generate and save cumulative data availability plots.
#     """
#     print('CUMULATIVE')
#
#     # Define the output directory
#     newdir = os.path.join(ts.da_folder, 'cumulative', f'{sw.start_a.year}-{sw.end_a.year}')
#     os.makedirs(newdir, exist_ok=True)
#
#     # Loop over cumulative periods from start to end, based on frequency
#     for current_date in pd.date_range(sw.start_a, sw.end_a, freq=sw.time_freq_a):
#         # Define the range labels for the plot
#         range_lab = f'{current_date.strftime("%Y%m")}_{(current_date + sw.time_freq_a).strftime("%Y%m")}'
#         print(range_lab)
#
#         # Draw the figure and save it
#         yyyy1 = sw.start_a
#         yyyy2 = current_date + sw.time_freq_a
#         ffig = draw_data_avail(yyyy1, yyyy2)
#         plt.suptitle(f'{sw.start_a.strftime("%b-%Y")} to {current_date.strftime("%b-%Y")}')
#
#         # Save the figure as PNG
#         plt.savefig(os.path.join(newdir, f'thaao_data_avail_{range_lab}_{sw.switch_instr_list}.png'), dpi=dpi)
#         plt.close(ffig)  # Close the figure to free resources
#
#     return

import os
import datetime as dt
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.cm as cm
from matplotlib import patches
from matplotlib.lines import Line2D
from PIL import Image, ImageDraw
import settings as ts
import switches as sw
import tools as tls

dpi_fac = 2
dpi = 300 * dpi_fac


def plot_data_avail(ax, inp, yy1, yy2, idx):
    """Optimized function to plot data availability"""
    try:
        data_val = pd.read_table(inp, sep=' ', names=['date', 'time', 'mask'])
        data_val['datetime'] = pd.to_datetime(data_val['date'] + ' ' + data_val['time'])
        data_val.set_index('datetime', inplace=True)
        data_val.drop(columns=['date', 'time'], inplace=True)
    except FileNotFoundError:
        print(f'File not found: {inp}')
        return

    instr_metadata = ts.instr_metadata.get(ts.instr_list[idx], {})
    start_seas, end_seas = instr_metadata.get('start_seas', 1), instr_metadata.get('end_seas', 12)
    start_instr, end_instr = instr_metadata.get('start_instr', yy1), instr_metadata.get('end_instr', yy2)

    data_na = pd.Series(False, index=pd.date_range(yy1, yy2, freq='720min'))
    data_na[(data_na.index.month < start_seas.month) | (data_na.index.month > end_seas.month) | (
                data_na.index < start_instr) | (
                    data_na.index > end_instr)] = True
    ax.errorbar(
            data_na.index[data_na], np.full_like(data_na.index[data_na], idx), fmt='.', color='lightgrey', markersize=0)

    if not data_val.empty:
        data_val = data_val[data_val.index.to_series().between(yy1,yy2)]
        ax.errorbar(
                data_val.index[data_val['mask'] == 1], np.full_like(data_val.index[data_val['mask'] == 1], idx),
                fmt='.', color=cm.rainbow(np.linspace(0, 1, 40))[idx], markersize=0)


def ax_style(ax, yy1, yy2, i_labs, i_length):
    """Sets axis styles and labels"""
    ax.set_xlim(yy1, yy2)
    ax.set_ylim(-1, i_length)
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y' if yy2.year - yy1.year > 10 else '%b-%Y'))
    ax.set_yticks(np.arange(i_length))
    ax.set_yticklabels(i_labs)


def draw_events(ax, a1, a2):
    """Draws historical events"""
    for event in ts.events_dict.values():
        if a1 <= event['date'] <= a2:
            ax.vlines(x=event['date'], ymin=-1, ymax=len(ts.instr_list) + 1, color='grey', ls='dotted')
            ax.text(
                    event['date'], np.random.randint(0, len(ts.instr_list)), event['label'],
                    bbox=dict(facecolor='white', edgecolor='black', alpha=0.8), fontweight='bold')


def draw_campaigns(ax, a1, a2):
    """Draws campaign periods"""
    for campaign in ts.campaigns_dict.values():
        if a1 <= campaign['start'] <= a2:
            ax.axvspan(campaign['start'], campaign['end'], alpha=0.3, color='cyan')


def draw_data_avail(a1, a2):
    """Generates data availability plots"""
    fig, ax = plt.subplots(figsize=(15, 10))
    ax2 = ax.twinx()
    i_labs = [instr for instr in ts.instr_list]

    for idx, instr in enumerate(ts.instr_list):
        print(instr)
        inp_file = tls.input_file_selection(i_labs, instr)
        plot_data_avail(ax, inp_file, a1, a2, idx)

    if sw.switch_history:
        draw_events(ax, a1, a2)
    if sw.switch_campaigns:
        draw_campaigns(ax, a1, a2)

    ax_style(ax, a1, a2, i_labs, len(i_labs))
    ax_style(ax2, a1, a2, i_labs, len(i_labs))

    legend_elements = [Line2D([0], [0], color=ts.institution_colors[key], label=key) for key in ts.institution_colors]
    legend_elements.append(patches.Rectangle((0, 0), 1, 1, facecolor='cyan', label='Field Campaign'))
    ax.legend(handles=legend_elements, loc='upper center', bbox_to_anchor=(0.5, -0.05), ncol=6, prop={'weight': 'bold'})
    return fig


def plot_rolling_panels():
    """Generates rolling panels"""
    newdir = os.path.join(ts.da_folder, 'rolling', f'{sw.start_c.year}-{sw.end_c.year}')
    os.makedirs(newdir, exist_ok=True)

    for j in pd.date_range(sw.start_c, sw.end_c, freq=sw.time_freq_c):
        yyyy1, yyyy2 = j - sw.time_window_c, j
        range_lab = f'{yyyy1.strftime("%Y%m")}_{yyyy2.strftime("%Y%m")}'
        fig = draw_data_avail(yyyy1, yyyy2)
        plt.savefig(os.path.join(newdir, f'thaao_data_avail_{range_lab}.png'), dpi=dpi, transparent=True)
        plt.close(fig)


def plot_yearly_panels():
    """Generates yearly panels"""
    newdir = os.path.join(ts.da_folder, 'yearly')
    os.makedirs(newdir, exist_ok=True)

    for year in pd.date_range(sw.start_y, sw.end_y, freq='YS'):
        fig = draw_data_avail(year, year + pd.DateOffset(years=1))
        plt.savefig(os.path.join(newdir, f'thaao_data_avail_{year.strftime("%Y")}.png'), dpi=dpi)
        plt.close(fig)


def plot_cumulative_panels():
    """Generates cumulative panels"""
    newdir = os.path.join(ts.da_folder, 'cumulative', f'{sw.start_a.year}-{sw.end_a.year}')
    os.makedirs(newdir, exist_ok=True)

    for date in pd.date_range(sw.start_a, sw.end_a, freq=sw.time_freq_a):
        fig = draw_data_avail(sw.start_a, date + sw.time_freq_a)
        plt.savefig(os.path.join(newdir, f'thaao_data_avail_{date.strftime("%Y%m")}.png'), dpi=dpi)
        plt.close(fig)
