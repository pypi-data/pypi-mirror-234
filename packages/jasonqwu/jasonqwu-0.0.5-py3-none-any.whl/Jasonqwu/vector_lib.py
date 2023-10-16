import math

EPSILON = 0

class Vector:
	@classmethod
	def zero(cls, dim):
		return cls([0] * dim)

	def __init__(self, *lst):
		self._values = list(lst)

	def __repr__(self):
		return f"Vector({self._values})"

	def __str__(self):
		return f"Vector({', '.join(str(ele) for ele in self._values)})"

	def __len__(self):
		return len(self._values)

	def __iter__(self):
		return self._values.__iter__()

	def __eq__(self, another):
		for a, b in zip(self, another):
			if a != b:
				return False
		return True

	def __neg__(self):
		return (-1) * self

	def __getitem__(self, index):
		return self._values[index]

	def __add__(self, another):
		"""
		>>> v1 = Vector(2, 4)
		>>> v2 = Vector(2, 1)
		>>> v1 + v2
		Vector([4, 5])
		"""
		assert len(self) == len(another), \
			"Error in adding. Length of vectors must be same."
		self._values = list(a + b for a, b in zip(self, another))
		return self

	def __sub__(self, another):
		"""
		>>> v1 = Vector(2, 4)
		>>> v2 = Vector(2, 1)
		>>> v1 - v2
		Vector([0, 3])
		"""
		assert len(self) == len(another), \
			"Error in subing. Length of vectors must be same."
		self._values = list(a - b for a, b in zip(self, another))
		return self

	def __mul__(self, k):
		"""
		返回数量乘法的结果向量：self * k
		>>> v1 = Vector(2, 4)
		>>> 5 * v1
		Vector([10, 20])
		"""
		self._values = list(k * i for i in self)
		return self

	def __rmul__(self, k):
		"""
		返回数量乘法的结果向量：k * self
		>>> v1 = Vector(2, 4)
		>>> v1 * 5
		Vector([10, 20])
		"""
		return self * k

	def __truediv__(self, k):
		"""
		返回数量除法的结果向量：self / k
		>>> v1 = Vector(10, 20)
		>>> v1 / 5
		Vector([2.0, 4.0])
		"""
		if k:
			return self * (1 / k)
		else:
			return self * 0

	def norm(self):
		"""返回向量的模"""
		return math.sqrt(sum(e ** 2 for e in self))

	def normalize(self):
		"""返回向量的单位向量"""
		if self.norm() < EPSILON:
			raise ZeroDivisionError("Normalize error! norm is zero.")
		return Vector(self._values) / self.norm()

	def dot(self, another):
		"""向量点乘，返回结果标量"""
		assert len(self) == len(another), \
			"Error in dot product. Length of vectors must be same."
		return sum(a * b for a, b in zip(self, another))