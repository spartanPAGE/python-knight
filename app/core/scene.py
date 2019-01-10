from enum import Enum, auto
from abc import ABCMeta, abstractmethod
from .resloader import load_scene_config
from .entity import Entity
import pygame
import math

class OnSceneDeath(Enum):
    POP=auto()
    QUIT=auto()


def mergedicts(dict1, dict2):
    for k in set(dict1.keys()).union(dict2.keys()):
        if k in dict1 and k in dict2:
            if isinstance(dict1[k], dict) and isinstance(dict2[k], dict):
                yield (k, dict(mergedicts(dict1[k], dict2[k])))
            else:
                # If one of the values is not a dict, you can't continue merging it.
                # Value from second dict overrides one in first and we move on.
                yield (k, dict2[k])
                # Alternatively, replace this with exception raiser to alert you of value conflicts
        elif k in dict1:
            yield (k, dict1[k])
        else:
            yield (k, dict2[k])


def render_obj(obj, dest, display):
    if type(obj) is pygame.Surface:
        display.blit(obj, dest=dest)
    elif obj['type'] == 'sprite_strip_animation' \
    or obj['type'] == 'entity_sprite_strip_animation':
        display.blit(obj['res'].next(), dest=dest)
    elif obj['type'] == 'text':
        display.blit(obj['res'], dest=dest)
    elif obj['type'] == 'gif':
        obj['res'].render(display, dest)
        

class Scene(metaclass=ABCMeta):
    def __init__(self, name='UNNAMED', on_death=OnSceneDeath.POP, game_vars={}, configs=None):
        self.alive = True
        self.name = name
        self.on_death = on_death
        self.game_vars = game_vars
        self.display = game_vars['screen']
        self.collected_ms = 0
        
        self.scene_config = {}
        for config_path in configs:
            self.scene_config = dict(mergedicts(self.scene_config, load_scene_config(config_path, frames=game_vars['frames'])))
            
        self.play_music()
        self.play_ambient_sounds()


    def entity(self, name):
        return Entity(self.scene_config, name)


    def _render_obj(self, obj, dest):
        render_obj(obj, dest, self.display)


    def play_ambient_sounds(self):
        for ambient_sound in self.scene_config['ambient sounds']:
            ambient_sound['res'].play(loops=-1)


    def play_music(self):
        music = self.scene_config['music']
        pygame.mixer.music.load(music['path'])
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(music['volume'])

    def render_bg(self):
        bg = self.scene_config['background']
        self._render_obj(bg, bg['pos'])

        
    def render_sprites(self):
        for key in self.scene_config['sprites'].keys():
            sprite = self.scene_config['sprites'][key]

            if 'omit' in sprite \
            and sprite['omit'] == True \
            or sprite['type'] == 'entity_sprite_strip_animation':
                continue
                
            dest = sprite['dest'] if 'dest' in sprite else sprite['pos']
            self._render_obj(sprite, dest)


    def render_entities(self):
        for key in self.scene_config['entities'].keys():
            entity = self.scene_config['entities'][key]
            states_stack = entity['states_stack']
            try:
                sprite = self.scene_config['sprites'][states_stack[-1]]
                pos = entity['pos']
                dest = [pos[0], pos[1]]
                if 'align' in entity and 'middledown' in entity['align']:
                    sprite_size = sprite['res'].get_size()
                    dest[0] -= sprite_size[0]/2
                    dest[1] -= sprite_size[1]
                self._render_obj(sprite, dest)
            except StopIteration:
                if entity['alive']:
                    sprite_name = states_stack.pop()
                    sprite = self.scene_config['sprites'][sprite_name]
                    sprite['res'].iter()
                else:
                    state = entity['states_stack'][0]
                    sprite = self.scene_config['sprites'][state]
                    self._render_obj(sprite['res'].images[-1], entity['pos'])


    def use_config(self):
        self.render_bg()
        self.render_sprites()
        self.render_entities()


    def render_transformations(self, ms):
        if not 'render transformations' in self.scene_config:
            return
        
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
