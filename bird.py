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
        
        self.true_gravity = 5
        self.fly_max = 30
        self.angle = 12

        self.gravity = self.true_gravity
        self.fly = False
        self.fly_count = 0
        self.alive = True

    def update(self):
        if not self.area.contains(self.rect) and self.rect.top > 0:
            self.alive = False
        else:
            if self.fly:
                self._fly()
            else:
                self._fall()

    def _fall(self):
        """move the monkey across the screen, and turn at the ends"""
        self.rect = self.rect.move((0, self.gravity))
        self.image = pygame.transform.rotate(self.original, -self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)
        self.gravity += 0.1

    def _fly(self):
        self.fly_count += 1
        self.gravity -= 0.05

        self.rect = self.rect.move((0, -self.gravity))
        self.image = pygame.transform.rotate(self.original, self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)

        if self.fly_count >= self.fly_max:
            self.fly_count = 0
            self.fly = False
            self.gravity = self.true_gravity

    def clicked(self):
        """this will cause the monkey to start spinning"""
        if not self.fly:
            self.fly = True
            self.fly_count = 0
            self.gravity = self.true_gravity