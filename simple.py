import pygame,sys
import numpy as np
from pygame.locals import*

pygame.init

screen=pygame.display.set_mode((800,600))

a=50
p0=(screen.get_width()/2,screen.get_height()/2)
p1=(screen.get_width()/2+a,screen.get_height()/2+a)
p2=(screen.get_width()/2-a,screen.get_height()/2+a)

p10=(700,100)
p20=(750,105)
p30=(800,170)
p40=(750,270)

while True:
    for event in pygame.event.get():
        if event.type==QUIT:
            pygame.quit()
            sys.exit()
        if event.type==pygame.KEYDOWN:
            if event.key==pygame.K_UP:
                p0=np.add(p0,(0,-10))
                p1=np.add(p1,(0,-10))
                p2=np.add(p2,(0,-10))
            if event.key==pygame.K_DOWN:
                p0=np.add(p0,(0,10))
                p1=np.add(p1,(0,10))
                p2=np.add(p2,(0,10))
            if event.key==pygame.K_LEFT:
                p0=np.add(p0,(-10,0))
                p1=np.add(p1,(-10,0))
                p2=np.add(p2,(-10,0))
            if event.key==pygame.K_RIGHT:
                p0=np.add(p0,(10,0))
                p1=np.add(p1,(10,0))
                p2=np.add(p2,(10,0))
            if event.key==pygame.K_SPACE:
                pygame.draw.polygon(screen,(255,255,255),(p10,p20,p30,p40),1)
    
    pygame.draw.polygon(screen,(255,255,255), (p0,p1,p2),0)

    pygame.display.update()