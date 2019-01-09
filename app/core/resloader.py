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
        loop=obj['loop'], frames=frames, colorkey=obj['colorkey']
    )


def load_mp3(obj, **options):
    pass


def load_font(obj, **options):
    return pygame.font.Font(obj['path'], obj['size'])

def load_text(obj, d, **options):
    return d['fonts'][obj['font']]['res'].render(
        obj['text'], True, obj['color']
    )
    

def load_scene_config(config_path, frames):
    loaders = {
        "gif": load_gif,
        "sprite_strip_animation": load_sprite_strip_animation,
        "mp3": load_mp3,
        "ttf": load_font,
        "text": load_text
    }
    
    logging.info(f'loading config: {config_path}')
    
    with open(config_path) as json_data:
        d = json.load(json_data)
        if 'fonts' in d:
            for key in d['fonts'].keys():
                font = d['fonts'][key];
                loader_func = loaders[font['type']]
                font['res'] = loader_func(font)
            
        if 'background' in d:
            bg = d['background']
            loader_func = loaders[bg['type']]
            bg['res'] = loader_func(bg)

        if 'sprites' in d:
            for key in d['sprites'].keys():
                sprite = d['sprites'][key]
                loader_func = loaders[sprite['type']]
                sprite['res'] = loader_func(sprite, frames=frames, d=d)
            
        return d
