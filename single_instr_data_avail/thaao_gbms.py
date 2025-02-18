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

instr = 'gbms'


def update_data_avail(instr):
    import os
    from glob import glob

    import pandas as pd

    import settings as ts
    import single_instr_data_avail.tools as sida_tls

    date_list = pd.date_range(
            ts.instr_metadata[instr]['start_instr'], ts.instr_metadata[instr]['end_instr'], freq='D').tolist()
    folder = os.path.join(ts.basefolder, 'thaao_' + instr)

    gbms = pd.DataFrame(columns=['dt', 'mask'])

    for i in date_list:
        fn = glob(os.path.join(folder, 'th*' + i.strftime('%y%m') + '.*'))
        try:
            if fn[0]:
                gbms.loc[i] = [i, True]
        except IndexError:
            pass
    sida_tls.save_txt(instr, gbms)
