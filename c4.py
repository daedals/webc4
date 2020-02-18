

import random

import numpy as np

from scipy.signal import convolve2d




class C4Game:


    def __init__(self, player1instance, player2instance):
        
        # values of board:
        # 0 -> nothing
        # 1 -> player 1
        # -1 -> player 2
        self.board = np.zeros((7,6))

        # apl := active player
        self.apl = random.choice([1, -1])


    def pprint(self):
        pass