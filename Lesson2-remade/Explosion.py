import pygame
from Env import *
from os import path
import random

ani_list=[]
class Explosion(pygame.sprite.Sprite):
    for i in range(0,9):
        ani_list.append(pygame.image.load(path.join(img_dir,"regularExplosion0%d.png"%i)))
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image=pygame.image.load(path.join(img_dir,"regularExplosion00.png"))
        self.rect=self.image.get_rect()
        self.rect.centerx=x
        self.rect.centery=y
        self.lastani=pygame.time.get_ticks()
        self.ani_delay=200
        self.ani_ind=0
    def update(self):
        now=pygame.time.get_ticks()
        if now-self.lastani>self.ani_delay:
            self.ani_ind+=1
            self.image=ani_list[random.randint(0,8)]
        if self.ani_ind>=8:
            self.kill()
    def play(self):
        pass