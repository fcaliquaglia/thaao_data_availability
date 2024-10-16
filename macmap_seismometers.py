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

import numpy as np
import pandas as pd

import thaao_settings as ts

instr = 'macmap_seisometers'
date_list = pd.date_range(
        ts.instr_na_list[instr]['start_instr'], ts.instr_na_list[instr]['end_instr'], freq='D').tolist()
folder = os.path.join(ts.basefolder, "thaao_" + instr)
if __name__ == "__main__":

    for station in [1, 2, 3, 4]:
        fn = os.path.join(folder, "lista_TH0" + str(station) + ".txt")
        list_file = pd.read_table(fn)
        date_converted = []
        for i in list_file.values:
            if str(i[0][-1]) == '*':
                val = str(i[0][-9:-2])
            else:
                val = str(i[0][-8:])
            date_converted.append(val)

        if station == 1:
            for man_dat in np.arange(125, 155):
                date_converted.append('2023.' + str(man_dat))
        if station == 2:
            for man_dat in np.arange(113, 120):
                date_converted.append('2023.' + str(man_dat))
        if station == 3:
            for man_dat in np.arange(110, 155):
                date_converted.append('2023.' + str(man_dat))
        if station == 4:
            for man_dat in np.arange(113, 155):
                date_converted.append('2023.' + str(man_dat))

        macmap_seismo = pd.DataFrame(columns=['dt', 'mask'])
        for i in date_list:
            if i.strftime('%Y.%j') in date_converted:
                macmap_seismo.loc[i] = [i, True]

        ts.save_txt(instr + '_' + str(station), macmap_seismo)
