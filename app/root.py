from .core import scaffolding
from .core.scene import Scene
from .core.gifimage import GIFImage
import logging
import pygame
import os
import sys

class MainScene(Scene):
    def __init__(self, game_vars):
        super().__init__(name='MAIN', game_vars=game_vars)
        self.background = GIFImage('res/scenes/main/background.gif')
        self.display = game_vars['screen']

    def on_loop(self):
        self.background.render(self.display, (0, 0))
        pygame.display.flip()
        pass

    def on_event(self, event):
        logging.info(f'MainScene:on_event: {event}')
        if event.type == pygame.KEYDOWN:
            if event.unicode == 'q':
                self.die()
        

def initialize_scenes(scenes=[]):
    logging.info(f'initialized: scenes {[scene.name for scene in scenes]}')
    return {'scenes': scenes}


def run():
    game_vars = scaffolding.initialize_pygame(screen_mode=(1344, 704))
    
    scenes = [MainScene(game_vars=game_vars)]
    
    game_vars.update(initialize_scenes(scenes))
    
    scaffolding.loop(game_vars)
    scaffolding.finalize()
