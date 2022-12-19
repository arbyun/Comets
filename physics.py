from main import *
from sprites import *
from button import *
import pygame
import time
import random

# gravity

gravity = -4


def explode(projectile, enemyhit):
    if enemyhit is None:
        return
    else:
        enemyhit.alive = False
    animation = Animation(projectile.y, projectile.x)
    return animation.play()


def shoot(x, y):
    # create new projectile at x, y
    projectile = Projectiles(x, y)
    # make it shoot straight ahead
    collider = pygame.sprite.spritecollide(projectile, enemies, False)
    projectile.y += 1
    if projectile.y >= 900:
        explode(projectile, None)
    if collider:
        enemyhit = collider[0].name
        explode(projectile, enemyhit)


def spawn_enemies(quantity, spawntimer):
    for quantity in range(quantity):
        x = random.randrange(1, 800)
        y = random.randrange(1, 600)
        newenemy = Comets(x, y)
        time.sleep(spawntimer)
        return newenemy


def gameOver():
    global run
    run = False
    show_scores_onscreen()


def title_screen():
    screen.fill(black)
    for entity in all_sprites:
        entity.kill()
    title = font.render('Comets', True, blue)
    textRect = title.get_rect()
    textRect.center = (600 // 2, 900 // 2)
    screen.blit(title, textRect)
    pygame.display.update()
    if pygame.K_KP_ENTER:
        screen.fill(black)
        startbtn_txt = font.render('start', True, blue)
        quitbtn_txt = font.render('quit', True, blue)
        rectstartbtn = startbtn_txt.get_rect()
        rectquitbtn = quitbtn_txt.get_rect()
        startbtn = Button(10, 30, 500, 400, red, None)
        quitbtn = Button(10, 30, 500, 400, red, None)
        rectstartbtn.center = (10 // 2, 30 // 2)
        rectquitbtn.center = (10 // 2, 30 // 2)
        screen.blit(startbtn)
        screen.blit(startbtn_txt, rectstartbtn)
        screen.blit(quitbtn)
        screen.blit(quitbtn_txt, rectquitbtn)
        if startbtn.pressed:
            if startbtn.released:
                screen.fill(black)
                global run
                run = True
        if quitbtn.pressed:
            if quitbtn.released:
                pygame.quit()


if run:
    for i in enemies:
        i.gravity()
    colliding = pygame.sprite.spritecollide(player, enemies, False)
    if colliding:
        gameOver()
    elif not colliding:
        pass

if not run:
    show_scores_onscreen()
    time.sleep(6)
    title_screen()
