#!/usr/local/bin/python3
# -*- coding: utf-8 -*-
"""
Script for managing instrument metadata, events, and campaigns.
"""

# =============================================================
# GENERAL INFORMATION
# =============================================================

__author__ = "Filippo Cali' Quaglia, Monica Tosco"
__credits__ = ["??????"]
__license__ = "GPL"
__version__ = "1.1"
__email__ = "filippo.caliquaglia@ingv.it"
__status__ = "Research"
__lastupdate__ = "February 2025"

import datetime as dt
import os

# =============================================================
# DEFINE BASE FOLDERS
# =============================================================

basefolder = os.path.join("H:\\Shared drives", "Dati_THAAO")
basefolder_skycam = os.path.join("H:\\Shared drives", "Dati_THAAO_skycam")
da_folder = os.path.join(basefolder, 'thaao_data_availability')

# =============================================================
# DEFINE COMMON DATES
# =============================================================

today = dt.datetime.today()
start_season = dt.datetime(1900, 1, 1)
end_season = dt.datetime(1900, 12, 31)

# =============================================================
# SUMMARY PLOTS
# =============================================================
time_res = 'D'
update_threshold = 7

# =============================================================
# DEFINE INSTRUMENT LISTS
# =============================================================

instr_sets = {
    "thaao": ['rs_sondes', 'rad_uli', 'rad_dli', 'rad_usi', 'rad_dsi', 'rad_par_up', 'rad_par_down', 'rad_tb', 'skycam',
              'mms_trios', 'metar', 'vespa', 'ceilometer', 'dir_rad_trkr', 'pm10', 'ftir', 'aeronet', 'gnss',
              'ecapac_mrr', 'ecapac_aws_snow', 'ecapac_disdro_precip', 'aws_vespa'],
    "legacy": ['uv-vis_spec', 'lidar_ae', 'o3_sondes', 'aero_sondes', 'gbms', 'wv_isotopes', 'lidar_temp', 'hatpro'],
    "hyso": ['hyso_seismo_1', 'hyso_seismo_2', 'hyso_seismo_3', 'hyso_seismo_4', 'hyso_tide_1'], }

instr_sets["all"] = instr_sets["legacy"] + instr_sets["hyso"] + instr_sets["thaao"]
instr_list = []

# =============================================================
# VARIABLES DICTIONARY
# =============================================================

vars_dict = {'cbh_vars': {'CBH_L1[m]'}, 'temp_vars': {'AirTC', 'tmpc'}, 'press_vars': {'mslp', 'BP_mbar'},
    'pm10_vars'        : {'PM10'}, 'relh_vars': {'relh', 'RH'}, 'tcc_vars': {'TCC[okt]'},
    'no2_vars'         : {'NO2 vertical column density (430 nm)'},
    'o3_vars'          : {'O3 vertical column density (510 nm)', 'O3 vertical column density (530 nm)', 'o3'},
    'atm_gases_vars'   : {'c2h6', 'co', 'h2co', 'hcn', 'hf', 'hno3', 'nh3', 'ocs'}, 'atm_ch4_vars': {'ch4'},
    'lwp_vars'         : {}, 'aod_vars': {'AOD_440nm'}, 'dsi_vars': {}, 'usi_vars': {}, 'bt_vars': {}, 'uli_vars': {},
    'dli_vars'         : {}, 'alb_vars': {}, 'iwv_vars': {'PWV'}}


# =============================================================
# FUNCTION: CREATE INSTRUMENT METADATA
# =============================================================

def create_instr_metadata(start_instr, end_instr=today, start_seas=start_season, end_seas=end_season,
                          data_avail_py=None, institution=None, plot_vars=None):
    """
    Creates a dictionary with instrument metadata.
    """
    return {'institution': institution, 'start_instr': start_instr, 'end_instr': end_instr, 'start_seas': start_seas,
            'end_seas'   : end_seas, 'data_avail_py': data_avail_py, 'plot_vars': plot_vars}


