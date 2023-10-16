import ipdb

class Reverse:
	'''例子：可把字符串反序输出的迭代器'''
	def __init__(self, data):
		self.data = data
		self.index = len(data)

	def __iter__(self):
		return self

	def __next__(self):
		# 把字符串挨个儿反序输出
		if self.index == 0:
			raise StopIteration

		self.index -= 1
		return self.data[self.index]

def main():
	r = Reverse("abc")

	for i in r:
		print(i)

	# from collections.abc import Iterable
	# print(isinstance(r, Iterable))

	# from collections.abc import Iterable
	# print(isinstance(r, Iterable))

if __name__ == '__main__':
	main()