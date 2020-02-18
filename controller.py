

import random
import numpy as np
from scipy.signal import convolve2d

from abc import ABC, abstractmethod


class Controller(ABC):


	def __init__(self, name):
		self.name = name


	@abstractmethod
	def make_move(self, board, active_player):
		NotImplementedError()



class PlayerController(Controller):


	def make_move(self, board, active_player):

		valid = False

		while not valid:
			try:
				inp = int(input())
				assert 0 < inp < 8
				valid = True
				
			except Exception as e:
				print("Invalid Input, try again.", e)

		return inp - 1

		
class RandomController(Controller):


	def make_move(self, board, active_player):
		return random.randrange(0, 7)


class AIController(Controller):

	def make_move(self, board, active_player):
		max_value = -100
		best_column = 0

		for row, column in self.valid_moves(board, active_player):

			new_board = np.copy(board)
			new_board[row, column] = active_player

			value = self.min_max(new_board, active_player, active_player*(-1), 2)
			if value > max_value:
				max_value = value
				best_column = column

		return best_column

	def valid_moves(self, board, active_player):
		for column in range(7):
			(column_values,) = np.where(board[:,column] == 0)
			
			if not len(column_values):
				continue

			row = column_values[-1]
			yield (row, column)

	def evaluate_board(self, board, player):

		evaluation = 0

		kernel = [
			np.array([[1, 1, 1, 1]], dtype=np.int8),
			np.array([[1], [1], [1], [1]], dtype=np.int8),
			np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]], dtype=np.int8),
			np.array([[0, 0, 0, 1], [0, 0, 1, 0], [0, 1, 0, 0], [1, 0, 0, 0]], dtype=np.int8)
		]

		for k in kernel:

			convolusion = convolve2d(board, k, mode="valid")
			# Check for winning position
			if np.any(convolusion == 4 * player):
			    return 100
			# Check for losing position
			elif np.any(convolusion == -4 * player):
			    return -100
			# Check for double attack

			# Check for seven
		
		evaluation = 5 * np.sum(board == player)

		return evaluation

	def search_board_for_pattern(self, board, pattern):
		pass

	def min_max(self, board, player, active_player, depth):
		print(depth)
		if not depth:
			return self.evaluate_board(board, player)
		
		min_max = 0

		for row, column in self.valid_moves(board,active_player):

			new_board = np.copy(board)
			new_board[row, column] = active_player

			evaluation = self.min_max(new_board, player, active_player*(-1), depth-1)
			if player == active_player:
				min_max = max(evaluation, min_max)
			else:
				min_max = min(evaluation, min_max)

		return min_max


