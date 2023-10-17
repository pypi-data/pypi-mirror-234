from shapely.geometry import Polygon
from shapely.prepared import prep
import numpy as np
import geopandas as gpd


def grid_bounds(geom, delta=0.24):
    """
        Return geometrical grids with equal size
    :param geom:
    :param delta: The edge length of each grid
        delta = 0.01 results in a 1km x 1km grid (approximately)
        delta = 0.03 results in a 3km x 3km grid (approximately)
        delta = 0.05 results in a 5km x 5km grid (approximately)
        delta = 0.08 results in a 10km x 10km grid (approximately)
        delta = 0.24 results in a 30km x 30km grid (approximately)

        Use https://www.nhc.noaa.gov/gccalc.shtml to approximate the size of grid
    :return:
    """

    minx, miny, maxx, maxy = geom.bounds
    nx = max(int((maxx - minx) / delta), 2)
    ny = max(int((maxy - miny) / delta), 2)
    gx, gy = np.linspace(minx, maxx, nx), np.linspace(miny, maxy, ny)
    grid = []

    # from left to right and from top to bottom
    for j in range(len(gy) - 1).__reversed__():
        for i in range(len(gx) - 1):
            poly_ij = Polygon([[gx[i], gy[j]], [gx[i], gy[j + 1]], [gx[i + 1], gy[j + 1]], [gx[i + 1], gy[j]]])
            grid.append(poly_ij)
    return grid


def partition(geom, delta):
    """
        Partition a geometry map of a county to multiple grids
    :param geom:
    :param delta:
    :return:
    """

    prepared_geom = prep(geom)
    grid = list(filter(prepared_geom.intersects, grid_bounds(geom, delta)))
    return grid


def get_county_name(state, county):
    csv_path = "https://github.com/fudonglin/PyPI_resources/blob/main/cropnet/US-counties.geojson?raw=true"
    geoData = gpd.read_file(csv_path)

    # Make sure the "id" column is an integer
    geoData.id = geoData.id.astype(str).astype(int)

    # Remove Alaska, Hawaii and Puerto Rico.
    stateToRemove = ['02', '15', '72']
    geoData = geoData[~geoData.STATE.isin(stateToRemove)]

    county = geoData[(geoData.STATE == state) & (geoData.COUNTY == county)]

    print(county)
