# DATA AVAILABILITY AT THAAO

> [!IMPORTANT]  
> This is an ongoing project.

## TODO (Thanks!)

### Most urgent

- [ ] run data availability for each instrument
- [ ] check missing data with other members of the THAAO community

### Efficiency improvements

- [ ] improve efficiency and speed (in cosa e dove cosa dove cosa? CSMT)
- [x] automatize instrument availability list creation if older than x months (for single instrument)
- [ ] develop gif creation

### Legacy data

- [ ] collect legacy weather data and homogenize them (from AdS)
- [ ] collect legacy radiation data and homogenize them (from AdS)
- [ ] collect other legacy data and homogenize them (from ???)

Suite of scripts for instruments at THAAO to generate data availability lists and plots.

Every script checks the existence of data (files) and create a .csv for each instrument.

Each script has to be launched singularly. Then `data_availability.py` can be launched inserting input to produce
specific plots.

## `data_availability.py`

Contains different plot options which you can manage through the input request.

There are three types of plot:

- gif panels (for animations)
- rolling panels (including yearly)

Additionally, you can specify if you want the historical events, the Italian field campaigns and the progress bar to be
plotted.
The instruments considered are selected in batches: thaao, legacy, hyso or all.

## `settings.py`

Contains list of instruments, dates of field campaigns and other relevant metadata.

## `tools.py`

Contains tools for saving files in specific format and some workaround for variable names reformatting due to folder
names.

## `plots.py`

- `plot_rolling_panels()` --> Panels for gif:
- `plot_cumulative_panels()` --> Full panels: