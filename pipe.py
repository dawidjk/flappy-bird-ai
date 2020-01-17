import pygame
from pygame.locals import *
from resources import *
import random 

class Pipe():
    """moves a clenched fist on the screen, following the mouse"""
    def __init__(self, offset=0):
        self.move_rate = 10
        self.top = PipeHalf('pipe_top.png', self.move_rate)
        self.bottom = PipeHalf('pipe_bottom.png', self.move_rate)
        self.pipe_clearance = 200
        self.screen = pygame.display.get_surface()
        self.set_center(offset)
    
    def set_center(self, offset = 0):
        x = self.screen.get_rect().right + offset
        y = random.randrange(self.pipe_clearance,self.screen.get_rect().bottom - self.pipe_clearance)
        self.top.rect.bottomleft = (x, y - self.pipe_clearance / 2)
        self.bottom.rect.topleft = (x, y + self.pipe_clearance / 2)

    def collide(self, target):
        return self.top.collide(target) or self.bottom.collide(target)
    
    def get_bottom(self):
        return self.bottom.rect.top
    
    def get_top(self):
        return self.top.rect.bottom

    def get_dist(self):
        return self.top.rect.left

class PipeHalf(pygame.sprite.Sprite):
    def __init__(self, name, move_rate):
        pygame.sprite.Sprite.__init__(self)  # call Sprite initializer
        self.image, self.rect = load_image(name, -1)
        self.move_rate = move_rate
    
    def set_center(self, x, y):
        self.rect.center = x, y
    
    def collide(self, target):
        hitbox = self.rect.inflate(0, 0)
        return hitbox.colliderect(target.rect)
    
    def check_offscreen(self):
        return self.rect.right < 0
    
    def update(self):
        self.rect = self.rect.move((-self.move_rate, 0))
