from main import player
from physics import *
import pygame

if pygame.KEYDOWN:
    if pygame.K_UP:
        player.y += 1
    elif pygame.K_DOWN:
        player.y -= 1
    elif pygame.K_LEFT:
        player.x -= 1
    elif pygame.K_RIGHT:
        player.x += 1
    elif pygame.K_ESCAPE:
        pygame.quit()
    elif pygame.K_SPACE:
        shoot(player.x, player.y)
