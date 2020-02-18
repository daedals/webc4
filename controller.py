

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
        return input()

        
class RandomController(Controller):


    def make_move(self, board, apl):
        return random.randrange(0, 7)
