#-*- coding:utf-8 -*-

from src.card import Card
from collections import OrderedDict

class Player(object):
  """
  Args:
    name: player name.
    hand: cards.
    pos: position(N,E,S,W).
    curr_round: Current number of rounds.
    cars: Has already played.

  class dictionaries to map the user input to the card associated
  suit_map = {'d':'diamond', 'c':'club','h':'heart','s':'spade'}
  value_map = {'2':2,'3':3,'4':4,'5':5,'6':6,'7':7,'8':8,'9':9,'10':10,'j':11,'q':12,'k':13,'a':14}
  """

  def __init__(self, name, pos):
    self.name = name
    self.hand = []
    self.pos = pos
    self.curr_round = 0
    self.cards = OrderedDict()
    #赢的墩数
    self.piers_num = 0
    #快速获取四个花色的牌{'S': [], 'H': [], 'D': [], 'C': []}
    self.four = OrderedDict()
    self.init_four()

  def card(self, round_num=0):
    """Get any round of cards, default current round.

    Args:
      wheel: int, Round.
    """
    if round_num < 0 or round_num > 14:
      raise ValueError("Its value should be between 1 and 13, not %d", round_num)
    if round_num == 0:
      return self.cards[str(self.curr_round)]
    return self.cards[str(round_num)]

  def init_four(self):
    for suit in 'S,H,D,C'.split(','):
      self.four[suit] = []

  def view(self):
    print('Cards in your hand:')
    for suit, cards in self.four.items():
      print(suit + ': ' + ' '.join(cards))

  def recv(self, card):
    self.hand.append(card)
    self.four[card.suit].append(card.rank)
    self.four[card.suit].sort(reverse=True)

  def pick(self, round_num, suit):
    while True:
      print('Selection must be of form: suit rank. e.g. S 9')
      print('Valid values: 2-10, J (jack), Q (queen), K (king), A (ace)')
      print('Valid suits: S (spades), H (hearts), D (diamonds), C (clubs)')
      print('')
      self.view()

      choice = input('Select card: ')
      choice = choice.split(' ')
      choice_card = Card(choice[1].upper(), choice[0].upper())
      #if the suit is not in the dictionary repeat the selection
      if choice_card not in self.hand:
        print('Invalid card')
        continue
      #now verify the card can be played
      if suit is None:
        #let them play because they have the card
        break
      #if the chosen card doesn't match the first suit played
      #but they dont have cards in that suit (a void)
      elif suit != choice_card.suit and not self.four[suit]:
        #let them play because they have a void
        break
      elif suit == choice_card.suit:
        #let them play because they are following suit
        break
      else:
        print('Must play a card from the suit: %s' % suit)
        continue

    #select the card object from the hand
    #remove the card from the hand
    self.hand.remove(choice_card)
    #remove the card from the organizer
    self.four[choice_card.suit].remove(choice_card.rank)
    print("%s successful card:" % self.name, choice_card)
    print("")

    self.cards[str(round_num)] = choice_card
    self.curr_round = round_num