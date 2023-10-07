from gval.utils.loading_datasets import handle_xarray_memory, adjust_memory_strategy
import rioxarray as rxr
from gval.statistics.test4 import a

if __name__ == '__main__':

    adjust_memory_strategy('aggressive')
    multi_cand = rxr.open_rasterio('s3://gval-test/candidate_categorical_multiband_aligned_0.tif', mask_and_scale=True,
                                   band_as_variable=True)

    multi_cand = handle_xarray_memory(multi_cand)
    a(multi_cand)
