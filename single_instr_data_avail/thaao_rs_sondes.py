#!/usr/local/bin/python3
# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------------
"""
OK
Reading and plotting data from EDT radiosounding.
ATTENTION! Before plotting data you need to format the data file using the script
C:\\Users\\FCQ\\iCloudDrive\\Documents\\bin\\thaao_rs_raw\\rs_1_convert_2022-on.py -- from 2022 onward
C:\\Users\\FCQ\\iCloudDrive\\Documents\\bin\\thaao_rs_raw\\rs_1_convert_2021.py -- for 2021
C:\\Users\\FCQ\\iCloudDrive\\Documents\\bin\\thaao_rs_raw\\rs_1_convert_2005-2020.py -- from 2006 to 2020
C:\\Users\\FCQ\\iCloudDrive\\Documents\\bin\\thaao_rs_raw\\rs_1_convert_wyo.py -- from 1973 to 2005
"""
#
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

instr = 'rs_sondes'


def update_data_avail(instr):
    import single_instr_data_avail.tools as sida_tls
    import os
    from glob import glob
    import pandas as pd

    import settings as ts
    date_list = pd.date_range(
            ts.instr_metadata[instr]['start_instr'], ts.instr_metadata[instr]['end_instr'], freq='D').tolist()
    folder = os.path.join(ts.basefolder, "thaao_" + instr, 'txt')

    rs_sondes = pd.DataFrame(columns=['dt', 'mask'])

    for i in date_list:
        fn = os.path.join(folder, i.strftime('%Y'), 'EDT_BGTL_' + i.strftime('%Y%m%d') + '*')
        if glob(fn):
            rs_sondes.loc[i] = [i, True]

    sida_tls.save_txt(instr, rs_sondes)
