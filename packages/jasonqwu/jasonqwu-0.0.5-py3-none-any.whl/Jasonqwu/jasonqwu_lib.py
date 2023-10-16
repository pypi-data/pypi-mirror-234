#
# -*- coding: UTF-8 -*-
# from __future__ import absolute_import 
# @author Jason Q. Wu
# @create 2021-04-27 07:22
#
# from os import supports_bytes_environ
# 
# pip install --upgrade torchsde
#  -i https://pypi.python.org/simple/
#  --trusted-host pypi.python.org
# pip freeze
# pip install wheel
# pip install twine
import argparse
import math
import configparser
import json
import commentjson
import random
import time
import pyttsx3
import pytest
from functools import reduce
from tqdm import trange
from Jasonqwu.logging_lib import *


__all__ = ["argparse",
           "math",
           "time",
           "pyttsx3",
           "reduce",
           "trange",
           "Config",
           "Timer",
           "Decorator",
           "Tool",
           "debug",
           "info",
           "warning",
           "error",
           "critical"]


class Config:
    MAX_LENGTH = 10
    MAX_VALUE = 100

    def __init__(self, file_name):
        self._file_name = file_name.encode('utf-8').decode('utf-8')
        self._config = configparser.ConfigParser()

    def get_config(self):
        return self._config

    def set_config(self, config):
        self._config = config

    def read(self):
        # with open(self.file_name, "rt", newline='', encoding="utf8") as cfg:
        self._config.read(self.file_name, encoding="utf-8")

    def write(self):
        with open(self.file_name, "w", encoding="utf-8") as cfg:
            self._config.write(cfg)

    def print(self, content=None):
        debug(self._config.sections())
        test_data = {}
        for section in self._config.sections():
            test_data[section] = {}
            debug(section, self._config[section])
            for key in self._config[section]:
                test_data[section][key] = self._config[section][key]
                debug(f"{key} = {self._config[section].get(key)}")
        if content:
            debug(content)
        else:
            debug(test_data)


# 资料描述器：实现了 get set
# 非资料描述器：仅仅实现了 get 方法，那么它就是一个非资料描述器
# 执行优先级：资料描述器  > 实例属性 > 非资料描述器
class Value:
    def __get__(self, instance, owner):
        debug("get method in class Value")
        return instance._value

    def __set__(self, instance, value):
        debug("set method in class Value")
        instance._value = value

    def __delete__(self, instance):
        debug("delete method in class Value")
        del instance._value


class Timer:
    __slots__ = ["_iteration"]

    def __init__(self, iteration=1):
        self._iteration = iteration

    def __call__(self, func):
        def wrapper(*args, **kwargs):
            start = time.time()
            for ign in range(self._iteration):
                result = func(*args, **kwargs)
            debug(f"Time: {time.time() - start}")
            return result
        return wrapper


class Decorator:
    def __init__(self, func):
        self.func = func

    def __call__(self, *args, **kwargs):
        self.func(*args, **kwargs)

    @staticmethod
    def add_str(cls):
        def __str__(self):
            return str(self.__str__)
        cls.__str__ = __str__
        return cls

    # @staticmethod
    def count(iteration):
        def inner(func):
            def wrapper(*args, **kwargs):
                counter = 0
                for ign in range(iteration):
                    result = func(*args, **kwargs)
                    counter += 1
                return result
            return wrapper
        return inner


