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

instr = 'wv_isotopes'


def update_data_avail(instr):
    import os

    import single_instr_data_avail.tools as sida_tls
    import pandas as pd

    import settings as ts

    date_list = pd.date_range(
            ts.instr_metadata[instr]['start_instr'], ts.instr_metadata[instr]['end_instr'], freq='D').tolist()
    folder = os.path.join(ts.basefolder, "thaao_" + instr)

    wv_isotopes = pd.DataFrame(columns=['dt', 'mask'])
    wv_isotopes_missing = pd.DataFrame(columns=['dt', 'mask'])

    fn1 = os.path.join(folder, 'BGK_MOSAiC_ADC_finaldataset.csv')
    wv_isotopes1 = pd.read_csv(fn1)
    wv_isotopes1['DateFormatted'] = pd.to_datetime(wv_isotopes1['DateTime_UTC'], format='%m/%d/%Y %H:%M')  # .round('h')

    fn2 = os.path.join(folder, 'thule_isotope_wx_10min_2017_2019.csv')
    wv_isotopes2 = pd.read_csv(fn2)
    wv_isotopes2['DateFormatted'] = pd.to_datetime(wv_isotopes2['min10break'], format='%d-%m-%y %H:%M')

    fn3 = os.path.join(folder, 'Thule_water_vapor_isotopes_16.csv')
    wv_isotopes3 = pd.read_csv(fn3)
    wv_isotopes3['DateFormatted'] = pd.to_datetime(wv_isotopes3['Date'], format='%Y-%m-%d %H:%M:%S')

    fn4 = os.path.join(folder, 'ThuleAFB_ppt_isotopes.csv')
    wv_isotopes4 = pd.read_csv(fn4)
    wv_isotopes4['DateFormatted'] = pd.to_datetime(wv_isotopes4['Date '], format='%m/%d/%y')

    wv_isotopes_dt = pd.DataFrame(
            pd.concat(
                    [wv_isotopes1['DateFormatted'], wv_isotopes2['DateFormatted'], wv_isotopes3['DateFormatted'],
                     wv_isotopes4['DateFormatted']]))
    wv_isotopes_dt.index = pd.DatetimeIndex(wv_isotopes_dt['DateFormatted'])

    for i in date_list:
        if i in wv_isotopes_dt.index:
            wv_isotopes.loc[i] = [i, True]
        else:
            wv_isotopes_missing.loc[i] = [i, True]

    sida_tls.save_txt(instr, wv_isotopes)
    sida_tls.save_txt(instr, wv_isotopes_missing, missing=True)
