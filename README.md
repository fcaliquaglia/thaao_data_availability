# DATA AVAILABILITY AT THAAO

Suite of scripts for instruments at THAAO to generate data availability lists and plots.

Every script checks the existence of data (files) and create a .txt for each instrument.

Each script has to be launched singularly. Then data_availability.py can be launched inserting input to produce specific plots.

## data_availability.py

Contains different plot options which you can manage through the input request.

There are three types of plot:
- plot_cumulative_panels() --> Panels for gif: 
- plot_yearly_panels() --> Yearly panels: 
  - It requires the start and end years. It plots avery years availability starting from January 1st to December 31st.
- plot_full_panels() --> Full panels: 
Additionally, you can specify if you want the historical events and the Italian field campaigns to be plotted.
The instruments considered are hard coded, and you can manually modify the list in thaao_settings.py --> instr_list

## thaao_settings.py

Contains list of instruments, dates of field campaigns and other relevant metadata.

## tools.py
Contains tools for saving files in specific format and some workaround for variable names reformatting due to folder names.