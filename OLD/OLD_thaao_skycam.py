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
import zipfile

import pandas as pd

import settings as ts
from single_instr_data_avail import tools as tls

instr = 'skycam'
date_list = pd.date_range(
        ts.instr_metadata[instr]['start_instr'], ts.instr_metadata[instr]['end_instr'], freq='D').tolist()
folder = os.path.join(ts.basefolder_skycam, "thaao_" + instr)

if __name__ == "__main__":

    skycam = pd.DataFrame(columns=['dt', 'mask'])
    skycam_missing = pd.DataFrame(columns=['dt', 'mask'])
    for ii, i in enumerate(date_list[:-1]):
        fn = os.path.join(
                folder, i.strftime('%Y'), i.strftime('%Y%m%d'))
        date_list_int = pd.date_range(
                date_list[ii], date_list[ii + 1], freq='5 min', inclusive='left').tolist()
        try:
            # # check daily folders
            # if os.path.exists(fn + '.zip'):
            #     print(i)
            #     skycam.loc[i] = [i, True]
            # else:
            #     skycam_missing.loc[i] = [i, False]
            # check at x minutes inside zip
            with zipfile.ZipFile(f'{fn}.zip', 'r') as myzip:
                file_list = [x.split('/')[1] for x in myzip.namelist()]
                for j in date_list_int:
                    if j.strftime('%Y%m%d_%H%M_raw.jpg') in file_list:
                        # print(j.strftime('%Y%m%d_%H%M_raw.jpg'))
                        skycam.loc[j] = [j, True]
                    else:
                        skycam_missing.loc[j] = [j, False]
            myzip.close()
            print(fn)
        except (FileNotFoundError, zipfile.BadZipFile) as e:
            print(e)

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
    tls.save_txt(instr, skycam_missing, missing=True)