class Tool:
    @staticmethod
    def find(array, item):
        if array is None or array == []:
            return None
        array.sort()
        '''
           left and right keep track of
           which part of the array you'll search in.
        '''
        left = 0
        right = len(array) - 1

        # While you haven't narrowed it down to one element ...
        while left <= right:
            # ... check the middle element
            middle = (left + right) // 2
            guess = array[middle]
            # Found the item.
            if guess == item:
                return middle
            # The guess was more than right.
            if guess > item:
                right = middle - 1
            # The guess was less than left.
            else:
                left = middle + 1

        # Item doesn't exist
        return None

    @staticmethod
    def find_most(array, item, order=True):
        if array is None or array == []:
            return None
        array.sort()
        '''
           left and right keep track of
           which part of the array you'll search in.
        '''
        left = 0
        right = len(array) - 1
        result = None

        # While you haven't narrowed it down to one element ...
        while left <= right:
            # ... check the middle element
            middle = (left + right) // 2
            guess = array[middle]
            # Found the item.
            if guess == item:
                result = middle
            if order:
                # The guess was more than right.
                if guess >= item:
                    right = middle - 1
                # The guess was less than left.
                else:
                    left = middle + 1
            else:
                # The guess was less than left.
                if guess <= item:
                    left = middle + 1
                # The guess was more than right.
                else:
                    right = middle - 1

        # Item doesn't exist
        return result

    @staticmethod
    def find_peak(array, order=True):
        if array is None or array == []:
            return None
        if len(array) == 1:
            return 0
        if order:
            left = 0
            if array[left] < array[left+1]:
                return left
            right = len(array) - 1
            if array[right] < array[right-1]:
                return right
            while left <= right:
                mid = (left + right) // 2
                if array[mid] > array[mid-1]:
                    right = mid - 1
                elif array[mid] > array[mid+1]:
                    left = mid + 1
                else:
                    return mid
        else:
            left = 0
            if array[left] > array[left+1]:
                return left
            right = len(array) - 1
            if array[right] > array[right-1]:
                return right
            while left <= right:
                mid = (left + right) // 2
                if array[mid] < array[mid-1]:
                    right = mid - 1
                elif array[mid] < array[mid+1]:
                    left = mid + 1
                else:
                    return mid

    @staticmethod
    def get_int(start=0, stop=100):
        return random.randint(start, stop)

    @staticmethod
    def get_float(start=0, stop=100):
        return random.random() * (stop - start) + start

    @staticmethod
    def get_array():
        result = []
        length = random.randint(0, Config.MAX_LENGTH)
        for i in range(length):
            result.append(random.randint(-Config.MAX_VALUE, Config.MAX_VALUE))
        return result

    @staticmethod
    def appoint_probability_01(probability):
        '''
        按照固定概率返回 0 和 1
        '''
        return 0 if random.random() < probability else 1

    @staticmethod
    # @Decorator.count(10000)
    def equal_probability_01(start, stop, probability=0.5):
        '''
        在 start 和 stop 区间中返回固定概率的 0 和 1
        '''
        if start >= stop:
            return None

        number = Tool.appoint_probability_01(probability)
        middle_number = (stop - start) / 2 + 1
        if (stop - start) % 2 == 0:
            while number == middle_number:
                number = Tool.appoint_probability_01(probability)
            if probability != 0.5:
                while number == Tool.appoint_probability_01(probability):
                    number = Tool.appoint_probability_01(probability)
        return number

    @staticmethod
    def create_binary(digit, start, stop, remove):
        result = 0
        for i in range(digit):
            result += Tool.equal_probability_01(start, stop, 0.5) << i
            # result += Tool.appoint_probability_01(0.5) << i
        while result >= remove:
            result = 0
            for i in range(digit):
                result += Tool.equal_probability_01(start, stop, 0.5) << i
                # result += Tool.appoint_probability_01(0.5) << i
        return result

    @staticmethod
    def read_from_json_file(filename):
        with open(filename, encoding="utf-8") as f:
            content = f.read()
            return commentjson.loads(content)

    @staticmethod
    def write_to_json_file(filename, config):
        with open(filename, 'w', encoding="utf-8") as f:
            json.dump(config, f, indent=4)

    @staticmethod
    def fibonacci(num):
        if num == 1 or num == 2:
            return 1
        return fibonacci(num - 1) + fibonacci(num - 2)

    @staticmethod
    def ladder(list1, list2, num):
        result = 0
        for _ in range(len(list1)):
            if num > list1[_]:
                result += (num - list1[_]) * list2[_]
                num = list1[_]
        return result

    @staticmethod
    def map_list(fn, lst):
        result = []
        for i in lst:
            temp = fn(i)
            result.append(temp)
        return result

    @staticmethod
    def set_students(persons, scores, s, num):
        students = []
        for i in range(len(scores)):
            if scores[i] == s:
                students.append(persons[i])
                students.append(scores[i])
        return students

    @staticmethod
    def to_bytes(bytes_or_str):
        if isinstance(bytes_or_str, str):
            value = bytes_or_str.encode("utf-8")
        else:
            value = bytes_or_str
        return value  # !Instance of str

    @staticmethod
    def to_int(string):
        try:
            ret = int(string)
        except ValueError:
            return None
        else:
            return ret

    @staticmethod
    def to_str(bytes_or_str):
        if isinstance(bytes_or_str, bytes):
            value = bytes_or_str.decode("utf-8")
        else:
            value = bytes_or_str
        return value  # !Instance of str

    @staticmethod
    def to_list(string):
        if string[0] == '[':
            string = string[1:]
        if string[-1] == ']':
            string = string[:-1]
        temp = string.split(',')
        ret = temp
        for i in list(reversed(range(len(temp)))):
            ret[i] = List(to_int(temp[i]))
            if i != len(temp) - 1:
                pass
        return ret

    @staticmethod
    def adjust(index, scope):
        if index >= scope:
            index = scope - 1
        elif index < 0:
            if index < -scope:
                index = 0
            else:
                index += scope
        return index

    @staticmethod
    def is_prime(number):
        if number < 2:
            return False
        for i in range(2, int(math.sqrt(number)) + 1):
            if number % i == 0:
                return False
        return True

    @staticmethod
    def factorial(num):
        while num == 0:
            return 1
        return num * Tool.factorial(num - 1)


