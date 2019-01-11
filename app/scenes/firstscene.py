from app.core import scaffolding
from app.core.scene import Scene
from app.core.entity import Entity
from app.core.scenefade import FadeWithGravityBlocks
import logging
import pygame

class Knight:
    def __init__(self, scene):
        self.me = scene.entity('knight')
        self.scene = scene
        self.moving = False
        self.dirs = [0, 0]

    @property
    def speed(self):
        return self.me.internal['speed']

    def is_moving(self):
        return self.moving

    @property
    def pos(self):
        return self.me.internal['pos']


    @pos.setter
    def pos(self, val):
        self.me.internal['pos'] = val


    def on_loop(self, ms):
        if self.is_moving():
            speed = [a*b*ms/100 for a,b in zip(self.dirs, self.speed)]
            self.pos = [a+b for a,b in zip(self.pos, speed)]
        pass

    def start_moving(self, axis, turn):
        logging.info('knight:moving:set: True')
        self.me.push_state('knight walk')
        self.dirs[axis] = turn
        self.moving = True

    def stop_moving(self):
        if self.is_moving() and 'knight walk' in self.me.internal['states_stack']:
            logging.info('knight:moving:set: False')
            self.me.remove_state('knight walk')
            
        self.moving = False


    def event_based_movement(self, event):  
        if self.moving and event.type ==pygame.KEYUP:
            if event.key in [pygame.K_RIGHT, pygame.K_LEFT]:
                self.stop_moving()
        
        if not self.is_busy():
            if event.type == pygame.KEYDOWN:
                if not self.moving:
                    if event.key == pygame.K_RIGHT:
                        self.start_moving(0, 1)
                        
                    if event.key == pygame.K_LEFT:
                        self.start_moving(0, -1)


    def event_based_death(self, event):
        if event.type == pygame.KEYDOWN:
            
            if event.key == pygame.K_q:
                self.scene.die()

            if event.key == pygame.K_k:
                # TODO: last frame is dislocated, don't know why; gotta investigate
                self.me.die()


    def event_based_busy_actions(self, event):
        if event.type == pygame.KEYDOWN:
            if not self.me.state() in self.busy_states():
                if event.key == pygame.K_SPACE:
                    self.me.push_state_if_alive('knight attack')

                if event.key == pygame.K_a:
                    self.stop_moving()
                    [self.me.push_state_if_alive(state)
                     for state in self.block_states()]

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                while self.me.state() in self.block_states():
                    self.me.pop_state()


    def on_event(self, event):
        self.event_based_movement(event)
        self.event_based_death(event)
        self.event_based_busy_actions(event)
                        


    def block_states(self):
        return ['knight block hold', 'knight block']


    def busy_states(self):
        return self.block_states() + ['knight attack']


    def is_busy(self):
        return self.me.state() in self.busy_states()



class FirstScene(Scene):
    def __init__(self, game_vars):
        configs = [
            'res/scenes/first/config.json',
            'res/common/knight/config.json'
        ]
        super().__init__(name='MAIN', configs=configs, game_vars=game_vars)
        self.knight = Knight(self)


    def on_loop(self, ms):
        super().on_loop(ms)
        self.knight.on_loop(ms)
        

    def on_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            print(event)

        self.knight.on_event(event)

        
