from .core import scaffolding
from .core.scene import Scene
from .core.gifimage import GIFImage
from .core.spritestripanimation import SpriteStripAnimation
from .core.resloader import load_scene_config
import logging
import pygame
import os
import sys
import math

class MainScene(Scene):
    def __init__(self, game_vars):
        super().__init__(name='MAIN', config_path='res/scenes/main/config.json', game_vars=game_vars)


    def on_loop(self, ms):
        super().on_loop(ms)
        

    def on_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.unicode == 'q':
                self.die()

            if event.unicode == ' ':
                self.scene_config['entities']['knight']['states_stack'].append('knight attack')

        
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
