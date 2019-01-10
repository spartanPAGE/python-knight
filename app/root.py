from .core import scaffolding
from .core.scene import Scene
from .core.entity import Entity
import logging
import pygame
import random

class GravityBlock:
    def __init__(self, start_x, end_x, vel):
        self.x = start_x
        self.width = end_x - start_x
        self.height = 0
        self.vel = float(vel)

    def tick(self, ms):
        self.height += self.vel/10
        self.vel += ms/100

    def render(self, display):
        color = (0, 0, 0)
        rect = (self.x, 0, self.width, self.height)
        pygame.draw.rect(display, color, rect)
        
class FadeWithGravityBlocks:
    def __init__(self, width, height, count=200):
        sections = list(sorted([random.randint(0, width) for i in range(count-1)] + [width]))
        self.blocks = []
        prev = 0
        for section in sections:
            self.blocks.append(GravityBlock(prev, section, random.randint(4, 21)))
            prev = section
        print(self.blocks)

    def tick(self, ms, display):
        for block in self.blocks:
            block.tick(ms)
            block.render(display)
    
class MainScene(Scene):
    def __init__(self, game_vars):
        configs = [
            'res/scenes/main/config.json',
            'res/common/knight/config.json'
        ]
        super().__init__(name='MAIN', configs=configs, game_vars=game_vars)
        self.knight = self.entity('knight')
        self.game_started = False
        self.fade = FadeWithGravityBlocks(*game_vars['screen_mode'])

    def on_loop(self, ms):
        super().on_loop(ms)
        if self.game_started:
            self.fade.tick(ms, self.display)


    def knight_block_states(self):
        return ['knight block hold', 'knight block']

    def knight_busy_states(self):
        return self.knight_block_states() + ['knight attack']
        

    def on_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                self.start_game()
                
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

    def start_game(self):
        self.game_started = True
                

        
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
