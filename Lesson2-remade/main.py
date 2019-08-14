import random
from os import path

import pygame

# TODO Refactor 將參數統一放到另外一個檔案
from Env import *

img_dir = path.join(path.dirname(__file__), 'img')
sound_dir = path.join(path.dirname(__file__), 'sound')
font_name = pygame.font.match_font('arial')
pygame.init()
pygame.mixer.init()
pygame.mixer.music.load(path.join(sound_dir, "bgm.mp3"))
pygame.mixer.music.play(-1)

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

    def update(self):
        self.keyEventHandling()

    def keyEventHandling(self):
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            player.move(-self.speedx, 0)
        if keystate[pygame.K_RIGHT]:
            player.move(self.speedx, 0)
        
        if keystate[pygame.K_UP]:
            player.move(0,-self.speedy)
        if keystate[pygame.K_DOWN]:
            player.move(0,self.speedy)

    def move(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy


class Meteor(pygame.sprite.Sprite):
    def __init__(self):
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

    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        old_center=self.rect.center
        self.angle=self.angle+self.rot_angle
        self.image=pygame.transform.rotate(self.image_origin,self.angle)
        self.rect=self.image.get_rect()
        self.rect.center=old_center
        if (self.rect.y > HEIGHT):
            newMeteor()
            self.kill()


class Bullet(pygame.sprite.Sprite):
    speedy=10
    def __init__(self, posx, posy):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load(path.join(img_dir, "laser_gun.png"))
        self.rect = self.image.get_rect()
        self.rect.centerx = posx
        self.rect.centery = posy
        #self.speedy = 10

    def update(self):
        self.rect.y -= self.speedy
        if self.rect.bottom < 0:
            self.kill()


def newMeteor():
    global all_sprites
    m = Meteor()
    meteors.add(m)
    all_sprites.add(m)


screen = pygame.display.set_mode((WIDTH, HEIGHT))
bg = pygame.image.load(path.join(img_dir,'background.png'))
bg_rect = bg.get_rect()
clock = pygame.time.Clock()

meteors = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
bullets = pygame.sprite.Group()
supports=pygame.sprite.Group()

last_shot = pygame.time.get_ticks()
now = 0
score = 0
player = Player(WIDTH / 2, HEIGHT - 50)

for i in range(8):
    newMeteor()

all_sprites.add(bullets)
all_sprites.add(player)
all_sprites.add(meteors)
running = True
sound_pew = pygame.mixer.Sound(path.join(sound_dir, "pew.wav"))
#live=pygame.image.load(path.join(img_dir,"playerShip1_orange.png"))
live=3
def draw_lives():
    global live
    img_live = pygame.transform.scale(player.image,(30,20))
    if player.shield<=0:
        live-=1
        if live!=0:
            player.shield=100
    for i in range(live):
        live_rect = img_live.get_rect()
        live_rect.x = 700+25*i
        live_rect.y = 10
        screen.blit(img_live,live_rect)
def draw_shield():
    shield_bar=pygame.rect.Rect(10,10,player.shield,10)
    outline=pygame.rect.Rect(10,10,100,10)
    pygame.draw.rect(screen,GREEN,shield_bar)
    pygame.draw.rect(screen,(255,255,255),outline,2)
def check_meteor_hit_player():
    global running, meteors
    hits = pygame.sprite.spritecollide(player, meteors, False,pygame.sprite.collide_circle_ratio(0.7))
    if hits:
        for hit in hits:
            hit.kill()
            # print("check_meteor_hit_player"        )
            newMeteor()
            
            player.shield-=hit.size
            #print(player.shield)
            #if player.shield<=0:
            #    running = False
weapon=False
weapon_time=0
def check_player_hit_supports():
    global running, supports,score,weapon,weapon_time
    hits = pygame.sprite.spritecollide(player,supports, False,pygame.sprite.collide_circle_ratio(0.7))
    if hits:
        for hit in hits:
            hit.kill()
            if hit.type==0:
                weapon=True
                weapon_time=pygame.time.get_ticks()
                Bullet.speedy=100
            elif hit.type==1:
                player.shield+=5
                if player.shield>100:
                    player.shield=100
            # print("check_meteor_hit_player")
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
class Support(pygame.sprite.Sprite):
    def __init__(self,x, y, type):
        pygame.sprite.Sprite.__init__(self)
        if type==0:
            self.image =pygame.image.load(path.join(img_dir,"enemyBlue1.png"))
        else:
            self.image =pygame.image.load(path.join(img_dir,"shield_silver.png"))
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        self.speedy = 8
        self.type=type
    
    def update(self):
        self.rect.centery = self.rect.centery + self.speedy
        if self.rect.centery>HEIGHT:
            self.kill()
def check_bullets_hit_meteor():
    global  score
    hits = pygame.sprite.groupcollide(meteors,bullets, True, True,pygame.sprite.collide_circle_ratio(1))
    if hits:
        for hit in hits:
            hit.kill()
            score += (hit.size)*2
            
            # print("check_bullets_hit_meteor")
            newMeteor()
            explosion=Explosion(hit.rect.centerx,hit.rect.centery)
            all_sprites.add(explosion)
            type=random.randint(0,1)
            support=Support(hit.rect.centerx,hit.rect.centery,type)
            supports.add(support)
            all_sprites.add(supports)

def draw_score():
    font = pygame.font.Font(font_name, 14)
    text_surface = font.render(str(score), True, YELLOW)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (WIDTH/2, 20)
    screen.blit(text_surface, text_rect)
    pass


def shoot():
    sound_pew.play()
    bullet = Bullet(player.rect.centerx, player.rect.centery)
    bullets.add(bullet)
    all_sprites.add(bullet)
def shoot2():
    sound_pew.play()
    bullet = Bullet(player.rect.centerx, player.rect.centery)
    bullets.add(bullet)
    all_sprites.add(bullet)
    bullet2 = Bullet(player.rect.centerx+20, player.rect.centery)
    all_sprites.add(bullet2)
gamestate="begin"
def show_text(text,x,y,size):
    font=pygame.font.Font(font_name,size)
    text=font.render(text,True,YELLOW)
    screen.blit(text,(x,y))
def show_begin_screen():
    show_text("SHUMP!",250,150,100)
    show_text("Arrow keys move. Space to Fire",230,300,30)
    show_text("Press Space to begin.",320,400,20)
while running:
    # clocks control how fast the loop will execute
    clock.tick(FPS)
    # event trigger
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    if gamestate=="begin":
        #show_begin_screen()
        keystate=pygame.key.get_pressed()
        if keystate[pygame.K_SPACE]:
            gamestate="start"
        else:
            show_begin_screen()
    elif gamestate=="start":
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_SPACE]:
            now=pygame.time.get_ticks()
            if now-last_shot>SHOT_DELAY:
                if weapon==False:
                    shoot()
                    last_shot=now
                else:
                    if pygame.time.get_ticks()-weapon_time<=10000:
                        shoot2()
                        last_shot=now
                    else:
                        weapon=False
                        Bullet.speedy=10
        if live==0:
            gamestate="begin"
            


        # update the state of sprites
        check_meteor_hit_player()
        #
        check_bullets_hit_meteor()
        check_player_hit_supports()

        all_sprites.update()

        # draw on screen

        # screen.fill(BLACK)
        screen.blit(bg,bg_rect)
        draw_score()
        draw_shield()
        draw_lives()
        
        all_sprites.draw(screen)
        # flip to display
    pygame.display.flip()

pygame.quit()
