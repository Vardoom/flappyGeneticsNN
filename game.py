import utils
from background import Background
from bird import Bird
from pipe import Pipe

import pygame
from pygame.locals import *

from itertools import cycle
import random
import sys


class Game:
    def __init__(self, fps_clock, screen, images, sounds, hit_masks):

        self.FPS_CLOCK = fps_clock
        self.SCREEN = screen
        self.IMAGES = images
        self.SOUNDS = sounds
        self.HIT_MASKS = hit_masks

        self.next_pipe_x = -1
        self.next_pipe_hole_y = -1

        background = Background()
        bird = Bird()
        pipe = Pipe()

        # select random background sprites
        self.IMAGES['background'] = pygame.image.load(background.background_name).convert()

        # select random player sprites
        im = list()
        for bird_name in bird.bird_name_list:
            im.append(pygame.image.load(bird_name).convert_alpha())
        self.IMAGES['bird'] = tuple(im)

        # select random pipe sprites
        self.IMAGES['pipe'] = (
            pygame.transform.rotate(pygame.image.load(pipe.pipe_name).convert_alpha(), 180),
            pygame.image.load(pipe.pipe_name).convert_alpha(),
        )

        # hitmask for pipes
        self.HIT_MASKS['pipe'] = (
            self.get_hit_mask(self.IMAGES['pipe'][0]),
            self.get_hit_mask(self.IMAGES['pipe'][1]),
        )

        # hitmask for bird
        self.HIT_MASKS['bird'] = (
            self.get_hit_mask(self.IMAGES['bird'][0]),
            self.get_hit_mask(self.IMAGES['bird'][1]),
            self.get_hit_mask(self.IMAGES['bird'][2]),
        )

    def show_welcome_animation(self):
        return {
            'playerY': int((utils.SCREEN_HEIGHT - self.IMAGES['bird'][0].get_height()) / 2),
            'baseX': 0,
            'playerIndexGen': cycle([0, 1, 2, 1]),
        }

    def get_random_pipe(self):
        """returns a randomly generated pipe"""
        # y of gap between upper and lower pipe
        gap_y = random.randrange(0, int(utils.BASE_Y * 0.6 - utils.PIPE_GAP_SIZE))
        gap_y += int(utils.BASE_Y * 0.2)
        pipe_height = self.IMAGES['pipe'][0].get_height()
        pipe_x = utils.SCREEN_WIDTH + 10

        return [{'x': pipe_x, 'y': gap_y - pipe_height},  # upper pipe
                {'x': pipe_x, 'y': gap_y + utils.PIPE_GAP_SIZE},  # lower pipe
                ]

    def show_score(self, score):
        """displays score in center of screen"""
        score_digits = [int(x) for x in list(str(score))]
        total_width = 0  # total width of all numbers to be printed

        for digit in score_digits:
            total_width += self.IMAGES['numbers'][digit].get_width()

        x_offset = (utils.SCREEN_WIDTH - total_width) / 2

        for digit in score_digits:
            self.SCREEN.blit(self.IMAGES['numbers'][digit], (x_offset, utils.SCREEN_HEIGHT * 0.1))
            x_offset += self.IMAGES['numbers'][digit].get_width()

    def check_crash(self, players, upper_pipes, lower_pipes, agent):
        """returns True if bird collided with base or pipes."""
        statuses = []
        for idx in range(agent.n_population):
            statuses.append(False)

        for idx in range(agent.n_population):
            statuses[idx] = False
            pi = players['index']
            players['w'] = self.IMAGES['bird'][0].get_width()
            players['h'] = self.IMAGES['bird'][0].get_height()
            # if player crashes into ground
            if players['y'][idx] + players['h'] >= utils.BASE_Y - 1:
                statuses[idx] = True
            player_rect = pygame.Rect(players['x'][idx], players['y'][idx], players['w'], players['h'])
            pipe_w = self.IMAGES['pipe'][0].get_width()
            pipe_h = self.IMAGES['pipe'][0].get_height()

            for uPipe, lPipe in zip(upper_pipes, lower_pipes):
                # upper and lower pipe rects
                u_pipe_rect = pygame.Rect(uPipe['x'], uPipe['y'], pipe_w, pipe_h)
                l_pipe_rect = pygame.Rect(lPipe['x'], lPipe['y'], pipe_w, pipe_h)

                # player and upper/lower pipe hitmasks
                p_hit_mask = self.HIT_MASKS['bird'][pi]
                u_hit_mask = self.HIT_MASKS['pipe'][0]
                l_hit_mask = self.HIT_MASKS['pipe'][1]

                # if bird collided with upipe or lpipe
                u_collide = self.pixel_collision(player_rect, u_pipe_rect, p_hit_mask, u_hit_mask)
                l_collide = self.pixel_collision(player_rect, l_pipe_rect, p_hit_mask, l_hit_mask)

                if u_collide or l_collide:
                    statuses[idx] = True
        return statuses

    def main_game(self, movement_info, agent):
        score = player_index = loop_iter = 0
        player_index_gen = movement_info['playerIndexGen']
        players_x_list = []
        players_y_list = []

        for idx in range(agent.n_population):
            player_x, player_y = int(utils.SCREEN_WIDTH * 0.2), movement_info['playerY']
            players_x_list.append(player_x)
            players_y_list.append(player_y)
        base_x = movement_info['baseX']
        base_shift = self.IMAGES['base'].get_width() - self.IMAGES['background'].get_width()

        # get 2 new pipes to add to upperPipes lowerPipes list
        new_pipe_1 = self.get_random_pipe()
        new_pipe_2 = self.get_random_pipe()

        # list of upper pipes
        upper_pipes = [
            {'x': utils.SCREEN_WIDTH + 200, 'y': new_pipe_1[0]['y']},
            {'x': utils.SCREEN_WIDTH + 200 + (utils.SCREEN_WIDTH / 2), 'y': new_pipe_2[0]['y']},
        ]

        # list of lower pipes
        lower_pipes = [
            {'x': utils.SCREEN_WIDTH + 200, 'y': new_pipe_1[1]['y']},
            {'x': utils.SCREEN_WIDTH + 200 + (utils.SCREEN_WIDTH / 2), 'y': new_pipe_2[1]['y']},
        ]

        self.next_pipe_x = lower_pipes[0]['x']
        self.next_pipe_hole_y = (lower_pipes[0]['y'] + (upper_pipes[0]['y'] + self.IMAGES['pipe'][0].get_height())) / 2

        pipe_vel_x = utils.PIPE_VEL_X

        # player velocity, max velocity, downward acceleration, acceleration on flap
        players_vel_y = []  # player's velocity along Y, default same as playerFlapped
        player_max_vel_y = utils.BIRD_MAX_VEL_Y  # max vel along Y, max descend speed
        player_min_vel_y = utils.BIRD_MIN_VEL_Y  # min vel along Y, max ascend speed
        players_acc_y = []  # players downward acceleration
        player_flap_acc = utils.BIRD_FLAP_ACC  # players speed on flapping
        players_flapped = []  # True when player flaps
        players_state = []

        for idx in range(agent.n_population):
            players_vel_y.append(-9)
            players_acc_y.append(1)
            players_flapped.append(False)
            players_state.append(True)

        alive_players = agent.n_population

        while True:
            for idxPlayer in range(agent.n_population):
                if players_y_list[idxPlayer] < 0 and players_state[idxPlayer]:
                    alive_players -= 1
                    players_state[idxPlayer] = False
            if alive_players == 0:
                return {
                    'y': 0,
                    'groundCrash': True,
                    'baseX': base_x,
                    'upperPipes': upper_pipes,
                    'lowerPipes': lower_pipes,
                    'score': score,
                    'playerVelY': 0,
                }
            for idxPlayer in range(agent.n_population):
                if players_state[idxPlayer]:
                    agent.fitness_score[idxPlayer] += 1
            self.next_pipe_x += pipe_vel_x
            for idxPlayer in range(agent.n_population):
                if players_state[idxPlayer]:
                    action = agent.predict_action(players_y_list[idxPlayer], self.next_pipe_x,
                                                  self.next_pipe_hole_y, idxPlayer)
                    if action == 1:
                        if players_y_list[idxPlayer] > -2 * self.IMAGES['bird'][0].get_height():
                            players_vel_y[idxPlayer] = player_flap_acc
                            players_flapped[idxPlayer] = True
                            # SOUNDS['wing'].play()
            for event in pygame.event.get():
                if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                    pygame.quit()
                    sys.exit()
                """
                if (event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP)):
                    if playery > -2 * IMAGES['player'][0].get_height():
                        playerVelY = playerFlapAcc
                        playerFlapped = True
                        SOUNDS['wing'].play()
                """

            # check for crash here, returns status list
            param = {'x': players_x_list, 'y': players_y_list, 'index': player_index}
            crash_test = self.check_crash(param, upper_pipes, lower_pipes, agent)

            for idx in range(agent.n_population):
                if players_state[idx] and crash_test[idx]:
                    alive_players -= 1
                    players_state[idx] = False
            if alive_players == 0:
                return {
                    'y': movement_info['playerY'],
                    'groundCrash': crash_test[1],
                    'baseX': base_x,
                    'upperPipes': upper_pipes,
                    'lowerPipes': lower_pipes,
                    'score': score,
                    'playerVelY': 0,
                }

            # check for score
            for idx in range(agent.n_population):
                if players_state[idx]:
                    pipe_idx = 0
                    playerMidPos = players_x_list[idx]
                    for pipe in upper_pipes:
                        pipeMidPos = pipe['x'] + self.IMAGES['pipe'][0].get_width()
                        if pipeMidPos <= playerMidPos < pipeMidPos + 4:
                            self.next_pipe_x = lower_pipes[pipe_idx + 1]['x']
                            self.next_pipe_hole_y = (lower_pipes[pipe_idx + 1]['y'] + (
                                upper_pipes[pipe_idx + 1]['y'] + self.IMAGES['pipe'][pipe_idx + 1].get_height())) / 2
                            score += 1
                            agent.fitness_score[idx] += 25
                            # SOUNDS['point'].play()
                        pipe_idx += 1

            # playerIndex basex change
            if (loop_iter + 1) % 3 == 0:
                playerIndex = next(player_index_gen)
            loop_iter = (loop_iter + 1) % 30
            base_x = -((-base_x + 100) % base_shift)

            # player's movement
            for idx in range(agent.n_population):
                if players_state[idx]:
                    if players_vel_y[idx] < player_max_vel_y and not players_flapped[idx]:
                        players_vel_y[idx] += players_acc_y[idx]
                    if players_flapped[idx]:
                        players_flapped[idx] = False
                    player_height = self.IMAGES['bird'][player_index].get_height()
                    players_y_list[idx] += min(players_vel_y[idx], utils.BASE_Y - players_y_list[idx] - player_height)

            # move pipes to left
            for uPipe, lPipe in zip(upper_pipes, lower_pipes):
                uPipe['x'] += pipe_vel_x
                lPipe['x'] += pipe_vel_x

            # add new pipe when first pipe is about to touch left of screen
            if 0 < upper_pipes[0]['x'] < 5:
                new_pipe = self.get_random_pipe()
                upper_pipes.append(new_pipe[0])
                lower_pipes.append(new_pipe[1])

            # remove first pipe if its out of the screen
            if upper_pipes[0]['x'] < -self.IMAGES['pipe'][0].get_width():
                upper_pipes.pop(0)
                lower_pipes.pop(0)

            # draw sprites
            self.SCREEN.blit(self.IMAGES['background'], (0, 0))

            for uPipe, lPipe in zip(upper_pipes, lower_pipes):
                self.SCREEN.blit(self.IMAGES['pipe'][0], (uPipe['x'], uPipe['y']))
                self.SCREEN.blit(self.IMAGES['pipe'][1], (lPipe['x'], lPipe['y']))

            self.SCREEN.blit(self.IMAGES['base'], (base_x, utils.BASE_Y))

            # print score so player overlaps the score
            self.show_score(score)

            for idx in range(agent.n_population):
                if players_state[idx]:
                    self.SCREEN.blit(self.IMAGES['bird'][player_index], (players_x_list[idx], players_y_list[idx]))

            pygame.display.update()
            self.FPS_CLOCK.tick(utils.FPS)

    @staticmethod
    def get_hit_mask(image):
        """returns a hitmask using an image's alpha."""
        mask = []
        for x in range(image.get_width()):
            mask.append([])
            for y in range(image.get_height()):
                mask[x].append(bool(image.get_at((x, y))[3]))
        return mask

    @staticmethod
    def pixel_collision(rect1, rect2, hit_mask_1, hit_mask_2):
        """Checks if two objects collide and not just their rects"""
        rect = rect1.clip(rect2)

        if rect.width == 0 or rect.height == 0:
            return False

        x1, y1 = rect.x - rect1.x, rect.y - rect1.y
        x2, y2 = rect.x - rect2.x, rect.y - rect2.y

        for x in range(rect.width):
            for y in range(rect.height):
                if hit_mask_1[x1 + x][y1 + y] and hit_mask_2[x2 + x][y2 + y]:
                    return True
        return False
