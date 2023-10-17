import ipdb
from random import *

# 中心下标是数组的一个下标，其左侧所有元素相加的和等于右侧所有元素相加的和。
# 如果数组不存在中心下标，返回 -1。如果数组有多个中心下标，应该返回最靠近左边的那一个。
# 注意：中心下标可能出现在数组的两端。
def center(list):
	center = 0
	left = 0
	right = 0
	res = -1
	for _ in list:
		right += _
	for _ in list:
		# ipdb.set_trace()
		res += 1
		left += center
		right -= _
		center = _
		if left == right:
			return res
		if left > right:
			break
	return -1

def main():
	length = randint(2, 20)
	data = []
	for _ in range(length):
		data.append(randint(-9, 9))
	print("data = {}".format(data))
	print(center(data))
	print("data = {}".format(data))

if __name__ == '__main__':
	main()