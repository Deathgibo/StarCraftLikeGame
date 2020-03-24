import numpy as np
import pygame


class Mineral():
    def __init__(self, x, y, imgsurf):
        xdimension = 75
        ydimension = 75
        # render
        self.rect = pygame.Rect(x, y, xdimension, ydimension)
        self.img = imgsurf
        # other
        self.circlecenter = np.array([int(x + .5 * xdimension), int(y + .70 * ydimension)])
        self.radius = int(xdimension / 5)
        self.mineralcount = 5

    def render(self, game):
        rectangle = pygame.Rect(int(round(self.rect[0])) - game.map._cameraposition[0],
                                int(round(self.rect[1])) - game.map._cameraposition[1],
                                int(round(self.rect[2])), int(round(self.rect[3])))
        game.drawimagerect(rectangle, self.img)
        color = (0, 255, 0)
        if self.mineralcount <= 0:
            color = (255, 0, 0)
        pygame.draw.circle(game._display_surfrender, color,
                           (int(round(self.circlecenter[0])) - game.map._cameraposition[0],
                            int(round(self.circlecenter[1])) - game.map._cameraposition[1]), self.radius, 1)
