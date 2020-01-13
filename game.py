import os, sys
import pygame
from pygame.locals import *

from bird import Bird
from pipe import Pipe

if not pygame.font:
    print('Warning, fonts are disabled')

if not pygame.mixer:
    print('Warning, sounds are disabled')

def start():
    pygame.init()
    screen = pygame.display.set_mode((1000, 600))
    pygame.display.set_caption("FlAppI")
    pygame.mouse.set_visible(False)

    background = pygame.Surface(screen.get_size()).convert()
    background.fill((80, 250, 239))

    screen.blit(background, (0, 0))
    pygame.display.flip()

    bird = Bird()
    # pipe = Pipe()
    all_sprites = pygame.sprite.RenderPlain((bird))
    clock = pygame.time.Clock()

    while True:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == QUIT:
                return
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                return
            elif event.type == KEYDOWN and event.key == K_SPACE:
                bird.clicked()
            

        all_sprites.update()

        screen.blit(background, (0, 0))
        all_sprites.draw(screen)
        pygame.display.flip()

if __name__ == "__main__":
    start()
    print("Finished")