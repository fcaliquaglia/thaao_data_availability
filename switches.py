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
__version__ = "0.1"
__email__ = "filippo.caliquaglia@gmail.com"
__status__ = "Research"
__lastupdate__ = ""

# switches
switch_instr_list = 'current'

switch_campaigns = 'True'  # Draw field campaigns?
switch_history = 'False'  # Draw historical events?
switch_prog_bar = 'False'  # Draw progress bar?

switch_cumulative_panels = 'False'  # Plot cumulative panels?
switch_rolling_panels = 'False'  # Plot panels for gif?

# inputs
# cumulative
start_c = '2020'
end_c = '2024'
time_freq_c = '6'

# rolling
start_r = '2022'
end_r = '2024'
time_freq_r = '12'
time_window_r = '12'
