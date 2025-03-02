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
import re

import settings as ts
import switches as sw
import tools as tls

scale_factor = 1.5
plt.rcParams.update({'font.size': 6 * scale_factor})
plt.rcParams.update({'figure.dpi': 300})
plt.rcParams.update({'figure.figsize': (15, 10)})


def draw_data_summary():
    data_all = pd.concat(
            [tls.load_data_file(instr).resample(ts.time_res).mean().add_prefix(f"{instr}__") for instr in
             ts.instr_list], axis=1).sort_index()

    var_list = []
    for instr in ts.instr_list:
        var_list += [instr + '__' + j for j in list(ts.instr_metadata[instr]['plot_vars'].keys())]

    subplt = []
    for var in var_list:
        escaped_var = re.escape(var)
        for key, values in ts.vars_dict.items():
            matching_columns = data_all.columns[data_all.columns.str.contains(escaped_var)]
            if not matching_columns.empty:
                if var.split('__')[1] in values:
                    subplt.append(key)
                    break  # Stop searching after finding the first match

    subplt = list(dict.fromkeys(subplt))  # remove duplicates
    subplt = dict(enumerate(subplt))

    data_filtered = data_all.loc[
        (data_all.index.year >= sw.start_date.year) & (data_all.index.year <= sw.end_date.year), var_list]

    # Create subplots with shared x-axis
    fig, axes = plt.subplots(len(subplt.keys()), 1, figsize=(22, 12), sharex=True)

    # Remove whitespace between subplots
    plt.subplots_adjust(hspace=0)

    def get_key_from_value(d, value):
        for key, val in d.items():
            if val == value:
                return key
        return None  # Return None if value is not found

    categories = [key for key, value in ts.vars_dict.items() if value['list']]

    # Iterate over each variable and its corresponding axis
    for i, var_ in enumerate(data_filtered.columns):
        instr, var = var_.split('__')  # Extract instrument and variable names
        print(f'Plotting {var}')
        # Assign specific columns to different axes based on name
        ax, lab, uom = None, None, None

        for category in categories:
            if var in ts.vars_dict[category]:
                ax = axes[get_key_from_value(subplt, category)]
                lab = ts.vars_dict[category]['label']
                uom = ts.vars_dict[category]['uom']
                break

        vars_details = ts.instr_metadata[instr]['plot_vars'][var]
        color = vars_details[0]  # Line color

        # Primary Y-Axis (Left)
        ax.plot(data_filtered.index, data_filtered[var_], color=color, marker='o', markersize=2, linestyle='-', label=instr)
        ax.set_ylabel(f"{lab} [{uom}]", color=color, fontsize=10, fontweight='bold')
        ax.tick_params(axis='y', colors=color, labelsize=8)
        ax.patch.set_facecolor('lightgrey')

        # Handling of the axes:
        if i == 0:  # First (uppermost) panel
            # Top x-axis: visible with spines, ticks, and labels
            ax.spines['top'].set_visible(True)
            ax.xaxis.set_ticks_position('top')  # Ensure ticks are on the top
            ax.set_xticklabels(data_filtered.index.year, rotation=45)
            ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
            ax.tick_params(axis='x', rotation=45, labelsize=9)  # Ensure labels on the top
            ax.spines['bottom'].set_visible(False)  # No bottom x-axis spines
            ax.get_xaxis().set_visible(True)  # Show x-axis on the bottom panel

        else:
            # For all intermediate panels (central ones)
            ax.spines['top'].set_visible(False)  # Hide the top x-axis
            ax.xaxis.set_ticks_position('bottom')  # Keep ticks on the bottom
            ax.set_xticklabels([])  # Remove x-axis labels
            ax.set_xlabel('')  # Remove x-axis title
            ax.get_xaxis().set_visible(False)  # Hide x-axis title and labels

        if i == len(data_filtered.columns) - 1:  # Last (lowermost) panel
            # Bottom x-axis: visible with spines, ticks, and labels
            ax.spines['bottom'].set_visible(True)
            ax.xaxis.set_ticks_position('bottom')  # Ensure ticks are on the bottom
            ax.xaxis.set_major_locator(mdates.YearLocator())
            ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
            ax.tick_params(axis='x', rotation=45, labelsize=9)  # Ensure labels on the bottom
        else:
            # Hide the bottom x-axis for all but the last panel
            ax.spines['bottom'].set_visible(False)

        # Apply grid to **all** subplots
        ax.grid(True, linestyle='--', alpha=0.5)

        # Draw events and campaigns based on switches
        if sw.switch_history:
            draw_events(ax, sw.start_date.year, sw.end_date.year)
        if sw.switch_campaigns:
            draw_campaigns(ax, sw.start_date.year, sw.end_date.year)

    # Add a logo **next to the title**
    logo = plt.imread('logo.png')
    logo_ax = fig.add_axes([0.05, 0.87, 0.12, 0.12], anchor='NE', zorder=10)  # Adjust the x-position (0.05) for left
    logo_ax.imshow(logo)
    logo_ax.axis('off')

    # Set title and layout
    fig.suptitle('Thule High Arctic Atmospheric Observatory - THAAO', fontsize=14, fontweight='bold')
    plt.tight_layout()

    return fig


