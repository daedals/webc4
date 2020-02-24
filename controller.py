

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
		NotImplementedError()

	def valid_moves(self, board, active_player):

		for column in [3, 2, 4, 1, 5, 0, 6]:
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

			convolution = convolve2d(board, k, mode="valid")
			# Check for winning position
			if np.any(convolution == 4 * player):
				return 100
			# Check for losing position
			elif np.any(convolution == -4 * player):
				return -100

		return 0


	def evaluate_board(self, board, player):

		# on finished game return immediately
		evaluation = 0
		
		kernel = [
			# horizontal
			np.array([
				[1, 1, 1, 1]
				], dtype=np.int8),
			# vertical
			np.array([
				[1], 
				[1], 
				[1], 
				[1]
				], dtype=np.int8),
			# diagonal
			np.array([
				[1, 0, 0, 0], 
				[0, 1, 0, 0], 
				[0, 0, 1, 0], 
				[0, 0, 0, 1]
				], dtype=np.int8),
			# diagonal
			np.array([
				[0, 0, 0, 1], 
				[0, 0, 1, 0], 
				[0, 1, 0, 0], 
				[1, 0, 0, 0]
				], dtype=np.int8)
		]

		# position_values = np.repeat(np.arange(6, dtype=np.int8)[:,np.newaxis], 7, axis=1)

		for k in kernel:

			convolution = convolve2d(board, k, mode="valid")
			
			# Check for winning position
			if np.any(convolution == 4 * player):
				return 100
			# Check for losing position
			elif np.any(convolution == -4 * player):
				return -100
			
			if np.any(abs(convolution) == 3):

				position_values = np.repeat(np.arange(5, convolution.shape[0]+5, dtype=np.int8)[:,np.newaxis], convolution.shape[1], axis=1)

				evaluation += 5 * np.sum(position_values[convolution == (3 * player)])
				evaluation -= 5 * np.sum(position_values[convolution == (-3 * player)])


		position_values = np.array([
			[1, 1, 1, 1, 1, 1, 1],
			[1, 1, 1, 1, 1, 1, 1],
			[1, 1, 1, 2, 1, 1, 1],
			[1, 1, 1, 3, 1, 1, 1],
			[1, 1, 2, 5, 2, 1, 1],
			[1, 1, 3, 9, 3, 1, 1],
		], dtype=np.int8)
		
		# check how many own pieces are in the middle row
		evaluation += np.sum(np.multiply(board, position_values))

		return evaluation




class MinMaxAIController(AIController):
	

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

			print(f"Column {column+1} was valued at {value}.")

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


class AlphaBetaAIController(AIController):


	def make_move(self, board, active_player):

		start_time = time_ns()
		max_value = -200
		best_column = None

		# check how many moves are left and adapt depth
		depth = min(6, np.sum(board == 0)) 

		for row, column in self.valid_moves(board, active_player):

			new_board = np.copy(board)
			new_board[row, column] = active_player

			value = self.a_b_prune(new_board, active_player, active_player*(-1), depth, -200, 200)
			if value > max_value:
				max_value = value
				best_column = column

			print(f"Column {column+1} was valued at {value}.")

		delta_time = time_ns() - start_time
		print(f"Choose Column {best_column+1} within {delta_time/10**9:.2f}s")
		return best_column


	def a_b_prune(self, board, player, active_player, depth, alpha, beta):

		# at maximum depth, return board evaluation
		if not depth:
			return self.evaluate_board(board, player)

		# if at any time any parties win is imminent, return immediately
		early_win = self.check_win_condition(board, player)
		if early_win:
			return early_win

		# set comparison value in dependence of whose turn it is
		if player == active_player:
			min_max = alpha
		else:
			min_max = beta

		# get all possible moves
		for row, column in self.valid_moves(board,active_player):

			# create new board with current move updated
			new_board = np.copy(board)
			new_board[row, column] = active_player

			# proceed a_b_pruning by checking local alpha or beta value
			if player == active_player:
				evaluation = self.a_b_prune(new_board, player, active_player*(-1), depth-1, min_max, beta)
				min_max = max(evaluation, min_max)
				if min_max >= beta:
					return min_max

			else:
				evaluation = self.a_b_prune(new_board, player, active_player*(-1), depth-1, alpha, min_max)
				min_max = min(evaluation, min_max)
				if min_max <= alpha:
					return min_max

		return min_max


def main():
	pass

if __name__ == "__main__":
	main()