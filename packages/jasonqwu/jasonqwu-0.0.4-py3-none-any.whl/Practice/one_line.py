import math
import random
import re

# 1. 多个变量赋值
a, b, *c = 4, 5.5, "hello", 4, 5

# 2. 交换两个变量
a, b = b, a

# 3. 列表中偶数的和
r = sum([_ for _ in range(1, 7) if _ % 2 == 0])

# 4. 从列表中删除多个元素
a = list(range(1, 6))
del a[1::2]

# 5. 读取文件
a = [line.strip() for line in open("data.txt")]

# 6. 将数据写入文件
with open("data.txt", 'a', newline='\n') as f:
    f.write("Python is awesome\n")

# 7. 创建列表
a = list(range(10))

# 8. 映射列表或类型转换整个列表
a = [float(_) for _ in [1, 2, 3]]

# 9. 创建集合
a = {_ ** 2 for _ in range(10) if _ % 2 == 0}

# 10. Fizz Buzz
a = ["FizzBuzz" if _ % 3 == 0 and _ % 5 == 0
     else "Fizz" if _ % 3 == 0
     else "Buzz" if _ % 5 == 0
     else _ for _ in range(20)]

# 11. 回文
a = "level" == "level"[::-1]

# 12. 用空格分隔的整数到一个列表
# a = list(map(int, input("请输入用空格分隔的整数：").split()))

# 13. Lambda 函数
a = lambda _: _ * _

# 14. 检查列表中数字的存在
if 5 in [1, 2, 3, 4, 5]:
    print(a(10))

# 15. 打印图案
print('\n'.join('😀' * _ for _ in range(1, 6)))

# 16. 查找阶乘
a = math.factorial(6)

# 17. 斐波那契数列
a = [0, 1]
[a.append(a[-2] + a[-1]) for _ in range(5)]

# 18. 质数
a = list(filter(lambda x: all(x % y != 0 for y in range(2, x)), range(2, 13)))

# 19. 查找最大数值
a = lambda x, y: x if x > y else y


# 20. 线性代数
def scale(lst, x):
    return [_ * x for _ in lst]


a = scale([2, 3, 4], 2)

# 21. 矩阵转置
aa = [[1, 2, 3],
      [4, 5, 6],
      [7, 8, 9]]
a = [list(_) for _ in zip(*aa)]

# 22. 计数
a = len(re.findall("python",
                   "python is a programming language. python is python."))

# 23. 用其他文本替换文本
a = "python is a programming language.python is python".replace("python",
                                                                "Java")

# 24. 模拟抛硬币
a = random.choice(["Head", "Tail"])

# 25. 生成组
a = [(a, b) for a in ['a', 'b'] for b in [1, 2, 3]]
print(a)
