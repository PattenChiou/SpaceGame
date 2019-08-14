import pygame
from Env import *
class Begin_state():
    def __init__(self,surf):
        self.surf=surf
        self.gamestate="begin"
    def show_text(self,surf,text,x,y,size):
        font_name = pygame.font.match_font('arial')
        font=pygame.font.Font(font_name,size)
        text=font.render(text,True,YELLOW)
        surf.blit(text,(x,y))
    def show_begin_screen(self):
        self.show_text(self.surf,"SHUMP!",250,150,100)
        self.show_text(self.surf,"Arrow keys move. Space to Fire",230,300,30)
        self.show_text(self.surf,"Press Space to begin.",320,400,20)
    def keyhandle(self):
        keystate=pygame.key.get_pressed()
        if keystate[pygame.K_SPACE]:
            self.gamestate="start"
            return True
    def updatestate(self):
        return self.gamestate
    def reset(self):
        self.gamestate="begin"
    