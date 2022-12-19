from sprites import *
from physics import *
from pygame_configs import *
import pygame
import leaderboard

'''''''''
'OBJECTS'
'''''''''

player = Player(400, 300)


class Difficulty:
    def level(self):
        if self == 1:
            enes = spawn_enemies(1, 0)
            enemy_list = pygame.sprite.Group()  # create enemy group
            enemy_list.add(enes)  # add enemy to group
            return enemy_list


def show_scores_onscreen():
    text = font.render(leaderboard.scores, False, white)
    screen.blit(text, (600, 900))


while True:
    pygame.init()
    font = pygame.font.SysFont(None, 15)
