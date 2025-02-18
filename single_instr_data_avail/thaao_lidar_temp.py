#!/usr/local/bin/python3
# -*- coding: utf-8 -*-


__author__ = "Filippo Cali' Quaglia"
__credits__ = ["??????"]
__license__ = "GPL"
__version__ = "1.1"
__email__ = "filippo.caliquaglia@ingv.it"
__status__ = "Research"
__lastupdate__ = "February 2025"

instr = 'lidar_temp'


def update_data_avail(instr):
    """
    Updates the availability of LIDAR temperature data by checking for existing
    zip files and matching file patterns in the specified directory.
    """
    import glob
    import pandas as pd
    from pathlib import Path
    import settings as ts
    import single_instr_data_avail.tools as sida_tls

    # Generate a list of dates based on instrument metadata
    date_list = pd.date_range(
            ts.instr_metadata[instr]['start_instr'], ts.instr_metadata[instr]['end_instr'], freq='D')

    folder = Path(ts.basefolder) / f"thaao_{instr}"
    rows = []

    for i in date_list:
        try:
            # Check for ZIP file
            if (folder / f"LIDAR_{i.strftime('%Y%m%d')}.zip").exists():
                rows.append({'dt': i, 'mask': True})

            # Check for other matching files using glob
            if glob.glob(str(folder / f"thte{i.strftime('%y%m')}.*")):
                rows.append({'dt': i, 'mask': True})

        except Exception as e:
            print(f"Error processing {i.strftime('%Y-%m-%d')}: {e}")

    # Create DataFrame efficiently
    if rows:
        lidar_temp = pd.DataFrame(rows)
        lidar_temp.index = lidar_temp['dt']
        lidar_temp.sort_index(inplace=True)

        # Save the DataFrame using sida_tls module
        sida_tls.save_txt(instr, lidar_temp)
