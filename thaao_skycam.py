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

import pandas as pd

import settings as ts
import tools as tls

instr = 'skycam'
date_list_old = pd.date_range(
        ts.instr_metadata[instr]['start_instr'], ts.instr_metadata[instr]['end_instr'], freq='5 min').tolist()
date_list_new = pd.date_range(
        ts.instr_metadata[instr]['start_instr'], ts.instr_metadata[instr]['end_instr'], freq='D').tolist()
folder = os.path.join(ts.basefolder, "thaao_" + instr)

if __name__ == "__main__":

    # TODO: rimuovere "*_stack.jpg", "*_sod.jpg",
    skycam = pd.DataFrame(columns=['dt', 'mask'])
    for i in date_list_old:
        while i.strftime('%Y') < 2024:
            fn = os.path.join(
                    folder, i.strftime('%Y'), i.strftime('%m'), i.strftime('%d'),
                    i.strftime('%Y%m%d_%H%M_raw') + ".jpg")
            if os.path.exists(fn):
                print(fn)
                skycam.loc[i] = [i, True]
    for i in date_list_old:
        while i.strftime('%Y') >= 2024:
            # TODO: unzip daily folders and check the content
            fn = os.path.join(
                    folder, i.strftime('%Y'), i.strftime('%Y%m%d'))
            if os.path.exists(fn):
                print(fn)
                skycam.loc[i] = [i, True]

    # # for online checks
    # import urllib.request
    # for i in date_list:
    #     imgURL = "https://www.thuleatmos-it.it/data/skythule/data/" + i.strftime(
    #             '%Y/%Y%m%d/THULE_IMAGE_%Y%m%d_') + i.strftime('%H%M') + ".jpg"
    #     try:
    #         urllib.request.urlopen(imgURL)
    #         skycam.loc[i] = [i, True]
    #         print(i)
    #     except urllib.request.HTTPError as e:
    #         pass
    #     except urllib.request.URLError as e:
    #         pass

    tls.save_txt(instr, skycam)
