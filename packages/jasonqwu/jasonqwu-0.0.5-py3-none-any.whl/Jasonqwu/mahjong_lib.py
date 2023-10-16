#
# @author Jason Q. Wu
# @create 2021-04-27 14:19
#
import collections
from random import *


class Deck:
    Mahjong = collections.namedtuple("Mahjong", ["rank", "suit"])
    ranks = [str(n) for n in range(1, 10)]
    suits = "筒 条 万".split()
    winds = "东 南 西 北 中 发 白".split()
    flowers = "春 夏 秋 冬 梅 兰 竹 菊".split()

    def __init__(self, status=None):
        if status == "empty":
            self._cards = []
            return
        self._cards = [
            Deck.Mahjong(rank, suit)
            for suit in Deck.suits
            for rank in Deck.ranks
            for ign in range(4)
        ]
        for wind in Deck.winds:
            for ign in range(4):
                self._cards.append(Deck.Mahjong(wind, "风"))
        for flower in Deck.flowers:
            self._cards.append(Deck.Mahjong(flower, "花"))

        if status is None:
            shuffle(self._cards)

    def __len__(self):
        return len(self._cards)

    def __getitem__(self, position):
        return self._cards[position]

    def __setitem__(self, key, value):
        self._cards[key] = value

    def empty(self):
        self._cards = []

    def push(self, value):
        self._cards.append(value)

    def pop(self, idx=None):
        if idx is None or idx != len(self._cards) - 1:
            return self._cards.pop()
        else:
            return self._cards.pop(idx)

    def show(self):
        for card in self._cards:
            print(card)


def deal_cards(deck, nums):
    result = []
    for ign in range(nums):
        result.append(Deck("empty"))
    for i in range(0, len(deck), nums):
        for j in range(nums):
            result[j].push(deck[i+j])
    return result


if __name__ == '__main__':
    PLAYER = 2
    deck = Deck()
    deck.show()
    # player = deal_cards(deck, PLAYER)
    table = Deck("empty")
    # for i in range(PLAYER):
    #     player[i].show()
    #     print("-" * 50)
    table.show()
