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

instr = 'ecapac_disdro_precip'


def update_data_avail(instr):
    import os

    import pandas as pd

    import settings as ts
    import single_instr_data_avail.sida_tools as sida_tls
    date_list = pd.date_range(
            ts.instr_metadata[instr]['start_instr'], ts.instr_metadata[instr]['end_instr'], freq='D').tolist()
    folder = os.path.join(ts.basefolder, "thaao_" + instr)

    ecapac_disdro_precip = pd.DataFrame(columns=['dt', 'mask'])

    # # currently no real date, only estimate
    # for i in date_list:
    #     ecapac_disdro_precip.loc[i] = [i, True]

    for i in date_list:
        fn = os.path.join(
                folder, 'DISDRO', i.strftime('%Y'), "DISDRO_THAAO_" + i.strftime('%Y_%m_%d') + '_00_00' + ".dat")
        if os.path.exists(fn):
            ecapac_disdro_precip.loc[i] = [i, True]

    sida_tls.save_csv(instr, ecapac_disdro_precip)
