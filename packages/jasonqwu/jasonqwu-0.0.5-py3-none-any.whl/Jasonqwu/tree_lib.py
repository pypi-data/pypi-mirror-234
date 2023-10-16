class Node:
	def __init__(self, value=None):
		self.value = value
		self.type = None
		self.parent = None
		self.children = []
		self.left = None
		self.right = None

	def __str__(self):
		return str(self.value)

	def add(self, node):
		if self == None or node == None:
			return
		if node.value < self.value:
			if self.left != None:
				self.left.add(node)
			else:
				self.left = node
		else:
			if self.right != None:
				self.right.add(node)
			else:
				self.right = node

class Tree:
	def __init__(self, node=None):
		self.root = node
		if self.root is None:
			self.length = 0
		else:
			self.length = 1

	def __str__(self):
		return self.root

	def append(self, node):
		level = []
		temp = []
		if self.root != None:
			level.append(self.root)
			while len(level) > 0:
				for each in level:
					temp.append(each)
				level.clear()
				for each in temp:
					if each.left != None:
						level.append(each.left)
					else:
						each.left = node
						self.length += 1
						return
					if each.right != None:
						level.append(each.right)
					else:
						each.right = node
						self.length += 1
						return
				temp.clear()
		else:
			self.root = node
		self.length += 1

	def remove(self, node):
		pass

	def __pre_order(self, node, temp):
		temp.append(node.value)
		if node.left != None:
			self.__pre_order(node.left, temp)
		if node.right != None:
			self.__pre_order(node.right, temp)

	def pre_order(self):
		result = []
		if self.root != None:
			self.__pre_order(self.root, result)
		# print(result)
		return result

	def __in_order(self, node, temp):
		if node.left != None:
			self.__in_order(node.left, temp)
		temp.append(node.value)
		if node.right != None:
			self.__in_order(node.right, temp)

	def in_order(self):
		result = []
		if self.root != None:
			self.__in_order(self.root, result)
		# print(result)
		return result

	def __post_order(self, node, temp):
		if node.left != None:
			self.__post_order(node.left, temp)
		if node.right != None:
			self.__post_order(node.right, temp)
		temp.append(node.value)

	def post_order(self):
		result = []
		if self.root != None:
			self.__post_order(self.root, result)
		# print(result)
		return result

	def level_order(self):
		level_number = 0
		levels = []
		result = []
		level = []
		temp = []
		if self.root != None:
			level.append(self.root)
			while len(level) > 0:
				for each in level:
					result.append(each.value)
					levels.append(level_number)
					temp.append(each)
					# print(each, sep=' ', end=' ')
				level.clear()
				level_number += 1
				# print()
				for each in temp:
					if each.left != None:
						level.append(each.left)
					if each.right != None:
						level.append(each.right)
				temp.clear()
		# print(result)
		return result, levels

	def __make_line(self, length):
		line = []
		for x in range(length):
			line.append("  ")
		return line

	# @pysnooper.snoop(watch=("order"))
	def display(self):
		temp = 0
		order = self.in_order()
		level, levels = self.level_order()
		# print(order)
		# print(level)
		# print(levels)
		print()
		line = self.__make_line(len(order))
		for index_level, data in enumerate(level):
			for index_order, value in enumerate(order):
				if data == value:
					if levels[index_level] != temp:
						temp = levels[index_level]
						for i in line:
							print(i, end='')
						print()
						line = self.__make_line(len(order))
					line[index_order] = "%2d" % value
					break
		for i in line:
			print(i, end='')
		print()

class SortedTree(Tree):
	def add(self, node):
		if self.root != None:
			self.root.add(node)
		else:
			self.root = node
		self.length += 1
