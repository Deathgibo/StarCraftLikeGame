import pygame
import numpy as np
import time
import mathfuncs

#This class contains player information like resources, units selected,etc.
#So if you need playerinfo in main its called self.__playerinfo, can just
#pass that to other functions

class playerinfo():
    def __init__(self):
        self.resources = 5
        self.supply = 0
        self.population = 0

        #unit selection
        self._selectionrect = np.array([0,0,0,0]) #(startingx,startingy,width,height)
        self._selectionrectrender = np.array([0,0,0,0])
        self._selectedlist = [] #holds entities
        self._selectedbuildinglist = [] #holds buildings
        self._firstclick = False
        self._firstclickmini = False
        self._aclicked = False
        self.selectedOverlay = False

    def giveresources(self, resource):
        self.resources = self.resources + resource

    def givepopulation(self, population):
        self.population = self.population + population

    def removepopulation(self, population):
        self.population = self.population - population

    def update(self, input, playerunits, map, displaysurf, playerbuildings, enemyunits, unitsquad, enemyunitsquad):
        #handle unit clicking and mouse drag
        worldcoords = map.windowtoworldtransform(input.mouseposition[0],input.mouseposition[1], displaysurf)
        #Normal Case of not selecting the overlay
        self.selectedOverlay = False
        if input.aclick:
            self._aclicked = True
            return

        if input.leftclickframe and map.ispointonminimap(input.mouseposition[0],input.mouseposition[1], displaysurf):
            self._firstclickmini = True
        if input.leftclick and not map.ispointonminimap(input.mouseposition[0],input.mouseposition[1], displaysurf):
            if input.leftclickframe:
                self._selectionrect = np.array([worldcoords[0],worldcoords[1],1,1])
                self._selectionrectrender = np.array([input.mouseclickposition[0],input.mouseclickposition[1],1,1])
                self._firstclick = True
            if self._firstclick == True:
                self._selectionrect[2] = worldcoords[0] - self._selectionrect[0]
                self._selectionrect[3] = worldcoords[1] - self._selectionrect[1]
                self._selectionrectrender[2] = input.mouseposition[0] - self._selectionrectrender[0]
                self._selectionrectrender[3] = input.mouseposition[1] - self._selectionrectrender[1]
        
        #Make overlay not change selection
        if input.mouseclickposition[0] >= 0 and input.mouseclickposition[0] <= displaysurf.get_width():
            if input.mouseclickposition[1] >= (displaysurf.get_height() - int(displaysurf.get_height() / 3)) and input.mouseclickposition[1] <= displaysurf.get_height():
                self.selectedOverlay = True
        if input.leftclickletgo and not self._firstclickmini and not self._aclicked:#self._selectionrect[3] != -1
            #If we select the overlay we dont want to clear either the unit/building selected list
            if not self.selectedOverlay:
                self._selectedbuildinglist.clear()
                #buildings
                for building in playerbuildings:
                    building.selected = False
                    if mathfuncs.mathfuncs.rectcirclecollision(self._selectionrect[0],self._selectionrect[1], self._selectionrect[2],
                    self._selectionrect[3],building.circlecenter[0], building.circlecenter[1],building.radius):
                        building.selected = True
                        self._selectedbuildinglist.append(building)

                self._selectedlist.clear()
                #starttime = time.time_ns()
                for unit in playerunits:
                    unit.selected = False
                    if mathfuncs.mathfuncs.rectcirclecollision(self._selectionrect[0],self._selectionrect[1], self._selectionrect[2],
                    self._selectionrect[3],unit.circlecenter[0], unit.circlecenter[1],unit.radius):
                        unit.selected = True
                        self._selectedlist.append(unit)
                for unit in enemyunits:
                    unit.selected = False
                    if mathfuncs.mathfuncs.rectcirclecollision(self._selectionrect[0],self._selectionrect[1], self._selectionrect[2],
                    self._selectionrect[3],unit.circlecenter[0], unit.circlecenter[1],unit.radius):
                        unit.selected = True
                        self._selectedlist.append(unit)
                #print(time.time_ns() - starttime)
            #units
            #starttime = time.time_ns()
            """This is a select loop for the quad tree, but im using the regular list
            for unitz in self._selectedlist:
                unitz.selected = False
            self._selectedlist.clear()

            extrasize = 10
            box = pygame.Rect(self._selectionrect[0] - extrasize,self._selectionrect[1] - extrasize, self._selectionrect[2] + extrasize, self._selectionrect[3] + extrasize)
            if box[2] < 0:
                box[0] = box[0] + box[2]
                box[2] = -box[2]
            if box[3] < 0:
                box[1] = box[1] + box[3]
                box[3] = -box[3]
            unitsquad.PointsInBoxStart(box, self._selectedlist)
            enemyunitsquad.PointsInBoxStart(box,self._selectedlist)
            #print(time.time_ns() - starttime)

            for unitz in self._selectedlist:
                unitz.selected = True
            """

            #reset
            self._firstclick = False
            self._selectionrect = (0,0,0,0)
            self._selectionrectrender = (0,0,0,0)
        if input.leftclickletgo:
            self._aclicked = False
        if input.leftclickletgo and self._firstclickmini:
            self._firstclickmini = False
        
        #Check if a unit is currently selected
        if self._selectedlist:
            #Removed selected unit from list when they die (changes overlay to no unit selected)
            if self._selectedlist[0].health <= 0:
                self._selectedlist.pop(0)
        #once we let go call a function to see what units we have

    def render(self, surface):
        #render the rect
        pygame.draw.rect(surface,(0,255,0,4),self._selectionrectrender, 1)



##These classes under probably won't be used

##Playerinfo = playerinfoLog()
##playerinfolocator.provide(Playerinfo)
##Playerinfo.giveresources(20)
##playerinfolocator.getplayerinfo().resources

class playerinfoLog():
    def __init__(self):
        self.resources = 5
        self.supply = 0
        self.population = 0
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
