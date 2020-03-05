import pygame
from pygame.locals import *
import numpy as np

import mathfuncs

class Entity():
    def __init__(self, rad,imgsurf, pyrect):
        #physics
        self.radius = rad
        self.circlexpercent = .5
        self.circleypercent = .85
        self.circlecenter = np.array([int(pyrect.x + self.circlexpercent*pyrect.w),int(pyrect.y + self.circleypercent*pyrect.h)])
        #render
        self.rect = np.array([float(pyrect[0]),float(pyrect[1]),float(pyrect[2]),float(pyrect[3])])
        self.img = imgsurf
        #other
        self.state = idlestate()
        self.selected = False
        self.movelocation = np.array([0,0])
        self.worker = False
        self.mineralpatch = None
        self.holdingmineral = False
        self.speed = 0

    def update(self, input, minerals, mapinfo, displaysurf):
        self.state.update(self)
        newstate = self.statetrigger(input,self, minerals, mapinfo, displaysurf)
        if newstate == None:
            newstate = self.state.handle_input(input,self)
        if newstate != None:
            self.state = newstate
            self.state.entry(self)

    def handleinput(self, input):
        pass

    def render(self, game):
        #print(self.circlecenter[0])
        rectangle = pygame.Rect(int(round(self.rect[0])) - game.map._cameraposition[0], int(round(self.rect[1])) - game.map._cameraposition[1],
        int(round(self.rect[2])), int(round(self.rect[3])))
        game.drawimagerect(rectangle,self.img)
        color = (0,0,255)
        if self.selected:
            color = (0,255,0)
        pygame.draw.circle(game._display_surfrender, color,(int(round(self.circlecenter[0])) - game.map._cameraposition[0],
        int(round(self.circlecenter[1])) - game.map._cameraposition[1]), self.radius,1)

    def Move(self,x,y):
        self.rect[0] = self.rect[0] + x
        self.rect[1] = self.rect[1] + y
        self.circlecenter = np.array([self.rect[0] + self.circlexpercent*self.rect[2],self.rect[1] + self.circleypercent*self.rect[3]])
        #print(self.circlecenter[0])

    def GetCircleCenter(self):
        return self.circlecenter

    def statetrigger(self, input, unit, minerals, mapinfo, displaysurf):
        if unit.selected:
            if input.keys[pygame.K_s]:
                return idlestate()
            if input.rightclickframe:
                worldcoords = mapinfo.windowtoworldtransform(input.mouseclickposition[0],input.mouseclickposition[1], displaysurf)
                if unit.worker:#check if clicked on a resource
                    for mineral in minerals:
                        if mathfuncs.mathfuncs.circlecirclecollision((mineral.circlecenter[0],mineral.circlecenter[1],mineral.radius), (worldcoords[0],worldcoords[1],1)):
                            unit.mineralpatch = mineral
                            return miningstate()
                unit.movelocation[0] = worldcoords[0]
                unit.movelocation[1] = worldcoords[1]
                return movestate()
        return None


######Entity State Classes######
class entity_state():
    def __init__(self):
        pass

    def entry(self, unit):
        #switch animations
        #set values
        pass

    def update(self, unit):
        pass

    def handle_input(self, input, unit):
        #check to see if we need to switch states
        return None

class miningstate(entity_state):
    def __init__(self):
        self.state = 0 #0 walking to mineral, 1 collecting mineral, 2 walking to base, 3 depositing in base
    def entry(self, unit):
        self.statezero(unit)
    def update(self, unit):
        if self.state == 0:
            unit.Move(self.dir[0] * unit.speed,self.dir[1] * unit.speed)
            if mathfuncs.mathfuncs.circlecirclecollision((unit.circlecenter[0],unit.circlecenter[1], unit.radius),
            (unit.mineralpatch.circlecenter[0],unit.mineralpatch.circlecenter[1], unit.mineralpatch.radius)):
                self.stateone(unit)

        if self.state == 1:
            if self.collectingcount >= self.collectingtime:
                if unit.mineralpatch.mineralcount <= 0:
                    return idlestate()
                unit.mineralpatch.mineralcount = unit.mineralpatch.mineralcount - 1
                unit.holdingmineral = True
            if unit.holdingmineral:
                self.statetwo(unit)
            self.collectingcount = self.collectingcount + 1

        if self.state == 2:
            unit.Move(self.dir[0] * unit.speed,self.dir[1] * unit.speed)
            if mathfuncs.mathfuncs.circlecirclecollision((unit.circlecenter[0],unit.circlecenter[1], unit.radius),
            (800,800, 5)):
                self.statethree(unit)

        if self.state == 3:
            if self.collectingcount >= self.collectingtime:
                unit.holdingmineral = False
                self.statezero(unit)
            self.collectingcount = self.collectingcount + 1
    def handle_input(self, input, unit):
        return None
    def statezero(self, unit):
        self.state = 0
        self.dir = np.array([unit.mineralpatch.circlecenter[0] - unit.circlecenter[0],unit.mineralpatch.circlecenter[1] - unit.circlecenter[1]])
        self.dir = self.dir / np.linalg.norm(self.dir)
    def stateone(self, unit):
        self.state = 1
        self.collectingcount = 0
        self.collectingtime = 100
    def statetwo(self, unit):
        self.state = 2
        self.dir = np.array([800 - unit.circlecenter[0], 800 - unit.circlecenter[1]]) #closest base coordinates
        self.dir = self.dir / np.linalg.norm(self.dir)
    def statethree(self, unit):
        self.state = 3
        self.collectingcount = 0
        self.collectingtime = 100


class idlestate(entity_state):
    def __init__(self):
        pass
    def entry(self, unit):
        print("entered idle")
    def update(self, unit):
        pass
        #print("idle")
    def handle_input(self, input, unit):
        return None

class movestate(entity_state):
    def __init__(self):
        pass
    def entry(self, unit):
        self.dir = np.array([unit.movelocation[0] - unit.circlecenter[0],unit.movelocation[1] - unit.circlecenter[1]])
        self.dir = self.dir / np.linalg.norm(self.dir)
        self.circle = (unit.movelocation[0],unit.movelocation[1],1)
    def update(self, unit):
        unit.Move(self.dir[0] * unit.speed,self.dir[1] * unit.speed)
    def handle_input(self, input, unit):
        #check if it reached destination
        if mathfuncs.mathfuncs.circlecirclecollision((unit.circlecenter[0],unit.circlecenter[1], unit.radius), self.circle):
            return idlestate()
        return None

class attackmovestate(entity_state):
    def __init__(self):
        pass
    def entry(self, unit):
        print("entered attackmove")
    def update(self, unit):
        print("attackmove")
    def handle_input(self, input, unit):
        if input == 6:
            return idlestate()
        return None

class attackstate(entity_state):
    def __init__(self):
        pass
    def entry(self, unit):
        print("entered attack")
    def update(self, unit):
        print("attack")
    def handle_input(self, input, unit):
        if input == 6:
            return idlestate()
        return None

class attacktargetstate(entity_state):
    def __init__(self):
        pass
    def entry(self, unit):
        print("entered attacktarget")
    def update(self, unit):
        print("attacktarget")
    def handle_input(self, input, unit):
        if input == 6:
            return idlestate()
        return None

class deadstate(entity_state):
    def __init__(self):
        pass
    def entry(self, unit):
        print("entered dead")
    def update(self, unit):
        print("dead")
    def handle_input(self, input, unit):
        if input == 6:
            return idlestate()
        return None
