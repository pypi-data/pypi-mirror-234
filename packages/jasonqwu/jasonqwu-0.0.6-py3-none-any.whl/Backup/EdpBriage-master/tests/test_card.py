#-*- coding:utf-8 -*-

import unittest
from src.card import Card
from src.errors import CardRankError, CardSuitError

class TestCard(unittest.TestCase):

	def test_init(self):
		card_2 = Card('2', 'S')
		with self.assertRaises(CardRankError):
			card_1 = Card('1', 'S')

		with self.assertRaises(CardSuitError):
			card_4 = Card('4', 'F')

	def test_equal(self):
		card_2 = Card('2', 'S')
		self.assertTrue(card_2 == Card('2', 'S'))
		self.assertFalse(card_2 == Card('2', 'H'))
		self.assertFalse(card_2 == Card('3', 'S'))
