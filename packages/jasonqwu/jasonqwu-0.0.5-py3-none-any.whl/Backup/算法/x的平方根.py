import ipdb
from score_lib import *

# 在不使用 sqrt(x) 函数的情况下，得到 x 的平方根的整数部分
# 重点考察：二分法、牛顿迭代
def sqrt_int1():
	x = int(input("请输入一个正整数："))
	for _ in range((x + 3) // 2):
		if _ * _ <= x and (_ + 1) * (_ + 1) > x:
			print(f"x 的平方根的整数部分是 {_}")
			break

def sqrt_int2():
	left = 0
	x = int(input("请输入一个正整数："))
	right = x
	while left <= right:
		# ipdb.set_trace()
		middle = (right - left) // 2
		if middle * middle > x:
			right = middle + 1
		elif (middle + 1) * (middle + 1) > x:
			print(f"x 的平方根的整数部分是 {middle}")
			break
		elif (middle + 1) * (middle + 1) == x:
			print(f"x 的平方根的整数部分是 {middle+1}")
			break
		else:
			left = middle

def main():
	sqrt_int2()

if __name__ == '__main__':
	main()
