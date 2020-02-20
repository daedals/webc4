

import random
import numpy as np
from scipy.signal import convolve2d

from abc import ABC, abstractmethod

from time import time_ns


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

		start_time = time_ns()
		max_value = -200
		best_column = None

		# check how many moves are left and adapt depth
		depth = min(4, np.sum(board == 0)) 

		for row, column in self.valid_moves(board, active_player):

			new_board = np.copy(board)
			new_board[row, column] = active_player

			value = self.min_max(new_board, active_player, active_player*(-1), depth)
			if value > max_value:
				max_value = value
				best_column = column

			# print(f"Column {column+1} was valued at {value}.")

		delta_time = time_ns() - start_time
		print(f"Choose Column {best_column+1} within {delta_time/10**9:.2f}s")
		return best_column


	def min_max(self, board, player, active_player, depth):

		# at maximum depth, return board evaluation
		if not depth:
			return self.evaluate_board(board, player)

		# if at any time any parties win is imminent, return immediately
		early_win = self.check_win_condition(board, player)
		if early_win:
			return early_win

		# set comparison value in dependence of whose turn it is
		min_max = 101 * (1,-1)[player == active_player]

		# get all possible moves
		for row, column in self.valid_moves(board,active_player):

			# create new board with current move updated
			new_board = np.copy(board)
			new_board[row, column] = active_player

			evaluation = self.min_max(new_board, player, active_player*(-1), depth-1)

			if player == active_player:
				min_max = max(evaluation, min_max)
			else:
				min_max = min(evaluation, min_max)

		return min_max


	def valid_moves(self, board, active_player):

		for column in range(7):
			(column_values,) = np.where(board[:,column] == 0)
			
			if not len(column_values):
				continue

			row = column_values[-1]
			yield (row, column)


	def check_win_condition(self, board, player):

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

		return 0


	def evaluate_board(self, board, player):

		# on finished game return immediately
		evaluation = self.check_win_condition(board, player)

		if evaluation:
			return evaluation
		
		# check for threats, namely 3 out of 4 are one color, the 4th is empty
		kernel = [
			np.array([[1, 1, 1, 1]], dtype=np.int8),
			np.array([[1], [1], [1], [1]], dtype=np.int8),
			np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]], dtype=np.int8),
			np.array([[0, 0, 0, 1], [0, 0, 1, 0], [0, 1, 0, 0], [1, 0, 0, 0]], dtype=np.int8)
		]

		for k in kernel:

			convolusion = convolve2d(board, k, mode="valid")
			
			if np.any(abs(convolusion) == 3):
				evaluation += 5 * np.sum(convolusion == 3 * player)
				evaluation -= 5 * np.sum(convolusion == -3 * player)

		
		# check how many own pieces are in the middle row
		evaluation += 3 * np.sum(board[:,3] == player)

		return evaluation


	def search_board_for_pattern(self, board, pattern):
		pass
