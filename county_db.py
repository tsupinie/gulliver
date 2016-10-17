
from itertools import izip

import shapefile

from fips import get_abbrev

class CountyDB(object):
    def __init__(self, sf_path="/Users/tsupinie/data/tl_2009_us_county"):
        self._sf = shapefile.Reader(sf_path)
        field_names = zip(*self._sf.fields)[0]
        self._ct_name_idx = field_names.index('NAME') - 1
        self._st_fips_idx = field_names.index('STATEFP') - 1

    def search(self, ct_list):
        geoms = []
        for n_rec, rec in enumerate(self._sf.records()):
            rec_name = rec[self._ct_name_idx]
            rec_st = get_abbrev(rec[self._st_fips_idx])
            if (rec_name, rec_st) in ct_list:
                geoms.append(self._sf.shape(n_rec))

        return geoms

    def __iter__(self):
        for rec, shp in izip(self._sf.iterRecords(), self._sf.iterShapes()):
            part_idxs = shp.parts
            part_idxs.append(len(shp.points))
            part_bnds = [ (part_idxs[idx], part_idxs[idx + 1]) for idx in xrange(len(part_idxs) - 1) ]

            cty_name = rec[self._ct_name_idx]

            yield {'state': get_abbrev(rec[self._st_fips_idx]),
                   'county': cty_name,
                   'points': [ shp.points[st:ed] for st, ed in part_bnds ]
                  }

if __name__ == "__main__":
    db = CountyDB()
#   print db.search([('Cleveland', 'OK')])
    for cty in db:
        print cty['county'], cty['state']
