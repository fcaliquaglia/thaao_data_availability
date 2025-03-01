"""
OK
"""

# =============================================================
# CREATED:
# AFFILIATION: INGV
# AUTHORS: Filippo Cali' Quaglia
# =============================================================

# -------------------------------------------------------------------------------
__author__ = "Filippo Cali' Quaglia"
__credits__ = ["??????"]
__license__ = "GPL"
__version__ = "1.1"
__email__ = "filippo.caliquaglia@ingv.it"
__status__ = "Research"
__lastupdate__ = "February 2025"

import datetime as dt
import os
from urllib.request import urlopen

import numpy as np
import pandas as pd
from metpy.units import units
from tqdm import tqdm

import settings as ts
import single_instr_data_avail.sida_tools as sida_tls

instr = "metar"


def update_data_avail(instr):
    """Updates data availability for the given instrument with a progress bar."""

    folder = os.path.join(ts.basefolder, f"thaao_{instr}")
    end_instr = ts.instr_metadata[instr]["end_instr"]

    url = (f"https://mesonet.agron.iastate.edu/cgi-bin/request/asos.py?"
           f"station=BGTL&data=all&year1=1928&month1=1&day1=1"
           f"&year2={end_instr.year}&month2={end_instr.month}&day2={end_instr.day}"
           f"&tz=Etc%2FUTC&format=onlycomma&latlon=no&elev=no&missing=M&trace=T&direct=no"
           f"&report_type=3&report_type=4")

    print(f"Fetching data from: {url}")

    file_path = os.path.join(folder, "BGTL_METAR.csv")
    if os.path.exists(file_path):
        last_modified = dt.datetime.fromtimestamp(os.path.getmtime(file_path))
        current_date = dt.datetime.now()
        # Check if the file is older than n days
        old_thresh = 7
        if (current_date - last_modified).days > old_thresh:
            print(f"{old_thresh} is older than {old_thresh} days. Downloading updated file...")
            # Call the function to regenerate the .csv file
            try:
                with urlopen(url, timeout=100) as response:
                    total_size = response.length  # Get file size from HTTP response
                    chunk_size = 1024 * 1024  # 1MB chunks

                    with open(file_path, "wb") as f, tqdm(
                            total=total_size, unit="B", unit_scale=True, desc="Downloading") as pbar:
                        for chunk in iter(lambda: response.read(chunk_size), b""):
                            f.write(chunk)
                            pbar.update(len(chunk))

            except Exception as e:
                print(f"Error fetching data: {e}")
                return
        else:
            print(f"{file_path} is up-to-date (up to a maximum of {old_thresh} days).")

    historical_data = pd.read_csv(
            file_path, usecols=["valid", "mslp", "relh", "tmpf"], index_col="valid", low_memory=False)
    historical_data[historical_data == 'M'] = np.nan
    historical_data["tmpc"] = (historical_data["tmpf"].astype(float).values * units.degF).to(units.degC)

    metar = pd.DataFrame(
            {"timestamp": historical_data.index, "mslp": historical_data.mslp, "relh": historical_data.relh,
             "tmpc"     : historical_data.tmpc})


    sida_tls.save_csv(instr, metar)
