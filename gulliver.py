import struct
from datetime import datetime
import argparse

import matplotlib
matplotlib.use('agg')
import pylab
from matplotlib.patches import Polygon
from matplotlib.transforms import Affine2D
from mpl_toolkits.axes_grid1.inset_locator import inset_axes

from mpl_toolkits.basemap import Basemap

from gulliver.county_db import CountyDB
from gulliver.travel import TravelManager

def main():
    ap = argparse.ArgumentParser()

    ap.add_argument('--shp', dest='shp', help="Path to county shapefile", required=True)
    ap.add_argument('--travel', dest='name', help="Name of the file (without the .py) that describes your travel.", default='default')

    args = ap.parse_args()

    # Lambert Conformal map of USA lower 48 states
    map_48 = Basemap(projection='lcc', resolution='i', 
        llcrnrlon=-119, llcrnrlat=22, urcrnrlon=-64, urcrnrlat=49,
        lat_1=33, lat_2=45, lon_0=-95, area_thresh=10000)

    map_ak = Basemap(projection='lcc', resolution='i', 
        llcrnrlon=-165, llcrnrlat=52, urcrnrlon=-115, urcrnrlat=71,
        lat_1=55, lat_2=65, lon_0=-145, area_thresh=10000)

    map_hi = Basemap(projection='lcc', resolution='i', 
        llcrnrlon=-160.5, llcrnrlat=18.7, urcrnrlon=-154.5, urcrnrlat=22.5,
        lat_1=19, lat_2=22, lon_0=-157, area_thresh=100)

    db = CountyDB(sf_path=args.shp)

    travel = __import__(args.name, globals(), locals(), ['name', 'visited', 'slept', 'lived'], -1)

    travel.slept = list(set(travel.slept) | set(travel.lived))
    travel.visited = list(set(travel.visited) | set(travel.slept))

    trvl_visited = TravelManager(travel.visited)
    trvl_slept = TravelManager(travel.slept)
    trvl_lived = TravelManager(travel.lived)

    trvl_visited.print_stats()

    pylab.figure(figsize=(10, 8), dpi=150)
    ax_48 = pylab.axes((0, 0, 1, 1))
    ax_ak = inset_axes(ax_48, width=1.75, height=1.75, loc=3, bbox_transform=Affine2D().translate(0, -14))
    ax_hi = inset_axes(ax_48, width=1.5, height=1.5, loc=3, bbox_transform=Affine2D().translate(270, -35))

    labels = {}
    legend_polys = []
    legend_labels = []

    for cty in db:
        color = 'none'
        label = "Not visited"
        if trvl_lived.contains(cty['county'], cty['state']):
            label = "Lived-in county"
            color = '#990066'
        elif trvl_slept.contains(cty['county'], cty['state']):
            label = "Slept-in county"
            color = '#000088'
        elif trvl_visited.contains(cty['county'], cty['state']):
            label = "Visited county"
            color = '#008800'
        elif trvl_lived.contains(cty['state']):
            label = "Lived-in state"
            color = '#ff99ff'
        elif trvl_slept.contains(cty['state']):
            label = "Slept-in state"
            color = '#8888ff'
        elif trvl_visited.contains(cty['state']):
            label = "Visited state"
            color = '#88ff88'

        for pt_list in cty['points']:
            if cty['state'] == 'AK':
                poly = Polygon(zip(*map_ak(*zip(*pt_list))), fc=color, lw=0.5, label=label)
                ax_ak.add_patch(poly)
            elif cty['state'] == 'HI':
                poly = Polygon(zip(*map_hi(*zip(*pt_list))), fc=color, lw=0.5, label=label)
                ax_hi.add_patch(poly)
            else:
                poly = Polygon(zip(*map_48(*zip(*pt_list))), fc=color, lw=0.5, label=label)
                ax_48.add_patch(poly)

        if label != "Not visited" and (label not in labels or not labels[label]):
            legend_polys.append(poly)
            legend_labels.append(label)
            labels[label] = True

    legend_polys, legend_labels = zip(*sorted(zip(legend_polys, legend_labels), key=lambda x: x[1]))

    pylab.sca(ax_48)
    map_48.drawcoastlines(linewidth=1.0)
    map_48.drawcountries(linewidth=1.0)
    map_48.drawstates(linewidth=1.0)

    pylab.sca(ax_ak)
    map_ak.drawcoastlines(linewidth=1.0)
    map_ak.drawcountries(linewidth=1.0)
    map_ak.drawstates(linewidth=1.0)

    pylab.sca(ax_hi)
    map_hi.drawcoastlines(linewidth=1.0)
    map_hi.drawcountries(linewidth=1.0)
    map_hi.drawstates(linewidth=1.0)

    pylab.figlegend(legend_polys, legend_labels, 'lower center', ncol=3)

    pylab.sca(ax_48)

    header = "%s's Travels" % travel.name
    update = "Last Updated %s" % datetime.now().strftime("%d %B %Y")
    stats = "Visited: %d (%d states) / Slept in: %d (%d states) / Lived in: %d (%d states)" % (trvl_visited.count(), trvl_visited.count(states=True), 
        trvl_slept.count(), trvl_slept.count(states=True), trvl_lived.count(), trvl_lived.count(states=True))

    pylab.title("%s\n%s\n%s" % (header, update, stats))
    pylab.savefig("%s_travels.png" % args.name, dpi=pylab.gcf().dpi)

    return

if __name__ == "__main__":
    main()