class TestTool:
    @pytest.mark.parametrize("array, number",
                             [([2, 3, 5, 4, 8, 9, 10, 18, 26, 32], 8),
                              ([2, 3, 5, 8, 9, 10, 18, 26, 32], 6),
                              ([], 4)])
    def test_find(self, array, number):
        index = Tool.find(array, number)
        try:
            source = array.index(number)
        except ValueError:
            source = None
        assert index == source

    @pytest.mark.parametrize("array, number, order",
                             [([1, 1, 1, 2, 2, 3, 4, 4, 5, 5, 6], 2, True),
                              ([1, 1, 1, 2, 2, 3, 4, 4, 5, 5, 6], 2, False),
                              ([1, 1, 1, 2, 2, 3, 4, 4, 5, 5, 6], 8, True),
                              ([], 4, True)])
    def test_find_most(self, array, number, order):
        index = Tool.find_most(array, number, order)
        try:
            if not order:
                array.reverse()
                source = array.index(number)
                source = len(array) - source - 1
            else:
                source = array.index(number)
        except Exception:
            source = None
        assert index == source

    @pytest.mark.parametrize("array, number, order",
                             [([1, 5, 1, 2, 7, 3, 8, 4, 5, 5, 6], 0, True),
                              ([1, 4, 1, 2, 7, 3, 8, 4, 5, 3, 6], 10, False),
                              ([7, 1, 5, 2, 6, 3, 4, 8, 5, 2, 6], 5, True),
                              ([], None, True)])
    def test_find_peak(self, array, number, order):
        index = Tool.find_peak(array, order)
        assert index == number


random.seed(time.time())
debug = Logger("show").get_level("debug")
info = Logger("show").get_level("info")
warning = Logger("show").get_level("warning")
error = Logger("show").get_level("error")
critical = Logger("show").get_level("critical")


if __name__ == '__main__':
    nums = Tool.get_array()
    debug(f"nums = {nums}")
    debug(f"number = {Tool.get_number(1, 100)}")
    conf = Config("pytest.ini")
    conf.print("xxxxx")
