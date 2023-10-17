import math

from rich_lib import *

def max_second(lst):
	max = None
	second = None
	for i in lst:
		if max == None:
			max = i
		elif second == None:
			if i > max:
				second = max
				max = i
			else:
				second = i
		elif i > max:
			second = max
			max = i
		elif i > second:
			second = i
	print("max = {}, second = {}".format(max, second))
	return max, second

def fulcrum(lst):
	res = []
	length = len(lst)
	for i in range(1, length - 1):
		left_sum = 0
		for j in range(i):
			left_sum += lst[j]
		right_sum = 0
		for k in range(i + 1, length):
			right_sum += lst[k]
		if left_sum == right_sum:
			res.append(i)
	print("支点元素是：{}".format(res))
	return res

def lucky(lst):
	back = False
	lucky = 0
	for i in lst:
		if i == 6 or i == 8 or i == 9:
			if back:
				lucky -= 1
			else:
				lucky += 1
		elif i == 4:
			if back:
				lucky += 1
			else:
				lucky -= 1
		if i == 0:
			back = True
		else:
			back = False
	print("lucky number = {}".format(lucky))
	return lucky

def dichotomy(lst, search):
	length = len(lst)
	left = 0
	right = length - 1
	flag = False
	while left < right:
		point = left + math.floor((right - left) / 2)
		if search < lst[point]:
			right = point
		elif search > lst[point]:
			left = point + 1
		else:
			print("找到位置：{}".format(point))
			flag = True
			break
	if not flag:
		print("没找到")

def continue_sub(lst):
	sub = []
	max_sub = []
	point = None
	n = 1
	max = 1
	for i in lst:
		if point == None:
			point = i
		elif point == i - 1:
			point += 1
			n += 1
		else:
			if n > max:
				max_sub = sub.copy()
				max = n
			sub.clear()
			point = i
			n = 1
		sub.append(point)
	print("最长子串：{},长度为：{}".format(max_sub, max))

def half():
	pass

def gastation():
	pass
	
if __name__ == '__main__':
	lst = [1, 30, 29, 47, 12, 6, 21, 33, 17, 39]
	max_second(lst)
	lst = [9, -3, 7, 5, 15, -9, 5, 4, -2]
	fulcrum(lst)
	lst = [6, 3, 8, 7, 2, 5, 9, 0, 6, 3, 8, 4, 8, 0, 6, 1, 5, 0, 9, 7, 6, 4]
	lucky(lst)
	lst = [3, 5, 9, 13, 17, 22, 25, 29, 33, 36, 41, 43, 44, 48, 49, 56, 61, 67]
	dichotomy(lst, 29)
	lst = [13, 5, 9, 3, 4, 5, 43, 2, 7, 5, 9, 10, 11, 12, 13, 24, 6, 17, 9]
	continue_sub(lst)
