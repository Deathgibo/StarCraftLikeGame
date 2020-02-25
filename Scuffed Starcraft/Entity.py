import pygame
from pygame.locals import *
import numpy as np

class Entity():
    def __init__(self, rad,imgsurf, pyrect):
        #physics
        self.radius = rad
        self.circlecenter = np.array([int(pyrect.x + .5*pyrect.w),int(pyrect.y + .85*pyrect.h)])
        #render
        self.x = int(pyrect.x + .5*pyrect.w)
        self.y = int(pyrect.y + .85*pyrect.h)
        self.rect = pyrect
        self.img = imgsurf
        #other
        self.state = idlestate()
        self.harvester = False

    def update(self, game):
        self.state.update()
        newstate = self.state.handle_input(input)
        if(newstate != None):
            self.state = newstate
            self.state.entry()

    def Move(self,x,y):
        self.rect.x = self.rect.x + x
        self.rect.y = self.rect.y + y
        self.circlecenter = np.array([int(self.rect.x + .5*self.rect.w),int(self.rect.y + .85*self.rect.h)])
        self.x = int(self.rect.x + .5*self.rect.w)
        self.y = int(self.rect.y + .85*self.rect.h)

    def GetCircleCenter(self):
        return self.circlecenter


######Entity State Classes######
class entity_state():
    def __init__(self):
        pass

    def entry(self):
        #switch animations
        #set values
        pass

    def update(self):
        pass

    def handle_input(self, input):
        #check to see if we need to switch states
        return None

class idlestate(entity_state):
    def __init__(self):
        pass
    def entry(self):
        print("entered idle")
    def update(self):
        print("idle")
    def handle_input(self, input):
        if input == 5:
            return movestate()
        return None

class movestate(entity_state):
    def __init__(self):
        pass
    def entry(self):
        print("entered move")
    def update(self):
        print("move")
    def handle_input(self, input):
        if input == 6:
            return idlestate()
        return None

class attackmovestate(entity_state):
    def __init__(self):
        pass
    def entry(self):
        print("entered attackmove")
    def update(self):
        print("attackmove")
    def handle_input(self, input):
        if input == 6:
            return idlestate()
        return None

class attackstate(entity_state):
    def __init__(self):
        pass
    def entry(self):
        print("entered attack")
    def update(self):
        print("attack")
    def handle_input(self, input):
        if input == 6:
            return idlestate()
        return None

class attacktargetstate(entity_state):
    def __init__(self):
        pass
    def entry(self):
        print("entered attacktarget")
    def update(self):
        print("attacktarget")
    def handle_input(self, input):
        if input == 6:
            return idlestate()
        return None

class deadstate(entity_state):
    def __init__(self):
        pass
    def entry(self):
        print("entered dead")
    def update(self):
        print("dead")
    def handle_input(self, input):
        if input == 6:
            return idlestate()
        return None
