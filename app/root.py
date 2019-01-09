from .core import scaffolding
from .core.scene import Scene
import logging

class MainScene(Scene):
    def __init__(self, game_vars):
        super().__init__(name='MAIN', game_vars=game_vars)


    def on_loop(self):
        pass

    def on_event(self):
        pass
        

def initialize_scenes(scenes=[]):
    logging.info(f'initialized: scenes {[scene.name for scene in scenes]}')
    return {'scenes': scenes}


def run():
    game_vars = scaffolding.initialize_pygame()
    
    scenes = [MainScene(game_vars=game_vars)]
    
    game_vars.update(initialize_scenes(scenes))
    
    scaffolding.loop(game_vars)
    scaffolding.finalize()
