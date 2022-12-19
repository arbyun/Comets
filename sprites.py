import random
from pygame_configs import *
import pygame
import sys
import os

colors = [red, blue, black, white, yellow]
randomcolor = random.choice(colors)

projectiles = pygame.sprite.Group()
enemies = pygame.sprite.Group()

all_sprites = pygame.sprite.Group()


class Comets(pygame.sprite.Sprite):
    def __init__(self, y, x):
        pygame.sprite.Sprite.__init__(self)
        enemies.add(self)
        all_sprites.add(self)
        self.image = pygame.draw.circle(screen, randomcolor, [x, y], 10, 0)
        self.rect = self.image
        self.y = y
        self.x = x
        self.alive = True

        while not self.alive:
            self.kill()

    def gravity(self):
        self.y -= 4


class Projectiles(pygame.sprite.Sprite):
    def __init__(self, y, x):
        pygame.sprite.Sprite.__init__(self)
        projectiles.add(self)
        all_sprites.add(self)
        self.image = pygame.draw.circle(screen, white, [x, y], 5, 0)
        self.rect = self.image
        self.y = y
        self.x = x


class Player(pygame.sprite.Sprite):
    def __init__(self, y, x):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.draw.circle(screen, red, [x, y], 30, 0)
        self.y = y
        self.x = x
        self.rect = self.image
        all_sprites.add(self)

    def control(self, y, x):
        self.x += x
        self.y += y

    def update(self):
        self.rect.x = self.rect.x + self.x
        self.rect.y = self.rect.y + self.y

        if self.rect.left > 600:
            self.rect.right = 0


class Animation(pygame.sprite.Sprite):
    def __init__(self, y, x):
        pygame.sprite.Sprite.__init__(self)
        self.y = y
        self.x = x
        f1 = pygame.image.load()
        f2 = pygame.image.load()
        f3 = pygame.image.load()
        f4 = pygame.image.load()
        f5 = pygame.image.load()
        self.animation = [f1, f2, f3, f4, f5]
        self.image = self.animation[1]
        self.frame = 0
        self.animation_timer = 0  # animation timer
        self.animation_delay = 100
        all_sprites.add(self)

    def play(self):
        if pygame.time.get_ticks() > self.animation_timer + self.animation_delay:
            self.animation_timer = pygame.time.get_ticks()
            self.frame = self.frame + 1

            if self.frame == 5:  # reset animation loop
                self.kill()

            self.image = self.animation[self.frame]
