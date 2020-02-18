

import random

from abc import ABC, abstractmethod


class Controller(ABC):


    def __init__(self, name):
        self.name = name


    @abstractmethod
    def make_move(self, board, apl):
        NotImplementedError()



class PlayerController(Controller):


    def make_move(self, board, apl):

        valid = False

        while not valid:
            try:
                inp = int(input())
                assert 0 < inp < 7
            except:
                print("Invalid Input, try again.")

        return inp - 1

        
class RandomController(Controller):


    def make_move(self, board, apl):
        return random.randrange(0, 7)
