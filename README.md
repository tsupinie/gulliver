# Gulliver
Create maps of US counties to show travels.

## Requirements:
* matplotlib
* basemap
* pyshp

You'll also need a counties shapefile. I recommend [this one](http://bit.ly/2e7LSzH).
You can either leave it zipped or unzip it.

## Usage
First, create a file that contains a list of counties you've visited. Perhaps call it `mytravel.py`.
It should contain the following:

```python
name = "Tim"

visited = [
    ('Cleveland', 'OK'), # Counties are specified by a tuple containing the 
                         # name and the postal abbreviation of the state
    # ...
]

slept = [
    # The variable `slept` must exist, even if it's just an empty list
    # Any counties listed in here that are not listed in `visited` will be
    #   counted as visited, as well. Similarly, any counties in the `lived`
    #   variable below will also be countied as both `visited` and `slept`.
    # ...
]

lived = [
    # The variable `lived` must exist, even if it's just an empty list
    # ...
]
```

See `default.py` for an example. Next, invoke the command

`$ python gulliver.py --shp /path/to/shapefile --travel mytravel`

to create the map. It will be placed in `<travel>_travels.png`.

If you've unzipped the shapefile, `/path/to/shapefile` should be the name of the shapefile without 
the `.dbf` or `.shp` extension.
