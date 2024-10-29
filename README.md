# DATA AVAILABILITY AT THAAO

Suite of scripts for instruments at THAAO to generate data availability lists and plots.

Every single script checks the existence of data (files) and create a .txt for each instrument.

Each script has to be launched singularly. Then data_availability.py produce specific plots.

## thaao_settings.py

Contains list of instruments, dates of field campaigns and other relevant metadata. 

## data_availability.py

Contains different plot options which you can manage changing state to the switches in thaao_settings.py (managed as
input)
