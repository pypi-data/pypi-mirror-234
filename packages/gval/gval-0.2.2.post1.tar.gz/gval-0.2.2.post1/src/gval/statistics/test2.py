# Test2.py

from gval import CatStats as CatSt
# from gval.statistics.test import cat_stats, register


if __name__ == "__main__":
    # Method 1 - Import from another file
    print(CatSt.available_functions())
    print(CatSt.matthews_correlation_coefficient(100, 0, 0, 0))
    # print(cat_stats.available_functions())
    # print("test", cat_stats.registered_functions["test"])
    # print(cat_stats.test(*[30, 20]))
    # print("test6", cat_stats.registered_functions["test6"])
    # print(cat_stats.test6(*[30, 20]))
    #
    # # Method 2 - Call register function from separate file
    # new_obj = CatSt()
    # register(new_obj)
    # print(new_obj.available_functions())
    # print("test", new_obj.registered_functions["test"])
    # print(new_obj.test(*[30, 20]))
    # print("test6", new_obj.registered_functions["test6"])
    # print(new_obj.test6(*[30, 20]))


# pending registration discusison
# persistence (disk? config? cache?)
# pending comments xarray accessor issue discussion
# pending jupyter notebook
