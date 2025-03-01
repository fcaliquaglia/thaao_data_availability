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
__version__ = "1.1"
__email__ = "filippo.caliquaglia@ingv.it"
__status__ = "Research"
__lastupdate__ = "February 2025"

instr = 'o3_sondes'


def update_data_avail(instr):
    import os
    from glob import glob

    import pandas as pd

    import single_instr_data_avail.tools as sida_tls

    import settings as ts

    date_list = pd.date_range(
            ts.instr_metadata[instr]['start_instr'], ts.instr_metadata[instr]['end_instr'], freq='D').tolist()
    folder = os.path.join(ts.basefolder, "thaao_" + instr)

    o3_sondes = pd.DataFrame(columns=['dt', 'mask'])
    o3_sondes_missing = pd.DataFrame(columns=['dt', 'mask'])

    for i in date_list:
        fn = glob(os.path.join(folder, 'th' + i.strftime('%y%m%d') + '.*'))
        try:
            if os.path.exists(fn[0]):
                o3_sondes.loc[i] = [i, True]
            else:
                o3_sondes_missing.loc[i] = [i, True]
        except IndexError:
            pass

    sida_tls.save_csv(instr, o3_sondes)
