import pygame
from pygame.locals import *
import numpy as np
import time
import mathfuncs

""" Entity Class

The entities work on a state machine, they have states like move, attack, dead.
If you need to play a sound when unit dies for example look at the deadstate class,
and the sound could be played on the onentry function. Theres function trigger which globally
switched state like if user presses S it stops no matter what state.
If you want to make a new unit create a class and inherit this, check the marine class for example,
theres certain attributes you need to override like health, attack damage.

"""

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
        self.healthrectwidth = pyrect[2]
        self.healthrect = np.array([float(pyrect[0]),float(pyrect[1]) - 8,float(self.healthrectwidth),5])
        #other
        self.state = idlestate()
        self.selected = False
        self.movelocation = np.array([0,0])
        self.movepaths = []
        self.worker = False
        self.mineralpatch = None
        self.holdingmineral = False
        #stats
        self.speed = 0
        self.attackrange = 0
        self.visionrange = 150
        self.health = 0
        self.maxhealth = 0
        self.damage = 0
        self.attackspeed = 0
        self.attackspeedcounter = 0
        #combat
        self.target = None
        self.followtarget = False
        self.attackmove = False
        self.alive = True
        self.wait = False

    def update(self, input, minerals, mapinfo, displaysurf, enemyunits, units, enemyunitsquad, unitsquad, graph):
        self.stateglobalupdate(input,self)
        self.state.update(self, enemyunits, units, enemyunitsquad, unitsquad)
        newstate = self.statetrigger(input,self, minerals, mapinfo, displaysurf, enemyunits, enemyunitsquad, unitsquad)
        if newstate == None:
            newstate = self.state.handle_input(input,self, enemyunits, enemyunitsquad)
        if newstate != None:
            self.state = newstate
            self.state.entry(self, graph)

    def handleinput(self, input):
        pass

    def render(self, game):
        #if hes outside cameraview dont render
        playerect = pygame.Rect(self.rect[0],self.rect[1],self.rect[2],self.rect[3])
        camerarect = pygame.Rect(game.map._cameraposition[0],game.map._cameraposition[1],game.map._renderdimensions[0],game.map._renderdimensions[1])
        if not playerect.colliderect(camerarect):
            return
        #rectangle image
        rectangle = pygame.Rect(int(round(self.rect[0])) - game.map._cameraposition[0], int(round(self.rect[1])) - game.map._cameraposition[1],
        int(round(self.rect[2])), int(round(self.rect[3])))
        game.drawimagerect(rectangle,self.img)

        #physics circle
        color = (0,0,255)
        if self.selected:
            color = (0,255,0)
        #pygame.draw.circle(game._display_surfrender, color,(int(round(self.circlecenter[0])) - game.map._cameraposition[0],
        #int(round(self.circlecenter[1])) - game.map._cameraposition[1]), self.radius,1)

        #healthbar
        self.healthrect[2] = self.healthrectwidth
        rectangle = pygame.Rect(int(round(self.healthrect[0])) - game.map._cameraposition[0], int(round(self.healthrect[1])) - game.map._cameraposition[1],
        int(round(self.healthrect[2])), int(round(self.healthrect[3])))
        pygame.draw.rect(game._display_surfrender,(50,50,50),rectangle)
        if self.health <= 0:
            percent = 0
        else:
            percent = float(self.health / self.maxhealth)
        self.healthrect[2] = int(self.healthrectwidth * percent)
        rectangle = pygame.Rect(int(round(self.healthrect[0])) - game.map._cameraposition[0], int(round(self.healthrect[1])) - game.map._cameraposition[1],
        int(round(self.healthrect[2])), int(round(self.healthrect[3])))
        pygame.draw.rect(game._display_surfrender,(255,0,0),rectangle)

    """def __eq__(self, other):
        if other is None:
            return self
        if self.circlecenter[0] == other.circlecenter[0] and self.circlecenter[1] == other.circlecenter[1] and self.health == other.health:
            return True
        return False"""

    def same(self,unit):
        if self.circlecenter[0] == unit.circlecenter[0] and self.circlecenter[1] == unit.circlecenter[1]:
            return True
        return False

    """
    #Experiment function for unit collision
    def Push(self, x,y, enemyunits, units, pushedby):
        #cant bump back unit and only has 1 call to move
        if enemyunits != None and units != None:
            for unit in units:
                if not self.same(unit):
                    if self.circlecenter[0] != unit.circlecenter[0] and self.circlecenter[1] != unit.circlecenter[1]:
                        if mathfuncs.mathfuncs.circlecirclecollision((self.circlecenter[0],self.circlecenter[1],self.radius),
                        (unit.circlecenter[0],unit.circlecenter[1],unit.radius)):
                            movevector = np.array([unit.circlecenter[0] - self.circlecenter[0],unit.circlecenter[1] - self.circlecenter[1]])
                            movevector = movevector / np.linalg.norm(movevector)
                            movevector = movevector * 5
                            unit.Move(movevector[0],movevector[1])
                            pass
                        #unit.Push(-5,0)
            for enemy in enemyunits:
                if self.circlecenter[0] != unit.circlecenter[0] and enemy.circlecenter[1] != enemy.circlecenter[1]:
                    if mathfuncs.mathfuncs.circlecirclecollision((self.circlecenter[0],self.circlecenter[1],self.radius),
                    (enemy.circlecenter[0],enemy.circlecenter[1],enemy.radius)):
                        movevector = np.array([enemy.circlecenter[0] - self.circlecenter[0],enemy.circlecenter[1] - self.circlecenter[1]])
                        movevector = movevector / np.linalg.norm(movevector)
                        movevector = movevector * 5
                        enemy.Move(movevector[0],movevector[1])
                        pass
                        #enemy.Push(-5,0)
        self.Move(x,y)"""

    def Move(self,x,y, enemyunits = None, units = None, enemyunitsquad = None, unitsquad = None, z = None):
        #if unit moved check physics
        if enemyunits != None and units != None:
            l = []
            if z is None:
                z = [self]
            #print(len(z))

            unit = unitsquad.PointsInCircleStart((self.circlecenter[0],self.circlecenter[1],self.radius*2),l, z)

            if unit is not None:
                movevector = np.array([unit.circlecenter[0] - self.circlecenter[0],unit.circlecenter[1] - self.circlecenter[1]])
                movevector = movevector / np.linalg.norm(movevector)
                movevector = movevector * 5
                z.append(unit)
                unit.Move(movevector[0],movevector[1], None, None, enemyunitsquad, unitsquad,z)
                #unit.Move(movevector[0],movevector[1], enemyunits, units, enemyunitsquad, unitsquad,z)
            self.wait = False
            """for unit in units:
                if self.circlecenter[0] != unit.circlecenter[0] and self.circlecenter[1] != unit.circlecenter[1]:
                    if mathfuncs.mathfuncs.circlecirclecollision((self.circlecenter[0],self.circlecenter[1],self.radius),
                    (unit.circlecenter[0],unit.circlecenter[1],unit.radius)):
                        movevector = np.array([unit.circlecenter[0] - self.circlecenter[0],unit.circlecenter[1] - self.circlecenter[1]])
                        movevector = movevector / np.linalg.norm(movevector)
                        movevector = movevector * 5
                        unit.Move(movevector[0],movevector[1], None, None, enemyunitsquad, unitsquad)
                        break
                        #unit.Push(-5,0)"""



            """for enemy in enemyunits:
                if self.circlecenter[0] != enemy.circlecenter[0] and self.circlecenter[1] != enemy.circlecenter[1]:
                    if mathfuncs.mathfuncs.circlecirclecollision((self.circlecenter[0],self.circlecenter[1],self.radius),
                    (enemy.circlecenter[0],enemy.circlecenter[1],enemy.radius)):
                        movevector = np.array([enemy.circlecenter[0] - self.circlecenter[0],enemy.circlecenter[1] - self.circlecenter[1]])
                        movevector = movevector / np.linalg.norm(movevector)
                        movevector = movevector * 5
                        enemy.Move(movevector[0],movevector[1])
                        pass
                        #enemy.Push(-5,0)
            """
        #update units quadtree
        if unitsquad is not None:
            unitsquad.deletestart(self)

        self.rect[0] = self.rect[0] + x
        self.rect[1] = self.rect[1] + y
        self.healthrect[0] = self.healthrect[0] + x
        self.healthrect[1] = self.healthrect[1] + y
        self.circlecenter = np.array([self.rect[0] + self.circlexpercent*self.rect[2],self.rect[1] + self.circleypercent*self.rect[3]])

        if unitsquad is not None:
            unitsquad.insertstart(self)

    def GetCircleCenter(self):
        return self.circlecenter

    def stateglobalupdate(self,input,unit):
        #handle reload
        if unit.attackspeedcounter >= unit.attackspeed:
            unit.attackspeedcounter = unit.attackspeed
        else:
            unit.attackspeedcounter = unit.attackspeedcounter + 1


    def statetrigger(self, input, unit, minerals, mapinfo, displaysurf, enemyunits, enemyunitsquad, unitsquad):
        if unit.health <= 0:
            return deadstate()
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
            if input.aclick:
                worldcoords = mapinfo.windowtoworldtransform(input.mouseclickposition[0],input.mouseclickposition[1], displaysurf)
                unit.movelocation[0] = worldcoords[0]
                unit.movelocation[1] = worldcoords[1]
                #if you clicked an enemy set unit.followtarget to True
                for enemy in enemyunits:
                    if mathfuncs.mathfuncs.Magnitude((worldcoords[0] - enemy.circlecenter[0],
                        worldcoords[1] - enemy.circlecenter[1])) < enemy.radius:
                        unit.followtarget = True
                        unit.target = enemy
                        return attackstate()
                unit.attackmove = True
                return movestate()
        return None

    def searchenemies(self, enemylist, enemyunitsquad):
        #check for enemies in vision range
        enemylist = []
        #starttime = time.time_ns()
        l = []
        enemy = enemyunitsquad.PointsInCircleStart((self.circlecenter[0],self.circlecenter[1],self.visionrange),enemylist,l)
        #print(time.time_ns() - starttime)
        if enemy is not None:
            return enemy

        #starttime = time.time()
        """for enemy in enemylist:
            if mathfuncs.mathfuncs.Magnitude((self.circlecenter[0] - enemy.circlecenter[0],self.circlecenter[1] - enemy.circlecenter[1])) <= self.visionrange:
                #print(time.time() - starttime)
                return enemy"""
        #print(time.time() - starttime)
        #check for nearby allies fighting
        return None

