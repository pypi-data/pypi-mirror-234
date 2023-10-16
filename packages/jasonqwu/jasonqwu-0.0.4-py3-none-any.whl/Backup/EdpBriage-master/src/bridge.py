#-*- coding:utf-8 -*-

from src.deck import Deck
from src.player import Player

def circleList(ls, start):
  ls = ls[start:] + ls[:start]
  return ls

class Bridge(object):

  def __init__(self):
    #intialize the players
    self.players = {n: Player(n, n) for n in ['N', 'E', 'S', 'W']}
    #initialize the deck
    self.deck = Deck()
    self.playing = None
    self.nt = False
    #deal out the cards
    for rnd in range(13):
      for player in self.players.values():
        card = self.deck.deal()
        player.recv(card)

  def _get_winner(self, suit):
    win_player = None
    for player in self._get_players(self.playing.pos):
      if win_player is None:
        win_player = player
        continue
      win_player = self._compare(win_player, player, suit)
    return win_player

  def _compare(self, player_a, player_b, suit):
    # TODO(zou): Calculate the card size of two players
    if player_a.card().value > player_b.card().value:
      return player_a
    else:
      return player_b

  def _get_players(self, start):
    if start == 'N':
      return [self.players['N'], self.players['E'], self.players['S'], self.players['W']]
    elif start == 'E':
      return [self.players['E'], self.players['S'], self.players['W'], self.players['N']]
    elif start == 'S':
      return [self.players['S'], self.players['W'], self.players['N'], self.players['E']]
    elif start == 'W':
      return [self.players['W'], self.players['N'], self.players['E'], self.players['S']]
    else:
      raise ValueError("Error start, %s" % start)

  def play(self):
    start = 'N'
    suit = None
    for rnd in range(13):
      players = self._get_players(start)
      self.playing = self.players[start]
      for player in players:
        player.pick(rnd, suit)
        print('%s play: %s' % (player.name, player.card()))
    
      win_player = self._get_winner(suit)
      start = win_player.pos
      suit = win_player.card().suit





