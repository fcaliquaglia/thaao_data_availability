#!/usr/local/bin/python3
# -*- coding: utf-8 -*-
"""
Brief description
"""

# =============================================================
# CREATED:
# AFFILIATION: INGV
# AUTHORS: Filippo Cali' Quaglia
# =============================================================
__author__ = "Filippo Cali' Quaglia, Monica Tosco"
__credits__ = ["??????"]
__license__ = "GPL"
__version__ = "0.1"
__email__ = "filippo.caliquaglia@ingv.it"
__status__ = "Research"
__lastupdate__ = ""

import datetime as dt
import os

# Define base folders for data
basefolder = os.path.join("H:\\Shared drives", "Dati_THAAO")
basefolder_skycam = os.path.join("H:\\Shared drives", "Dati_THAAO_skycam")
da_folder = os.path.join(basefolder, 'thaao_data_availability')

# Define instrument lists
instr_list_current = ['rs_sondes', 'rad_uli', 'rad_dli', 'rad_usi', 'rad_dsi', 'rad_par_up', 'rad_par_down', 'rad_tb',
                      'skycam', 'mms_trios', 'metar', 'vespa', 'ceilometer', 'hatpro', 'dir_rad_trkr', 'pm10', 'ftir',
                      'aeronet', 'gnss', 'ecapac_mrr', 'ecapac_aws_snow', 'ecapac_disdro_precip', 'aws_vespa']
instr_list_legacy = ['uv-vis_spec', 'lidar_ae', 'o3_sondes', 'aero_sondes', 'gbms', 'wv_isotopes', 'lidar_temp']
instr_list_macmap = ['macmap_seismometer_1', 'macmap_seismometer_2', 'macmap_seismometer_3', 'macmap_seismometer_4',
                     'macmap_tide_gauge']

# Dynamically build instr_sets
instr_sets = {"all"   : instr_list_current + instr_list_legacy + instr_list_macmap, "macmap": instr_list_macmap,
              "legacy": instr_list_legacy, "current": instr_list_current}

# Define default values for common dates to avoid repetition
today = dt.datetime.today()
start_season = dt.datetime(1900, 1, 1)
end_season = dt.datetime(1900, 12, 31)


# Define a function to reduce redundancy in instrument metadata
def create_instr_metadata(start_instr, end_instr=today, start_seas=start_season, end_seas=end_season, institution=None):
    return {'institution': institution, 'start_instr': start_instr, 'end_instr': end_instr, 'start_seas': start_seas,
            'end_seas'   : end_seas}


