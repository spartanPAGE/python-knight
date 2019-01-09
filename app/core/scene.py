from enum import Enum, auto

class OnSceneDeath(Enum):
    POP=auto(),
    QUIT=auto()

class Scene:
    def __init__(self, on_death=OnSceneDeath.POP):
        self.alive = True
        self.on_death = on_death