metadata_entries = {'aeronet'                                                                                    : create_instr_metadata(
        dt.datetime(2007, 3, 1), institution='NCAR/NASA', start_seas=dt.datetime(1900, 3, 1),
        end_seas=dt.datetime(1900, 10, 31), data_avail_py='thaao_aeronet.py', plot_vars={'AOD_440nm': ('green', '')}),
    'aero_sondes'                                                                                                : create_instr_metadata(
            dt.datetime(1992, 1, 1), dt.datetime(1998, 12, 31), institution='DMI',
            data_avail_py='thaao_aero_sondes.py'),
    'aws_vespa'                                                                                                  : create_instr_metadata(
            dt.datetime(2016, 1, 1), institution='INGV', data_avail_py='thaao_aws_vespa.py'),
    'ceilometer'                                                                                                 : create_instr_metadata(
            dt.datetime(2019, 11, 1), institution='ENEA', data_avail_py='thaao_ceilometer.py',
            plot_vars={'CBH_L1[m]': ('red', ''), 'TCC[okt]': ('red', '')}),
    'dir_rad_trkr'                                                                                               : create_instr_metadata(
            dt.datetime(2002, 10, 1), institution='DMI+ENEA', start_seas=dt.datetime(1900, 2, 1),
            end_seas=dt.datetime(1900, 10, 31), data_avail_py='thaao_dir_rad_trkr.py'),
    'ecapac_mrr'                                                                                                 : create_instr_metadata(
            dt.datetime(2023, 3, 1), institution='ENEA', data_avail_py='thaao_ecapac_mrr.py'),
    'ecapac_aws_snow'                                                                                            : create_instr_metadata(
            dt.datetime(2023, 3, 1), institution='ENEA', data_avail_py='thaao_ecapac_aws_snow.py',
            plot_vars={'AirTC': ('grey', 'degC'), 'RH': ('blue', '%'), 'BP_mbar': ('cyan', 'hPa')}),
    'ecapac_disdro_precip'                                                                                       : create_instr_metadata(
            dt.datetime(2023, 3, 1), institution='ENEA', data_avail_py='thaao_ecapac_disdro_precip.py'),
    'ftir'                                                                                                       : create_instr_metadata(
            dt.datetime(1999, 10, 1), institution='NCAR/NASA', start_seas=dt.datetime(1900, 3, 1),
            end_seas=dt.datetime(1900, 10, 31), data_avail_py='thaao_ftir.py',
            plot_vars={'ch4' : ('red', '??'), 'o3': ('purple', '??'), 'c2h6': ('green', '??'), 'co': ('green', '??'),
                       'h2co': ('green', '??'),
                       # 'clono2': ('green', '??'), 'hcl': ('green', '??'),'n20': ('green', '??'),
                       'hcn' : ('green', '??'), 'hf': ('green', '??'), 'hno3': ('green', '??'), 'nh3': ('green', '??'),
                       'ocs' : ('green', '??')}),
    'gbms'                                                                                                       : create_instr_metadata(
            dt.datetime(1992, 1, 1), dt.datetime(2012, 12, 31), institution='U.Alaska,Florence,StonyBrook/USSF',
            data_avail_py='thaao_gbms.py'),
    'hatpro'                                                                                                     : create_instr_metadata(
            dt.datetime(2017, 1, 1), dt.datetime(2024, 9, 30), institution='ENEA', data_avail_py='thaao_hatpro.py'),
    'lidar_temp'                                                                                                 : create_instr_metadata(
            dt.datetime(1993, 11, 1), institution='U.Sap+ENEA', start_seas=dt.datetime(1900, 11, 1),
            end_seas=dt.datetime(1900, 3, 31), data_avail_py='thaao_lidar_temp.py'),
    'lidar_ae'                                                                                                   : create_instr_metadata(
            dt.datetime(1991, 9, 1), dt.datetime(1996, 3, 31), institution='U.Sap+ENEA',
            data_avail_py='thaao_lidar_ae.py'),
    'hyso_seismo_1'                                                                                              : create_instr_metadata(
            dt.datetime(2021, 8, 1), institution='INGV', start_seas=dt.datetime(1900, 3, 1),
            end_seas=dt.datetime(1900, 10, 31), data_avail_py='thaao_hyso_seismo_1.py'),
    'hyso_seismo_2'                                                                                              : create_instr_metadata(
            dt.datetime(2021, 8, 1), institution='INGV', start_seas=dt.datetime(1900, 3, 1),
            end_seas=dt.datetime(1900, 10, 31), data_avail_py='thaao_hyso_seismo_2.py'),
    'hyso_seismo_3'                                                                                              : create_instr_metadata(
            dt.datetime(2021, 8, 1), institution='INGV', start_seas=dt.datetime(1900, 3, 1),
            end_seas=dt.datetime(1900, 10, 31), data_avail_py='thaao_hyso_seismo_3.py'),
    'hyso_seismo_4'                                                                                              : create_instr_metadata(
            dt.datetime(2022, 9, 1), institution='INGV', start_seas=dt.datetime(1900, 3, 1),
            end_seas=dt.datetime(1900, 10, 31), data_avail_py='thaao_hyso_seismo_4.py'),
    'hyso_tide_1'                                                                                                : create_instr_metadata(
            dt.datetime(2021, 8, 1), institution='INGV', start_seas=dt.datetime(1900, 3, 1),
            end_seas=dt.datetime(1900, 10, 31), data_avail_py='thaao_hyso_tide_1.py'),
    'metar'                                                                                                      : create_instr_metadata(
            dt.datetime(1951, 10, 1), institution='U.Alaska,Florence,StonyBrook/USSF', data_avail_py='thaao_metar.py',
            plot_vars={'tmpc': ('brown', 'degC'), 'relh': ('blue', '%'), 'mslp': ('purple', 'hPa')}),
    'mms_trios'                                                                                                  : create_instr_metadata(
            dt.datetime(2021, 9, 1), institution='INGV', data_avail_py='thaao_mms_trios.py'),
    'o3_sondes'                                                                                                  : create_instr_metadata(
            dt.datetime(1991, 12, 1), dt.datetime(2016, 12, 31), institution='DMI', data_avail_py='thaao_o3_sondes.py'),
    'pm10'                                                                                                       : create_instr_metadata(
            dt.datetime(2010, 1, 1), institution='U.Alaska,Florence,StonyBrook/USSF', data_avail_py='thaao_pm10.py',
            plot_vars={'PM10': ('black', 'ug m-3')}),
    'rad_dli'                                                                                                    : create_instr_metadata(
            dt.datetime(2009, 1, 1), institution='ENEA', data_avail_py='thaao_rad.py'),
    'rad_dsi'                                                                                                    : create_instr_metadata(
            dt.datetime(2003, 2, 1), institution='DMI+ENEA', data_avail_py='thaao_rad.py'),
    'rad_par_down'                                                                                               : create_instr_metadata(
            dt.datetime(2016, 7, 1), institution='ENEA', data_avail_py='thaao_rad.py'),
    'rad_par_up'                                                                                                 : create_instr_metadata(
            dt.datetime(2016, 7, 1), institution='ENEA', data_avail_py='thaao_rad.py'),
    'rad_tb'                                                                                                     : create_instr_metadata(
            dt.datetime(2017, 1, 1), institution='ENEA', data_avail_py='thaao_rad.py'),
    'rad_uli'                                                                                                    : create_instr_metadata(
            dt.datetime(2016, 7, 1), institution='ENEA', data_avail_py='thaao_rad.py'),
    'rad_usi'                                                                                                    : create_instr_metadata(
            dt.datetime(2016, 7, 1), institution='ENEA', data_avail_py='thaao_rad.py'),
    'rs_sondes'                                                                                                  : create_instr_metadata(
            dt.datetime(1973, 1, 1), institution='DMI+INGV', data_avail_py='thaao_rs_sondes.py'),
    'skycam'                                                                                                     : create_instr_metadata(
            dt.datetime(2016, 7, 1), institution='ENEA', data_avail_py='thaao_skycam.py'),
    'gnss'                                                                                                       : create_instr_metadata(
            dt.datetime(2021, 5, 1), institution='INGV', data_avail_py='thaao_gnss.py'),
    'uv-vis_spec'                                                                                                : create_instr_metadata(
            dt.datetime(1991, 2, 1), dt.datetime(2016, 11, 30), institution='DMI',  # 1991-2016
            data_avail_py='thaao_uv-vis_spec.py', plot_vars={'NO2 vertical column density (430 nm)': ('orange', '??'),
                                                             'O3 vertical column density (510 nm)' : ('green', '??'),
                                                             'O3 vertical column density (530 nm)' : ('green', '??')}),
    'vespa'                                                                                                      : create_instr_metadata(
            dt.datetime(2016, 7, 1), institution='INGV', data_avail_py='thaao_vespa.py',
            plot_vars={'PWV': ('cyan', '??')}),
    'wv_isotopes'                                                                                                : create_instr_metadata(
            dt.datetime(2011, 6, 1), dt.datetime(2019, 12, 31), institution='U.Alaska,Florence,StonyBrook/USSF',
            data_avail_py='thaao_wv_isotopes.py')}

