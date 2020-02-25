import pygame
from pygame.locals import *
import os
import sys
import math
import numpy as np

import Entity
import input
import mathfuncs

class App():
    def __init__(self):
        self._running = True
        self._display_surf = None
        self._image_surf = None
        self._cwdpath = None

    def on_init(self):
        if self.initpygame() is False:
            return False
        self._running = True

        #initialize window
        self._display_surf = pygame.display.set_mode((800,600), pygame.HWSURFACE | pygame.DOUBLEBUF | pygame.RESIZABLE)
        self._cwdpath = os.getcwd()
        pygame.display.set_caption("Scuffed StarCraft")
        pygame.display.set_icon(pygame.image.load(os.path.join(self._cwdpath,"Images","sc2.png")))

        #initialize other values
        self._cameraposition = np.array([0,0])
        self._camerachange = np.array([0,0])
        self._lasttime = 0
        self._input = input.input()

        self.load_media()
        self.load_entities()

    def initpygame(self):
        pygame.init()
        pygame.mixer.init()
        if pygame.mixer.get_init() is None:
            print("Error initializing mixer!\n")
            return False

    def load_entities(self):
        marinesurf = pygame.image.load(os.path.join(self._cwdpath,"Images","marauder.png")).convert()
        marinerect = pygame.Rect(0,0,45,45)
        entity1 = Entity.Entity(15, marinesurf,marinerect)
        self._entitylist = []
        self._entitylist.append(entity1)
        self.line = [(100,100),(200,200)]
        self.circle = (200,100,20)
        self.pumpcircle = (400,250,80)

    def load_media(self): #Load sounds and images
        self._image_surf = pygame.image.load(os.path.join(self._cwdpath,"Images","lilpump.jpg")).convert()
        self._image_bigmap = pygame.image.load(os.path.join(self._cwdpath,"Images","bigmap3.jpg")).convert()
        self._image_map = pygame.image.load(os.path.join(self._cwdpath,"Images","map3.jpg")).convert()
        self.sound_esketit = pygame.mixer.Sound(os.path.join(self._cwdpath,"Sounds","esketit.wav"))

    def on_update(self):
        cameraspeed = 6
        if pygame.mouse.get_pos()[0] < 50:
            self._cameraposition[0] = self._cameraposition[0] - cameraspeed
        if pygame.mouse.get_pos()[0] > self._display_surf.get_width() - 50:
            self._cameraposition[0] = self._cameraposition[0] + cameraspeed
        if pygame.mouse.get_pos()[1] < 50:
            self._cameraposition[1] = self._cameraposition[1] - cameraspeed
        if pygame.mouse.get_pos()[1] > self._display_surf.get_height() - 50:
            self._cameraposition[1] = self._cameraposition[1] + cameraspeed

        if self._cameraposition[0] < 0:
            self._cameraposition[0] = 0
        if self._cameraposition[0] > self._image_bigmap.get_width():
            self._cameraposition[0] = self._image_bigmap.get_width()
        if self._cameraposition[1] < 0:
            self._cameraposition[1] = 0
        if self._cameraposition[1] > self._image_bigmap.get_height():
            self._cameraposition[1] = self._image_bigmap.get_height()

        answer = mathfuncs.mathfuncs.circlesegcollision(self._entitylist[0].radius,self._entitylist[0].x,self._entitylist[0].y,
        self.line[0][0],self.line[0][1],self.line[1][0],self.line[1][1])
        answer2 = mathfuncs.mathfuncs.circlecirclecollision((self._entitylist[0].x,self._entitylist[0].y,
         self._entitylist[0].radius), self.circle)
        #print("Line collision: %d Circle collision: %d" % (answer, answer2))
        if mathfuncs.mathfuncs.circlecirclecollision((self._entitylist[0].x,self._entitylist[0].y, self._entitylist[0].radius), self.pumpcircle):
            self.sound_esketit.set_volume(.05)
            self.sound_esketit.play();

        #if not pygame.mixer.music.get_busy():
        #    pygame.mixer.music.load(os.path.join(self._cwdpath,"Sounds","100 on my wrist.wav"))
        #    pygame.mixer.music.set_volume(0.5)
        #    pygame.mixer.music.play()
            #self.sound_esketit.set_volume(.05)
            #self.sound_esketit.play();

    def on_render(self):
        self._display_surf.fill((255,255,255))
        #self.drawimagerect(pygame.Rect(0,0,self._display_surf.get_width(),self._display_surf.get_height()),self._image_map)
        widthsub = 0
        if self._cameraposition[0] + self._display_surf.get_width() > self._image_bigmap.get_width():
            widthsub = self._cameraposition[0] + self._display_surf.get_width() - self._image_bigmap.get_width()
        heightsub = 0
        if self._cameraposition[1] + self._display_surf.get_height() > self._image_bigmap.get_height():
            heightsub = self._cameraposition[1] + self._display_surf.get_height() - self._image_bigmap.get_height()

        rectclip = pygame.Rect(self._cameraposition[0],self._cameraposition[1],self._display_surf.get_width() - widthsub,self._display_surf.get_height() - heightsub)
        #self._image_bigmap.set_clip(rectclip)
        #print(rectclip)
        subimage = self._image_bigmap.subsurface(rectclip)
        #newimage = pygame.transform.scale(subimage,(800,600))
        self._display_surf.blit(subimage,(0,0))
        self.drawimagerect(pygame.Rect(350,200,100,100),self._image_surf)
        for x in self._entitylist:
            self.drawimagerect(x.rect,x.img)
            pygame.draw.circle(self._display_surf, (0,255,0),(x.x,x.y), x.radius,1)
        pygame.draw.line(self._display_surf,(0,0,0),(100,100),(200,200))
        pygame.draw.circle(self._display_surf, (0,0,255),self.circle[:2], self.circle[2],1)

        pygame.display.flip()

    def drawimagerect(self, rect, image): #renders an image on a rect while preserving original image size
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
            self._display_surf = pygame.display.set_mode(event.size, pygame.HWSURFACE | pygame.DOUBLEBUF | pygame.RESIZABLE)
            pass

        elif event.type == KEYUP:
            self._input.keys[event.key] = 0

        elif event.type == KEYDOWN: #event.key (pygame.K_x) event.mod == pygame.KMOD_LSHIFT
            speed = 10
            self._input.keys[event.key] = 1
            if event.key == pygame.K_w:
                self._entitylist[0].Move(0,-speed)
            if event.key == pygame.K_a:
                self._entitylist[0].Move(-speed,0)
            if event.key == pygame.K_s:
                self._entitylist[0].Move(0,speed)
            if event.key == pygame.K_d:
                self._entitylist[0].Move(speed,0)
            if event.key == pygame.K_ESCAPE:
                self.on_exit()

        elif event.type == MOUSEMOTION: #event.buttons, event.pos, event.rel
            self._input.mouseposition = event.pos
            self._input.mousechange = event.rel

        elif event.type == MOUSEBUTTONUP: #event.button, #event.pos
            if event.button == 1:
                self._input.leftclick = False
            elif event.button == 2:
                pass
            elif event.button == 3:
                self._input.right = False

        elif event.type == MOUSEBUTTONDOWN: #event.button, #event.pos
            if event.button == 1: #l
                self._input.leftclick = True
            elif event.button == 2: #m
                pass
            elif event.button == 3: #r
                self._input.right = True

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
