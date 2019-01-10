from app.core import scaffolding
from app.core.scene import Scene
from app.core.entity import Entity
from app.core.scenefade import FadeWithGravityBlocks
import logging
import pygame

class FirstScene(Scene):
    def __init__(self, game_vars):
        configs = [
            'res/scenes/first/config.json',
            'res/common/knight/config.json'
        ]
        super().__init__(name='MAIN', configs=configs, game_vars=game_vars)
        self.knight = self.entity('knight')


    def on_loop(self, ms):
        super().on_loop(ms)


    def knight_block_states(self):
        return ['knight block hold', 'knight block']


    def knight_busy_states(self):
        return self.knight_block_states() + ['knight attack']
        

    def on_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            print(event)
        pass
