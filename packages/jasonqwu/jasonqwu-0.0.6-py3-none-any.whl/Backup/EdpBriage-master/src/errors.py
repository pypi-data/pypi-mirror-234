#-*- coding:utf-8 -*-

class CardAppendError(ValueError):
	def __init__(self):
		super(CardAppendError, self).__init__('Can not add, must be a "Card" object to add.')


class CardSpilloverError(ValueError):
	def __init__(self):
		super(CardSpilloverError, self).__init__('Can not add, can only have 13 cards.')


class CardRankError(ValueError):
	def __init__(self):
		super(CardRankError, self).__init__('Illega value, the value must be str and in "2 3 4 5 6 7 8 9 10 J Q K A".')


class CardSuitError(ValueError):
	def __init__(self):
		super(CardSuitError, self).__init__('Illega value, the value must be str and  in "S H D C".')
