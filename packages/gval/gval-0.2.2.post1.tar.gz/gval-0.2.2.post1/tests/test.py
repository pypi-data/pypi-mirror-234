import memray
import gval
import rioxarray as rxr
import subprocess
import os


def run():
    candidate = rxr.open_rasterio('candidate_map_two_class_categorical.tif', mask_and_scale=True)
    benchmark = rxr.open_rasterio('benchmark_map_two_class_categorical.tif', mask_and_scale=True)

    candidate.gval.categorical_compare(benchmark,
                                                 positive_categories=[2],
                                                 negative_categories=[0, 1])


if __name__ == '__main__':

    file_name = "output.bin"

    if os.path.exists(file_name):
        os.remove(file_name)

    with memray.Tracker(file_name):
        run()

    subprocess.call(['memray', 'summary', file_name])

