import Building
import pygame
import numpy as np


class CommandCenter(Building.Building):
    def __init__(self, x, y, imgsurf):
        super().__init__(x, y, imgsurf)
        # render
        xsize = 200
        ysize = 200
        self.rect = pygame.Rect(x - xsize / 2, y - ysize / 2, xsize, ysize)
        self.img = imgsurf
        # physics
        self.circlecenter = np.array([int(x), int(y)])
        self.radius = int(xsize / 5)
        #stats
        self.health = 1500
        self.maxhealth = 1500

    def update(self, input):
        self.handle_input(input)

    def handle_input(self, input):
        if self.selected:
            if input.keys[pygame.K_s]:
                print("creating worker!")
