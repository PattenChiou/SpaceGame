import pygame
from Env import *
from os import path
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        image = pygame.image.load(path.join(img_dir, "ship.png"))
        self.image = pygame.transform.scale(image, (50, 30))
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        self.speedx = 8
        self.speedy=8
        self.shield=100
        #self.ax=0
        #self.ay=0

    def update(self):
        self.keyEventHandling()

    def keyEventHandling(self):
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            #self.ax=-0.1
            self.move(-self.speedx, 0)
        if keystate[pygame.K_RIGHT]:
            self.move(self.speedx, 0)
            #self.ax=0.1
        if keystate[pygame.K_UP]:
            self.move(0,-self.speedy)
            #self.ay=-0.1
        if keystate[pygame.K_DOWN]:
            self.move(0,self.speedy)
            #self.ay=0.1
        #self.speedx+=self.ax
        #self.speedy+=self.ay
        #self.ax=0
        #self.ay=0
        #self.move(self.speedx,self.speedy)
    def move(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy
#player = Player(WIDTH / 2, HEIGHT - 50)