instr_metadata = {
    name: {**meta, 'end_instr': meta.get('end_instr', today), 'start_seas': meta.get('start_seas', start_season),
           'end_seas'         : meta.get('end_seas', end_season), } for name, meta in metadata_entries.items()}

for idx, key in enumerate(metadata_entries.keys()):
    instr_metadata[key]["idx"] = idx

# metadata_entries = {
#     'aeronet': create_instr_metadata(
#         dt(2007, 3, 1), institution='NCAR/NASA', start_seas=dt(1900, 3, 1),
#         end_seas=dt(1900, 10, 31), data_avail_py='thaao_aeronet.py',
#         plot_vars={'AOD_440nm': {'color': 'green', 'unit': '', 'category': 'aod'}}
#     ),
#     'metar': create_instr_metadata(
#         dt(1951, 10, 1), institution='U.Alaska,Florence,StonyBrook/USSF',
#         data_avail_py='thaao_metar.py',
#         plot_vars={'tmpc': {'color': 'brown', 'unit': '°C', 'category': 'temp'},
#                    'mslp': {'color': 'purple', 'unit': 'hPa', 'category': 'press'}}
#     ),
#     # Add more instruments here...
# }
#
# # Function to get variables for each category for a given instrument
# def get_vars_by_all_categories(instrument_name):
#     instrument = metadata_entries.get(instrument_name)
#
#     if not instrument:
#         return {}  # Return empty dictionary if the instrument is not found
#
#     # Initialize a dictionary to store variables by category
#     vars_by_category = {}
#
#     # Loop through each variable in plot_vars and group by category
#     for var_name, var_info in instrument['plot_vars'].items():
#         category = var_info.get('category')  # Get the category of the variable
#         if category:  # Check if the category exists
#             if category not in vars_by_category:
#                 vars_by_category[category] = []
#             vars_by_category[category].append(var_name)
#
#     return vars_by_category
#
#
# # Example usage:
# instrument_name = 'metar'  # Choose your instrument name
# vars_by_category = get_vars_by_all_categories(instrument_name)
# print(vars_by_category)

