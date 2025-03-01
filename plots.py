import datetime as dt
import gc
import os

import matplotlib.cm as cm
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib import patches
from matplotlib.lines import Line2D
from tqdm import tqdm

import settings as ts
import switches as sw
import tools as tls

scale_factor = 1.5
plt.rcParams.update({'font.size': 6 * scale_factor})
plt.rcParams.update({'figure.dpi': 300})
plt.rcParams.update({'figure.figsize': (15, 10)})


def draw_data_summary(instr_data, iii_labs):
    print('UNDER DEVELOPMENT')


    data_all = pd.DataFrame()
    for instr_idx, (inp_file, _) in enumerate(instr_data):
        data_orig = tls.load_data_file(inp_file)
        data = data_orig.resample('D').mean()
        data_all = pd.concat([data_all, data])

    # Define variables to plot (modify based on actual data columns)
    variables = {'AirTC': ('black', 'degC'), 'RH': ('blue', '%')}

    import matplotlib.dates as mdates

    # Create figure and subplots
    fig, axes = plt.subplots(len(variables), 1, figsize=(12, 12), sharex=True, dpi=200)

    # Plot each variable
    for i, (ax, (var, (color, unit))) in enumerate(zip(axes, variables.items())):
        ax.plot(data.index, data[var], color=color, marker='o', markersize=2, linestyle='-')
        ax.set_ylabel(f"{var} ({unit})", color=color, fontsize=10, fontweight='bold')
        ax.tick_params(axis='y', colors=color, labelsize=8)
        ax.grid(True, linestyle='--', alpha=0.5)

        # Remove the top x-axis spine for all subplots
        ax.spines['top'].set_visible(False)

        # Remove the bottom x-axis spine for all but the last subplot (the last one will keep the bottom spine)
        if i < len(variables) - 1:
            ax.spines['bottom'].set_visible(False)

        # Remove x-axis ticks for all but the last subplot
        if i < len(variables) - 1:
            ax.xaxis.set_ticks_position('none')  # No ticks for upper and bottom axes
        else:
            ax.xaxis.set_ticks_position('bottom')  # Show ticks only on the bottom for the last subplot

    # Format x-axis with year labels
    axes[-1].xaxis.set_major_locator(mdates.YearLocator())
    axes[-1].xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
    plt.xticks(rotation=45, fontsize=9)

    # Add a logo (comment out if not needed)
    logo = plt.imread('logo.png')
    newax = fig.add_axes([0.1, 0.75, 0.15, 0.15], anchor='NW', zorder=1)
    newax.imshow(logo)
    newax.axis('off')

    # Title and show plot
    fig.suptitle('Thle High Arctic Atmospheric Observatory', fontsize=14, fontweight='bold')

    return fig


def plot_data_avail(ax, inp, yy1, yy2, idx):
    """Plot data availability"""
    data_val = tls.load_data_file(inp)

    # Filter data within the specified range (yy1, yy2) using .loc[]
    data_val = data_val.loc[(data_val.index >= yy1) & (data_val.index <= yy2), 'mask']

    if data_val.empty:
        print(f'all data are NAN')
        return  # Exit early if no data

    # Convert mask values to integer (0 or 1) while handling NaNs
    data_val = data_val.fillna(0).astype(int)

    # Determine color for plotting
    color = cm.rainbow(np.linspace(0, 1, 40))[idx]

    # Get valid indices where data is available (mask == 1)
    valid_indices = data_val.index[data_val == 1]

    if not valid_indices.empty:
        ax.errorbar(
                valid_indices, np.full(len(valid_indices), idx), xerr=None, yerr=0.3, fmt='.', color=color, capsize=0,
                markersize=0)

    del data_val
    return


def plot_data_na(ax, yy1, yy2, idx):
    """Plot NA data"""

    # Generate date index directly as a Pandas Series with a boolean mask
    date_index = pd.date_range(yy1, yy2, freq='12h')

    # Fetch instrument metadata once
    instr_metadata = ts.instr_metadata.get(ts.instr_list[idx])
    start_seas, end_seas = pd.Timestamp(instr_metadata['start_seas']).month, pd.Timestamp(
            instr_metadata['end_seas']).month

    start_instr, end_instr = pd.Timestamp(instr_metadata['start_instr']), pd.Timestamp(instr_metadata['end_instr'])

    # Compute mask directly on Series
    if instr_metadata['start_seas'] < instr_metadata['end_seas']:
        mask = (date_index.month < start_seas) | (date_index.month > end_seas) | (date_index < start_instr) | (
                date_index > end_instr)
    if instr_metadata['start_seas'] > instr_metadata['end_seas']:
        mask = (date_index.month > start_seas) | (date_index.month < end_seas) | (date_index < start_instr) | (
                date_index > end_instr)

    # Plot missing data (grey color) only for masked values
    ax.errorbar(
            date_index[mask], np.full(mask.sum(), idx), xerr=None, yerr=0.3, fmt='.', color='lightgrey', capsize=0,
            markersize=0)

    # Explicitly free memory (optional but useful in large loops)
    del date_index, mask

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


