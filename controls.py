import pygame,sys
from pygame.locals import*


pygame.init()

    
while True:
    for event in pygame.event.get():
        if event.type==QUIT:
            pygame.quit()
            sys.exit()
        if event.type==pygame.KEYDOWN:
            if event.key==pygame.K_UP:
                y=y+1
            if event.key==pygame.K_DOWN:
                y=y-1 
            if event.key==pygame.K_LEFT:
                x=x-1
            if event.key==pygame.K_RIGHT:
                x=x+1
            if event.key==pygame.K_ESCAPE:
                pygame.quit()
            if event.key==pygame.K_SPACE:
                pass
        