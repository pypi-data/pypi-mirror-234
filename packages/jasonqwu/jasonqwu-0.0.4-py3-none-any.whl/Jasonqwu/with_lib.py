# import pdb; pdb.set_trace()
import contextlib
import functools
from jasonqwu_lib import *


@functools.total_ordering
class With:
    def __init__(self, value=1):
        self._value = value

    def __str__(self):
        return str(self._value)

    def __enter__(self):
        debug("enter")
        return self

    def __exit__(self, exc_type, exc_value, exc_tb):
        debug(f"self = {self._value}")
        debug(f"exc_type = {exc_type}")
        debug(f"exc_value = {exc_value}")
        debug(f"exc_tb = {exc_tb}")
        import traceback
        # traceback.print_exc()
        debug("exit")
        return True

    def __eq__(self, other):
        debug("eq")

    def __lt__(self, other):
        debug("lt")

    def __getitem__(self, item):
        debug("getitem")
        self._value += 1
        if self._value >= 5:
            raise StopIteration("停止遍历")
        return self._value

    def __iter__(self):
        debug("iter")
        self._value = 1
        return self

    def __next__(self):
        debug("next")
        self._value += 1
        if self._value >= 5:
            raise StopIteration("停止遍历")
        return self._value

    def close(self):
        debug("资源释放")


@contextlib.contextmanager
def zero_division():
    try:
        yield "xxx"
    except ZeroDivisionError as e:
        debug(f"error: {e}")


# 快速实现上下文管理器
# with contextlib.closing(With()) as x:
with With() as x:
    debug(f"body = {x}")
    1 / 0

with zero_division() as x:
    debug(f"3, {x}")
    1 / 0

if __name__ == '__main__':
    w1 = With()
    w2 = With()
    debug(w1 >= w2)
    for i in w1:
        debug(i)

    for i in w1:
        debug(i)
