import os, sys
import pygame
from pygame.locals import *
import time
import random 

from bird import Bird
from pipe import Pipe

import neat
import visualize

if not pygame.font:
    print('Warning, fonts are disabled')

if not pygame.mixer:
    print('Warning, sounds are disabled')

MAX_BIRDS = 100
WIDTH = 1000
HEIGHT = 600

def run(config_file):
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_file)
    p = neat.Population(config)

    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    p.add_reporter(neat.Checkpointer(5))

    # Run for up to 1000 generations.
    winner = p.run(start, 1000)
    # Display the winning genome.
    print('\nBest genome:\n{!s}'.format(winner))

    node_names = {-1: 'Top Pipe Height', -2: 'Bottom Pipe Height', -
                  3: 'Top of Bird', -4: 'Distance to Pipe', 0: 'Flap'}
    visualize.draw_net(config, winner, True, node_names=node_names)
    visualize.plot_stats(stats, ylog=False, view=True)
    visualize.plot_species(stats, view=True)

    p = neat.Checkpointer.restore_checkpoint('neat-checkpoint-4')
    p.run(start, 10)

def start(genomes, config):
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("NEAT: Flappy Bird")
    pygame.mouse.set_visible(False)

    background = pygame.Surface(screen.get_size()).convert()
    background.fill((80, 250, 239))

    screen.blit(background, (0, 0))
    pygame.display.flip()

    pipe0 = Pipe()
    pipe1 = Pipe(500)

    all_sprites = pygame.sprite.Group()
    all_sprites.add(pipe0.top)
    all_sprites.add(pipe0.bottom)
    all_sprites.add(pipe1.top)
    all_sprites.add(pipe1.bottom)

    bird_list = []

    for index in range(MAX_BIRDS):
        bird_thing = Bird()
        bird_list.append(bird_thing)
        all_sprites.add(bird_thing)

    nets = []

    for genome_id, genome in genomes:
        nets.append(neat.nn.FeedForwardNetwork.create(genome, config))
        genome.fitness = 0

    clock = pygame.time.Clock()
    dead_count = 0
    start_time = int(round(time.time() * 1000))

    while True:
        if dead_count == MAX_BIRDS:
            return

        # for event in pygame.event.get():
        #     if event.type == QUIT:
        #         return
        #     elif event.type == KEYDOWN and event.key == K_ESCAPE:
        #         return
        #     elif event.type == KEYDOWN and event.key == K_SPACE: #and bird.alive:
        #         for index, bird in enumerate(bird_list):
        #             bird.clicked()

        #     elif event.type == KEYDOWN and event.key == K_r:
        #         for index in range(MAX_BIRDS):
        #             bird_thing = Bird(150, index * 5)
        #             bird_list.append(bird_thing)
        #             all_sprites.add(bird_thing)
        #         pipe0.set_center(0)
        #         pipe1.set_center(500)
        closest_pipe = pipe0
        if pipe0.get_dist() > pipe1.get_dist() and pipe1.get_dist() > 100:
            closest_pipe = pipe1

        for index, bird in enumerate(bird_list):
            output = 0
            try:
                # print((closest_pipe.get_top(), closest_pipe.get_bottom(), closest_pipe.get_dist(), bird.get_height()))
                input = ((closest_pipe.get_top() - bird.get_top())/HEIGHT, (bird.get_bottom() - closest_pipe.get_bottom())/HEIGHT, (closest_pipe.get_dist() - bird.get_right())/WIDTH, (bird.get_vert_speed())/HEIGHT)
                output = nets[index].activate(input)
                output = output[0]

            except Exception:
                pass

            if output >= 0.5:
                bird.clicked()

            if bird.to_be_killed or pipe0.collide(bird) or pipe1.collide(bird):
                bird.kill()
                bird_list.remove(bird)
                all_sprites.remove(bird)
                try:
                    del nets[index]
                except Exception:
                    pass
                dead_count += 1
                genomes[index][1].fitness = (bird.time_of_death - start_time)
        
        if pipe0.top.check_offscreen():
            pipe0.set_center()
        
        if pipe1.top.check_offscreen():
            pipe1.set_center()

        all_sprites.update()
        screen.blit(background, (0, 0))
        all_sprites.draw(screen)
        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'neat.config')
    run(config_path)
    print("Finished")