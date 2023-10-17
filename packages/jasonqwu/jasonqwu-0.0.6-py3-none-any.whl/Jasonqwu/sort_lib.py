import numpy as np
from copy import copy, deepcopy
import pytest
from Jasonqwu.jasonqwu_lib import *


@Timer(100000)
def select_sort(nums, reverse=False):
    if nums is None or len(nums) < 2:
        return nums
    for i in range(len(nums)):
        peak = i
        for j in range(i + 1, len(nums)):
            if reverse:
                if nums[peak] < nums[j]:
                    peak = j
            else:
                if nums[peak] > nums[j]:
                    peak = j
        if peak != i:
            nums[peak], nums[i] = nums[i], nums[peak]
    return nums


@pytest.mark.parametrize("nums, reverse",
                         [([5, 3, 5, 2, 8], False),
                          ([5, 3, 5, 2, 8], True)])
def test_select(nums, reverse):
    temp = deepcopy(nums)
    temp.sort(reverse=reverse)
    assert select_sort(nums, reverse) == temp


@Timer(100000)
def barrel_sort(nums, total, reverse=False):
    if nums is None or len(nums) < 2:
        return nums
    barrels = [0 for ign in range(total)]
    ret = []
    for i in range(len(nums)):
        if nums[i] is None:
            debug("输入错误。")
        else:
            barrels[nums[i]] += 1
    for i in range(total):
        while barrels[i]:
            ret.append(i)
            barrels[i] -= 1
    if reverse:
        ret.reverse()
    return ret


@pytest.mark.parametrize("nums, total, reverse",
                         [([5, 3, 5, 2, 8], 11, False),
                          ([5, 3, 5, 2, 8], 11, True)])
def test_barrel(nums, total, reverse):
    temp = deepcopy(nums)
    temp.sort(reverse=reverse)
    assert barrel_sort(nums, total, reverse) == temp


@Timer(100000)
def bubble_sort(nums, reverse=False):
    if nums is None or len(nums) < 2:
        return nums
    for i in range(len(nums)-1, -1, -1):
        for j in range(i):
            if reverse:
                if nums[j] < nums[j+1]:
                    nums[j], nums[j+1] = nums[j+1], nums[j]
            else:
                if nums[j] > nums[j+1]:
                    nums[j], nums[j+1] = nums[j+1], nums[j]
    return nums


@pytest.mark.parametrize("nums, reverse",
                         [([5, 3, 5, 2, 8], False),
                          ([5, 3, 5, 2, 8], True)])
def test_bubble(nums, reverse):
    temp = deepcopy(nums)
    temp.sort(reverse=reverse)
    assert bubble_sort(nums, reverse) == temp


def quick_sort(nums, reverse=False):
    """
    >>> quick_sort([5, 3, 5, 2, 8])
    [2, 3, 5, 5, 8]
    >>> quick_sort([5, 3, 5, 2, 8], True)
    [8, 5, 5, 3, 2]
    """
    if nums is None or len(nums) < 2:
        return nums
    pivot = nums.pop()
    smaller: list[int] = []
    greater: list[int] = []
    for element in nums:
        (smaller if pivot > element else greater).append(element)
    nums.append(pivot)

    if reverse:
        return quick_sort(greater, reverse) + \
            [pivot] + \
            quick_sort(smaller, reverse)
    else:
        return quick_sort(smaller) + [pivot] + quick_sort(greater)


@pytest.mark.parametrize("nums, reverse",
                         [([5, 3, 5, 2, 8], False),
                          ([5, 3, 5, 2, 8], True)])
def test_quick(nums, reverse):
    temp = deepcopy(nums)
    temp.sort(reverse=reverse)
    Timer(100000)(quick_sort)(nums, reverse)
    assert quick_sort(nums, reverse) == temp


@Timer(100000)
def insert_sort(arr, reverse=False, simulation=False):
    if arr is None or len(arr) < 2:
        return arr
    for i in range(1, len(arr)):
        if simulation:
            debug(f"iteration {i - 1}: {arr}")
        curr = arr[i]
        idx = i
        for j in range(i - 1, -1, -1):
            if reverse:
                if arr[j] < curr:
                    arr[idx] = arr[j]
                    idx -= 1
            else:
                if arr[j] > curr:
                    arr[idx] = arr[j]
                    idx -= 1
        arr[idx] = curr
    else:
        if simulation:
            debug(f"iteration {i}: {arr}")
    return arr


@pytest.mark.parametrize("nums, reverse",
                         [([5, 3, 5, 2, 8], False),
                          ([5, 3, 5, 2, 8], True)])
def test_insert(nums, reverse):
    temp = deepcopy(nums)
    temp.sort(reverse=reverse)
    assert insert_sort(nums, reverse) == temp


if __name__ == '__main__':
    # import doctest
    # doctest.testmod(verbose=True)
    # py -m doctest -v Packages\sort_lib.py
    # from sort_lib import *

    # nums = get_array("请输入一个整数数组：")
    # print(barrel_sort(nums, 11))
    # print(barrel_sort(nums, 11, True))

    # nums = get_array("请输入一个整数数组：")
    # print(bubble_sort(nums))
    # print(bubble_sort(nums, True))

    # nums = get_array("请输入一个整数数组：")
    # print(quick_sort(nums))
    # print(quick_sort(nums, True))

    size = np.random.randint(1, 10)
    pop_list = np.random.randint(100, size=size)
    debug(insert_sort(pop_list, simulation=False))
