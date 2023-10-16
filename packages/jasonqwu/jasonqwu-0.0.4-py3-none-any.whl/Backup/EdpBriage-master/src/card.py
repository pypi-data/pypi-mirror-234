#-*- coding:utf-8 -*-

import logging
from src.errors import CardAppendError
from src.errors import CardSpilloverError
from src.errors import CardRankError
from src.errors import CardSuitError


class Card(object):
  """Card object

  :rank str value (2~10AKQJ)
  :suit str suit (S, H, D, C)
  """
  rank_val = {'J': 11, 'Q': 12, 'K': 13, 'A': 14}

  def __init__(self, rank, suit):
    self._logger = logging.getLogger('EdpBriage.Card')

    self.rank = self.check_rank(rank)
    self.suit = self.check_suit(suit)

  @property
  def value(self):
    val = self.rank_val.get(self.rank)
    if val is None:
      return int(self.rank)
    return val

  def check_rank(self, rank):
    if rank not in '2,3,4,5,6,7,8,9,10,J,Q,K,A'.split(','):
      self._logger.error('The value of the card should be in the range of \
                          "2 3 4 5 6 7 8 9 10 J Q K A".')
      raise CardRankError
    return rank.upper()

  def check_suit(self, suit):
    if suit not in 'S,H,D,C'.split(','):
      raise CardSuitError
    return suit

  def __str__(self):
    return 'Card(suit="%s", rank="%s")' % (self.suit, self.rank)

  def __repr__(self):
    return self.__str__()

  def __eq__(self, other):
    if self.rank == other.rank \
        and self.suit == other.suit:
      return True
    return False


class Hand(object):
  
  def __init__(self):
    self._cards = []

  def append(self, card):
    if not isinstance(card, Card):
        raise CardAppendError
    if len(self) >= 13:
        raise CardSpilloverError
    self._cards.append(card)

  def clear(self):
    self._cards = []

  def __str__(self):
    card_str = ''
    for card in self._cards:
        card_str += '%s%s ' % (card.suit, card.rank)
    return card_str

  def __len__(self):
    return len(self._cards)

  def __contains__(self, card):
    return any(c == card for c in self._cards)
