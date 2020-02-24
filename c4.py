

import random
import numpy as np
from scipy.signal import convolve2d

from controller import *

class Color:
	blue = '\033[94m'
	red = '\033[91m'
	white = '\033[0m'


class C4Game:


	def __init__(self, player1instance, player2instance):
		
		# values of board:
		# 0 -> nothing
		# 1 -> player 1
		# -1 -> player 2
		self.board = np.zeros((6, 7), dtype=np.int8)

		# active_player := active player
		self.active_player = random.choice([1, -1])

		assert isinstance(player1instance, Controller) and isinstance(player2instance, Controller)

		# indices to match (-1, 0, 1) for board values
		self.players = [None, player1instance, player2instance]

		# track turn number
		self.turn = 0


	def pprint(self):
		"""
		pretty print the board
		"""

		w = 7
		print( "╓─" + (w-1) * "──┬─" + "──╖" )
		for row in self.board:
			print( "║", " │ ".join([" XO"[col] for col in row]), "║" )
			print( "╟─" + (w-1) * "──┼─" + "──╢" )

		print("║", " │ ".join([str(i+1) for i in range(w)]), "║")
		print( "╙─" + (w-1) * "──┴─" + "──╜" )


	def do_turn(self):

		valid = False

		while not valid:
			try:
				column = self.players[self.active_player].make_move(self.board, self.active_player)

				assert isinstance(column, int), "Input type check failed."
				assert 0 <= column <= 6, "Boundary check failed."

				(column_values,) = np.where(self.board[:,column] == 0)

				assert len(column_values), "Supplied Column is already occupied."

				row = column_values[-1]

				self.board[row, column] = self.active_player

				self.pprint()

				valid = True

			except AssertionError as e:
				print(e)


	def game_loop(self):

		while True:

			print(f"{self.players[self.active_player].name} ({'.XO'[self.active_player]}) has to move.")

			self.do_turn()
			self.turn += 1

			if self.check_win_condition():
				print(f"{self.players[self.active_player].name} ({'.XO'[self.active_player]}) won the game!")
				break

			if self.turn > 41:
				print("It was a Tie!")
				break

			self.active_player *= -1


	def check_win_condition(self):
		
		kernel = [
			np.array([[1, 1, 1, 1]], dtype=np.int8),
			np.array([[1], [1], [1], [1]], dtype=np.int8),
			np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]], dtype=np.int8),
			np.array([[0, 0, 0, 1], [0, 0, 1, 0], [0, 1, 0, 0], [1, 0, 0, 0]], dtype=np.int8)
		]

		for k in kernel:

			convolusion = convolve2d(self.board, k, mode="valid")

			if np.any(abs(convolusion) == 4):
				return True

		return False
			


def main():

	c4 = C4Game(AlphaBetaAIController("ABP"), MinMaxAIController("MM"))

	c4.game_loop()


if __name__ == "__main__":
	main()