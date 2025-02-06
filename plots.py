import datetime as dt
import os

import matplotlib.cm as cm
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib import patches
from matplotlib.lines import Line2D

import settings as ts
import switches as sw

dpi_fac = 2
dpi = 200 * dpi_fac


def load_data_file(inp):
    """
    Loads the data from the input file. Returns a DataFrame with 'datetime' as the index
    and 'mask' column indicating data availability.
    """
    try:
        data_val = pd.read_table(inp, sep=' ')
        data_val.columns = ['date', 'time', 'mask']
        data_val['datetime'] = pd.to_datetime(data_val['date'] + ' ' + data_val['time'])
        data_val.set_index('datetime', inplace=True)
        data_val.drop(columns=['date', 'time'], inplace=True)
        return data_val
    except FileNotFoundError:
        print(f'{inp} not found or corrupted!')
        # Return an empty DataFrame for missing data
        return pd.DataFrame(
                {'mask': []}, index=pd.date_range(dt.datetime(1900, 1, 1), dt.datetime.today(), freq='720min'))


def plot_data_avail(ax, inp, yy1, yy2, idx):
    """Optimized function to plot data availability"""
    data_val = load_data_file(inp)

    # Filter data within the specified range (yy1, yy2)
    data_val = data_val[(data_val.index >= yy1) & (data_val.index <= yy2)]

    # Initialize 'data_na' for missing data mask
    data_na = pd.DataFrame(index=pd.date_range(yy1, yy2, freq='720min'), columns=['mask'], data=False)

    # Excluding seasonal unavailability
    instr_metadata = ts.instr_metadata.get(ts.instr_list[idx])
    start_seas = pd.Timestamp(instr_metadata['start_seas']).month
    end_seas = pd.Timestamp(instr_metadata['end_seas']).month
    start_instr = pd.Timestamp(instr_metadata['start_instr'])
    end_instr = pd.Timestamp(instr_metadata['end_instr'])

    # Update missing data based on instrument availability (seasons, start/end dates)
    data_na['mask'] = np.where(
            (data_na.index.month < start_seas) | (data_na.index.month > end_seas) | (data_na.index < start_instr) | (
                    data_na.index > end_instr), True, False)

    # Plotting missing data (grey color)
    ax.errorbar(
            data_na.index[data_na['mask']], np.repeat(idx, len(data_na.index[data_na['mask']])), xerr=None, yerr=0.3,
            fmt='.', color='lightgrey', capsize=0, markersize=0)

    # Plotting actual data availability
    color = cm.rainbow(np.linspace(0, 1, 40))[idx] if not data_val.empty else 'black'

    # Plot the available data
    try:
        data_val = data_val['mask'].astype(int)
        ax.errorbar(
                data_val.index[data_val == 1], np.repeat(idx, len(data_val.index[data_val == 1])), xerr=None, yerr=0.3,
                fmt='.', color=color, capsize=0, markersize=0)
    except pd.errors.IntCastingNaNError:
        print(f'{ts.instr_list[idx]} - all data are NAN')
    return


def ax_style(axx, yy1, yy2, i_labs):
    """
    Customizes the axis appearance, including setting limits, formatting date ticks,
    and styling y-ticks based on instrument metadata.
    """

    i_length = len(i_labs)
    axx.set_xlim(yy1, yy2)
    axx.set_ylim(-1, i_length)

    # Date formatting for x-axis
    date_format = '%Y' if yy2.year - yy1.year > 10 else '%b-%Y'
    axx.xaxis.set_major_formatter(mdates.DateFormatter(date_format))

    # Y-axis styling
    axx.set_yticks(np.arange(i_length))
    axx.set_yticklabels(i_labs)

    # Style y-ticks based on instrument metadata
    for ytick in axx.get_yticklabels():
        label_text = ytick.get_text()
        instr_metadata = ts.instr_metadata.get(label_text)

        if instr_metadata is None:
            continue

        # Set color and font weight based on availability
        if instr_metadata['end_instr'] < yy1 or instr_metadata['start_instr'] > yy2:
            ytick.set_color('grey')
        else:
            institution_color = ts.institution_colors.get(instr_metadata['institution'], 'black')
            ytick.set_color(institution_color)
            ytick.set_fontweight('bold')


def draw_events(ax, a1, a2):
    """Draw events on the given axis within the date range [a1, a2]."""
    event_range = pd.date_range(a1, a2)

    for event_idx, event in enumerate(ts.events_dict.values()):
        if event['date'] in event_range:
            ax.vlines(x=event['date'], ymin=-1., ymax=len(ts.instr_list) + 1, color='grey', ls='dotted')
            ax.text(
                    event['date'], np.random.randint(0, len(ts.instr_list) + 1), event['label'], fontweight='bold',
                    bbox=dict(facecolor='white', edgecolor='black', boxstyle='round,pad=1', alpha=0.8), zorder=10)


