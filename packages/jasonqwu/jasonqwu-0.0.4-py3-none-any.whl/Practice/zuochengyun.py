 from jasonqwu_lib import *


class Practice:
    def program00():
        times = 100000
        count = 0
        for i in range(times):
            result = Tool.create_binary(3, 1, 5, 7)
            if result == 1:
                count += 1
        debug(f"result = {count / times}")
        debug(f"Tool.create_binary(3, 1, 5, 7) = " +
              f"{Tool.create_binary(3, 1, 5, 7) + 1}")

    def program01():
        pass


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
