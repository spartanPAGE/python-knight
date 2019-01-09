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

def event_loop():
    pass

def loop(game_vars):
    logging.info('initialized: game loop')
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

def init():
    collected_variables = {}
    funcs = [
        init_logging,
        init_pygame,
        init_screen
    ]
    for f in funcs:
        collected_variables.update(f() or {})
    return collected_variables
    
def run():
    game_vars = {}
    game_vars.update(init())
    print(game_vars.keys())

    loop(game_vars)
