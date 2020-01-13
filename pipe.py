import pygame
from pygame.locals import *
from resources import *
import random 

class Pipe(pygame.sprite.Sprite):
    """moves a clenched fist on the screen, following the mouse"""
    def __init__(self, offset=-10):
        pygame.sprite.Sprite.__init__(self)  # call Sprite initializer
        self.image, self.rect = load_image('pipe.png', -1)
        self.pipe_clearance = 300
        self.move_rate = 10
        self.screen = pygame.display.get_surface()
        self.set_center(offset)

    def update(self):
        """move the fist based on the mouse position"""
        self.rect = self.rect.move((-self.move_rate, 0))

        if self.rect.right < 0:
            self.set_center(0)
    
    def set_center(self, offset):
        x = self.screen.get_rect().right + offset
        y = random.randrange(self.pipe_clearance / 2,self.screen.get_rect().bottom - (self.pipe_clearance / 2))
        self.rect.center = x, y

    def collide(self, target):
        return hitbox.colliderect(target.rect)
