import datetime as dt
import gc
import os
import re

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


def draw_data_summary():
    # Create an empty DataFrame to store processed data
    data_all = pd.DataFrame()

    # Load and process data for each instrument
    for instr in ts.instr_list:
        try:
            # Load data file, resample based on time resolution, compute mean, and add a prefix
            tmp = tls.load_data_file(instr).resample(ts.time_res).mean().add_prefix(f"{instr}__")

            # Concatenate with existing data and sort by index
            data_all = pd.concat([data_all, tmp], axis=1).sort_index()
        except (ValueError, UnboundLocalError):
            print(f'ERROR with {instr}')  # Print error message for debugging

    # Apply transformations to specific columns if they exist
    column_transformations = {'aeronet__N[Precipitable_Water(cm)]': lambda x: x / 10,  # Convert to appropriate unit
                              'hyso_tide_1__sea_level'            : lambda x: x.mask(x > 10, np.nan),
                              # Replace values > 10 with NaN
                              'hatpro__IWV'                       : lambda x: x.mask(x > 50, np.nan),
                              # Replace outliers > 50 with NaN
                              'hatpro__LWP_gm-2'                  : lambda x: x.mask(x > 1000, np.nan),
                              # Replace outliers > 1000 with NaN
                              'ftir__ch4'                         : lambda x: x.mask(x < 3.4E19, np.nan)
                              # Replace values below threshold with NaN
                              }

    # Apply transformations if the corresponding column exists in the DataFrame
    for col, func in column_transformations.items():
        if col in data_all.columns:
            data_all[col] = func(data_all[col])

    # Generate a list of variable names for each instrument
    var_list = [f"{instr}__{var}"  # Format: 'instrument__variable'
                for instr in ts.instr_list for var in ts.instr_metadata[instr]['plot_vars'].keys()]

    # Identify subplots based on variable categories
    subplt = []
    for var in var_list:
        escaped_var = re.escape(var)  # Escape special characters in variable name for regex matching
        for key, values in ts.vars_dict.items():
            matching_columns = data_all.columns[data_all.columns.str.contains(escaped_var)]  # Find matching columns
            if not matching_columns.empty:
                if var.split('__')[1] in values['list']:  # Check if variable belongs to the category
                    subplt.append(key)
                    break  # Stop searching after the first match

    # Remove duplicate categories while preserving order
    subplt = list(dict.fromkeys(subplt))

    # Convert the list into an enumerated dictionary for subplot indexing
    subplt = dict(enumerate(subplt))

    # Filter data within the specified date range
    data_filtered = data_all.loc[
        (data_all.index.year >= sw.start_date.year) & (data_all.index.year <= sw.end_date.year), var_list]

    # plt.xkcd()
    # Create subplots with shared x-axis
    fig, axes = plt.subplots(len(subplt.keys()), 1, figsize=ts.figure_sizes[ts.fig_size], sharex=True)

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
            if var in ts.vars_dict[category]['list']:
                ax = axes[get_key_from_value(subplt, category)]
                lab = ts.vars_dict[category]['label']
                uom = ts.vars_dict[category]['uom']
                break

        vars_details = ts.instr_metadata[instr]['plot_vars'][var]
        color = vars_details[0]  # Line color

        # Primary Y-Axis (Left)
        ax.plot(
                data_filtered.index, data_filtered[var_], color=color, marker='o', markersize=2, linestyle='-',
                label=instr)
        ax.set_ylabel(f"{lab} \n [{uom}]", color=color, fontsize=10, fontweight='bold')
        ax.set_xlim(sw.start_date, sw.end_date)
        ax.tick_params(axis='y', colors=color, labelsize=8)
        ax.patch.set_facecolor('lightgrey')
        ax.legend(ncols=5, fontsize=8)

        # Enable right spine, ticks, and labels
        ax.spines['right'].set_visible(True)
        ax.yaxis.set_ticks_position('right')

        # Enable left spine, ticks, and labels
        ax.spines['left'].set_visible(True)
        ax.yaxis.set_ticks_position('left')

        # Handling of the axes:
        ax.spines['top'].set_visible(False)
        ax.spines['bottom'].set_visible(False)
        ax.set_xticklabels([])  # Remove x labels
        ax.xaxis.set_ticks_position('none')
        # Top subplot
        axes[0].set_xlim(sw.start_date, sw.end_date)
        axes[0].spines['top'].set_visible(True)
        axes[0].spines['bottom'].set_visible(False)
        axes[0].xaxis.set_ticks_position('top')
        axes[0].set_xticks(ax.get_xticks())  # Ensure tick positions are set
        axes[0].set_xticklabels(ax.get_xticks())  # Now set the corresponding labels
        # Automatically adjust the number of date ticks and labels
        axes[0].xaxis.set_major_locator(mdates.AutoDateLocator())  # Auto locates dates
        axes[0].xaxis.set_major_formatter(mdates.DateFormatter('%Y'))

        axes[-1].set_xlim(sw.start_date, sw.end_date)
        axes[-1].spines['top'].set_visible(False)
        axes[-1].spines['bottom'].set_visible(True)
        axes[-1].xaxis.set_ticks_position('bottom')
        # Automatically adjust the number of date ticks and labels
        axes[-1].xaxis.set_major_locator(mdates.AutoDateLocator())  # Auto locates dates
        axes[-1].xaxis.set_major_formatter(mdates.DateFormatter('%Y'))

        # Draw events and campaigns based on switches
        if sw.switch_history:
            draw_events(ax, sw.start_date.year, sw.end_date.year)
        if sw.switch_campaigns:
            draw_campaigns(ax, sw.start_date.year, sw.end_date.year)

    # Rotate date labels to make them readable
    plt.xticks(rotation=45)

    # Add a logo **next to the title**
    logo = plt.imread('logo.png')
    logo_ax = fig.add_axes([0.05, 0.87, 0.12, 0.12], anchor='NE', zorder=10)  # Adjust the x-position (0.05) for left
    logo_ax.imshow(logo)
    logo_ax.axis('off')

    # Set title and layout
    fig.suptitle(
        'Thule High Arctic Atmospheric Observatory in Pituffik, Greenland - THAAO', fontsize=14, fontweight='bold')
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

    fig, ax = plt.subplots(figsize=ts.figure_sizes[ts.fig_size][::-1], sharex=True)
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
                        newdir, f'thaao_data_avail_{yyyy1.strftime("%Y%m")}_{yyyy2.strftime("%Y%m")}_{ts.fig_size}.png')
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
                        newdir,
                        f'thaao_data_avail_{sw.start_date.strftime("%Y%m")}_{end.strftime("%Y%m")}_{ts.fig_size}.png')
                plt.savefig(figname, transparent=False)
                plt.clf()
                plt.close(fig)
                gc.collect()
                pbar.update(1)

    elif plot_type == 'summary':
        fig = draw_data_summary()
        figname = os.path.join(
                os.path.dirname(newdir),
                f'thaao_data_avail_{sw.start_date.year}_{sw.end_date.year}_{dt.datetime.today().strftime("%Y%m%d")}_{ts.time_res}_{ts.fig_size}.png')
        plt.savefig(figname, transparent=False)
        plt.clf()
        plt.close(fig)
        gc.collect()

    return