######Entity State Classes######
class entity_state():
    def __init__(self):
        pass

    def entry(self, unit, graph):
        #switch animations
        #set values
        pass

    def update(self, unit, enemyunits = None, units = None, enemyunitsquad = None, unitsquad = None):
        pass

    def handle_input(self, input, unit, enemyunits = None, enemyunitsquad = None):
        #see if enemy is near
        return None

class miningstate(entity_state):
    def __init__(self):
        self.state = 0 #0 walking to mineral, 1 collecting mineral, 2 walking to base, 3 depositing in base
    def entry(self, unit, graph):
        self.statezero(unit)
    def update(self, unit, enemyunits = None, units = None, enemyunitsquad = None, unitsquad = None):
        if self.state == 0:
            unit.Move(self.dir[0] * unit.speed,self.dir[1] * unit.speed, enemyunits, units, enemyunitsquad, unitsquad)
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
            unit.Move(self.dir[0] * unit.speed,self.dir[1] * unit.speed, enemyunits, units, enemyunitsquad, unitsquad)
            if mathfuncs.mathfuncs.circlecirclecollision((unit.circlecenter[0],unit.circlecenter[1], unit.radius),
            (900,700, 5)):
                self.statethree(unit)

        if self.state == 3:
            if self.collectingcount >= self.collectingtime:
                unit.holdingmineral = False
                self.statezero(unit)
            self.collectingcount = self.collectingcount + 1
    def handle_input(self, input, unit, enemyunits = None, enemyunitsquad = None):
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
        self.dir = np.array([900 - unit.circlecenter[0], 700 - unit.circlecenter[1]]) #closest base coordinates
        self.dir = self.dir / np.linalg.norm(self.dir)
    def statethree(self, unit):
        self.state = 3
        self.collectingcount = 0
        self.collectingtime = 100


