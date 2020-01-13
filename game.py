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
    pipe0 = Pipe()
    pipe1 = Pipe(500)
    all_sprites = pygame.sprite.RenderPlain((bird, pipe0.top, pipe0.bottom, pipe1.top, pipe1.bottom))
    clock = pygame.time.Clock()

    while True:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == QUIT:
                return
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                return
            elif event.type == KEYDOWN and event.key == K_SPACE and bird.alive:
                bird.clicked()
            elif event.type == KEYDOWN and event.key == K_r:
                bird.restart()
                pipe0.set_center(0)
                pipe1.set_center(500)
        
        if pipe0.collide(bird) or pipe1.collide(bird):
            bird.alive = False
        
        if pipe0.top.check_offscreen():
            pipe0.set_center()
        
        if pipe1.top.check_offscreen():
            pipe1.set_center()

        all_sprites.update()
        screen.blit(background, (0, 0))
        all_sprites.draw(screen)
        pygame.display.flip()

if __name__ == "__main__":
    start()
    print("Finished")