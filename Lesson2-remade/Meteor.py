import pygame
from os import path
from Env import *
import random

class Meteor(pygame.sprite.Sprite):
    def __init__(self,meteors,all):
        pygame.sprite.Sprite.__init__(self)
        self.size = random.randrange(3, 8)
        image = pygame.image.load(path.join(img_dir, "meteor.png"))
        self.image = pygame.transform.scale(image, (self.size * 8, self.size * 8))

        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(0, WIDTH)
        self.rect.y = 0
        self.speedx = random.randint(-5, 5)
        self.speedy = random.randint(7, 15)
        self.image_origin=self.image
        self.rot_angle=5
        self.angle=0
        self.group=meteors
        self.all_sprites=all

    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        old_center=self.rect.center
        self.angle=self.angle+self.rot_angle
        self.image=pygame.transform.rotate(self.image_origin,self.angle)
        self.rect=self.image.get_rect()
        self.rect.center=old_center
        if (self.rect.y > HEIGHT):
            self.newMeteor()
            self.kill()


    def newMeteor(self):
        #global all_sprites
        m = Meteor(self.group,self.all_sprites)
        self.group.add(m)
        self.all_sprites.add(m)    