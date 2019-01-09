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
        super().__init__(name='MAIN', game_vars=game_vars)
        self.scene_config = load_scene_config('res/scenes/main/config.json', frames=game_vars['frames'])
        self.background = GIFImage('res/scenes/main/background.gif')
        pygame.mixer.music.load('res/scenes/main/March of the Templars.mp3')
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(game_vars['music_volume'])

        effect = pygame.mixer.Sound('res/common/wind/wind-looped.wav')
        effect.play(loops=-1)

        font = pygame.font.Font('res/fonts/joystix monospace.ttf', 40)
        self.text_image = text = font.render('Press any key to start...', True, (0, 0, 0))
        self.text_pos = (286, 152)

        self.collected_ms = 0

        self.display = game_vars['screen']


    def use_config(self):
        bg = self.scene_config['background']
        bg['res'].render(self.display, bg['pos'])

        for key in self.scene_config['sprites'].keys():
            sprite = self.scene_config['sprites'][key]
            if sprite['type'] == 'sprite_strip_animation':
                self.display.blit(sprite['res'].next(), dest=sprite['pos'])
            elif sprite['type'] == 'text':
                self.display.blit(sprite['res'], dest=sprite['pos'])


    def on_loop(self, ms):
        self.use_config()
        self.collected_ms += ms

        # text_dist = (self.text_pos[0], self.text_pos[1]+6*math.sin(self.collected_ms/1000))
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
