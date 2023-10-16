import ipdb
from random import *

def remove_duplicates(list):
	fast = 0
	slow = 0
	length = len(list)
	for _ in list:
		if fast == 0:
			fast += 1
			continue
		if _ == list[slow]:
			length -= 1
			fast += 1
			continue
		else:
			list[slow+1] = list[fast]
			fast += 1
			slow += 1
	for i in range(length, len(list)):
		# ipdb.set_trace()
		del list[length]
	return length

def main():
	length = randint(2, 20)
	data = []
	for _ in range(length):
		data.append(randint(0, 9))
	data.sort()
	print("data = {}".format(data))
	print(remove_duplicates(data))
	print("data = {}".format(data))

if __name__ == '__main__':
	main()