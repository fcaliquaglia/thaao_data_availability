# DATA AVAILABILITY AT THAAO

Suite of scripts for instruments at THAAO to generate data availability lists and plots.

Every script checks the existence of data (files) and create a .txt for each instrument.

Each script has to be launched singularly. Then data_availability.py can be launched inserting input to produce specific plots.

There are three types of plot:
- Panels for gif: 
- Single-year panels: it requires the start and end years. It plots avery years availability starting from January 1st to December 31st.
- Full panels: 
Additionally, you can specify if you want the historical events and the Italian field campaigns to be plotted.
## thaao_settings.py

Contains list of instruments, dates of field campaigns and other relevant metadata. 

## data_availability.py

Contains different plot options which you can manage changing state to the switches in thaao_settings.py (managed as
input)

## tools.py
