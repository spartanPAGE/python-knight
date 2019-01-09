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

        self.knightStrip = SpriteStripAnimation(
            'res/common/knight/idle.png', (0, 0, 4*42, 4*42), 4, loop=True, frames=game_vars['frames'], colorkey=-1
        )
        self.knight_pos = (850, 347)

        font = pygame.font.Font('res/fonts/joystix monospace.ttf', 40)
        self.text_image = text = font.render('Press any key to start...', True, (0, 0, 0))
        self.text_pos = (286, 152)

        self.display = game_vars['screen']


    def on_loop(self):
        knight_image = self.knightStrip.next()
        
        self.background.render(self.display, (0, 0))
        
        self.display.blit(knight_image, dest=self.knight_pos)

        self.display.blit(self.text_image, dest=self.text_pos)
        # special_flags=pygame.BLEND_RGBA_SUB
        

    def on_event(self, event):
        # logging.info(f'MainScene:on_event: {event}')
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
