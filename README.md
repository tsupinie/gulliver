# Gulliver
Create maps of US counties to show travels.

## Requirements:
* matplotlib
* basemap
* pyshp

You'll also need a counties shapefile. I recommend [this one](ftp://ftp2.census.gov/geo/tiger/TIGER2016/COUNTY/tl_2016_us_county.zip).
You can either leave it zipped or unzip it.

## Usage
First, create a file that contains a list of counties you've visited (see `default.py` for an example). Perhaps call it `mytravel.py`.
Then invoke the command

`$ python gulliver.py --shp /path/to/shapefile --travel mytravel`

to create the map.