# Instrument metadata with optimized structure
instr_metadata = {'aeronet'                                                                : create_instr_metadata(
        dt.datetime(2007, 3, 1), institution='NCAR/NASA'), 'aero_sondes'                   : create_instr_metadata(
        dt.datetime(1992, 1, 1), dt.datetime(1998, 12, 31), institution='DMI'), 'aws_vespa': create_instr_metadata(
        dt.datetime(2016, 1, 1), institution='INGV'), 'ceilometer'                         : create_instr_metadata(
        dt.datetime(2019, 11, 1), institution='ENEA'), 'dir_rad_trkr'                      : create_instr_metadata(
        dt.datetime(2002, 10, 1), institution='DMI+ENEA', start_seas=dt.datetime(1900, 2, 1),
        end_seas=dt.datetime(1900, 10, 31)), 'ecapac_mrr'                                  : create_instr_metadata(
        dt.datetime(2022, 9, 1), institution='ENEA'), 'ecapac_aws_snow'                    : create_instr_metadata(
        dt.datetime(2022, 9, 1), institution='ENEA'), 'ecapac_disdro_precip'               : create_instr_metadata(
        dt.datetime(2022, 9, 1), institution='ENEA'), 'ftir'                               : create_instr_metadata(
        dt.datetime(1999, 10, 1), institution='NCAR/NASA', start_seas=dt.datetime(1900, 3, 1),
        end_seas=dt.datetime(1900, 10, 31)), 'gbms'                                        : create_instr_metadata(
        dt.datetime(1992, 1, 1), dt.datetime(2012, 12, 31), institution='U.Alaska,Florence,StonyBrook/USSF'),
    'hatpro'                                                                               : create_instr_metadata(
        dt.datetime(2017, 1, 1), dt.datetime(2024, 9, 30), institution='ENEA'),
    'lidar_temp'                                                                           : create_instr_metadata(
            dt.datetime(1993, 11, 1), institution='U.Sap+ENEA', start_seas=dt.datetime(1900, 11, 1),
            end_seas=dt.datetime(1900, 3, 31)), 'lidar_ae'                                 : create_instr_metadata(
            dt.datetime(1991, 9, 1), dt.datetime(1996, 3, 31), institution='U.Sap+ENEA',
            start_seas=dt.datetime(1900, 9, 1),
            end_seas=dt.datetime(1900, 3, 31)),
    'macmap_seismometer_1'                                                                 : create_instr_metadata(
        dt.datetime(2021, 8, 1), institution='INGV'),
    'macmap_seismometer_2'                                                                 : create_instr_metadata(
        dt.datetime(2021, 8, 1), institution='INGV'),
    'macmap_seismometer_3'                                                                 : create_instr_metadata(
        dt.datetime(2021, 8, 1), institution='INGV'),
    'macmap_seismometer_4'                                                                 : create_instr_metadata(
        dt.datetime(2022, 9, 1), institution='INGV'),
    'macmap_tide_gauge'                                                                    : create_instr_metadata(
        dt.datetime(2021, 8, 1), institution='INGV'),
    'metar'                                                                                : create_instr_metadata(
        dt.datetime(1951, 10, 1), institution='U.Alaska,Florence,StonyBrook/USSF'),
    'mms_trios'                                                                            : create_instr_metadata(
        dt.datetime(2021, 9, 1), institution='INGV'),
    'o3_sondes'                                                                            : create_instr_metadata(
        dt.datetime(1991, 12, 1), dt.datetime(2016, 12, 31), institution='DMI'),
    'pm10'                                                                                 : create_instr_metadata(
        dt.datetime(2010, 1, 1), institution='U.Alaska,Florence,StonyBrook/USSF'),
    'rad_dli'                                                                              : create_instr_metadata(
        dt.datetime(2009, 1, 1), institution='ENEA'),
    'rad_dsi'                                                                              : create_instr_metadata(
        dt.datetime(2003, 2, 1), institution='DMI+ENEA'),
    'rad_par_down'                                                                         : create_instr_metadata(
        dt.datetime(2016, 7, 1), institution='ENEA'),
    'rad_par_up'                                                                           : create_instr_metadata(
        dt.datetime(2016, 7, 1), institution='ENEA'),
    'rad_tb'                                                                               : create_instr_metadata(
        dt.datetime(2017, 1, 1), institution='ENEA'),
    'rad_uli'                                                                              : create_instr_metadata(
        dt.datetime(2016, 7, 1), institution='ENEA'),
    'rad_usi'                                                                              : create_instr_metadata(
        dt.datetime(2016, 7, 1), institution='ENEA'),
    'rs_sondes'                                                                            : create_instr_metadata(
        dt.datetime(1973, 1, 1), institution='DMI+INGV'),
    'skycam'                                                                               : create_instr_metadata(
        dt.datetime(2016, 7, 1), institution='ENEA'),
    'gnss'                                                                                 : create_instr_metadata(
        dt.datetime(2021, 5, 1), institution='INGV'),
    'uv-vis_spec'                                                                          : create_instr_metadata(
        dt.datetime(1991, 2, 1), dt.datetime(2016, 11, 30), institution='DMI'),
    'vespa'                                                                                : create_instr_metadata(
        dt.datetime(2016, 7, 1), institution='INGV'), 'wv_isotopes'                        : create_instr_metadata(
            dt.datetime(2011, 6, 1), dt.datetime(2019, 12, 31), institution='U.Alaska,Florence,StonyBrook/USSF')}

# Define institution colors
institution_colors = {'DMI'       : 'green', 'INGV': 'blue', 'ENEA': 'red', 'NCAR/NASA': 'purple',
                      'ENEA+INGV' : 'olive', 'U.Sap+ENEA': 'brown', 'DMI+INGV': 'orange',
                      'DMI+ENEA'  : 'pink', 'U.Alaska,Florence,StonyBrook/USSF': 'black',
                      'not active': 'grey'}

