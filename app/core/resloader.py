from .gifimage import GIFImage
from .spritestripanimation import SpriteStripAnimation
import logging
import pygame
import os
import sys
import math
import json


def load_gif(obj, **options):
    return GIFImage(obj['path'])


def load_sprite_strip_animation(obj, frames, **options):
    return SpriteStripAnimation(
        filename=obj['path'], rect=obj['rect'], count=obj['count'],
        loop=obj['loop'], frames=obj['frames'] or frames, colorkey=obj['colorkey']
    )


def load_mp3(obj, **options):
    pass


def load_wav(obj, **options):
    return pygame.mixer.Sound(obj['path'])


def load_font(obj, **options):
    return pygame.font.Font(obj['path'], obj['size'])


def load_text(obj, d, **options):
    return d['fonts'][obj['font']]['res'].render(
        obj['text'], True, obj['color']
    )


def _load_res(d, loaders, frames, obj):
    loader_func = loaders[obj['type']]
    obj['res'] = loader_func(obj, frames=frames, d=d)
    

def load_scene_config(config_path, frames):
    loaders = {
        "gif": load_gif,
        "sprite_strip_animation": load_sprite_strip_animation,
        "entity_sprite_strip_animation": load_sprite_strip_animation,
        "mp3": load_mp3,
        "ttf": load_font,
        "text": load_text,
        "wav": load_wav
    }
    
    logging.info(f'loading config: {config_path}')
    
    with open(config_path) as json_data:
        d = json.load(json_data)

        def load_res(obj):
            _load_res(d, loaders, frames, obj)
            
        if 'fonts' in d:
            for key in d['fonts'].keys():
                load_res(d['fonts'][key])
            
        if 'background' in d:
            load_res(d['background'])

        if 'ambient sounds' in d:
            for ambient_sound in d['ambient sounds']:
                load_res(ambient_sound)

        if 'sprites' in d:
            for key in d['sprites'].keys():
                load_res(d['sprites'][key])
            
        return d
