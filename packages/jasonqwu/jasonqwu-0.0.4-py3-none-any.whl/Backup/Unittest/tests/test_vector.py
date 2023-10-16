import unittest
from vector_lib import Vector

class TestVector(unittest.TestCase):
	def setUp(self):
		pass

	def tearDown(self):
		pass

	def test_init(self):
		v = Vector(1, 2)
		self.assertEqual(v.x, 1)
		self.assertEqual(v.y, 2)

	def test_001(self):
		pass

	def test_002(self):
		pass

if __name__ == '__main__':
	suite = unittest.TestSuite()
	suite.addTest('test_001')
	unittest.TextTestRunner(verbosity=2).run(suite)
