#!/usr/local/bin/python3
# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------------
#
"""
PHAAO meteo plot. Data format is the one of downloaded data from the website
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

from utils import thaao_settings as ts

instr = 'metar'

folder = os.path.join(ts.basefolder, "thaao_" + instr)

if __name__ == "__main__":
    # THULE
    # https://mesonet.agron.iastate.edu/request/download.phtml?network=GL__ASOS
    # https://mesonet.agron.iastate.edu/cgi-bin/request/asos.py?station=BGTL&data=all&year1=1928&month1=1&day1=1&year2=2023&month2=7&day2=30&tz=Etc%2FUTC&format=onlycomma&latlon=no&elev=no&missing=M&trace=T&direct=no&report_type=3&report_type=4
    # TODO: implementare download da script python

    url = (
            'https://mesonet.agron.iastate.edu/cgi-bin/request/asos.py?station=BGTL&data=all&year1=1928&month1=1&day1=1&year2=' + str(
            ts.instr_na_list['macmap_tide_gauge']['end_instr'].year) + '&month2=' + str(
            ts.instr_na_list['macmap_tide_gauge']['end_instr'].month) + '&day2=' + str(
            ts.instr_na_list['macmap_tide_gauge'][
                'end_instr'].day) + '&tz=Etc%2FUTC&format=onlycomma&latlon=no&elev=no&missing=M&trace=T&direct=no&report_type=3&report_type=4')

    response = urlopen(url)
    with open(os.path.join(folder, 'metar', 'BGTL_METAR.csv'), 'wb') as f:
        f.write(response.read())

    historical_data_all = pd.read_csv(os.path.join(folder, 'BGTL_METAR.csv'), low_memory=False, index_col='valid')
    historical_data_metar = historical_data_all['metar']
    del historical_data_all

    vals = np.repeat(True, len(historical_data_metar))
    metar = pd.concat([pd.Series(historical_data_metar.index), pd.Series(vals)], axis=1)
    ts.save_txt(instr, metar)
