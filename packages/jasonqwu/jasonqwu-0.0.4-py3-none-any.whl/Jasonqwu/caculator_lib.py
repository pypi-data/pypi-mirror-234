# import win32com.client

# # 1. 创建一个播报器对象
# speaker = win32com.client.Dispatch("SAPI.SpVoice")

# # 2. 通过这个播报器对象，直接播放相对应的语音字符串就可以
# speaker.Speak("我的名字是伍强")
from .jasonqwu_lib import *

class Caculator:
    def __check_num(function):
        def inner(self, integer):
            if not isinstance(integer, int):
                raise TypeError("当前这个数据类型有问题，应该是一个整数。")
            return function(self, integer)
        return inner

    @__check_num
    def __init__(self, num):
        self.__result = num

    @__check_num
    def add(self, num):
        self.__result += num

    @__check_num
    def sub(self, num):
        self.__result -= num

    @__check_num
    def mul(self, num):
        self.__result *= num

    @__check_num
    def div(self, num):
        self.__result /= num

    def print(self):
        debug(f"result = {self.__result}")
