from enum import Enum, auto
from abc import ABCMeta, abstractmethod
from .resloader import load_scene_config
import pygame
import math

class OnSceneDeath(Enum):
    POP=auto()
    QUIT=auto()


class Scene(metaclass=ABCMeta):
    def __init__(self, name='UNNAMED', on_death=OnSceneDeath.POP, game_vars={}, config_path=None):
        self.alive = True
        self.name = name
        self.on_death = on_death
        self.game_vars = game_vars
        self.scene_config = load_scene_config(config_path, frames=game_vars['frames'])
        self.play_music()
        self.play_ambient_sounds()
        self.display = game_vars['screen']
        self.collected_ms = 0


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


    def die(self):
        self.alive = False


    def on_loop(self, ms):
        self.render_transformations(self.collected_ms)
        self.use_config()
        self.collected_ms += ms


    @abstractmethod
    def on_event(self, event):
        pass
