# import timeit
from jasonqwu_lib import *


class Practice:
    def program00():
        debug("-----数字的阶乘-----")
        number = Tool.get_int(1, 100)
        if number < 0:
            debug("输入了一个负数。")
        else:
            debug(f"{number} 的阶乘 = {Tool.factorial(number):e}")

    def program01():
        debug("-----求园的面积-----")
        number = Tool.get_float(-5, 100)
        if number < 0:
            debug("输入了一个负数。")
        else:
            debug(f"半径为 {number} 的圆的面积 = " +
                  f"{round(math.pi * number * number, 2)}")


def program02():
    pass


def program03():
    pass


func = {
    0: Practice.program00,
    1: Practice.program01,
}


if __name__ == '__main__':
    for i in range(2):
        debug(f"======================{i:02d}======================")
        func[i]()
