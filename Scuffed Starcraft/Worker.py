import Entity
import pygame

class Worker(Entity.Entity):

    def __init__(self, rad,imgsurf, pyrect):
        super().__init__(rad,imgsurf,pyrect)
        self.circlexpercent = .5
        self.circleypercent = .75
        self.Move(0,0)
        self.collecting = False
        self.worker = True
        self.speed = 5
        #extra

    def render(self, game):
        super().render(game)
        #render gem in hand
        if self.holdingmineral:
            rectangle = pygame.Rect(int(round(self.rect[0])) - game.map._cameraposition[0], int(round(self.rect[1])) - game.map._cameraposition[1] + int(.5*self.rect[3]),
            45, 45)
            game.drawimagerect(rectangle,game._mineralimg)
