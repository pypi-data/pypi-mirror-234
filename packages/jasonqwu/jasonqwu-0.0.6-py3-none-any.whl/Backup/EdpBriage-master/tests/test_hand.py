#-*- coding:utf-8 -*-

import unittest
from src.card import Card, Hand
from src.errors import CardAppendError, CardSpilloverError

class TestHand(unittest.TestCase):

	def setUp(self):
		self.hand = Hand()


	def test_append(self):
		self.hand.clear()
		self.hand.append(Card('2', 'S'))

		with self.assertRaises(CardAppendError):
			card_2 = 'error_card'
			self.hand.append(card_2)

		self.assertTrue(len(self.hand) == 1)

		for rank in '3 4 5 6 7 8 9 10 J Q K A'.split(' '):
			self.hand.append(Card(rank, 'S'))

		self.assertTrue(len(self.hand) == 13)

		with self.assertRaises(CardSpilloverError):
			self.hand.append(Card('A', 'H'))

	def test_contains(self):
		self.hand.clear()
		for rank in '3 4 5 6 7 8 9 10 J Q K A'.split(' '):
			self.hand.append(Card(rank, 'S'))
		self.assertTrue(Card('3', 'S') in self.hand)
		self.assertFalse(Card('2', 'S') in self.hand)