class idlestate(entity_state):
    def __init__(self):
        pass
    def entry(self, unit, graph):
        pass
    def update(self, unit, enemyunits = None, units = None, enemyunitsquad = None, unitsquad = None):
        pass
    def handle_input(self, input, unit, enemyunits = None, enemyunitsquad = None):
        enemy = unit.searchenemies(enemyunits, enemyunitsquad)
        if enemy != None:
            unit.target = enemy
            return attackstate()
        return None

class movestate(entity_state):
    def __init__(self):
        self.attackmove = False
    def entry(self, unit, graph):
        if unit.attackmove:
            self.attackmove = True
            unit.attackmove = False
        #run path algorithm to get a list of vertices
        #look at first entry and get circle and dir
        l = graph.UnitPath((unit.circlecenter[0],unit.circlecenter[1]), (unit.movelocation[0], unit.movelocation[1]))
        #return a tuple (desintationvertex, oldvertex, physics true or false, normal)
        self.movepaths = l
        #print(self.movepaths)
        if len(self.movepaths) > 0:
            unit.movelocation = np.array([self.movepaths[0][0][0],self.movepaths[0][0][1]])
            self.physicsinfo = (np.array([self.movepaths[0][1][0],self.movepaths[0][1][1]]), self.movepaths[0][2], self.movepaths[0][3])
            self.dir = np.array([unit.movelocation[0] - unit.circlecenter[0],unit.movelocation[1] - unit.circlecenter[1]])
            self.dir = self.dir / np.linalg.norm(self.dir)
            self.circle = (unit.movelocation[0],unit.movelocation[1],1)
    def update(self, unit, enemyunits = None, units = None, enemyunitsquad = None, unitsquad = None):
        self.dir = np.array([unit.movelocation[0] - unit.circlecenter[0],unit.movelocation[1] - unit.circlecenter[1]])
        self.dir = self.dir / np.linalg.norm(self.dir)
        unit.Move(self.dir[0] * unit.speed,self.dir[1] * unit.speed, enemyunits, units, enemyunitsquad, unitsquad)
        #check physics
        return
        for x in self.movepaths:
            if x[2]:
                if mathfuncs.mathfuncs.circlesegcollisionfatline(unit.radius,unit.circlecenter[0],unit.circlecenter[1], x[1][0], x[1][1], x[0][0], x[0][1]):
                    unit.Move(x[3][0] * unit.speed, x[3][1] * unit.speed, enemyunits, units, enemyunitsquad, unitsquad) #probably put to none
        return
        if self.physicsinfo[1]:
            if mathfuncs.mathfuncs.circlesegcollisionfatline(unit.radius * 5,unit.circlecenter[0],unit.circlecenter[1], unit.movelocation[0], unit.movelocation[1], self.physicsinfo[0][0], self.physicsinfo[0][1]):
                #handle collision
                push = 20
                unit.Move(self.physicsinfo[2][0] * unit.speed, self.physicsinfo[2][1] * unit.speed, enemyunits, units, enemyunitsquad, unitsquad) #probably put to none


    def handle_input(self, input, unit, enemyunits = None, enemyunitsquad = None):
        #if attackmove check for enemies
        if self.attackmove:
            enemy = unit.searchenemies(enemyunits, enemyunitsquad)
            if enemy != None:
                unit.target = enemy
                return attackstate()
        #check if it reached destination
        if mathfuncs.mathfuncs.circlecirclecollision((unit.circlecenter[0],unit.circlecenter[1], unit.radius), self.circle):
            #pop from list and get next item from path if empty go idle
            self.movepaths.pop(0)
            if len(self.movepaths) > 0:
                unit.movelocation = np.array([self.movepaths[0][0][0],self.movepaths[0][0][1]])
                self.physicsinfo = (np.array([self.movepaths[0][1][0],self.movepaths[0][1][1]]), self.movepaths[0][2], self.movepaths[0][3])
                self.circle = (unit.movelocation[0],unit.movelocation[1],1)
            else:
                return idlestate()
        return None
