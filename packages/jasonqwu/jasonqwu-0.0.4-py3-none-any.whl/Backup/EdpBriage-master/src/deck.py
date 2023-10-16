#-*- coding:utf-8 -*-

from src.card import Card
from random import shuffle as std_shuffle


class Deck(object):

  ranks = [str(n) for n in range(2, 11)] + list('JQKA')
  suits = ['S', 'H', 'D', 'C']

  def __init__(self):
    self._cards = [Card(rank, suit) for suit in self.suits
                                    for rank in self.ranks]
    self.shuffle()

  def shuffle(self):
    std_shuffle(self._cards)

  def deal(self):
    return self._cards.pop()

  def __len__(self):
    return len(self._cards)

  def __getitem__(self, index):
    return self._cards[index]
