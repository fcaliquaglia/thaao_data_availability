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
__author__ = "Filippo Cali' Quaglia, Monica Tosco"
__credits__ = ['??????']
__license__ = 'GPL'
__version__ = '0.1'
__email__ = 'filippo.caliquaglia@ingv.it'
__status__ = 'Research'
__lastupdate__ = "February 2025"

instr = 'ftir'


def update_data_avail(instr):
    import os

    import pandas as pd

    import settings as ts
    import single_instr_data_avail.sida_tools as sida_tls
    import datetime as dt

    # date_list = pd.date_range(
    #         ts.instr_metadata[instr]['start_instr'], ts.instr_metadata[instr]['end_instr'], freq='D').tolist()
    folder = os.path.join(ts.basefolder, 'thaao_' + instr)
    gas_species = 'c2h6'

    ftir = pd.DataFrame(columns=['dt', 'mask'])

    files = [j for j in os.listdir(folder) if j.startswith('groundbased_ftir.' + gas_species + '_ncar001_thule_')]
    for file in files:
        ftir_tmp = pd.DataFrame(columns=['dt', 'mask'])
        try:
            start = file.split('_')[4]
            end = file.split('_')[5]
            date_list_avail = pd.date_range(
                    dt.datetime.strptime(start[0:8], '%Y%m%d'), dt.datetime.strptime(end[0:8], '%Y%m%d'),
                    freq='D').tolist()
            for i in date_list_avail:
                ftir_tmp.loc[i] = [i, True]

        except IndexError:
            pass
        ftir = pd.concat([ftir_tmp, ftir])

    sida_tls.save_csv(instr, ftir)
