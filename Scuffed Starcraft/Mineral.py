import numpy as np
import pygame

class Mineral():
    def __init__(self, x, y, imgsurf):
        xdimension = 70
        ydimension = 70
        #render
        self.rect = pygame.Rect(x,y,xdimension,ydimension)
        self.img = imgsurf
        #other
        self.circlecenter = np.array([int(x + .5*xdimension),int(y + .70*ydimension)])
        self.radius = 15
        self.mineralcount = 5

    def render(self, game):
        game.drawimagerect(self.rect,self.img)
        color = (0,255,0)
        if self.mineralcount <= 0:
            color = (255,0,0)
        pygame.draw.circle(game._display_surf, color,(self.circlecenter[0],self.circlecenter[1]), self.radius, 1)
