import gval
from gval.comparison.pairing_functions import _make_pairing_dict
import rioxarray as rxr
import xarray as xr
import numpy as np
import geopandas as gpd
from geocube.api.core import make_geocube


def run():
    c = rxr.open_rasterio('/home/sven/repos/fim/inputs/test_cases/ras2fim_test_cases/07100006_ras2fim/testing_versions/test4/5yr/inundation_extent_07100006.tif', mask_and_scale=True)
    b = rxr.open_rasterio('/home/sven/repos/fim/inputs/test_cases/ras2fim_test_cases/validation_data_ras2fim/07100006/5yr/ras2fim_huc_07100006_extent_5yr.tif', mask_and_scale=True)

    c.data = xr.where(c >= 0, 1, c)
    c.data = xr.where(c < 0, 0, c)

    mask_dict = {'levees': {'path': '~/repos/fim/inputs/inputs/nld_vectors/Levee_protected_areas.gpkg',
                            'buffer': None, 'operation': 'exclude'},
                 'waterbodies': {'path': '~/repos/fim/inputs/inputs/nwm_hydrofabric/nwm_lakes.gpkg',
                                 'buffer': None, 'operation': 'exclude'}}

    df = gpd.read_file(mask_dict['levees']['path'], bbox=c.rio.bounds())
    df['mask'] = 4
    df2 = gpd.read_file(mask_dict['waterbodies']['path'], bbox=c.rio.bounds())
    df2['mask'] = 4

    e = make_geocube(df, ['mask'], like=c)
    f = make_geocube(df2, ['mask'], like=c)
    g = xr.merge([e, f]).to_array()

    c.data = xr.where(g.data == 4, 4, c)

    pairing_dictionary = {(0.0, 0.0): 0,
     (0.0, 1.0): 1,
     (0.0, np.nan): np.nan,
     (1.0, 0.0): 2,
     (1.0, 1.0): 3,
     (1.0, np.nan): np.nan,
     (4.0, 0.0): 4,
     (4.0, 1.0): 4,
     (4.0, np.nan): np.nan,
     (np.nan, 0.0): np.nan,
     (np.nan, 1.0): np.nan,
     (np.nan, np.nan): np.nan}


    aaa, bbb, ccc = c.gval.categorical_compare(b, positive_categories=[1],
                                          negative_categories=[0],
                                          comparison_function='pairing_dict',
                                          allow_candidate_values=[0, 1, 4],
                                          allow_benchmark_values=[0, 1, 4],
                                          pairing_dict=pairing_dictionary)

if __name__ == '__main__':

    run()