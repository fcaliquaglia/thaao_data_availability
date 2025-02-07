#!/usr/local/bin/python3
# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------------
#
"""
OK
"""

# =============================================================
# CREATED: 
# AFFILIATION: INGV
# AUTHORS: Filippo Cali' Quaglia
# =============================================================
#
# -------------------------------------------------------------------------------
__author__ = "Filippo Cali' Quaglia"
__credits__ = ["??????"]
__license__ = "GPL"
__version__ = "0.1"
__email__ = "filippo.caliquaglia@ingv.it"
__status__ = "Research"
__lastupdate__ = "October 2024"

import os
from urllib.request import urlopen

import numpy as np
import pandas as pd

import settings as ts
from single_instr_data_avail import tools as tls

instr = 'metar'

folder = os.path.join(ts.basefolder, "thaao_" + instr)

if __name__ == "__main__":
    url = (
            'https://mesonet.agron.iastate.edu/cgi-bin/request/asos.py?station=BGTL&data=all&year1=1928&month1=1&day1=1&year2=' + str(
            ts.instr_metadata['hyso_tide']['end_instr'].year) + '&month2=' + str(
            ts.instr_metadata['hyso_tide']['end_instr'].month) + '&day2=' + str(
            ts.instr_metadata['hyso_tide'][
                'end_instr'].day) + '&tz=Etc%2FUTC&format=onlycomma&latlon=no&elev=no&missing=M&trace=T&direct=no&report_type=3&report_type=4')

    print(url)
    response = urlopen(url, timeout=10000)

    with open(os.path.join(folder, 'BGTL_METAR.csv'), 'wb') as f:
        f.write(response.read())

    historical_data_all = pd.read_csv(os.path.join(folder, 'BGTL_METAR.csv'), low_memory=False, index_col='valid')
    historical_data_metar = historical_data_all['metar']
    del historical_data_all

    # TODO: modificare usando ts.save_mask_txt
    vals = np.repeat(True, len(historical_data_metar))
    metar = pd.concat([pd.Series(historical_data_metar.index), pd.Series(vals)], axis=1)
    tls.save_txt(instr, metar)