def draw_campaigns(ax, a1, a2):
    """Draw campaign periods on the given axis."""
    campaign_range = pd.date_range(a1, a2)

    for campaign in ts.campaigns_dict.values():
        if campaign['start'] in campaign_range:
            ax.axvspan(campaign['start'], campaign['end'], alpha=0.25, color='cyan', zorder=10)


def input_file_selection(i_list, i_name):
    """Select the appropriate input file for each instrument."""
    try:
        if i_name == 'skycam':
            inp_file = os.path.join(ts.basefolder_skycam, 'thaao_skycam', i_name + '_data_avail_list.txt')
        elif i_name.startswith('rad'):
            inp_file = os.path.join(ts.basefolder, 'thaao_rad', i_name + '_data_avail_list.txt')
        else:
            inp_file = os.path.join(ts.basefolder, 'thaao_' + i_name, i_name + '_data_avail_list.txt')
        i_list.append(i_name)
    except FileNotFoundError:
        inp_file = None
        print(f'File for {i_name} was not found')

    return inp_file, i_name


def draw_data_avail(a1, a2):
    """Draws data availability with legends for instruments and campaigns."""
    fig, ax = plt.subplots(figsize=(len(ts.instr_list) / 2 * 1.5, len(ts.instr_list) / 2))
    ax2 = ax.twinx()

    ii_labs = []
    instrument_data = [input_file_selection(ii_labs, instr_name) for instr_idx, instr_name in enumerate(ts.instr_list)]
    start = a1.strftime('%b %Y')
    end = a2.strftime('%b %Y')
    print(f'period:{start}-{end}')
    for instr_idx, (inp_file, _) in enumerate(instrument_data):
        print(f'{instr_idx:02}:{ts.instr_list[instr_idx]}')
        plot_data_avail(ax, inp_file, a1, a2, instr_idx)

    # Draw events and campaigns based on switches
    if sw.switch_history:
        draw_events(ax, a1, a2)
    if sw.switch_campaigns:
        draw_campaigns(ax, a1, a2)

    # Style the axis
    ax_style(ax, a1, a2, ii_labs)
    ax_style(ax2, a1, a2, ii_labs)

    # Generate the legend efficiently
    legend_elements = [Line2D([0], [0], marker='', lw=0, color=ts.institution_colors[elem], label=elem) for elem in
                       ts.institution_colors]
    legend_elements.extend(
            [patches.Rectangle((0, 0), 1, 1, facecolor='cyan', label='Field Campaign'),
             patches.Rectangle((0, 0), 1, 1, facecolor='black', label='N/A')])

    ax.legend(
            handles=legend_elements, loc='upper center', bbox_to_anchor=(0.5, -0.05), fancybox=True, shadow=True,
            ncol=6, labelcolor=[ts.institution_colors[elem] for elem in ts.institution_colors], prop={'weight': 'bold'})

    return fig


def plot_panels(plot_type):
    """Generates panels for different types (rolling, yearly, cumulative)."""
    print(plot_type)

    if plot_type == 'rolling':
        newdir = os.path.join(ts.da_folder, 'rolling', f'{sw.start_c.year}-{sw.end_c.year}')
        os.makedirs(newdir, exist_ok=True)

        for j in pd.date_range(sw.start_c, sw.end_c, freq=sw.time_freq_c):
            yyyy1, yyyy2 = j - sw.time_window_c, j
            range_lab = f'{yyyy1.strftime("%Y%m")}_{yyyy2.strftime("%Y%m")}'
            fig = draw_data_avail(yyyy1, yyyy2)
            plt.savefig(
                    os.path.join(newdir, f'thaao_data_avail_{range_lab}_{sw.switch_instr_list}.png'), dpi=dpi,
                    transparent=False)
            plt.close(fig)

    elif plot_type == 'yearly':
        newdir = os.path.join(ts.da_folder, 'yearly')
        os.makedirs(newdir, exist_ok=True)

        for year in pd.date_range(sw.start_y, sw.end_y, freq='YS'):
            fig = draw_data_avail(year, year + pd.DateOffset(years=1))
            plt.savefig(
                    os.path.join(newdir, f'thaao_data_avail_{year.strftime("%Y")}_{sw.switch_instr_list}.png'), dpi=dpi)
            plt.close(fig)

    elif plot_type == 'cumulative':
        newdir = os.path.join(ts.da_folder, 'cumulative', f'{sw.start_a.year}-{sw.end_a.year}')
        os.makedirs(newdir, exist_ok=True)

        for date in pd.date_range(sw.start_a, sw.end_a, freq=sw.time_freq_a):
            fig = draw_data_avail(sw.start_a, date + sw.time_freq_a)
            plt.savefig(
                    os.path.join(newdir, f'thaao_data_avail_{date.strftime("%Y%m")}_{sw.switch_instr_list}.png'),
                    dpi=dpi)
            plt.close(fig)
