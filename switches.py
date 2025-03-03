#!/usr/local/bin/python3
# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------------
#
"""
Brief description
"""

# =============================================================
# CREATED: 
# AFFILIATION: UNIVE, INGV
# AUTHORS: Filippo Cali' Quaglia
# =============================================================
#
# -------------------------------------------------------------------------------
__author__ = "Filippo Cali' Quaglia"
__credits__ = ["??????"]
__license__ = "GPL"
__version__ = "1.1"
__email__ = "filippo.caliquaglia@gmail.com"
__status__ = "Research"
__lastupdate__ = ""

import datetime as dt

# switches
data_avail_update = False

switch_instr_list = 'thaao'

switch_campaigns = False  # Draw field campaigns?
switch_history = False  # Draw historical events?

switch_cumulative_panels = False
switch_rolling_panels = False
switch_summary_panel = True

# inputs

DEFAULT_START_YEAR = 1990
DEFAULT_END_YEAR = 2024
start_date = dt.datetime(DEFAULT_START_YEAR, 1, 1)
end_date = dt.datetime(DEFAULT_END_YEAR, 12, 31)

# cumulative
time_freq_c = '6'

# rolling
time_freq_r = '12'
time_window_r = '12'

DEFAULT_FILE_AGE_DAYS = 14
