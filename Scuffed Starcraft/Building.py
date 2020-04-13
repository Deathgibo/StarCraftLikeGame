#needs to be rendered, produce units with commandsw
import numpy as np
import pygame

class Building():
    def __init__(self, x, y, imgsurf, isEnemy):
        #other
        self.buildingunit = False
        self.selected = False
        self.enemy = isEnemy
        #stats
        self.health = 0
        self.maxhealth = 0
        #map coords
        self.x = x
        self.y = y


    def update(self, input):
        self.handle_input(input)

    def handle_input(self, input):
        if self.selected:
            if input.keys[pygame.K_s]:
                print("creating worker!")

    def render(self, game):
        rectangle = pygame.Rect(int(round(self.rect[0])) - game.map._cameraposition[0], int(round(self.rect[1])) - game.map._cameraposition[1],
        int(round(self.rect[2])), int(round(self.rect[3])))
        game.drawimagerect(rectangle,self.img)

        color = (0,0,255)
        if self.selected:
            color = (0,255,0)
        pygame.draw.circle(game._display_surfrender, color,(int(round(self.circlecenter[0])) - game.map._cameraposition[0],
        int(round(self.circlecenter[1])) - game.map._cameraposition[1]), self.radius, 1)

        if self.buildingunit:
            pass
