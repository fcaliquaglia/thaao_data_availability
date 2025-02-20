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

instr = 'pm10'


def update_data_avail(instr):
    import single_instr_data_avail.tools as sida_tls
    import os

    import numpy as np
    import pandas as pd

    import settings as ts

    date_list = pd.date_range(
            ts.instr_metadata[instr]['start_instr'], ts.instr_metadata[instr]['end_instr'], freq='D').tolist()
    folder = os.path.join(ts.basefolder, 'thaao_' + instr)

    pm10_tmp = pd.DataFrame(columns=['dt', 'mask'])

    fn = os.path.join(folder, 'Thule_2010_sampling_3mag23_modificato_per_data_availability.xls')
    pm10_tmp = pd.read_excel(fn, index_col=0)
    vals = np.repeat(True, len(pm10_tmp))

    pm10 = pd.concat([pd.Series(pd.DatetimeIndex(pm10_tmp.index)), pd.Series(vals)], axis=1)

    sida_tls.save_txt(instr, pm10)
