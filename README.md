# DATA AVAILABILITY AT THAAO

> [!IMPORTANT]  
> This is an ongoing project.

## TODO (Thanks!)

### SKYCAM

#### to GDrive

- [x] 2016
- [x] 2017
- [x] 2018
- [x] 2019
- [x] 2020
- [x] 2021
- [x] 2022
- [x] 2023

#### to THAAO website

- [x] 2016
- [ ] 2017
- [ ] 2018
- [ ] 2019
- [ ] 2020
- [ ] 2021
- [x] 2022
- [x] 2023

### Most urgent

- [ ] run data availability for each instrument
- [ ] check missing data with other members of the THAAO community

### Efficiency improvements

- [ ] improve efficiency and speed (in cosa e dove cosa dove cosa?CSMT)
- [ ] automatize instrument availability list creation if older than x months
- [ ] develop gif creation

### Legacy data

- [ ] collect legacy weather data and homogenize them (from AdS)
- [ ] collect legacy radiation data and homogenize them (from AdS)
- [ ] collect other legacy data and homogenize them (from ???)

Suite of scripts for instruments at THAAO to generate data availability lists and plots.

Every script checks the existence of data (files) and create a .txt for each instrument.

Each script has to be launched singularly. Then `data_availability.py` can be launched inserting input to produce
specific plots.

## `data_availability.py`

Contains different plot options which you can manage through the input request.

There are three types of plot:

- yearly panels
- gif panels (for animations)
- rolling panels

Additionally, you can specify if you want the historical events, the Italian field campaigns and the progress bar to be
plotted.
The instruments considered are hard coded, and you can manually modify the list in `settings.py` --> settings.instr_list

## `settings.py`

Contains list of instruments, dates of field campaigns and other relevant metadata.

## `tools.py`

Contains tools for saving files in specific format and some workaround for variable names reformatting due to folder
names.

## `plots.py`

- `plot_rolling_panels()` --> Panels for gif:
- `plot_yearly_panels()` --> Yearly panels:
    - It requires the start and end years. It plots avery years availability starting from January 1st to December 31st.
- `plot_rolling_panels()` --> Full panels: