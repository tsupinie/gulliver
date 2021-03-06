
from itertools import izip
import zipfile
import shutil
import cStringIO
import os

import shapefile

from fips import get_abbrev

class CountyDB(object):
    def __init__(self, sf_path="./tl_2016_us_county"):
        if os.path.exists("%s.dbf" % sf_path) and os.path.exists("%s.shp" % sf_path) and os.path.exists("%s.shx" % sf_path):
            mem_dbf = open("%s.dbf" % sf_path, 'rb')
            mem_shp = open("%s.shp" % sf_path, 'rb')
            mem_shx = open("%s.shx" % sf_path, 'rb')

        elif os.path.exists(sf_path) and sf_path.endswith('.zip') or os.path.exists("%s.zip" % sf_path):
            if not sf_path.endswith('.zip'):
                sf_path = "%s.zip" % sf_path

            sf_name = os.path.basename(sf_path)[:-4]

            # Unzip the shapefile in memory before passing the files off to the shapefile reader.
            def _decompress(fzip, name):
                mem_f = cStringIO.StringIO()
                f = fzip.open(name)
                shutil.copyfileobj(f, mem_f)
                mem_f.seek(0)
                return mem_f

            fzip = zipfile.ZipFile(sf_path, 'r')
            mem_dbf = _decompress(fzip, "%s.dbf" % sf_name)
            mem_shp = _decompress(fzip, "%s.shp" % sf_name)
            mem_shx = _decompress(fzip, "%s.shx" % sf_name)
        else:
            raise IOError("Unable to find shapefile '%s'" % sf_path)

        self._sf = shapefile.Reader(dbf=mem_dbf, shp=mem_shp, shx=mem_shx)
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
            st_abbrv = get_abbrev(rec[self._st_fips_idx])

            if cty_name.startswith('Do') and cty_name.endswith('a Ana'):
                cty_name = 'Dona Ana'

            yield {'state': st_abbrv,
                   'county': cty_name,
                   'points': [ shp.points[st:ed] for st, ed in part_bnds ]
                  }

if __name__ == "__main__":
    db = CountyDB()
#   print db.search([('Cleveland', 'OK')])
    for cty in db:
        print cty['county'], cty['state']
