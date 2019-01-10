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
        self.vel += ms/70

    def render(self, display):
        color = (0, 0, 0)
        rect = (self.x, 0, self.width, self.height)
        pygame.draw.rect(display, color, rect)

    def is_done(self, dest_height):
        return self.height >= dest_height

        
class FadeWithGravityBlocks:
    def __init__(self, width, height, count=200):
        self.screen_height = height
        sections = list(sorted([random.randint(0, width) for i in range(count-1)] + [width]))
        self.blocks = []
        prev = 0
        for section in sections:
            self.blocks.append(GravityBlock(prev, section, random.randint(4, 21)))
            prev = section

    def tick(self, ms, display):
        for block in self.blocks:
            block.tick(ms)
            block.render(display)

    def is_done(self):
        return len(self.blocks) == \
               sum([
                   block.is_done(self.screen_height)
                    for block in self.blocks
                   ])
