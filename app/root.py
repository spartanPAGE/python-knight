from .core import scaffolding
from .core.scene import Scene
from .core.entity import Entity
import logging
import pygame

class MainScene(Scene):
    def __init__(self, game_vars):
        super().__init__(name='MAIN', config_path='res/scenes/main/config.json', game_vars=game_vars)
        self.knight = self.entity('knight')

    def on_loop(self, ms):
        super().on_loop(ms)
        

    def on_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.unicode == 'q':
                self.die()

            if event.unicode == ' ' and self.knight.is_alive():
                self.knight.push_state('knight attack')

            if event.unicode == 'k':
                self.knight.die()

        
def initialize_scenes(scenes=[]):
    logging.info(f'initialized: scenes {[scene.name for scene in scenes]}')
    return {'scenes': scenes}


def run():
    FPS = 120
    game_vars = scaffolding.initialize_pygame(screen_mode=(1344, 704))
    game_vars.update({
        'FPS': FPS,
        'frames': FPS / 12
    })
    
    scenes = [MainScene(game_vars=game_vars)]
    
    game_vars.update(initialize_scenes(scenes))
    
    scaffolding.loop(game_vars)
    scaffolding.finalize()
