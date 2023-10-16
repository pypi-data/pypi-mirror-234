# import random_lib
import logging_lib
import bogo_sort
import insertion_sort
from jasonqwu_lib import *


def int_list(base_func, compare_func, times, max_size, max_value):
    # log = logging_lib.Logger("log0")
    source = Tool.get_array()
    debug(source)
    a = base_func(source)
    b = compare_func(source)
    for i in range(max_size):
        if a[i] == b[i]:
            debug(f"a[{i}] = {a[i]}, b[{i}] = {b[i]}")


if __name__ == '__main__':
    int_list(bogo_sort.bogo_sort, insertion_sort.insertion_sort, 2, Config.MAX_LENGTH, Config.MAX_VALUE)