def plot_data_avail(ax, instr, yy1, yy2):
    """Plot data availability"""

    idx = ts.instr_metadata[instr]['idx']
    data_val = tls.load_data_file(instr)

    # Filter data within the specified range (yy1, yy2) using .loc[]
    data_val = data_val.iloc[(data_val.index >= yy1) & (data_val.index <= yy2), 0]

    if data_val.empty:
        print(f'all data are NAN')
        return  # Exit early if no data

    # Get valid indices where data is not nan nor inf
    valid_indices = data_val.index[~data_val.isna() & ~data_val.isin([np.inf, -np.inf])]

    # Determine color for plotting
    color = cm.rainbow(np.linspace(0, 1, 40))[idx]
    if not valid_indices.empty:
        ax.errorbar(
                valid_indices, np.full(len(valid_indices), ts.instr_list.index(instr)), xerr=None, yerr=0.3, fmt='.',
                color=color, capsize=0, markersize=0)

    del data_val
    return


def plot_data_na(ax, instr, yy1, yy2):
    """Plot NA data"""
    # Generate date index directly as a Pandas Series with a boolean mask
    date_index = pd.date_range(yy1, yy2, freq='12h')

    # Fetch instrument metadata once
    instr_metadata = ts.instr_metadata.get(instr)
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
            date_index[mask], np.full(mask.sum(), ts.instr_list.index(instr)), xerr=None, yerr=0.3, fmt='.',
            color='lightgrey', capsize=0, markersize=0)

    # Explicitly free memory (optional but useful in large loops)
    del date_index, mask

    return


def ax_style(axx, yy1, yy2):
    """
    Customizes the axis appearance, including setting limits, formatting date ticks,
    and styling y-ticks based on instrument metadata.
    """

    i_length = len(ts.instr_list)
    axx.set_xlim(yy1, yy2)
    axx.set_ylim(-1, i_length)

    # Date formatting for x-axis
    date_format = '%Y' if yy2.year - yy1.year > 10 else '%b-%Y'
    axx.xaxis.set_major_formatter(mdates.DateFormatter(date_format))

    # Y-axis styling
    axx.set_yticks(np.arange(i_length))
    i_labs = [i for i in ts.instr_list]
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


