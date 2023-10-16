import math
from vector_lib import Vector


class Matrix:
    @classmethod
    def zero(cls, r, c):
        '''返回一个 r 行 c 列的零矩阵'''
        return cls([[0] * c for _ in range(r)])

    def __init__(self, list2d=[]):
        self._values = [row[:] for row in list2d]

    def __repr__(self):
        return f"Matrix({self._values})"

    def __str__(self):
        return f"({', '.join(str(ele) for ele in self._values)})"

    def __len__(self):
        r, c = self.shape()
        return r * c

    def __iter__(self):
        return self._values.__iter__()

    def __eq__(self, another):
        for a, b in zip(self, another):
            if a != b:
                return False
        return True

    def __pos__(self):
        return 1 * self

    def __neg__(self):
        return (-1) * self

    def __getitem__(self, pos):
        '''返回矩阵 pos 位置的元素'''
        r, c = pos
        return self._values[r][c]

    def __add__(self, another):
        '''返回两个矩阵的加法结果'''
        assert len(self) == len(another), \
            "Error in adding. Length of matrix must be same."
        return Matrix([[a + b for a, b in zip(
            self.row_vector(i), another.row_vector(i))]
            for i in range(self.row_num())])

    def __sub__(self, another):
        assert len(self) == len(another), \
            "Error in subing. Length of matrix must be same."
        return Matrix([[a - b for a, b in zip(
            self.row_vector(i), another.row_vector(i))]
            for i in range(self.row_num())])

    def __mul__(self, k):
        """返回数量乘法的结果向量：self * k"""
        return Matrix([[a * k for a in self.row_vector(i)] for i in range(
            self.row_num())])

    def __rmul__(self, k):
        """返回数量乘法的结果向量：k * self"""
        return self * k

    def __truediv__(self, k):
        """返回数量除法的结果向量：self / k"""
        if k:
            return self * (1 / k)
        else:
            return self * 0

    def shape(self):
        """返回矩阵的形状：（行数，列数）"""
        return len(self._values), len(self._values[0])

    def row_num(self):
        """返回矩阵的形状：行数"""
        return len(self._values)

    def col_num(self):
        """返回矩阵的形状：列数"""
        return len(self._values[0])

    def row_vector(self, index):
        """返回矩阵的第 index 个行向量"""
        return Vector(self._values[index])

    def col_vector(self, index):
        """返回矩阵的第 index 个列向量"""
        return Vector([row[index] for row in self._values])

    def normalize(self):
        """返回向量的单位向量"""
        return Vector(self._values) / self.norm()

    def dot(self, another):
        """向量点乘，返回结果标量"""
        assert len(self) == len(another), \
            "Error in dot product. Length of vectors must be same."
        return sum(a * b for a, b in zip(self, another))
