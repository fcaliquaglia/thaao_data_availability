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

instr = 'hyso_seismo_3'


def update_data_avail(instr):
    import os

    import pandas as pd

    import settings as ts
    import single_instr_data_avail.tools as sida_tls

    date_list = pd.date_range(
            ts.instr_metadata[instr]['start_instr'], ts.instr_metadata[instr]['end_instr'], freq='D').tolist()
    folder = os.path.join(ts.basefolder, "thaao_" + instr)

    fn = os.path.join(folder, f"lista_TH03.txt")
    list_file = pd.read_table(fn)
    date_converted = []
    for i in list_file.values:
        if str(i[0][-1]) == '*':
            val = str(i[0][-9:-2])
        else:
            val = str(i[0][-8:])
        date_converted.append(val)

    hyso_seismo = pd.DataFrame(columns=['dt', 'mask'])
    hyso_seismo_missing = pd.DataFrame(columns=['dt', 'mask'])
    for i in date_list:
        if i.strftime('%Y.%j') in date_converted:
            hyso_seismo.loc[i] = [i, True]
        else:
            hyso_seismo_missing.loc[i] = [i, True]

    sida_tls.save_txt(instr, hyso_seismo)
    sida_tls.save_txt(instr, hyso_seismo_missing, missing=True)