"""
class attackmovestate(entity_state):
    def __init__(self):
        pass
    def entry(self, unit):
        self.dir = np.array([unit.movelocation[0] - unit.circlecenter[0],unit.movelocation[1] - unit.circlecenter[1]])
        self.dir = self.dir / np.linalg.norm(self.dir)
        self.circle = (unit.movelocation[0],unit.movelocation[1],1)
    def update(self, unit, enemyunits = None, units = None):
        unit.Move(self.dir[0] * unit.speed,self.dir[1] * unit.speed, enemyunits, units)
    def handle_input(self, input, unit, enemyunits = None):
        #check if any enemies are in range or if any allies are fighting within range
        for enemy in enemyunits:
            if mathfuncs.mathfuncs.Magnitude((unit.circlecenter[0] - enemy.circlecenter[0],unit.circlecenter[1] - enemy.circlecenter[1])) <= unit.visionrange:
                unit.target = enemy
                return attackstate()
        #check if you reached destination then go idle
        if mathfuncs.mathfuncs.circlecirclecollision((unit.circlecenter[0],unit.circlecenter[1], unit.radius), self.circle):
            return idlestate()
        return None
"""

class attackstate(entity_state):
    def __init__(self):
        self.attackchase = False
        self.attacking = False
        self.attacklength = 20
        self.attackingcounter = 0
    def entry(self, unit, graph):
        if unit.followtarget:
            self.followtarget = True
        else:
            self.followtarget = False
    def update(self, unit, enemyunits = None, units = None, enemyunitsquad = None, unitsquad = None):
        #check if enemy is within range, if not check if any other enemy is closer to unit than current target
        if not self.attacking:
            targetdistance = mathfuncs.mathfuncs.Magnitude((unit.circlecenter[0] - unit.target.circlecenter[0],unit.circlecenter[1] - unit.target.circlecenter[1]))
            if targetdistance > unit.attackrange:
                self.attackchase = True
                if not self.followtarget:
                    enemylist = []
                    l = []
                    enemy = enemyunitsquad.PointsInCircleStart((unit.circlecenter[0],unit.circlecenter[1],targetdistance),enemylist,l)
                    if enemy is not None:
                        unit.target = enemy
                        if mathfuncs.mathfuncs.Magnitude((unit.circlecenter[0] - enemy.circlecenter[0],unit.circlecenter[1] - enemy.circlecenter[1])) <= unit.attackrange:
                            self.attackchase = False

                    """for enemy in enemyunits:
                        enemydistance = mathfuncs.mathfuncs.Magnitude((unit.circlecenter[0] - enemy.circlecenter[0],unit.circlecenter[1] - enemy.circlecenter[1]))
                        if enemydistance < targetdistance: #unit.attackrange
                            unit.target = enemy
                            if enemydistance <= unit.attackrange:
                                self.attackchase = False
                            break"""
            else:
                self.attackchase = False

        #the current target is far away move to him
        if self.attackchase:
            self.dir = np.array([unit.target.circlecenter[0] - unit.circlecenter[0],unit.target.circlecenter[1] - unit.circlecenter[1]])
            self.dir = self.dir / np.linalg.norm(self.dir)
            unit.Move(self.dir[0] * unit.speed,self.dir[1] * unit.speed, enemyunits, units, enemyunitsquad, unitsquad)
        else:
            if unit.attackspeedcounter == unit.attackspeed:
                self.attacking = True
        #attack animation function
        if self.attacking:
            if self.attackingcounter >= self.attacklength:
                unit.target.health = unit.target.health - unit.damage
                unit.attackspeedcounter = 0
                self.attackingcounter = 0
                self.attacking = False
            self.attackingcounter =  self.attackingcounter + 1

    def handle_input(self, input, unit, enemyunits = None, enemyunitsquad = None):
        #if enemy is dead return to idle
        if unit.target.health <= 0:
            return idlestate()
        return None

