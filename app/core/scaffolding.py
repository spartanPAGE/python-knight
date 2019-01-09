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


def event_loop(game_vars):
    for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_vars['game_running'] = False


def loop(game_vars):
    logging.info('initialized: game loop')
    game_vars['game_running'] = True
    while game_vars['game_running']:
        event_loop(game_vars)


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
