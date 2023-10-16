#
# -*- coding: UTF-8 -*-
# @author Jason Q. Wu
# @create 2021-05-13 10:41
#
import sys
import re
from math import ceil
from collections import Counter


def chunk(lst, size):
    return list(
        map(lambda _: lst[_ * size:_ * size + size],
            list(range(0, ceil(len(lst) / size)))))


def spread(arg):
    ret = []
    for _ in arg:
        if isinstance(_, list):
            ret.extend(_)
        else:
            ret.append(_)
    return ret


def deep_flatten(lst):
    ret = []
    ret.extend(
        spread(
            list(map(lambda _: deep_flatten(_)
                     if type(_) == list else _, lst))))
    return ret


if __name__ == '__main__':
    # 1. 检查给定的列表中是否有重复的元素
    x = [1, 1, 2, 2, 3, 2, 3, 4, 5, 6]
    y = [1, 2, 3, 4, 5]
    print(f"{x} all unique: {len(x) == len(set(x))}")  # False
    print(f"{y} all unique: {len(y) ==len(set(y))}")  # True

    # 2. 检查两个字符串是否互为变位词
    print(
        f'"abcd3" and "3acdb" is anagram: {Counter("abcd3") == Counter("3acdb")}'
    )

    # 3. 检查变量的内存使用情况
    x = "abcde"
    print(f"The size of the variable is {sys.getsizeof(x)} bytes.")

    # 4. 以字节为单位显示字符串长度
    print(len("我们".encode("utf-8")))

    # 5. 重复打印字符串
    print("Programming" * 2)

    # 6. 首字母大写
    print("programming is awesome".title())

    # 7. 分块
    print(chunk([1, 2, 3, 4, 5], 2))

    # 8. 压缩
    print(list(filter(bool, [0, 1, False, 2, None, 3, 'a', 's', 34])))

    # 9. 间隔数
    array = [['a', 'b', 'x'], ['c', 'd'], ['e', 'f']]
    transposed = zip(*array)
    print(list(transposed))

    # 10. 链式比较
    a = 3
    print(2 < a < 8)
    print(1 == a < 2)

    # 11. 逗号分隔
    hobbies = ["basketball", "football", "swimming"]
    print("My hobbies are: " + ','.join(hobbies))

    # 12. 计算元音字母数
    print(
        f'The count of vowel is {len(re.findall("[aeiou]", "foobar", re.IGNORECASE))}'
    )
    print(
        f'The count of vowel is {len(re.findall("[aeiou]", "gym", re.IGNORECASE))}'
    )

    # 13. 首字母恢复小写
    print("Foobar"[:1].lower() + "FooBar"[1:])

    # 14. 平面化
    print(deep_flatten([1, [2], [[3], 4], 5]))

    # 15. 差异
    print(list(set([0, 1, 2, 3]).difference(set([1, 2, 4]))))

    # 16. 正则表达式带括号与不带括号的区别
    string = "abcdefg  acbdgef  abcdgfe  cadbgfe"
    regex = re.compile("((\w+)\s+\w+)")
    print(regex.findall(string))
    regex1 = re.compile("(\w+)\s+\w+")
    print(regex1.findall(string))
    regex2 = re.compile(r"\w+\s+\w+")
    print(regex2.findall(string))
