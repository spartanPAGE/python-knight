import sys
import pygame
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
    
    while game_vars['game_running'] and len(game_vars['scenes']) > 0:
        scene = game_vars['scenes'][-1]
        scene.on_loop()
        event_loop(scene, game_vars)

        if not scene.alive:
            game_vars['scenes'].pop()


def initialize_pygame():
    collected_variables = {}
    funcs = [
        init_logging,
        init_pygame,
        init_screen
    ]
    for f in funcs:
        collected_variables.update(f() or {})
    return collected_variables


def finalize():
    pygame.quit()
    logging.info('finalized: pygame')
