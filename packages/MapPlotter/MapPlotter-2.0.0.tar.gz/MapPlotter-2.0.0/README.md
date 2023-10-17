[![Build status](https://github.com/ArnauMiro/MapPlotter/actions/workflows/build_python.yml/badge.svg)](https://github.com/ArnauMiro/MapPlotter/actions)
[![License](https://img.shields.io/badge/license-GPL3-orange)](https://opensource.org/license/gpl-3-0/)

# Map Plotter

Map Plotter is a toolkit that provides a framework for 2D map plots of data and NetCDF files. It consists of a python class (_MapPlotter_) that interfaces with [cartopy](https://scitools.org.uk/cartopy/docs/latest/) to generate beautiful maps.

This tool depends on:
* the [PROJ library](https://proj.org/)
* [Cartopy](https://scitools.org.uk/cartopy/docs/latest/)
* the [requests](https://pypi.org/project/requests/) module

Two examples (_example_MapPlotter_1.py_ and _example_MapPlotter_2.py_) are provided as a reference.

For any issues please contact: [arnau.miro(at)upc(dot)edu](mailto:arnau.miro@upc.edu).

## Installation

A _Makefile_ is provided within the tool to automate the installation for easiness of use for the user. To install the tool simply create a virtual environment as stated below or use the system Python. Once this is done simply type:
```bash
make
```
This will install all the requirements and install the package to your active python. To uninstall simply use
```bash
make uninstall
```

The previous operations can be done one step at a time using
```bash
make requirements
```
to install all the requirements and
```bash
make install
```
to install the tool.

### Virtual environment

The package can be installed in a Python virtual environement to avoid messing with the system Python installation.
Next, we will use [Conda](https://docs.conda.io/projects/conda/en/latest/index.html) for this purpose.
Assuming that Conda is already installed, we can create a virtual environment with a specific python version and name (`my_env`) using
```bash
conda create -n my_env python=3.8
```
The environment is placed in `~/.conda/envs/my_env`.
Next we activate it be able to install packages using `conda` itself or another Python package manager in the environment directory:
```bash
conda activate my_env
```
Then just follow the instructions as stated above.

### Get cartopy

Cartopy can be installed using the pip tool by doing:
```bash
pip install cartopy
```
Sometimes a segmentation fault can appear when running some projections. In that case the following fixes the issue:
```bash
pip uninstall shapely
pip install --no-binary :all: shapely
```

## Usage

### The MAPPLOTTER class

Plot NETCDF data using CARTOPY. Example python snippets:

```python
import MapPlotter as mp

# Define class instance
plotter = mp.MapPlotter(projection='PlateCarree')
params  = plotter.defaultParams() # Create basic parameters dictionary

# To plot already loaded fields
plotter.plot(lon,lat,data,params=params)

# To plot data from NetCDF data
plotter.plot_from_file(filename,varname,lonname,latname,iTime=0,iDepth=0,params=params)

# To see the data
plotter.save('outfile.png',dpi=300)
plotter.show() # wrapper of plt.show()
```

### Command line tool

A command line tool is also provided so that maps can easily be generated from NetCDF files through the command prompt. It can be accessed as:
```bash
map_plotter [-h] -f FILE -v VAR [-m MASK] [--lon LON] [--lat LAT] 
			[-t TIME] [-d DEPTH] [-c CONF] -o OUT [--dpi DPI]
```
Arguments:
* -h, --help               show this help message and exit
* -f FILE, --file FILE     NetCDF file path
* -v VAR, --var VAR        Variable to plot
* -m MASK, --mask MASK     Mask file
* --lon LON                Longitude variable name (default: glamt)
* --lat LAT                Latitude variable name (default: gphit)
* -t TIME, --time TIME     Time index for NetCDF (default: 0)
* -d DEPTH, --depth DEPTH  Depth index for NetCDF (default: 0)
* -c CONF, --conf CONF     Configuration file path
* -o OUT, --outfile OUT    Output file name
* --dpi DPI                Output file DPI (default: 300)