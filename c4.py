

import random
import numpy as np
from scipy.signal import convolve2d

from controller import PlayerController, RandomController



class C4Game:


    def __init__(self, player1instance, player2instance):
        
        # values of board:
        # 0 -> nothing
        # 1 -> player 1
        # -1 -> player 2
        self.board = np.zeros((7,6))

        # apl := active player
        self.apl = random.choice([1, -1])

        assert isinstance(player1instance, Controller) and isinstance(player2instance, Controller)

        # indeices to match (-1, 0, 1) for board values
        self.players = [None, player1instance, player2instance]


    def pprint(self):
        for r in self.board:
            print( *[" XO"[val] for val in r] )



def main():
    PlayerController()


if __name__ == "__main__":
    main()