# =============================================================
# INSTITUTION COLORS
# =============================================================

institution_colors = {'DMI'                              : 'cyan', 'INGV': 'black', 'ENEA': 'red',
                      'NCAR/NASA'                        : 'purple', 'ENEA+INGV': 'green', 'U.Sap+ENEA': 'brown',
                      'DMI+INGV'                         : 'orange', 'DMI+ENEA': 'pink',
                      'U.Alaska,Florence,StonyBrook/USSF': 'blue', 'not active': 'grey'}

# =============================================================
# IMPORTANT EVENTS DICTIONARY
# =============================================================

events_dict = {1 : {'date': dt.datetime(2012, 6, 30), 'label': 'bldg. #1985 --> \n bldg. #1971'},
               2 : {'date': today, 'label': 'today'},
               3 : {'date': dt.datetime(1951, 6, 6), 'label': 'TAB installation \n starts'},
               4 : {'date': dt.datetime(1951, 10, 1), 'label': 'TAB installation \n ends'},
               5 : {'date': dt.datetime(1945, 9, 2), 'label': 'WW II ends'},
               6 : {'date': dt.datetime(1989, 9, 1), 'label': 'Berlin Wall falls'},
               7 : {'date': dt.datetime(1991, 11, 12), 'label': 'I was born :)'},
               8 : {'date': dt.datetime(1910, 6, 30), 'label': 'Thule Outpost'},
               9 : {'date': dt.datetime(1912, 6, 30), 'label': "First (of 7) Rasmussen's \n Expeditions"},
               10: {'date': dt.datetime(2023, 4, 6), 'label': 'TAB --> PSB'},
               11: {'date': dt.datetime(1933, 3, 30), 'label': 'Thule Outpost under \n the Danish Gov. control'},
               12: {'date': dt.datetime(1914, 7, 28), 'label': 'WW I starts'},
               13: {'date': dt.datetime(1918, 11, 11), 'label': 'WW I ends'},
               14: {'date': dt.datetime(1959, 3, 30), 'label': 'First NSF prj \n in Thule funded'},
               15: {'date': dt.datetime(1903, 3, 30), 'label': 'Danish Literary \n Expedition'},
               16: {'date': dt.datetime(1968, 1, 21), 'label': 'B-52 crash'},
               17: {'date': dt.datetime(2007, 3, 1), 'label': 'Fourth IPY --> APECS!'},
               18: {'date': dt.datetime(1958, 3, 30), 'label': 'Camp Century \n construction'},
               19: {'date': dt.datetime(1961, 3, 30), 'label': 'BMEWS \n construction'},
               20: {'date': dt.datetime(1966, 3, 30), 'label': 'Camp Century \n abandoned'},
               21: {'date': dt.datetime(1939, 9, 1), 'label': 'WW II starts'},
               22: {'date': dt.datetime(1958, 3, 30), 'label': 'Op. Chrome \n Dome '},
               23: {'date': dt.datetime(1953, 3, 30), 'label': 'Op. IceCap'},
               24: {'date': dt.datetime(1991, 6, 15), 'label': 'Mt. Pinatubo \n eruption'},
               25: {'date': dt.datetime(1982, 3, 29), 'label': 'El Chichón eruption'},
               27: {'date': dt.datetime(1981, 3, 18), 'label': 'Italy signs \n the Antarctic Treaty'},
               28: {'date': dt.datetime(2013, 6, 30), 'label': 'PRA'},
               29: {'date': dt.datetime(1997, 6, 30), 'label': 'CNR "Dirigibile Italia" \n station'},
               30: {'date': dt.datetime(1928, 5, 24), 'label': 'U. Nobile above \n North Pole'},
               31: {'date': dt.datetime(1932, 6, 30), 'label': 'Second IPY'},
               32: {'date': dt.datetime(1957, 6, 30), 'label': 'Third IPY'},
               33: {'date': dt.datetime(1990, 6, 30), 'label': 'IT lidar \n @bldg. #216 \n @TAB'},
               34: {'date': dt.datetime(2010, 6, 30), 'label': 'IT lidar --> \n bldg. #1971@S.Mount.'},
               35: {'date': dt.datetime(1972, 6, 30), 'label': 'DMI lab \n @bldg. #1985 ?'},
               36: {'date': dt.datetime(1943, 6, 30), 'label': 'Bluie West 6 \n Met Station'},
               37: {'date': dt.datetime(1954, 12, 1), 'label': 'DMI takes over \n the Bluie West 6 \n Met Station'},
               38: {'date': dt.datetime(1985, 6, 30), 'label': 'Greenland \n exits CEE'},
               39: {'date': dt.datetime(1953, 6, 30), 'label': 'Greenland ex-Danish \n colony'},
               40: {'date': dt.datetime(2023, 4, 6), 'label': 'Greenland National \n Research Strategy \n Plan'},
               41: {'date': dt.datetime(2012, 6, 30), 'label': 'IT Observatory Status \n @ Arctic Council'},
               42: {'date': dt.datetime(1954, 6, 30), 'label': 'DEW line \n building'},
               43: {'date': dt.datetime(2020, 2, 1), 'label': 'COVID hits'},
               44: {'date': dt.datetime(2019, 5, 14), 'label': 'CLARA2 prj \n PNRA 3y'},
               45: {'date': dt.datetime(2020, 6, 30), 'label': 'MACMAP prj \n INGV 3y'},
               46: {'date': dt.datetime(2021, 1, 4), 'label': 'ECAPAC prj \n PRA 2y'},
               47: {'date': dt.datetime(2021, 6, 30), 'label': 'SEANA prj \n ext 2y'},
               48: {'date': dt.datetime(2016, 6, 30), 'label': 'OASIS-YOPP prj \n PNRA 2y'},
               49: {'date': dt.datetime(2015, 6, 30), 'label': 'SVAAP prj \n PNRA 1y'},
               50: {'date': dt.datetime(2014, 6, 30), 'label': 'ARCA prj \n MIUR 2y'},
               51: {'date': dt.datetime(1947, 1, 30), 'label': 'DMI Geomagnetic Obs'},
               52: {'date': dt.datetime(1953, 6, 30), 'label': 'Pituffik inhabitants \n relocated to Qaanaaq'},
               53: {'date': dt.datetime(1941, 6, 30), 'label': 'Bluie West Program \n starts'},
               54: {'date': dt.datetime(2024, 7, 1), 'label': 'NASA ARCSIX'},
               55: {'date': dt.datetime(2024, 6, 1), 'label': 'THAAO funded as \n INGV infrastructure'}, }

