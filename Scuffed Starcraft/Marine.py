import Entity
import pygame


class Marine(Entity.Entity):

    def __init__(self, rad, imgsurf, pyrect):
        super().__init__(rad, imgsurf, pyrect)
        self.circlexpercent = .5
        self.circleypercent = .75
        self.Move(0, 0)
        self.speed = 2.3
        self.attackrange = 100
        self.health = 10
        self.maxhealth = self.health
        self.attackspeed = 65
        self.attackspeedcounter = self.attackspeed
        self.damage = 1
        # extra

    def abilities(self):
        # if t activate stim pack
        pass

    def render(self, game):
        super().render(game)
