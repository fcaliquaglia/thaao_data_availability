# #!/usr/local/bin/python3
# # -*- coding: utf-8 -*-
# # -------------------------------------------------------------------------------
# #
# """
# OK
# """
#
# # =============================================================
# # CREATED:
# # AFFILIATION: INGV
# # AUTHORS: Filippo Cali' Quaglia
# # =============================================================
# #
# # -------------------------------------------------------------------------------
# __author__ = "Filippo Cali' Quaglia"
# __credits__ = ["??????"]
# __license__ = "GPL"
# __version__ = "1.1"
# __email__ = "filippo.caliquaglia@ingv.it"
# __status__ = "Research"
# __lastupdate__ = "February 2025"
#
# instr = 'metar'
#
#
# def update_data_avail(instr):
#     import os
#
#     import pandas as pd
#     import single_instr_data_avail.sida_tools as sida_tls
#     from urllib.request import urlopen
#
#     import numpy as np
#     import settings as ts
#
#     folder = os.path.join(ts.basefolder, "thaao_" + instr)
#
#     url = (
#             'https://mesonet.agron.iastate.edu/cgi-bin/request/asos.py?station=BGTL&data=all&year1=1928&month1=1&day1=1&year2=' + str(
#             ts.instr_metadata[instr]['end_instr'].year) + '&month2=' + str(
#             ts.instr_metadata[instr]['end_instr'].month) + '&day2=' + str(
#             ts.instr_metadata[instr][
#                 'end_instr'].day) + '&tz=Etc%2FUTC&format=onlycomma&latlon=no&elev=no&missing=M&trace=T&direct=no&report_type=3&report_type=4')
#
#     print(url)
#     response = urlopen(url, timeout=10000)
#
#     with open(os.path.join(folder, 'BGTL_METAR.csv'), 'wb') as f:
#         f.write(response.read())
#
#     historical_data_all = pd.read_csv(os.path.join(folder, 'BGTL_METAR.csv'), low_memory=False, index_col='valid')
#     historical_data_metar = historical_data_all['metar']
#     del historical_data_all
#
#     vals = np.repeat(True, len(historical_data_metar))
#     metar = pd.concat([pd.Series(historical_data_metar.index), pd.Series(vals)], axis=1)
#     sida_tls.save_csv(instr, metar)

# !/usr/local/bin/python3
# -*- coding: utf-8 -*-

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

import os
from urllib.request import urlopen

import pandas as pd
from tqdm import tqdm
from metpy.units import units
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

    historical_data = pd.read_csv(
        file_path, usecols=["valid", "mslp", "relh", "tmpf"], index_col="valid", low_memory=False)
    historical_data["tmpc"] = (historical_data["tmpf"].values * units.degF).to(units.degC)
    historical_data.tmpf = historical_data.tmpf
    metar = pd.DataFrame(
            {"timestamp": historical_data.index, "mslp": historical_data.mslp, "relh": historical_data,
             "tmpc"     : historical_data.tmpc})

    sida_tls.save_csv(instr, metar)