# =============================================================
# CAMPAIGNS DICTIONARY
# =============================================================

campaigns_dict = {1 : {'start': dt.datetime(1991, 1, 1), 'end': dt.datetime(1991, 1, 31)},
                  2 : {'start': dt.datetime(1991, 12, 1), 'end': dt.datetime(1991, 12, 31)},
                  3 : {'start': dt.datetime(1992, 1, 1), 'end': dt.datetime(1992, 1, 31)},
                  4 : {'start': dt.datetime(1992, 11, 1), 'end': dt.datetime(1992, 11, 30)},
                  5 : {'start': dt.datetime(1993, 1, 1), 'end': dt.datetime(1993, 1, 31)},
                  6 : {'start': dt.datetime(1993, 7, 1), 'end': dt.datetime(1993, 7, 31)},
                  7 : {'start': dt.datetime(1994, 1, 1), 'end': dt.datetime(1994, 1, 31)},
                  8 : {'start': dt.datetime(1994, 7, 1), 'end': dt.datetime(1994, 7, 31)},
                  9 : {'start': dt.datetime(1995, 1, 1), 'end': dt.datetime(1995, 1, 31)},
                  10: {'start': dt.datetime(1997, 1, 1), 'end': dt.datetime(1997, 1, 31)},
                  11: {'start': dt.datetime(1998, 5, 1), 'end': dt.datetime(1998, 5, 31)},
                  12: {'start': dt.datetime(2002, 1, 1), 'end': dt.datetime(2002, 1, 31)},
                  13: {'start': dt.datetime(2003, 1, 1), 'end': dt.datetime(2003, 1, 31)},
                  14: {'start': dt.datetime(2006, 12, 1), 'end': dt.datetime(2006, 12, 31)},
                  15: {'start': dt.datetime(2009, 1, 1), 'end': dt.datetime(2009, 1, 31)},
                  16: {'start': dt.datetime(2010, 1, 1), 'end': dt.datetime(2010, 1, 31)},
                  17: {'start': dt.datetime(2010, 10, 1), 'end': dt.datetime(2010, 10, 31)},
                  18: {'start': dt.datetime(2012, 1, 1), 'end': dt.datetime(2012, 2, 29)},
                  19: {'start': dt.datetime(2013, 2, 21), 'end': dt.datetime(2013, 3, 18)},
                  20: {'start': dt.datetime(2014, 1, 1), 'end': dt.datetime(2014, 2, 28)},
                  21: {'start': dt.datetime(2016, 6, 11), 'end': dt.datetime(2016, 7, 18)},
                  22: {'start': dt.datetime(2017, 2, 16), 'end': dt.datetime(2017, 2, 21)},
                  23: {'start': dt.datetime(2018, 2, 22), 'end': dt.datetime(2018, 3, 2)},
                  24: {'start': dt.datetime(2019, 2, 27), 'end': dt.datetime(2019, 3, 8)},
                  25: {'start': dt.datetime(2019, 11, 6), 'end': dt.datetime(2019, 11, 15)},
                  26: {'start': dt.datetime(2021, 4, 21), 'end': dt.datetime(2021, 5, 21)},
                  27: {'start': dt.datetime(2021, 8, 10), 'end': dt.datetime(2021, 8, 27)},
                  28: {'start': dt.datetime(2022, 3, 22), 'end': dt.datetime(2022, 4, 9)},
                  29: {'start': dt.datetime(2022, 9, 7), 'end': dt.datetime(2022, 9, 23)},
                  30: {'start': dt.datetime(2023, 4, 18), 'end': dt.datetime(2023, 5, 6)},
                  31: {'start': dt.datetime(2023, 9, 26), 'end': dt.datetime(2023, 10, 5)},
                  32: {'start': dt.datetime(2024, 3, 19), 'end': dt.datetime(2024, 4, 6)},
                  33: {'start': dt.datetime(2024, 5, 25), 'end': dt.datetime(2024, 6, 17)},
                  34: {'start': dt.datetime(2024, 7, 22), 'end': dt.datetime(2024, 8, 7)},
                  35: {'start': dt.datetime(2024, 9, 26), 'end': dt.datetime(2024, 10, 5)}}
