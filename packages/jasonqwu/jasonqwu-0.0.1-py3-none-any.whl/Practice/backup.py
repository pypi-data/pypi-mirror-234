# import timeit
from jasonqwu_lib import *


class Practice:
    def program00():
        pass


def program01():
    pass


def program02():
    pass


func = {
    0: Practice.program00,
}


if __name__ == '__main__':
    for i in range(1):
        debug(f"======================{i:02d}======================")
        func[i]()
