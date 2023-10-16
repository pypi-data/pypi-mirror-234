import ipdb
import random

class Score():
	def __init__(self):
		self.score_dic = {'AAA': 0, 'A': 0, 'B': 0, 'C': 0, 'D': 0, 'E': 0}

	def alpha(self, score):
		# ipdb.set_trace()
		match score:
			case x if x < 0 or x > 100 or x % 1 != 0:
				print(f"您输入的成绩 {x} 不合理，请检查后重新输入。")
				return
			case x if 98 <= x <= 100:
				alpha = 'AAA'
			case x if 90 <= x <= 97:
				alpha = 'A'
			case x if 80 <= x <= 89:
				alpha = 'B'
			case x if 70 <= x <= 79:
				alpha = 'C'
			case x if 60 <= x <= 69:
				alpha = 'D'
			case _:
				alpha = 'E'
		self.score_dic[alpha] += 1

	def show(self):
	    for _ in self.score_dic.keys():
	        print(f"{_}: {self.score_dic[_]}")

def main():
	score = Score()
	for _ in range(10):
		r = random.randrange(101)
		score.alpha(r)
	score.alpha(10.2)
	score.alpha(-10)
	score.show()

if __name__ == "__main__":
	main()

'''score'''
# import score_lib

# score_lib.main()