def draw_data_avail(a1, a2, instr_data, iii_labs):
    """Draws data availability with legends for instruments and campaigns."""
    fig, ax = plt.subplots()
    ax2 = ax.twinx()

    start = a1.strftime('%b %Y')
    end = a2.strftime('%b %Y')

    total_steps = len(instr_data)
    with tqdm(
            total=total_steps, desc=f"Plotting instr data", position=1, colour='green',
            bar_format="{l_bar}{bar} {n_fmt}/{total_fmt} [{elapsed}<{remaining}]\n") as sbar:
        for instr_idx, (inp_file, _) in enumerate(instr_data):
            print(f'period:{start}-{end} --> {instr_idx:02}:{ts.instr_list[instr_idx]}')
            plot_data_avail(ax, inp_file, a1, a2, instr_idx)
            plot_data_na(ax, a1, a2, instr_idx)
            gc.collect()
            sbar.update(1)

    # Draw events and campaigns based on switches
    if sw.switch_history:
        draw_events(ax, a1, a2)
    if sw.switch_campaigns:
        draw_campaigns(ax, a1, a2)

    # Style the axis
    ax_style(ax, a1, a2, iii_labs)
    ax_style(ax2, a1, a2, iii_labs)

    # Generate the legend
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
    """Generates panels for different types (rolling, cumulative)."""

    ii_labs = []
    instrument_data = [tls.input_file_selection(ii_labs, instr_name) for instr_idx, instr_name in
                       enumerate(ts.instr_list)]

    if plot_type == 'rolling':
        newdir = os.path.join(ts.da_folder, 'rolling', sw.switch_instr_list, f'{sw.start.year}-{sw.end.year}')
        os.makedirs(newdir, exist_ok=True)

        loop_data = pd.date_range(sw.start, sw.end, freq=sw.time_freq_r)
        total_steps = len(loop_data)
        with tqdm(
                total=total_steps, desc=f"\nPlotting {plot_type} data",
                bar_format="{l_bar}{bar} {n_fmt}/{total_fmt} [{elapsed}<{remaining}]\n") as pbar:
            for ibar, j in enumerate(loop_data):
                yyyy1, yyyy2 = j, j + sw.time_window_r
                fig = draw_data_avail(yyyy1, yyyy2, instrument_data, ii_labs)
                figname = os.path.join(
                        newdir,
                        f'thaao_data_avail_{yyyy1.strftime("%Y%m")}_{yyyy2.strftime("%Y%m")}_{sw.switch_instr_list}.png')
                plt.savefig(figname, transparent=False)
                plt.clf()
                plt.close(fig)
                gc.collect()
                pbar.update(1)

    elif plot_type == 'cumulative':
        newdir = os.path.join(ts.da_folder, 'cumulative', sw.switch_instr_list, f'{sw.start.year}-{sw.end.year}')
        os.makedirs(newdir, exist_ok=True)

        loop_data = pd.date_range(sw.start, sw.end, freq=sw.time_freq_c)
        total_steps = len(loop_data)
        with tqdm(
                total=total_steps, desc=f"\nPlotting {plot_type} data",
                bar_format="{l_bar}{bar} {n_fmt}/{total_fmt} [{elapsed}<{remaining}]\n") as pbar:
            for ibar, date in enumerate(loop_data):
                end = date + sw.time_freq_c
                fig = draw_data_avail(sw.start, end, instrument_data, ii_labs)
                figname = os.path.join(
                        newdir,
                        f'thaao_data_avail_{sw.start.strftime("%Y%m")}_{end.strftime("%Y%m")}_{sw.switch_instr_list}.png')
                plt.savefig(figname, transparent=False)
                plt.clf()
                plt.close(fig)
                gc.collect()
                pbar.update(1)

    elif plot_type == 'summary':
        newdir = os.path.join(ts.da_folder, 'summary', f'{sw.start.year}-{sw.end.year}')
        os.makedirs(newdir, exist_ok=True)

        total_steps = len(ii_labs)
        with tqdm(
                total=total_steps, desc=f"\nPlotting {plot_type} data",
                bar_format="{l_bar}{bar} {n_fmt}/{total_fmt} [{elapsed}<{remaining}]\n") as pbar:
            for ibar, instr in enumerate(ii_labs):
                fig = draw_data_summary(instrument_data, ii_labs)
                figname = os.path.join(
                        newdir,
                        f'thaao_data_avail_{sw.start.year}_{sw.end.year}_{sw.switch_instr_list}_{dt.datetime.today().strftime("%Y%m%d")}.png')
                plt.savefig(figname, transparent=False)
                plt.clf()
                plt.close(fig)
                gc.collect()
                pbar.update(1)

    return
