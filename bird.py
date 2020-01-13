import pygame
from pygame.locals import *
from resources import *

class Bird(pygame.sprite.Sprite):
    """moves a monkey critter across the screen. it can spin the
       monkey when it is punched."""
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)  # call Sprite intializer
        self.image, self.rect = load_image('bird.png', -1)
        self.original = self.image
        screen = pygame.display.get_surface()
        self.area = screen.get_rect()
        self.rect.topleft = 150, 50
        
        self.start_speed = 5
        self.fly_max = 15
        self.angle = 12
        self.jump_speed = -10
        self.gravity = 0.5

        self.vert_speed = self.start_speed
        self.alive = True
    
    def restart(self):
        self.rect.topleft = 150, 50
        self.vert_speed = self.start_speed
        self.alive = True

    def kill(self):
        self.alive = False

    def update(self):
        if not self.area.contains(self.rect) and self.rect.top > 0:
            self.kill()
        
        self._fall()

    def _fall(self):
        """move the monkey across the screen, and turn at the ends"""
        self.rect = self.rect.move((0, self.vert_speed))
        self.image = pygame.transform.rotate(self.original, -self.vert_speed)
        self.rect = self.image.get_rect(center=self.rect.center)
        self.vert_speed += self.gravity

    def clicked(self):
        """this will cause the monkey to start spinning"""
        self.vert_speed = self.jump_speed