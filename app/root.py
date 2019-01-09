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
        self.play_music()
        self.play_ambient_sounds()

        self.collected_ms = 0
        self.display = game_vars['screen']


    def play_ambient_sounds(self):
        for ambient_sound in self.scene_config['ambient sounds']:
            ambient_sound['res'].play(loops=-1)


    def play_music(self):
        music = self.scene_config['music']
        pygame.mixer.music.load(music['path'])
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(music['volume'])


    def use_config(self):
        bg = self.scene_config['background']
        bg['res'].render(self.display, bg['pos'])

        for key in self.scene_config['sprites'].keys():
            sprite = self.scene_config['sprites'][key]
            dest = sprite['dest'] if 'dest' in sprite else sprite['pos']
            if sprite['type'] == 'sprite_strip_animation':
                self.display.blit(sprite['res'].next(), dest=dest)
            elif sprite['type'] == 'text':
                self.display.blit(sprite['res'], dest=dest)


    def render_transformations(self, ms):
        for transformation in self.scene_config['render transformations']:
            sprite = self.scene_config['sprites'][transformation['sprite']]
            for action in transformation['actions']:
                exec(action)

    def on_loop(self, ms):
        self.render_transformations(self.collected_ms)
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
