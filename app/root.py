from .core import scaffolding
from .core.scene import Scene
from .core.gifimage import GIFImage
from .core.spritestripanimation import SpriteStripAnimation
import logging
import pygame
import os
import sys

class MainScene(Scene):
    def __init__(self, game_vars):
        super().__init__(name='MAIN', game_vars=game_vars)
        self.background = GIFImage('res/scenes/main/background.gif')
        pygame.mixer.music.load('res/scenes/main/March of the Templars.mp3')
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(game_vars['music_volume'])

        effect = pygame.mixer.Sound('res/common/wind/wind-looped.wav')
        effect.play(loops=-1)

        knightsStrip = SpriteStripAnimation(
            'res/common/knight/idle.png', (0, 0, 42, 42), 4, loop=True, frames=game_vars['frames']
        )

        self.display = game_vars['screen']


    def on_loop(self):
        self.background.render(self.display, (0, 0))
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
    FPS = 120
    game_vars = scaffolding.initialize_pygame(screen_mode=(1344, 704))
    game_vars.update({
        'music_volume': 0.5,
        'FPS': FPS,
        'frames': FPS / 12
    })
    
    scenes = [MainScene(game_vars=game_vars)]
    
    game_vars.update(initialize_scenes(scenes))
    
    scaffolding.loop(game_vars)
    scaffolding.finalize()
