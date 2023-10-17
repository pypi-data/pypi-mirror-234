#
# -*- coding: UTF-8 -*-
# @author Jason Q. Wu
# @create 2021-04-27 07:22
#
# 1. 重复元素判定
# 以下方法可以检查给定列表是不是存在重复元素，它会使用 set() 函数来移除所有重复元素。
def all_unique(list):
    return len(list) == len(set(list))

# 15. 列表的差
# 该方法将返回第一个列表的元素，其不在第二个列表内。如果同时要反馈第二个列表独有的元素，还需要加一句 set_b.difference(set_a)。
def difference(a, b):
    set_a = set(a)
    set_b = set(b)
    comparison = set_a.difference(set_b)
    return list(comparison)

# 16. 通过函数取差
# 如下方法首先会应用一个给定的函数，然后再返回应用函数后结果有差别的列表元素。
from math import floor
def difference_by(a, b, fn):
    b = set(map(fn, b))
    return [item for item in a if fn(item) not in b]

# 17. 链式函数调用
# 你可以在一行代码内调用多个函数
def add(a, b):
    return a + b

def subtract(a, b):
    return a - b

# 18. 检查重复项
# 如下代码将检查两个列表是不是有重复项。
def has_duplicates(list):
    return len(list) != len(set(list))

# 19. 合并两个字典
# 下面的方法将用于合并两个字典。
def merge_two_dicts(a, b):
    from copy import copy
    c = a.copy()
    c.update(b)
    return c

def merge_dictionaries(a, b):
    return {**a, **b}

# 20. 将两个列表转化为字典
# 如下方法将会把两个列表转化为单个字典
def to_dictionary(keys, values):
    return dict(zip(keys, values))

# 21. 使用枚举
# 我们常用 For 循环来遍历某个列表，同样我们也能枚举列表的索引与值。

# 22. 执行时间
# 如下代码块可以用来计算执行特定代码所花费的时间。
from decorator_lib import *
@deco
def sum_two(a, b):
    c = a + b
    print(c)

# 23. Try else
# 我们在使用 try/except 语句的时候也可以加一个 else 子句，如果没有触发错误的话，这个子句就会被运行。

# 24. 元素频率
# 下面的方法会根据元素频率取列表中最常见的元素
def most_frequent(list):
    return max(set(list), key=list.count)

# 25. 回文序列
# 以下方法会检查给定的字符串是不是回文序列，它首先会把所有字母转化为小写，并移除非英文字母符号。最后，它会对比字符串与反向字符串是否相等，相等则表示为回文序列。
def palindrome(string):
    from re import sub
    s = sub('[\W]','',string.lower())
    return s == s[::-1]

# 26. 不使用 if-else 的计算子
# 这一段代码可以不使用条件语句就实现加减乘除、求幂操作，它通过字典这一数据结构实现。

# 27. Shuffle
# 该算法会打乱列表元素的顺序，它主要会通过 Fisher-Yates 算法对新列表进行排序。
from copy import deepcopy
from random import randint
def shuffle(list):
    temp_list = deepcopy(list)
    m = len(temp_list)
    while(m):
        m -= 1
        i = randint(0, m)
        temp_list[m], temp_list[i] = temp_list[i], temp_list[m]
    return temp_list

# 28. 展开列表
# 将列表内的所有元素，包括子列表，都展开成一个列表
def spread(arg):
    ret = []
    for i in arg:
        if isinstance(i, list):
            ret.extend(i)
        else:
            ret.append(i)
    return ret

# 29. 交换值
# 不需要额外的操作就能交换两个变量的值。
def swap(a, b):
    return b, a

# 30. 字典默认值
# 通过 Key 取对应的 Value 值，可以通过以下方式设置默认值。如果 get() 方法没有设置默认值，那么如果遇到不存在的 Key，则会返回 None。

if __name__ == '__main__':
    # 15. 列表的差
    print(difference([1,2,3], [1,2,4]))

    # 16. 通过函数取差
    print(difference_by([2.1,1.2],[2.3,3.4],floor))
    # print(difference_by({'x':2},{'x':1},lambda v:v['x']))

    # 17. 链式函数调用
    a, b = 4, 5
    print((subtract if a > b else add)(a, b))

    # 18. 检查重复项
    x = [1, 2, 3, 4, 5, 5]
    y = [1, 2, 3, 4, 5]
    print(has_duplicates(x))
    print(has_duplicates(y))

    # 19. 合并两个字典
    a = {'x':1, 'y':2,}
    b = {'y':3, 'z':4}
    print(merge_two_dicts(a, b))
    print(merge_dictionaries(a, b))

    # 20. 将两个列表转化为字典
    keys = ["a", "b", "c"]
    values = [2, 3, 4]
    print(to_dictionary(keys, values))

    # 21. 使用枚举
    list = ["a", "b", "c", "d"]
    for index, element in enumerate(list):
        print("Value", element, "Index", index)

    # 22. 执行时间
    sum_two(1, 2)

    # 23. Try else
    try:
        2 * 3
    except TypeError:
        print("An exception was raised.")
    else:
        print("Thank God, no exceptions were raised.")

    # 24. 元素频率
    list = [1, 2, 1, 2, 3, 2, 1, 4, 2]
    print(most_frequent(list))

    # 25. 回文序列
    print(palindrome("taco cat"))

    # 26. 不使用 if-else 的计算子
    import operator
    action = {"+":operator.add, "-":operator.sub, "*":operator.mul, "/":operator.truediv, "**":operator.pow}
    print(action["-"](50, 25))

    # 27. Shuffle
    foo = [1, 2, 3]
    print(shuffle(foo))

    # 28. 展开列表
    print(spread([1,2,3,[4,5,6],[7],8,9]))

    # 29. 交换值
    print(swap(a, b))

    # 30. 字典默认值
    print(d.get('c', 3))