def draw_data_avail(a1, a2):
    """Draws data availability with legends for instruments and campaigns."""

    fig, ax = plt.subplots()
    ax2 = ax.twinx()

    start = a1.strftime('%b %Y')
    end = a2.strftime('%b %Y')

    total_steps = len(ts.instr_list)
    with tqdm(
            total=total_steps, desc=f"Plotting instr data", position=1, colour='green',
            bar_format="{l_bar}{bar} {n_fmt}/{total_fmt} [{elapsed}<{remaining}]\n") as sbar:
        for instr in ts.instr_list:
            idx = ts.instr_metadata[instr]['idx']
            print(f'period:{start}-{end} --> {idx:02}:{instr}')
            plot_data_avail(ax, instr, a1, a2)
            plot_data_na(ax, instr, a1, a2)
            gc.collect()
            sbar.update(1)

    # Draw events and campaigns based on switches
    if sw.switch_history:
        draw_events(ax, a1, a2)
    if sw.switch_campaigns:
        draw_campaigns(ax, a1, a2)

    # Style the axis
    ax_style(ax, a1, a2)
    ax_style(ax2, a1, a2)

    # Generate the legend
    legend_elements = [Line2D([0], [0], marker='', lw=0, color=ts.institution_colors[elem], label=elem) for elem in
                       ts.institution_colors]
    legend_elements.extend(
            [patches.Rectangle((0, 0), 1, 1, facecolor='cyan', label='Field Campaign'),
             patches.Rectangle((0, 0), 1, 1, facecolor='black', label='N/A')])

    ax.legend(
            handles=legend_elements, loc='upper center', bbox_to_anchor=(0.5, -0.05), fancybox=True, shadow=True,
            ncol=6, labelcolor=[ts.institution_colors[elem] for elem in ts.institution_colors], prop={'weight': 'bold'})
    plt.tight_layout()

    return fig


def plot_panels(plot_type):
    """Generates panels for different types (rolling, cumulative)."""
    newdir = os.path.join(ts.da_folder, plot_type, f'{sw.start_date.year}-{sw.end_date.year}')
    os.makedirs(newdir, exist_ok=True)

    if plot_type == 'rolling':
        loop_data = pd.date_range(sw.start_date, sw.end_date, freq=sw.time_freq_r)
        total_steps = len(loop_data)
        with tqdm(
                total=total_steps, desc=f"\nPlotting {plot_type} data",
                bar_format="{l_bar}{bar} {n_fmt}/{total_fmt} [{elapsed}<{remaining}]\n") as pbar:
            for ibar, j in enumerate(loop_data):
                yyyy1, yyyy2 = j, j + sw.time_window_r
                fig = draw_data_avail(yyyy1, yyyy2)
                figname = os.path.join(
                        newdir, f'thaao_data_avail_{yyyy1.strftime("%Y%m")}_{yyyy2.strftime("%Y%m")}.png')
                plt.savefig(figname, transparent=False)
                plt.clf()
                plt.close(fig)
                gc.collect()
                pbar.update(1)

    elif plot_type == 'cumulative':
        loop_data = pd.date_range(sw.start_date, sw.end_date, freq=sw.time_freq_c)
        total_steps = len(loop_data)
        with tqdm(
                total=total_steps, desc=f"\nPlotting {plot_type} data",
                bar_format="{l_bar}{bar} {n_fmt}/{total_fmt} [{elapsed}<{remaining}]\n") as pbar:
            for ibar, date in enumerate(loop_data):
                end = date + sw.time_freq_c
                fig = draw_data_avail(sw.start_date, end)
                figname = os.path.join(
                        newdir, f'thaao_data_avail_{sw.start_date.strftime("%Y%m")}_{end.strftime("%Y%m")}.png')
                plt.savefig(figname, transparent=False)
                plt.clf()
                plt.close(fig)
                gc.collect()
                pbar.update(1)

    elif plot_type == 'summary':
        fig = draw_data_summary()
        figname = os.path.join(
                os.path.dirname(newdir),
                f'thaao_data_avail_{sw.start_date.year}_{sw.end_date.year}_{dt.datetime.today().strftime("%Y%m%d")}_{ts.time_res}.png')
        plt.savefig(figname, transparent=False)
        plt.clf()
        plt.close(fig)
        gc.collect()

    return