"""
#perhaps combine with a boolean on attackstate
class attacktargetstate(entity_state):
    def __init__(self):
        self.attackchase = False
        self.attacking = False
        self.attacklength = 30
        self.attackingcounter = 0
    def entry(self, unit):
        print("entered attacktarget")
    def update(self, unit, enemyunits = None, units = None):
        if self.attackchase:#the current target is far away move to him
            self.dir = np.array([unit.target.circlecenter[0] - unit.circlecenter[0],unit.target.circlecenter[1] - unit.circlecenter[1]])
            self.dir = self.dir / np.linalg.norm(self.dir)
            unit.Move(self.dir[0] * unit.speed,self.dir[1] * unit.speed, enemyunits, units)
        else:
            if unit.attackspeedcounter == unit.attackspeed:
                self.attacking = True
                #unit.target.health = unit.target.health - unit.damage
                #unit.attackspeedcounter = 0
        if self.attacking:
            if self.attackingcounter >= self.attacklength:
                unit.target.health = unit.target.health - unit.damage
                unit.attackspeedcounter = 0
                self.attackingcounter = 0
                self.attacking = False
            self.attackingcounter =  self.attackingcounter + 1
    def handle_input(self, input, unit, enemyunits = None):
        #if target is dead go to idle
        if unit.target.health <= 0:
            return idlestate()
        if not self.attacking:
            if mathfuncs.mathfuncs.Magnitude((unit.circlecenter[0] - unit.target.circlecenter[0],unit.circlecenter[1] - unit.target.circlecenter[1])) > unit.attackrange:
                self.attackchase = True
            else:
                self.attackchase = False
        return None
"""
"""
#state not used
class firingstate(entity_state):
    def __init__(self):
        self.attacklength = 30
        self.attackingcounter = 0
        self.fired = False
    def entry(self, unit):
        pass
    def update(self, unit, enemyunits = None, units = None):
        if self.attackingcounter >= self.attacklength:
            unit.target.health = unit.target.health - unit.damage
            unit.attackspeedcounter = 0
            self.attackingcounter = 0
            self.attacking = False
            self.fired = True
        self.attackingcounter =  self.attackingcounter + 1
        pass
    def handle_input(self, input, unit, enemyunits = None):
        if self.fired:
            pass
        return None
"""
class deadstate(entity_state):
    def __init__(self):
        pass
    def entry(self, unit, graph):
        unit.alive = False
    def update(self, unit, enemyunits = None, units = None, enemyunitsquad = None, unitsquad = None):
        #play death animation
        #once done
        unit.alive = False
    def handle_input(self, input, unit, enemyunits = None, enemyunitsquad = None):
        return None
