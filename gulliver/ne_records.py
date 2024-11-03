
import cartopy.feature as cfeature
from cartopy.io import shapereader

_NATURAL_EARTH_CACHE = {}

class NaturalEarthFeatureRecords(cfeature.NaturalEarthFeature):
    def _get_reader(self):
        key = (self.name, self.category, self.scale)
        if key not in _NATURAL_EARTH_CACHE:
            path = shapereader.natural_earth(resolution=self.scale,
                                             category=self.category,
                                             name=self.name)
            reader = shapereader.Reader(path)
            _NATURAL_EARTH_CACHE[key] = reader
        else:
            reader = _NATURAL_EARTH_CACHE[key]

        return reader

    def geometries(self):
        """
        Returns an iterator of (shapely) geometries for this feature.

        """
        return self._get_reader().geometries()
    
    def records(self):
        """
        Returns an iterator of records for this feature.

        """
        return self._get_reader().records()