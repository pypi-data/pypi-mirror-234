from .jasonqwu_lib import *

class Caculator:
    def __check_num(function):
        def inner(self, integer):
            if not isinstance(integer, int):
                raise TypeError("当前这个数据类型有问题，应该是一个整数。")
            return function(self, integer)
        return inner

    def __say(self, word):
        if "self.__engine" not in locals().keys():
            self.__engine = pyttsx3.init()
        self.engine.say(word)

    def __create_say(word=""):
        def inner(function):
            def wrapper(self, number):
                self.__say(word + str(number))
                return function(self, number)
            return wrapper
        return inner

    @__check_num
    @__create_say()
    def __init__(self, num):
        self.__result = num

    @property
    def engine(self):
        return self.__engine

    @__check_num
    @__create_say("加上")
    def add(self, num):
        self.__result += num
        return self

    @__check_num
    @__create_say("减去")
    def sub(self, num):
        self.__result -= num
        return self

    @__check_num
    @__create_say("乘以")
    def mul(self, num):
        self.__result *= num
        return self

    @__check_num
    @__create_say("除以")
    def div(self, num):
        self.__result /= num
        return self

    def print(self):
        debug(f"result = {self.__result}")
        self.__say("等于" + str(self.__result))
        txt = "颖颖，你好。认识你很高兴。我是伍强6，6，6"
        self.engine.save_to_file(txt, "access.mp3")
        self.engine.runAndWait()
        return self
