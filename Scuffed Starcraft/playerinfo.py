import pygame
import numpy as np

import mathfuncs

##Playerinfo = playerinfoLog()
##playerinfolocator.provide(Playerinfo)
##Playerinfo.giveresources(20)
##playerinfolocator.getplayerinfo().resources

class playerinfo():
    def __init__(self):
        self.resources = 5
        self.supply = 0

        #unit selection
        self._selectionrect = np.array([0,0,0,0]) #(startingx,startingy,width,height)
        self._selectedlist = [] #holds entities
        self._firstclick = False
        self._firstclickmini = False

    def giveresources(self, resource):
        self.resources = self.resources + resource

    def update(self, input, playerunits, map, displaysurf):
        #handle unit clicking and mouse drag
        if input.leftclickframe and map.ispointonminimap(input.mouseposition[0],input.mouseposition[1], displaysurf):
            self._firstclickmini = True
        if input.leftclick and not map.ispointonminimap(input.mouseposition[0],input.mouseposition[1], displaysurf):
            if input.leftclickframe:
                self._selectionrect = np.array([input.mouseposition[0],input.mouseposition[1],1,1])
                self._firstclick = True
            if self._firstclick == True:
                self._selectionrect[2] = input.mouseposition[0] - self._selectionrect[0]
                self._selectionrect[3] = input.mouseposition[1] - self._selectionrect[1]
        if input.leftclickletgo and not self._firstclickmini:
            #reset all to false
            self._firstclick = False
            self._selectedlist.clear()
            for unit in playerunits:
                unit.selected = False
                if mathfuncs.mathfuncs.rectcirclecollision(self._selectionrect[0],self._selectionrect[1], self._selectionrect[2],
                self._selectionrect[3],unit.circlecenter[0], unit.circlecenter[1],unit.radius):
                    unit.selected = True
                    self._selectedlist.append(unit)
            self._selectionrect = (0,0,0,0)
        if input.leftclickletgo and self._firstclickmini:
            self._firstclickmini = False
        #once we let go call a function to see what units we have

        self.resources = self.resources + 1
    def render(self, surface):
        #render the rect
        pygame.draw.rect(surface,(0,255,0,4),self._selectionrect, 1)


class playerinfoLog():
    def __init__(self):
        self.resources = 5
        self.supply = 0
        print("initialized")

    def giveresources(self, resource):
        print("resources given to player")
        self.resources = self.resources + resource

    def update(self):
        self.resources = self.resources + 1
        print("updated")

class playerinfolocator():#make null exceptions
    playerinfo_ref = None
    @staticmethod
    def provide(playerinfo):
        playerinfolocator.playerinfo_ref = playerinfo
    @staticmethod
    def getplayerinfo():
        return playerinfolocator.playerinfo_ref
