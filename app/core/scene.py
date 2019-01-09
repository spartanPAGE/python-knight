from enum import Enum, auto
from abc import ABCMeta, abstractmethod

class OnSceneDeath(Enum):
    POP=auto()
    QUIT=auto()


class Scene(metaclass=ABCMeta):
    def __init__(self, name='UNNAMED', on_death=OnSceneDeath.POP, game_vars={}):
        self.alive = True
        self.name = name
        self.on_death = on_death
        self.game_vars = game_vars

    def die():
        self.alive = False

    @abstractmethod
    def on_loop(self):
        pass


    @abstractmethod
    def on_event(self, event):
        pass
