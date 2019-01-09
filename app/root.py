from .core import scaffolding
from .core.scene import Scene
import logging

class MainScene(Scene):
    def __init__(self):
        super().__init__('MAIN')
        

def initialize_scenes(scenes=[MainScene()]):
    logging.info(f'initialized: scenes {[scene.name for scene in scenes]}')
    return {'scenes': scenes}


def run():
    game_vars = scaffolding.initialize_pygame()
    game_vars.update(initialize_scenes())
    
    scaffolding.loop(game_vars)
    scaffolding.finalize()
