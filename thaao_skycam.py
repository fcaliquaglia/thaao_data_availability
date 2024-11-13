#!/usr/local/bin/python3
# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------------
#
"""
Brief description
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
import urllib.request

import pandas as pd

import settings as ts

instr = 'skycam'
date_list = pd.date_range(
        ts.instr_metadata[instr]['start_instr'], ts.instr_metadata[instr]['end_instr'], freq='D').tolist()
folder = os.path.join(ts.basefolder, "thaao_" + instr)

if __name__ == "__main__":

    skycam = pd.DataFrame(columns=['dt', 'mask'])
    for i in date_list:
        imgURL = "https://www.thuleatmos-it.it/data/skythule/data/" + i.strftime(
                '%Y/%Y%m%d/THULE_IMAGE_%Y%m%d_') + i.strftime('%H%M') + ".jpg"
        try:
            urllib.request.urlopen(imgURL)
            skycam.loc[i] = [i, True]
            print(i)
        except urllib.request.HTTPError as e:
            pass
        except urllib.request.URLError as e:
            pass

    ts.save_txt(instr, skycam)
