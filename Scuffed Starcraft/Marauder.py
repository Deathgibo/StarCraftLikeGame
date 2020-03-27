import Entity
import pygame

class Marauder(Entity.Entity):

    def __init__(self, rad,imgsurf, pyrect):
        super().__init__(rad,imgsurf,pyrect)
        self.circlexpercent = .5
        self.circleypercent = .75
        self.Move(0,0)
        self.speed = 2
        self.attackrange = 100
        self.health = 10
        self.maxhealth = self.health
        self.attackspeed = 75
        self.attackspeedcounter = self.attackspeed
        self.damage = 2
        #extra

    def render(self, game, healthbar):
        super().render(game, healthbar)
