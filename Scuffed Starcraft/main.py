import pygame
from pygame.locals import *
import pygame.mixer
import os
import sys
import math
import numpy as np

import Entity
import input
import mathfuncs
import Map
import Worker
import playerinfo
import Mineral

class App():
    def __init__(self):
        self._running = True
        self._display_surf = None
        self._image_surf = None
        self._cwdpath = None

    def on_init(self):
        os.environ['SDL_VIDEO_CENTERED'] = '1'

        if self.initpygame() is False:
            return False
        self._running = True

        #initialize window
        self._infoObject = pygame.display.Info()
        self._display_surfrender = pygame.Surface((1500,1500))
        self._display_surf = pygame.display.set_mode((800,600), pygame.RESIZABLE)
        self._cwdpath = os.getcwd()
        pygame.display.set_caption("Scuffed StarCraft")
        pygame.display.set_icon(pygame.image.load(os.path.join(self._cwdpath,"Images","sc2.png")))
        pygame.mouse.set_visible(False)
        pygame.event.set_grab(True)

        #initialize other values
        self._lasttime = 0
        self._input = input.input()

        self._playerinfo = playerinfo.playerinfo()

        self.map = Map.Map()

        self.load_media()
        self.load_entities()
        self.load_resources()


    def initpygame(self):
        pygame.init()
        pygame.mixer.init()
        if pygame.mixer.get_init() is None:
            print("Error initializing mixer!\n")
            return False

    def load_resources(self):
        #minerals
        self.minerallist = []
        mineral1 = Mineral.Mineral(450,450,self._mineralimg)
        mineral2 = Mineral.Mineral(500,400,self._mineralimg)
        mineral3 = Mineral.Mineral(600,350,self._mineralimg)
        self.minerallist.append(mineral1)
        self.minerallist.append(mineral2)
        self.minerallist.append(mineral3)

    def load_entities(self):
        marinesurf = pygame.image.load(os.path.join(self._cwdpath,"Images","marauder.png")).convert()
        scvsurf = pygame.image.load(os.path.join(self._cwdpath,"Images","scv2.png")).convert_alpha()
        marinerect = pygame.Rect(0,0,85,85)
        entity1 = Worker.Worker(25,scvsurf,marinerect)
        marinerect = pygame.Rect(100,50,85,85)
        entity2 = Worker.Worker(25,scvsurf,marinerect)
        self._entitylist = []
        self._entitylist.append(entity1)
        self._entitylist.append(entity2)
        self.line = [(100,100),(200,200)]
        self.circle = (200,100,20)
        self.pumpcircle = (400,250,80)

    def load_media(self): #Load sounds and images
        self._image_surf = pygame.image.load(os.path.join(self._cwdpath,"Images","lilpump.jpg")).convert()
        self._mineralimg = pygame.image.load(os.path.join(self._cwdpath,"Images","mineralt.png")).convert_alpha()
        self.map._mapimage = pygame.image.load(os.path.join(self._cwdpath,"Images","bigmap3.jpg")).convert()
        self._mouseimg1 = pygame.image.load(os.path.join(self._cwdpath,"Images","mouse1t.png")).convert_alpha()
        self._mouseimg2 = pygame.image.load(os.path.join(self._cwdpath,"Images","mouse2t.png")).convert_alpha()
        self._mouseimg3 = pygame.image.load(os.path.join(self._cwdpath,"Images","mouse3t.png")).convert_alpha()
        self._mouseimg4 = pygame.image.load(os.path.join(self._cwdpath,"Images","mouse4t.png")).convert_alpha()
        self._mouseimg5 = pygame.image.load(os.path.join(self._cwdpath,"Images","mouse5t.png")).convert_alpha()
        self._mouseimgoffset = np.array([10,10])
        self._mouseimglist = [self._mouseimg1,self._mouseimg2,self._mouseimg3,self._mouseimg4,self._mouseimg5]
        self._mouseimgcurrent = self._mouseimg1
        self.sound_esketit = pygame.mixer.Sound(os.path.join(self._cwdpath,"Sounds","esketit.wav"))

    def on_update(self):
        #update map and mouse information
        mouseinfo = self.map.handleinput(self._input, self._display_surf,self._mouseimgcurrent, self._mouseimglist)
        self._mouseimgcurrent = self._mouseimglist[mouseinfo[0]]
        self._mouseimgoffset[0] = mouseinfo[1]
        self._mouseimgoffset[1] = mouseinfo[2]

        self._playerinfo.update(self._input, self._entitylist,self.map,self._display_surf)

        for units in self._entitylist:
            units.update(self._input,self.minerallist, self.map,self._display_surf)

        #for units in self._playerinfo._selectedlist:
            #units.handleinput(self)

        answer = mathfuncs.mathfuncs.circlesegcollision(self._entitylist[0].radius,self._entitylist[0].circlecenter[0],self._entitylist[0].circlecenter[1],
        self.line[0][0],self.line[0][1],self.line[1][0],self.line[1][1])
        answer2 = mathfuncs.mathfuncs.circlecirclecollision((self._entitylist[0].circlecenter[0],self._entitylist[0].circlecenter[1],
         self._entitylist[0].radius), self.circle)
        #print("Line collision: %d Circle collision: %d" % (answer, answer2))
        if mathfuncs.mathfuncs.circlecirclecollision((self._entitylist[0].circlecenter[0],self._entitylist[0].circlecenter[1], self._entitylist[0].radius), self.pumpcircle):
            self.sound_esketit.set_volume(.05)
            self.sound_esketit.play();

        #if not pygame.mixer.music.get_busy():
        #    pygame.mixer.music.load(os.path.join(self._cwdpath,"Sounds","100 on my wrist.wav"))
        #    pygame.mixer.music.set_volume(0.5)
        #    pygame.mixer.music.play()
            #self.sound_esketit.set_volume(.05)
            #self.sound_esketit.play();

    def on_render(self):
        self._display_surfrender.fill((255,255,255))

        #map
        self.map.render(self._display_surfrender)

        #units
        for x in self._entitylist:
            x.render(self)

        #minerals
        for x in self.minerallist:
            x.render(self)

        #transform surface to fit screen size
        resized_screen = pygame.transform.scale(self._display_surfrender, (self._display_surf.get_width(),self._display_surf.get_height()))
        self._display_surf.blit(resized_screen, (0, 0))

        #UI
        #mini map
        self.map.renderminimap(self._display_surf)
        #green box
        self._playerinfo.render(self._display_surf)

        #cursor
        mousesize = 44
        self.drawimagerectgui(pygame.Rect(self._input.mouseposition[0] - int(mousesize/2) + self._mouseimgoffset[0],
          self._input.mouseposition[1] - int(mousesize/2) + self._mouseimgoffset[1],mousesize,mousesize),self._mouseimgcurrent)

        pygame.display.update()

    def drawimagerect(self, rect, image): #renders an image on a rect while preserving original image size
        newimage = pygame.transform.scale(image,(rect.w,rect.h))
        self._display_surfrender.blit(newimage,(rect.x,rect.y))

    def drawimagerectgui(self, rect, image):
        newimage = pygame.transform.scale(image,(rect.w,rect.h))
        self._display_surf.blit(newimage,(rect.x,rect.y))

    def on_exit(self):
        self._running = False

    def on_cleanup(self):
        pygame.quit()
        pygame.mixer.quit()

    def on_execute(self):
        if self.on_init() == False:
            self._running = False
        pygame.time.get_ticks()
        while( self._running ):
            self._input.reset()
            for event in pygame.event.get():
                self.on_event(event)
            self.on_update()
            self.on_render()
            self.handlefps()
        self.on_cleanup()

    def handlefps(self):
        frametime = pygame.time.get_ticks() - self._lasttime
        if frametime != 0:
            fps = 1000 / frametime #1000 miliseconds = 1 second, so
            pygame.display.set_caption("Scuffed StarCraft fps: %f" % fps)
            if frametime < 17:
                pygame.time.delay(17 - frametime)
        self._lasttime = pygame.time.get_ticks()

    def on_event(self, event): #INPUT HANDLING FUNCTION
        if event.type == QUIT:
            self.on_exit()

        elif event.type >= USEREVENT:
            pass

        elif event.type == VIDEOEXPOSE:
            pass

        elif event.type == VIDEORESIZE: # event.size, event.w, event.h
            self._display_surf = pygame.display.set_mode(event.size, pygame.RESIZABLE)
            pass

        elif event.type == KEYUP:
            self._input.keys[event.key] = 0

        elif event.type == KEYDOWN: #event.key (pygame.K_x) event.mod == pygame.KMOD_LSHIFT
            speed = 10
            self._input.keys[event.key] = 1
            if event.key == pygame.K_1:
                pygame.display.set_mode((800, 600),  pygame.RESIZABLE)
            if event.key == pygame.K_2:
                pygame.display.set_mode((1350,750),  pygame.RESIZABLE)
                pygame.display.update()
            if event.key == pygame.K_ESCAPE:
                self.on_exit()

        elif event.type == MOUSEMOTION: #event.buttons, event.pos, event.rel
            self._input.mouseposition = event.pos
            self._input.mousechange = event.rel

        elif event.type == MOUSEBUTTONUP: #event.button, #event.pos
            if event.button == 1:
                self._input.leftclick = False
                self._input.leftclickletgo = True
            elif event.button == 2:
                pass
            elif event.button == 3:
                self._input.right = False

        elif event.type == MOUSEBUTTONDOWN: #event.button, #event.pos
            if event.button == 1: #l
                self._input.leftclick = True
                self._input.leftclickframe = True
                self._input.mouseclickposition = event.pos
            elif event.button == 2: #m
                pass
            elif event.button == 3: #r
                self._input.rightclick = True
                self._input.rightclickframe = True
                self._input.mouseclickposition = event.pos
            elif event.button == 4: #r
                self._input.mousewheel = 1
            elif event.button == 5: #r
                self._input.mousewheel = -1

        elif event.type == ACTIVEEVENT:
            if event.state == 1:
                if event.gain:
                    pass #self.on_mouse_focus()
                else:
                    pass #self.on_mouse_blur()
            elif event.state == 2:
                if event.gain:
                    pass #self.on_input_focus()
                else:
                    pass #self.on_input_blur()
            elif event.state == 4:
                if event.gain:
                    pass #self.on_restore()
                else:
                    pass #self.on_minimize()

if __name__ == "__main__" :
    print(sys.version)
    theApp = App()
    theApp.on_execute()