events_dict = {1 : {'date': dt.datetime(2012, 6, 30), 'label': 'bldg. #1985 --> \n bldg. #1971'},
               2 : {'date': dt.datetime.today(), 'label': 'today'},
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


# #!/usr/local/bin/python3
# # -*- coding: utf-8 -*-
# # -------------------------------------------------------------------------------
# #
# """
# Brief description
# """
#
# # =============================================================
# # CREATED:
# # AFFILIATION: INGV
# # AUTHORS: Filippo Cali' Quaglia
# # =============================================================
# #
# # -------------------------------------------------------------------------------
# __author__ = "Filippo Cali' Quaglia, Monica Tosco"
# __credits__ = ["??????"]
# __license__ = "GPL"
# __version__ = "0.1"
# __email__ = "filippo.caliquaglia@ingv.it"
# __status__ = "Research"
# __lastupdate__ = ""
#
# import datetime as dt
# import os
#
# basefolder = os.path.join("H:\\Shared drives", "Dati_THAAO")
# basefolder_skycam = os.path.join("H:\\Shared drives", "Dati_THAAO_skycam")
# da_folder = os.path.join(basefolder, 'thaao_data_availability')
#
# instr_list_current = ['rs_sondes', 'rad_uli', 'rad_dli', 'rad_usi', 'rad_dsi', 'rad_par_up', 'rad_par_down', 'rad_tb',
#                       'skycam', 'mms_trios', 'metar', 'vespa', 'ceilometer', 'hatpro', 'dir_rad_trkr', 'pm10', 'ftir',
#                       'aeronet', 'gnss', 'ecapac_mrr', 'ecapac_aws_snow', 'ecapac_disdro_precip', 'aws_vespa']
# instr_list_legacy = ['uv-vis_spec', 'lidar_ae', 'o3_sondes', 'aero_sondes', 'gbms', 'wv_isotopes', 'lidar_temp']
# instr_list_macmap = ['macmap_seismometer_1', 'macmap_seismometer_2', 'macmap_seismometer_3', 'macmap_seismometer_4',
#                      'macmap_tide_gauge']
# instr_sets = {"all"   : instr_list_current + instr_list_legacy + instr_list_macmap,
#               "macmap": instr_list_macmap, "legacy": instr_list_legacy, "current": instr_list_current}
#
# # This dictionary summarizes when instruments are not available and/or when they are not acquiring (i.e., sun below the horizon)
# # start_instr: when the instrument was installed
# # end_instr: to instrument was uninstalled
# # start_seas: for each year, when the instrument starts acquiring (e.g., the sunlit period for sunphotometers)
# # end_seas: when the instrument stops acquiring
# instr_metadata = {
#     'aeronet'             : {'institution': 'NCAR/NASA', 'start_instr': dt.datetime(2007, 3, 1),
#                              'end_instr'  : dt.datetime.today(), 'start_seas': dt.datetime(1900, 3, 1),
#                              'end_seas'   : dt.datetime(1900, 10, 31)},
#     'aero_sondes'         : {'institution': 'DMI', 'start_instr': dt.datetime(1992, 1, 1),
#                              'end_instr'  : dt.datetime(1998, 12, 31), 'start_seas': dt.datetime(1900, 1, 1),
#                              'end_seas'   : dt.datetime(1900, 12, 31)},
#     'aws_vespa'           : {'institution': 'INGV', 'start_instr': dt.datetime(2016, 1, 1),
#                              'end_instr'  : dt.datetime.today(), 'start_seas': dt.datetime(1900, 1, 1),
#                              'end_seas'   : dt.datetime.today()},
#     'ceilometer'          : {'institution': 'ENEA', 'start_instr': dt.datetime(2019, 11, 1),
#                              'end_instr'  : dt.datetime.today(), 'start_seas': dt.datetime(1900, 1, 1),
#                              'end_seas'   : dt.datetime(1900, 12, 31)},
#     'dir_rad_trkr'        : {'institution': 'DMI+ENEA', 'start_instr': dt.datetime(2002, 10, 1),
#                              'end_instr'  : dt.datetime.today(), 'start_seas': dt.datetime(1900, 2, 1),
#                              'end_seas'   : dt.datetime(1900, 10, 31)},
#     'ecapac_mrr'          : {'institution': 'ENEA', 'start_instr': dt.datetime(2022, 9, 1),
#                              'end_instr'  : dt.datetime.today(), 'start_seas': dt.datetime(1900, 1, 1),
#                              'end_seas'   : dt.datetime(1900, 12, 31)},
#     'ecapac_aws_snow'     : {'institution': 'ENEA', 'start_instr': dt.datetime(2022, 9, 1),
#                              'end_instr'  : dt.datetime.today(), 'start_seas': dt.datetime(1900, 1, 1),
#                              'end_seas'   : dt.datetime(1900, 12, 31)},
#     'ecapac_disdro_precip': {'institution': 'ENEA', 'start_instr': dt.datetime(2022, 9, 1),
#                              'end_instr'  : dt.datetime.today(), 'start_seas': dt.datetime(1900, 1, 1),
#                              'end_seas'   : dt.datetime(1900, 12, 31)},
#     'ftir'                : {'institution': 'NCAR/NASA', 'start_instr': dt.datetime(1999, 10, 1),
#                              'end_instr'  : dt.datetime.today(), 'start_seas': dt.datetime(1900, 3, 1),
#                              'end_seas'   : dt.datetime(1900, 10, 31)},
#     'gbms'                : {'institution': 'U.Alaska,Florence,StonyBrook/USSF', 'start_instr': dt.datetime(1992, 1, 1),
#                              'end_instr'  : dt.datetime(2012, 12, 31), 'start_seas': dt.datetime(1900, 1, 1),
#                              'end_seas'   : dt.datetime(1900, 12, 31)},
#     'hatpro'              : {'institution': 'ENEA', 'start_instr': dt.datetime(2017, 1, 1),
#                              'end_instr'  : dt.datetime(2024, 9, 30), 'start_seas': dt.datetime(1900, 1, 1),
#                              'end_seas'   : dt.datetime(1900, 12, 31)},
#     'lidar_temp'          : {'institution': 'U.Sap+ENEA', 'start_instr': dt.datetime(1993, 11, 1),
#                              'end_instr'  : dt.datetime.today(), 'start_seas': dt.datetime(1900, 11, 1),
#                              'end_seas'   : dt.datetime(1900, 3, 31)},
#     'lidar_ae'            : {'institution': 'U.Sap+ENEA', 'start_instr': dt.datetime(1991, 9, 1),
#                              'end_instr'  : dt.datetime(1996, 3, 31), 'start_seas': dt.datetime(1900, 9, 1),
#                              'end_seas'   : dt.datetime(1900, 3, 31)},
#     'macmap_seismometer_1': {'institution': 'INGV', 'start_instr': dt.datetime(2021, 8, 1),
#                              'end_instr'  : dt.datetime.today(), 'start_seas': dt.datetime(1900, 3, 1),
#                              'end_seas'   : dt.datetime(1900, 11, 30)},
#     'macmap_seismometer_2': {'institution': 'INGV', 'start_instr': dt.datetime(2021, 8, 1),
#                              'end_instr'  : dt.datetime.today(), 'start_seas': dt.datetime(1900, 3, 1),
#                              'end_seas'   : dt.datetime(1900, 11, 30)},
#     'macmap_seismometer_3': {'institution': 'INGV', 'start_instr': dt.datetime(2021, 8, 1),
#                              'end_instr'  : dt.datetime.today(), 'start_seas': dt.datetime(1900, 3, 1),
#                              'end_seas'   : dt.datetime(1900, 11, 30)},
#     'macmap_seismometer_4': {'institution': 'INGV', 'start_instr': dt.datetime(2022, 9, 1),
#                              'end_instr'  : dt.datetime.today(), 'start_seas': dt.datetime(1900, 3, 1),
#                              'end_seas'   : dt.datetime(1900, 11, 30)},
#     'macmap_tide_gauge'   : {'institution': 'INGV', 'start_instr': dt.datetime(2021, 8, 1),
#                              'end_instr'  : dt.datetime.today(), 'start_seas': dt.datetime(1900, 3, 1),
#                              'end_seas'   : dt.datetime(1900, 11, 30)},
#     'metar'               : {'institution': 'U.Alaska,Florence,StonyBrook/USSF',
#                              'start_instr': dt.datetime(1951, 10, 1),
#                              'end_instr'  : dt.datetime.today(), 'start_seas': dt.datetime(1900, 1, 1),
#                              'end_seas'   : dt.datetime(1900, 12, 31)},
#     'mms_trios'           : {'institution': 'INGV', 'start_instr': dt.datetime(2021, 9, 1),
#                              'end_instr'  : dt.datetime.today(), 'start_seas': dt.datetime(1900, 3, 1),
#                              'end_seas'   : dt.datetime(1900, 10, 31)},
#     'o3_sondes'           : {'institution': 'DMI', 'start_instr': dt.datetime(1991, 12, 1),
#                              'end_instr'  : dt.datetime(2016, 12, 31), 'start_seas': dt.datetime(1900, 1, 1),
#                              'end_seas'   : dt.datetime(1900, 12, 31)},
#     'pm10'                : {'institution': 'U.Alaska,Florence,StonyBrook/USSF', 'start_instr': dt.datetime(2010, 1, 1),
#                              'end_instr'  : dt.datetime.today(), 'start_seas': dt.datetime(1900, 1, 1),
#                              'end_seas'   : dt.datetime(1900, 12, 31)},
#     'rad_dli'             : {'institution': 'ENEA', 'start_instr': dt.datetime(2009, 1, 1),
#                              'end_instr'  : dt.datetime.today(), 'start_seas': dt.datetime(1900, 1, 1),
#                              'end_seas'   : dt.datetime(1900, 12, 31)},
#     'rad_dsi'             : {'institution': 'DMI+ENEA', 'start_instr': dt.datetime(2003, 2, 1),
#                              'end_instr'  : dt.datetime.today(), 'start_seas': dt.datetime(1900, 1, 1),
#                              'end_seas'   : dt.datetime(1900, 12, 31)},
#     'rad_par_down'        : {'institution': 'ENEA', 'start_instr': dt.datetime(2016, 7, 1),
#                              'end_instr'  : dt.datetime.today(), 'start_seas': dt.datetime(1900, 1, 1),
#                              'end_seas'   : dt.datetime(1900, 12, 31)},
#     'rad_par_up'          : {'institution': 'ENEA', 'start_instr': dt.datetime(2016, 7, 1),
#                              'end_instr'  : dt.datetime.today(), 'start_seas': dt.datetime(1900, 1, 1),
#                              'end_seas'   : dt.datetime(1900, 12, 31)},
#     'rad_tb'              : {'institution': 'ENEA', 'start_instr': dt.datetime(2017, 1, 1),
#                              'end_instr'  : dt.datetime.today(), 'start_seas': dt.datetime(1900, 1, 1),
#                              'end_seas'   : dt.datetime(1900, 12, 31)},
#     'rad_uli'             : {'institution': 'ENEA', 'start_instr': dt.datetime(2016, 7, 1),
#                              'end_instr'  : dt.datetime.today(), 'start_seas': dt.datetime(1900, 1, 1),
#                              'end_seas'   : dt.datetime(1900, 12, 31)},
#     'rad_usi'             : {'institution': 'ENEA', 'start_instr': dt.datetime(2016, 7, 1),
#                              'end_instr'  : dt.datetime.today(), 'start_seas': dt.datetime(1900, 1, 1),
#                              'end_seas'   : dt.datetime(1900, 12, 31)},
#
#     'rs_sondes'           : {'institution': 'DMI+INGV', 'start_instr': dt.datetime(1973, 1, 1),
#                              'end_instr'  : dt.datetime.today(), 'start_seas': dt.datetime(1900, 1, 1),
#                              'end_seas'   : dt.datetime(1900, 12, 31)},
#     'skycam'              : {'institution': 'ENEA', 'start_instr': dt.datetime(2016, 7, 1),
#                              'end_instr'  : dt.datetime.today(), 'start_seas': dt.datetime(1900, 1, 1),
#                              'end_seas'   : dt.datetime(1900, 12, 31)},
#     'gnss'                : {'institution': 'INGV', 'start_instr': dt.datetime(2021, 5, 1),
#                              'end_instr'  : dt.datetime.today(), 'start_seas': dt.datetime(1900, 1, 1),
#                              'end_seas'   : dt.datetime(1900, 12, 31)},
#     'uv-vis_spec'         : {'institution': 'DMI', 'start_instr': dt.datetime(1991, 2, 1),
#                              'end_instr'  : dt.datetime(2016, 11, 30), 'start_seas': dt.datetime(1900, 2, 1),
#                              'end_seas'   : dt.datetime(1900, 11, 30)},
#     'vespa'               : {'institution': 'INGV', 'start_instr': dt.datetime(2016, 7, 1),
#                              'end_instr'  : dt.datetime.today(), 'start_seas': dt.datetime(1900, 1, 1),
#                              'end_seas'   : dt.datetime(1900, 12, 31)},
#     'wv_isotopes'         : {'institution': 'U.Alaska,Florence,StonyBrook/USSF',
#                              'start_instr': dt.datetime(2011, 6, 1), 'end_instr': dt.datetime(2019, 12, 31),
#                              'start_seas' : dt.datetime(1900, 1, 1), 'end_seas': dt.datetime(1900, 12, 31)},
#
# }
#
# institution_colors = {'DMI'       : 'green', 'INGV': 'blue', 'ENEA': 'red', 'NCAR/NASA': 'purple',
#                       'ENEA+INGV' : 'olive', 'U.Sap+ENEA': 'brown', 'DMI+INGV': 'orange',
#                       'DMI+ENEA'  : 'pink', 'U.Alaska,Florence,StonyBrook/USSF': 'black',
#                       'not active': 'grey'}
#
# events_dict = {1 : {'date': dt.datetime(2012, 6, 30), 'label': 'bldg. #1985 --> \n bldg. #1971'},
#                2 : {'date': dt.datetime.today(), 'label': 'today'},
#                3 : {'date': dt.datetime(1951, 6, 6), 'label': 'TAB installation \n starts'},
#                4 : {'date': dt.datetime(1951, 10, 1), 'label': 'TAB installation \n ends'},
#                5 : {'date': dt.datetime(1945, 9, 2), 'label': 'WW II ends'},
#                6 : {'date': dt.datetime(1989, 9, 1), 'label': 'Berlin Wall falls'},
#                7 : {'date': dt.datetime(1991, 11, 12), 'label': 'I was born :)'},
#                8 : {'date': dt.datetime(1910, 6, 30), 'label': 'Thule Outpost'},
#                9 : {'date': dt.datetime(1912, 6, 30), 'label': "First (of 7) Rasmussen's \n Expeditions"},
#                10: {'date': dt.datetime(2023, 4, 6), 'label': 'TAB --> PSB'},
#                11: {'date': dt.datetime(1933, 3, 30), 'label': 'Thule Outpost under \n the Danish Gov. control'},
#                12: {'date': dt.datetime(1914, 7, 28), 'label': 'WW I starts'},
#                13: {'date': dt.datetime(1918, 11, 11), 'label': 'WW I ends'},
#                14: {'date': dt.datetime(1959, 3, 30), 'label': 'First NSF prj \n in Thule funded'},
#                15: {'date': dt.datetime(1903, 3, 30), 'label': 'Danish Literary \n Expedition'},
#                16: {'date': dt.datetime(1968, 1, 21), 'label': 'B-52 crash'},
#                17: {'date': dt.datetime(2007, 3, 1), 'label': 'Fourth IPY --> APECS!'},
#                18: {'date': dt.datetime(1958, 3, 30), 'label': 'Camp Century \n construction'},
#                19: {'date': dt.datetime(1961, 3, 30), 'label': 'BMEWS \n construction'},
#                20: {'date': dt.datetime(1966, 3, 30), 'label': 'Camp Century \n abandoned'},
#                21: {'date': dt.datetime(1939, 9, 1), 'label': 'WW II starts'},
#                22: {'date': dt.datetime(1958, 3, 30), 'label': 'Op. Chrome \n Dome '},
#                23: {'date': dt.datetime(1953, 3, 30), 'label': 'Op. IceCap'},
#                24: {'date': dt.datetime(1991, 6, 15), 'label': 'Mt. Pinatubo \n eruption'},
#                25: {'date': dt.datetime(1982, 3, 29), 'label': 'El Chichón eruption'},
#                27: {'date': dt.datetime(1981, 3, 18), 'label': 'Italy signs \n the Antarctic Treaty'},
#                28: {'date': dt.datetime(2013, 6, 30), 'label': 'PRA'},
#                29: {'date': dt.datetime(1997, 6, 30), 'label': 'CNR "Dirigibile Italia" \n station'},
#                30: {'date': dt.datetime(1928, 5, 24), 'label': 'U. Nobile above \n North Pole'},
#                31: {'date': dt.datetime(1932, 6, 30), 'label': 'Second IPY'},
#                32: {'date': dt.datetime(1957, 6, 30), 'label': 'Third IPY'},
#                33: {'date': dt.datetime(1990, 6, 30), 'label': 'IT lidar \n @bldg. #216 \n @TAB'},
#                34: {'date': dt.datetime(2010, 6, 30), 'label': 'IT lidar --> \n bldg. #1971@S.Mount.'},
#                35: {'date': dt.datetime(1972, 6, 30), 'label': 'DMI lab \n @bldg. #1985 ?'},
#                36: {'date': dt.datetime(1943, 6, 30), 'label': 'Bluie West 6 \n Met Station'},
#                37: {'date': dt.datetime(1954, 12, 1), 'label': 'DMI takes over \n the Bluie West 6 \n Met Station'},
#                38: {'date': dt.datetime(1985, 6, 30), 'label': 'Greenland \n exits CEE'},
#                39: {'date': dt.datetime(1953, 6, 30), 'label': 'Greenland ex-Danish \n colony'},
#                40: {'date': dt.datetime(2023, 4, 6), 'label': 'Greenland National \n Research Strategy \n Plan'},
#                41: {'date': dt.datetime(2012, 6, 30), 'label': 'IT Observatory Status \n @ Arctic Council'},
#                42: {'date': dt.datetime(1954, 6, 30), 'label': 'DEW line \n building'},
#                43: {'date': dt.datetime(2020, 2, 1), 'label': 'COVID hits'},
#                44: {'date': dt.datetime(2019, 5, 14), 'label': 'CLARA2 prj \n PNRA 3y'},
#                45: {'date': dt.datetime(2020, 6, 30), 'label': 'MACMAP prj \n INGV 3y'},
#                46: {'date': dt.datetime(2021, 1, 4), 'label': 'ECAPAC prj \n PRA 2y'},
#                47: {'date': dt.datetime(2021, 6, 30), 'label': 'SEANA prj \n ext 2y'},
#                48: {'date': dt.datetime(2016, 6, 30), 'label': 'OASIS-YOPP prj \n PNRA 2y'},
#                49: {'date': dt.datetime(2015, 6, 30), 'label': 'SVAAP prj \n PNRA 1y'},
#                50: {'date': dt.datetime(2014, 6, 30), 'label': 'ARCA prj \n MIUR 2y'},
#                51: {'date': dt.datetime(1947, 1, 30), 'label': 'DMI Geomagnetic Obs'},
#                52: {'date': dt.datetime(1953, 6, 30), 'label': 'Pituffik inhabitants \n relocated to Qaanaaq'},
#                53: {'date': dt.datetime(1941, 6, 30), 'label': 'Bluie West Program \n starts'},
#                54: {'date': dt.datetime(2024, 7, 1), 'label': 'NASA ARCSIX'},
#                55: {'date': dt.datetime(2024, 6, 1), 'label': 'THAAO funded as \n INGV infrastructure'}, }
#
# campaigns_dict = {1 : {'start': dt.datetime(1991, 1, 1), 'end': dt.datetime(1991, 1, 31)},
#                   2 : {'start': dt.datetime(1991, 12, 1), 'end': dt.datetime(1991, 12, 31)},
#                   3 : {'start': dt.datetime(1992, 1, 1), 'end': dt.datetime(1992, 1, 31)},
#                   4 : {'start': dt.datetime(1992, 11, 1), 'end': dt.datetime(1992, 11, 30)},
#                   5 : {'start': dt.datetime(1993, 1, 1), 'end': dt.datetime(1993, 1, 31)},
#                   6 : {'start': dt.datetime(1993, 7, 1), 'end': dt.datetime(1993, 7, 31)},
#                   7 : {'start': dt.datetime(1994, 1, 1), 'end': dt.datetime(1994, 1, 31)},
#                   8 : {'start': dt.datetime(1994, 7, 1), 'end': dt.datetime(1994, 7, 31)},
#                   9 : {'start': dt.datetime(1995, 1, 1), 'end': dt.datetime(1995, 1, 31)},
#                   10: {'start': dt.datetime(1997, 1, 1), 'end': dt.datetime(1997, 1, 31)},
#                   11: {'start': dt.datetime(1998, 5, 1), 'end': dt.datetime(1998, 5, 31)},
#                   12: {'start': dt.datetime(2002, 1, 1), 'end': dt.datetime(2002, 1, 31)},
#                   13: {'start': dt.datetime(2003, 1, 1), 'end': dt.datetime(2003, 1, 31)},
#                   14: {'start': dt.datetime(2006, 12, 1), 'end': dt.datetime(2006, 12, 31)},
#                   15: {'start': dt.datetime(2009, 1, 1), 'end': dt.datetime(2009, 1, 31)},
#                   16: {'start': dt.datetime(2010, 1, 1), 'end': dt.datetime(2010, 1, 31)},
#                   17: {'start': dt.datetime(2010, 10, 1), 'end': dt.datetime(2010, 10, 31)},
#                   18: {'start': dt.datetime(2012, 1, 1), 'end': dt.datetime(2012, 2, 29)},
#                   19: {'start': dt.datetime(2013, 2, 21), 'end': dt.datetime(2013, 3, 18)},
#                   20: {'start': dt.datetime(2014, 1, 1), 'end': dt.datetime(2014, 2, 28)},
#                   21: {'start': dt.datetime(2016, 6, 11), 'end': dt.datetime(2016, 7, 18)},
#                   22: {'start': dt.datetime(2017, 2, 16), 'end': dt.datetime(2017, 2, 21)},
#                   23: {'start': dt.datetime(2018, 2, 22), 'end': dt.datetime(2018, 3, 2)},
#                   24: {'start': dt.datetime(2019, 2, 27), 'end': dt.datetime(2019, 3, 8)},
#                   25: {'start': dt.datetime(2019, 11, 6), 'end': dt.datetime(2019, 11, 15)},
#                   26: {'start': dt.datetime(2021, 4, 21), 'end': dt.datetime(2021, 5, 21)},
#                   27: {'start': dt.datetime(2021, 8, 10), 'end': dt.datetime(2021, 8, 27)},
#                   28: {'start': dt.datetime(2022, 3, 22), 'end': dt.datetime(2022, 4, 9)},
#                   29: {'start': dt.datetime(2022, 9, 7), 'end': dt.datetime(2022, 9, 23)},
#                   30: {'start': dt.datetime(2023, 4, 18), 'end': dt.datetime(2023, 5, 6)},
#                   31: {'start': dt.datetime(2023, 9, 26), 'end': dt.datetime(2023, 10, 5)},
#                   32: {'start': dt.datetime(2024, 3, 19), 'end': dt.datetime(2024, 4, 6)},
#                   33: {'start': dt.datetime(2024, 5, 25), 'end': dt.datetime(2024, 6, 17)},
#                   34: {'start': dt.datetime(2024, 7, 22), 'end': dt.datetime(2024, 8, 7)},
#                   35: {'start': dt.datetime(2024, 9, 26), 'end': dt.datetime(2024, 10, 5)}}
