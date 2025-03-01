#!/usr/local/bin/python3
# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------------
"""
OKcsv
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

instr = 'ecapac_aws_snow'


def update_data_avail(instr):
    import os

    import pandas as pd
    import numpy as np
    import settings as ts
    import single_instr_data_avail.tools as sida_tls

    date_list = pd.date_range(
            ts.instr_metadata[instr]['start_instr'], ts.instr_metadata[instr]['end_instr'], freq='D').tolist()
    folder = os.path.join(ts.basefolder, "thaao_" + instr)

    ecapac_aws_snow = pd.DataFrame()
    for i in date_list:
        fn = generate_file_path(i, folder)
        print(fn)
        if os.path.exists(fn):
            tmp = pd.read_table(
                    fn, skiprows=4, header=None, sep=',', parse_dates={'datetime': [0]},
                    date_format='%Y-%m-%d %H:%M:%S', index_col='datetime',
                    names=["TIMESTAMP", "RECORD", "BattV", "PTemp_C", "BP_mbar", "AirTC", "RH", "WS_aws", "WD_aws",
                           "DT", "Q", "TCDT", "PR", "WAVG", "PRTOT", "PRLAST", "RIINST", "RI", "T_pluvio", "U",
                           "STATUS", "PRcor", "PRTOTCOR", "WS_pluvio", "PRINST"])
            ecapac_aws_snow = pd.concat([ecapac_aws_snow, tmp])  # cleanup
    msk = ecapac_aws_snow["BP_mbar"][ecapac_aws_snow["BP_mbar"] < 940].index
    ecapac_aws_snow.loc[msk, "BP_mbar"] = np.nan
    ecapac_aws_snow = ecapac_aws_snow[["BP_mbar", "AirTC", "RH"]]

    # Save the DataFrame to a text file
    sida_tls.save_csv(instr, ecapac_aws_snow)


def generate_file_path(date, fol):
    import os
    """Generate the file path for the given date."""
    year_dir = os.path.join(fol, "AWS_ECAPAC", date.strftime('%Y'))
    file_name = f"AWS_THAAO_{date.strftime('%Y_%m_%d')}_00_00.dat"
    return os.path.join(year_dir, file_name)
