import sys
import pygame
from pygame.locals import Color
import logging

def init_logging(stream=sys.stdout, level=logging.DEBUG, format='%(asctime)s %(message)s'):
    logging.basicConfig(stream=stream, level=level, format=format)
    logging.info(f'initialized: logging | stream={stream} | level={level} | format={format}'.replace('|', '\n\t->'))


def init_pygame():
    pygame.init()
    logging.info('initialized: pygame')


def init_screen(mode = (640*2, 480*2)):
    screen = pygame.display.set_mode(mode)
    logging.info(f'initialized: screen display {mode}')
    return {'screen': screen}


def event_loop(scene, game_vars):
    for event in pygame.event.get():
        scene.on_event(event)
        if event.type == pygame.QUIT:
            game_vars['game_running'] = False


def loop(game_vars):
    logging.info('initialized: game loop')
    game_vars['game_running'] = True
    
    black = Color('black')
    clock = pygame.time.Clock()
    game_vars['clock'] = clock
    screen = game_vars['screen']
    ms = 0
    while game_vars['game_running'] and len(game_vars['scenes']) > 0:
        screen.fill(black)
    
        scene = game_vars['scenes'][-1]
        scene.on_loop(ms)
        event_loop(scene, game_vars)

        if not scene.alive:
            game_vars['scenes'].pop()

        pygame.display.flip()
        ms = clock.tick(game_vars['FPS'])
        game_vars['ms']=ms


def initialize_pygame(screen_mode=(640*2, 480*2)):
    collected_variables = {
        'screen_mode': screen_mode
    }
    res = [
        init_logging(),
        init_pygame(),
        init_screen(mode=screen_mode)
    ]
    for r in res:
        collected_variables.update(r or {})
    return collected_variables


def finalize():
    pygame.quit()
    logging.info('finalized: pygame')
