
import numpy as np

from datetime import datetime
import argparse
from importlib import import_module

import matplotlib as mpl
mpl.use('agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from matplotlib.transforms import Affine2D
from mpl_toolkits.axes_grid1.inset_locator import inset_axes

import cartopy
import cartopy.crs as ccrs
import cartopy.feature as cfeature

from gulliver.travel import TravelManager
from gulliver.ne_records import NaturalEarthFeatureRecords


def create_county_travel_feature(feat_source, trvl):
    geoms = []

    for rec in feat_source.records():
        if trvl.contains(rec.attributes['NAME_EN'], rec.attributes['REGION']):
            geoms.append(rec.geometry)

    return cfeature.ShapelyFeature(geoms, ccrs.PlateCarree())


def create_state_travel_feature(feat_source, trvl):
    geoms = []

    for rec in feat_source.records():
        if rec.attributes['iso_a2'] == 'US':
            if trvl.contains_state(rec.attributes['postal']):
                geoms.append(rec.geometry)

    return cfeature.ShapelyFeature(geoms, ccrs.PlateCarree())


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--travel', dest='name', help="Name of the file (without the .py) that describes your travel.", default='default')

    args = ap.parse_args()

    crs_conus = ccrs.LambertConformal(central_longitude=-97.5, central_latitude=38.5, standard_parallels=(33, 45))
    crs_ak = ccrs.LambertConformal(central_longitude=-150, central_latitude=60, standard_parallels=(55, 65))
    crs_hi = ccrs.LambertConformal(central_longitude=-157, central_latitude=20, standard_parallels=(19, 22))

    travel = import_module(args.name)

    travel.slept = list(set(travel.slept) | set(travel.lived))
    travel.visited = list(set(travel.visited) | set(travel.slept))

    trvl_visited = TravelManager(travel.visited)
    trvl_slept = TravelManager(travel.slept)
    trvl_lived = TravelManager(travel.lived)

    trvl_visited.print_stats()

    fig = plt.figure(figsize=(10, 8), dpi=300)
    ax_48 = plt.axes((0, 0, 1, 1), projection=crs_conus)
    ax_48.set_extent((-119.2, -74, 23, 50))

    ax_ak = inset_axes(ax_48, width=1.85, height=1.85, loc=3, bbox_transform=Affine2D().translate(0, -46), 
                       axes_class=cartopy.mpl.geoaxes.GeoAxes, axes_kwargs=dict(projection=crs_ak))
    ax_ak.set_extent((-165, -129, 53.4, 71))

    ax_hi = inset_axes(ax_48, width=1.4, height=1.4, loc=3, bbox_transform=Affine2D().translate(574, -70), 
                       axes_class=cartopy.mpl.geoaxes.GeoAxes, axes_kwargs=dict(projection=crs_hi))
    ax_hi.set_extent((-160.5, -154.5, 18.7, 22.5))

    legend_polys = []
    legend_labels = []

    counties = NaturalEarthFeatureRecords('cultural', 'admin_2_counties_lakes', '10m')
    states = NaturalEarthFeatureRecords('cultural', 'admin_1_states_provinces_lakes', '10m')
    countries = cfeature.NaturalEarthFeature('cultural', 'admin_0_countries_lakes', '10m')
        
    visited_county_feature = create_county_travel_feature(counties, trvl_visited)
    slept_county_feature = create_county_travel_feature(counties, trvl_slept)
    lived_county_feature = create_county_travel_feature(counties, trvl_lived)
    visited_state_feature = create_state_travel_feature(states, trvl_visited)
    slept_state_feature = create_state_travel_feature(states, trvl_slept)
    lived_state_feature = create_state_travel_feature(states, trvl_lived)

    for ax in [ax_48, ax_ak, ax_hi]:
        for feat, color, label in [(visited_state_feature, '#88ff88', 'Visited state'),
                                   (slept_state_feature, '#8888ff', 'Slept-in state'),
                                   (lived_state_feature, '#ff99ff', 'Lived-in state'),
                                   (visited_county_feature, '#008800', 'Visited county'),
                                   (slept_county_feature, '#000088', 'Slept-in county'),
                                   (lived_county_feature, '#990066', 'Lived-in county')]:
            ax.add_feature(feat, edgecolor='none', facecolor=color)

            if ax == ax_48:
                legend_labels.append(label)
                legend_polys.append(Polygon(np.array([]).reshape((0, 2)), facecolor=color, edgecolor='k'))

        for feat, linewidth in [(counties, 0.5),
                                (states, 1.0),
                                (countries, 1.5)]:
            ax.add_feature(feat, edgecolor='k', facecolor='none', linewidth=linewidth)

    legend_polys, legend_labels = zip(*sorted(zip(legend_polys, legend_labels), key=lambda x: x[1]))

    plt.figlegend(legend_polys, legend_labels, 'lower center', ncol=3)

    header = "%s's Travels" % travel.name
    update = "Last Updated %s" % datetime.now().strftime("%d %B %Y")
    stats = "Visited: %d (%d states) / Slept in: %d (%d states) / Lived in: %d (%d states)" % (trvl_visited.count(), trvl_visited.count(states=True), 
        trvl_slept.count(), trvl_slept.count(states=True), trvl_lived.count(), trvl_lived.count(states=True))

    ax_48.set_title("%s\n%s\n%s" % (header, update, stats))

    plt.savefig("%s_travels.png" % args.name, dpi=fig.dpi)

    return

if __name__ == "__main__":
    main()
