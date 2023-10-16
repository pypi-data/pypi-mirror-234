#
# @author Jason Q. Wu
# @create 2021-04-27 14:19
#
import collections
from random import *


class Deck:
    Card = collections.namedtuple("Card", ["suit", "rank"])
    suits = "草花 方块 红桃 黑桃".split()
    ranks = [str(n) for n in range(2, 11)] + list("JQKA")

    def __init__(self, rank=None, has_monster=True, decks=1):
        if rank == "empty":
            self._cards = []
            return
        if rank is None:
            self._cards = [
                Deck.Card(suit, rank)
                for suit in Deck.suits
                for rank in Deck.ranks
            ]
            if has_monster:
                self._cards.append(Deck.Card("小", "怪"))
                self._cards.append(Deck.Card("大", "怪"))
            if decks > 1:
                self._cards *= decks
            shuffle(self._cards)
        else:
            self._cards = [Deck.Card(None, r) for r in rank]

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
        if idx is None or idx >= len(self._cards) - 1:
            return self._cards.pop()
        else:
            return self._cards.pop(idx)

    def show(self):
        for card in self._cards:
            print(card)


class Lin:
    def __init__(self, file_name):
        self.file_name = file_name
        self.data = []

    def get_data(self):
        return self.data

    def set_data(self, data):
        self.data = data

    def read(self):
        with open(self.file_name, 'r', newline='', encoding="utf8") as file:
            self.data = file.readlines()

    def write(self):
        with open(self.file_name, 'w', newline='', encoding="utf8") as file:
            file.writelines(self.data)

    def show_data(self):
        print(self.data)


def card_value(card):
    rank_value = Deck.ranks.index(card.rank)
    suit_values = dict(spades=3, hearts=2, diamonds=1, clubs=0)
    return rank_value * len(suit_values) + suit_values[card.suit]


def deal_cards(deck, nums):
    result = []
    for ign in range(nums):
        result.append(Deck("empty"))
    for i in range(0, len(deck), nums):
        for j in range(nums):
            result[j].push(deck[i+j])
    return result


def in_table(table, card):
    result = [0, False]
    for i in range(len(table)):
        if card.rank == table[i].rank:
            result[0] = i
            result[1] = True
    return result


def backups():
    # People = collections.namedtuple("People", "name, age, like")
    # zhangsan = People(name="张三", age=22, like="在法律的边缘试探！")
    # print(zhangsan[1])
    # print(zhangsan.name)
    # zhangsan.name = "法外狂徒"

    # d = Lin("jason.lin")
    # d.read()
    # data = d.get_data()
    # data.append("sss\n")
    # d.set_data(data)
    # d.show_data()
    # d.write()
    # cfg = Config("lin.ini")

    # config = cfg.get_config()
    # config["Default"] = {
    #     "IP": "127.0.0.1",
    #     "port": 3000,
    #     "user": "root",
    #     "passwd": 123456
    # }

    # config["uat"] = {
    #     "IP": "192.168.1.101",
    #     "port": 3000,
    #     "user": "root",
    #     "passwd": 123456
    # }

    # cfg.set_config(config)
    # cfg.write_config()
    # print(cfg.file_name)
    # cfg.read_config()
    # cfg.show_config()
    deck = Deck()
    print(len(deck))
    print(deck[0])
    print(deck[-1])
    print(choice(deck))
    print(choice(deck))
    print(choice(deck))
    # deck.show()
    deck[13] = Deck.Card(suit="Clubs", rank="4")
    print(deck[13], choice(deck))
    # for card in sorted(deck, key=spades_high):
    #     print(card)
    # for card in deck:
    #     print(card)
    # for card in reversed(deck):
    #     print(card)
    # print(len(deck))
    print(Deck.Card("Hearts", 'Q') in deck)
    print(Deck.Card("Hearts", 'F') in deck)
    # for card in sorted(deck, key=card_value):
    #     print(card)


if __name__ == '__main__':
    PLAYER = 2
    # backups()
    player = [Deck([2, 4, 1, 2, 5, 6]), Deck([3, 1, 3, 5, 6, 4])]
    # deck = Deck(has_monster=True, decks=1)
    # player = deal_cards(deck, PLAYER)
    table = Deck("empty")
    for i in range(PLAYER):
        player[i].show()
        print("-" * 50)
    while len(player[0]) and len(player[1]):
        for i in range(PLAYER):
            temp = player[i].pop(0)
            # print(temp)
            idx, has_card = in_table(table, temp)
            # print(idx, has_card)
            if has_card:
                for j in range(idx, len(table)):
                    player[i].push(table.pop(j))
                # break
                player[i].push(temp)
                i -= 1
                continue
            else:
                table.push(temp)
        # str = input()
        # if str == '1':
        #     player[0].show()
        # if str == '2':
        #     player[1].show()
        # if str == 't':
        #     table.show()
        # if str == 'q':
        #     break
        for i in range(PLAYER):
            player[i].show()
            print(f"-{i}" * 50)
        table.show()
        print("-t" * 50)
        # for i in range(len(table)):
        #     if temp.rank == table[i].rank:
        #         pass

    for i in range(PLAYER):
        if len(player[i]) == 0:
            print(f"PLAYER {i+1} 赢了。")
        player[i].show()
        print("-" * 50)
    table.show()
