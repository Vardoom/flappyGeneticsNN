import pygame
import sys
import numpy as np
import matplotlib.pyplot as plt

import utils
from agent import Agent
from game import Game


def main():
    pygame.init()
    FPS_CLOCK = pygame.time.Clock()
    SCREEN = pygame.display.set_mode((int(utils.SCREEN_WIDTH), int(utils.SCREEN_HEIGHT)))
    pygame.display.set_caption('Flappy Bird')

    n_population = utils.N_POPULATION
    n_generation = utils.N_GENERATION

    # image, sound and hitmask dicts
    IMAGES, SOUNDS, HIT_MASKS = {}, {}, {}

    # numbers sprites for score display
    IMAGES['numbers'] = (
        pygame.image.load('assets/sprites/0.png').convert_alpha(),
        pygame.image.load('assets/sprites/1.png').convert_alpha(),
        pygame.image.load('assets/sprites/2.png').convert_alpha(),
        pygame.image.load('assets/sprites/3.png').convert_alpha(),
        pygame.image.load('assets/sprites/4.png').convert_alpha(),
        pygame.image.load('assets/sprites/5.png').convert_alpha(),
        pygame.image.load('assets/sprites/6.png').convert_alpha(),
        pygame.image.load('assets/sprites/7.png').convert_alpha(),
        pygame.image.load('assets/sprites/8.png').convert_alpha(),
        pygame.image.load('assets/sprites/9.png').convert_alpha()
    )

    # game over sprite
    IMAGES['game_over'] = pygame.image.load('assets/sprites/gameover.png').convert_alpha()
    # message sprite for welcome screen
    IMAGES['message'] = pygame.image.load('assets/sprites/message.png').convert_alpha()
    # base (ground) sprite
    IMAGES['base'] = pygame.image.load('assets/sprites/base.png').convert_alpha()

    # sounds
    if 'win' in sys.platform:
        sound_ext = '.wav'
    else:
        sound_ext = '.ogg'

    SOUNDS['die'] = pygame.mixer.Sound('assets/audio/die' + sound_ext)
    SOUNDS['hit'] = pygame.mixer.Sound('assets/audio/hit' + sound_ext)
    SOUNDS['point'] = pygame.mixer.Sound('assets/audio/point' + sound_ext)
    SOUNDS['swoosh'] = pygame.mixer.Sound('assets/audio/swoosh' + sound_ext)
    SOUNDS['wing'] = pygame.mixer.Sound('assets/audio/wing' + sound_ext)

    generation = 0
    agent = Agent(generation, n_population)
    traveled_distance = np.zeros((n_generation, n_population))

    for idx_i in range(n_generation):
        print("Generation nb: {}".format(agent.generation))
        new_game = Game(FPS_CLOCK, SCREEN, IMAGES, SOUNDS, HIT_MASKS)
        movement_info = new_game.show_welcome_animation()
        crash_info = new_game.main_game(movement_info, agent)
        res = agent.genetic_breeding(method=0)
        for idx_j in range(n_population):
            traveled_distance[idx_i, idx_j] = res[idx_j]

    plt.figure()
    for idx in range(n_population):
        plt.plot(range(n_generation), traveled_distance[:, idx], 'ro')
    plt.show()


if __name__ == '__main__':
    main()
