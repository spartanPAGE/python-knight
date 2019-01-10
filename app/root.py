from .core import scaffolding
from .core.scene import Scene
from .core.entity import Entity
import logging
import pygame

class MainScene(Scene):
    def __init__(self, game_vars):
        configs = [
            'res/scenes/main/config.json',
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
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                self.die()

            if event.key == pygame.K_k:
                self.knight.die()

            if not self.knight.state() in self.knight_busy_states():
                
                if event.key == pygame.K_SPACE:
                    self.knight.push_state_if_alive('knight attack')

                if event.key == pygame.K_a:
                    [self.knight.push_state_if_alive(state)
                     for state in self.knight_block_states()]

        if event.type == pygame.KEYUP:
            
            if event.key == pygame.K_a:
                while self.knight.state() in self.knight_block_states():
                    self.knight.pop_state()
                

        
def initialize_scenes(scenes=[]):
    logging.info(f'initialized: scenes {[scene.name for scene in scenes]}')
    return {'scenes': scenes}


def run():
    FPS = 120
    game_vars = scaffolding.initialize_pygame(screen_mode=(1344, 704))
    game_vars.update({
        'FPS': FPS,
        'frames': FPS / 12
    })
    
    scenes = [MainScene(game_vars=game_vars)]
    
    game_vars.update(initialize_scenes(scenes))
    
    scaffolding.loop(game_vars)
    scaffolding.finalize()
