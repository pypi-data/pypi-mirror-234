import os
from decorator_lib import *
from stack_lib import *

# 递归代替循环
def for_order(i):
	if i < 10:
		print(i)
		for_order(i + 1)

def for_rev(i):
	if i < 10:
		for_rev(i + 1)
		print(i)

# 显示九九乘法表
@deco
def multiplication_for(n):
    for i in range(n, 10):
        for j in range(1, i + 1):
            print(f"{j} * {i} = {i * j}", end='\t')
        print(end='\n')

@deco
def multiplication_rec(n):
    if n < 10:
        for i in range(1, n + 1):
            print("{} * {} = {}".format(i, n, i * n), end = '\t')
        print()
        multiplication_rec(n + 1)

# 舍罕王赏麦
def wheat(n):
	if n > 1:
		sum, res = wheat(n - 1)
		res = res * 2
		sum += res
		return sum, res
	else:
		return 1, 1

# 遍历文件
def display_file(path):
	for each in os.listdir(path):
		absolute_path = os.path.join(path, each)
		is_file = os.path.isfile(absolute_path)
		if is_file:
			print(each)
		else:
			print("-----", each, "-----")
			display_file(absolute_path)
			print("-----", each, "-----")

# 斐波那契数列
@deco
def fibonacci_order(n):
	if n > 1:
		a = 1
		b = 1
		fib = 0
		for i in range(2, n + 1):
			fib = a + b
			a = b
			b = fib
		return fib
	else:
		return 1

@deco
def fibonacci_rec(n):
	if n > 1:
		return fibonacci_rec(n - 1) + fibonacci_rec(n - 2)
	else:
		return 1

def move(n, s1, s2, s3):
	if n != 1:
		move(n - 1, s1, s3, s2)
		move(1, s1, s2, s3)
		move(n - 1, s2, s1, s3)
	else:
		# s1 -> s3
		s3.push(s1.pop())
		print("{} => {}".format(s1.name, s3.name))

def hano(n):
	a = Stack("A")
	b = Stack("B")
	c = Stack("C")
	for i in range(n, 0, -1):
		a.push(i)
	move(n, a, b, c)
	for i in range(n):
		print(c.pop())

def test_for(n):
	for_order(n)
	for_rev(n)

def test_multiplication(n):
	multiplication_for(n)
	multiplication_rec(n)

def test_wheat(n):
	sum, res = wheat(n)
	print("舍罕王赏麦 = {}".format(sum))

def test_display_file(path):
	display_file(path)

def test_fibonacci(n):
	for i in range(n):
		print(fibonacci_order(i))
	for i in range(n):
		print(fibonacci_rec(i))
