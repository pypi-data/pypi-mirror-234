#
# -*- coding: UTF-8 -*-
# @author Jason Q. Wu
# @create 2021-05-19 09:24
#
# from decorator_lib import *
from decorator import decorator
from jasonqwu_lib import *

__all__ = ["deco"]


@decorator
def deco(func, timelimit=60, *args, **kwargs):
    start_time = time.time()

    debug("Ready to run task")
    ret = func(*args, **kwargs)
    debug("Successful to run task")
    total_time = time.time() - start_time

    if total_time > timelimit:
        debug(f"{func.__name__} took {total_time} seconds")
    else:
        debug(f"{func.__name__} took {total_time} seconds")
    return ret


@deco
def print_odds(limit=10000):
    sum = 0
    for i in range(limit):
        if i % 2 == 1:
            sum += 1
    return sum


def is_prime(num):
    if num < 2:
        return False
    elif num == 2:
        return True
    else:
        for i in range(2, num):
            if num % i == 0:
                return False
        return True


@deco
def prime_nums():
    sum = 0
    for i in range(2, 10000):
        if is_prime(i):
            sum += i


if __name__ == '__main__':
    debug(f"Wrap the function of {print_odds.__name__}")
    print_odds()
    debug(f"Wrap the function of {prime_nums.__name__}")
    prime_nums()
