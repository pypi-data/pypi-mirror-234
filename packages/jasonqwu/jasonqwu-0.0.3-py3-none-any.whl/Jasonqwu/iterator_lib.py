#
# @author Jason Q. Wu
# @create 2021-04-28 09:07
#
from collections.abc import Iterator, Iterable
from jasonqwu_lib import *


class IT:
    def __init__(self):
        self.counter = 0

    def __iter__(self):
        return self

    def __next__(self):
        self.counter += 1
        if self.counter == 3:
            raise StopIteration()
        return self.counter


class Foo:
    def __iter__(self):
        return IT()


class IterRange:
    def __init__(self, num):
        self.num = num
        self.counter = -1

    def __iter__(self):
        return self

    def __next__(self):
        self.counter += 1
        if self.counter == self.num:
            raise StopIteration()
        return self.counter


class Xrange:
    def __init__(self, max_num):
        self.max_num = max_num

    def __iter__(self):
        counter = 0
        while counter < self.max_num:
            yield counter
            counter += 1
        return IterRange(self.max_num)


def creater():
    yield 5
    yield 8
    yield 18


if __name__ == "__main__":
    obj1 = IT()
    obj1.counter = 5

    v1 = next(obj1)
    debug(v1)

    v2 = next(obj1)
    debug(v2)

    v3 = next(obj1)
    debug(v3)

    obj2 = IT()
    for item in obj2:
        debug(item)

    obj1 = creater()
    v1 = next(obj1)
    debug(v1)

    v2 = next(obj1)
    debug(v2)

    v3 = next(obj1)
    debug(v3)

    obj2 = creater()
    for item in obj2:
        debug(item)

    obj = Foo()
    for item in obj:
        debug(item)

    obj = Xrange(10)
    for item in obj:
        debug(item)

    v1 = [11, 22, 33]
    debug(isinstance(v1, Iterator))
    debug(isinstance(v1, Iterable))

    v2 = v1.__iter__()
    debug(isinstance(v2, Iterator))
    debug(isinstance(v2, Iterable))
