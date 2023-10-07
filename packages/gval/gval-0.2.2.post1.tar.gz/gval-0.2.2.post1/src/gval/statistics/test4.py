from gval.utils.loading_datasets import handle_xarray_memory


def a(c):

    c = handle_xarray_memory(c)
    return c


if __name__ == '__main__':
    pass