import pygame                   #init(), display()
from pygame.locals import *     #QUIT, USEREVENT, ect.
import pygame.mixer
import os                       #getcwd(), os.environ
import sys                      #version()
import math
import numpy as np
import time

import Entity
import input
import mathfuncs
import Map
import Worker
import Marauder
import Marine
import playerinfo
import Mineral
import Overlay
import Building
import CommandCenter
import Quadtree
import MapGraph

class App():
    def __init__(self):
        self._running = True
        self._display_surf = None       #UI Surface/Foreground/Display Window (800x600)
        self._display_surfrender = None #Background/Map
        self._cwdpath = None            #Get working directory to retrieve images

    def on_init(self):
        #(from: on_execute)
        #Puts pygame window in the middle
        os.environ['SDL_VIDEO_CENTERED'] = '1'

        #Check that Mixer was initiated. on_execute will fail/stop the program otherwise.
        if self.initpygame() is False:
            return False

        #Initialize Game Window
        # (Not Used Yet!) Video Display Object: If called before pygame.display.set_mode() can provide user's screen resolution
        #initialize window
        self._infoObject = pygame.display.Info()
        # Map Image in Background (Needs to be rendered)
        # Window Size
        resolutionx = 1000
        resolutiony = 800
        self._display_surfrender = pygame.Surface((resolutionx, resolutiony))  # Map 800,600
        self._display_surf = pygame.display.set_mode((800, 600), pygame.RESIZABLE)
        # CWD path for images
        self._cwdpath = os.getcwd()
        pygame.display.set_caption("Scuffed StarCraft")
        pygame.display.set_icon(pygame.image.load(os.path.join(self._cwdpath,"Images","sc2.png")))
        #Ignore cursor for now need to figure out a way to do it on the OS probably because it lags
        #pygame.mouse.set_visible(False)
        pygame.event.set_grab(True)

        #Initialize FPS value (see .handlefps())
        #initialize other values
        self._lasttime = 0

        self._input = input.input()

        self._playerinfo = playerinfo.playerinfo()

        #Initialize Map Dimensions and Camera Set-Up
        self.map = Map.Map(resolutionx, resolutiony)

        #Initialize Overlay (UI)
        self.overlay = Overlay.Overlay()
        self.overlay.load_media(self._cwdpath)

        #Initialize Cursor/Map/Sounds and other general media
        self.load_media()

        #Initialize Troops and smaller entities
        self.load_entities()

        #Initialize Map resources
        self.load_resources()
        self.load_buildings()

        #Initialize Graph for Map
        self.load_Graph()

        #GAME OPTIONS
        self.overlay_enable = True #Toggles overlay
        self.worldgraph_editmode = True #Toggles being able to edit the world graph nodes
        self.worldgraph_render = False #Toggles being able to see the world graph
        self.bspgraph_render = False #Toggles being able to see the bsp graph

        self.clickcount = 0
        self.clickpoints = []

    def initpygame(self):
        #(from: on_execute-> on_init)
        #Check that Mixer was initiated. on_execute will fail/stop the program otherwise.
        pygame.init()
        pygame.mixer.init()
        if pygame.mixer.get_init() is None:
            print("Error initializing mixer!\n")
            return False

    def load_Graph(self):
        self.worldgraph = MapGraph.MapGraph()


    def load_buildings(self):
        self._building_list = []
        building1 = CommandCenter.CommandCenter(900,700,self._commandcenterimg)
        self._building_list.append(building1)

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
        #Load entity images
        maraudersurf = pygame.image.load(os.path.join(self._cwdpath,"Images","maraudert.png")).convert_alpha()
        scvsurf = pygame.image.load(os.path.join(self._cwdpath,"Images","scv2.png")).convert_alpha()
        marinesurf = pygame.image.load(os.path.join(self._cwdpath,"Images","marine.png")).convert_alpha()

        #Create units and enemies and set up data structures
        marinerect = pygame.Rect(700,300,45,45)
        worker1 = Worker.Worker(15,scvsurf,marinerect)
        marinerect = pygame.Rect(700,350,45,45)
        worker2 = Worker.Worker(15,scvsurf,marinerect)
        self._entitylist = []
        self._entitylist.append(worker1)
        self._entitylist.append(worker2)
        thesize = 5
        #Fill entity List structure
        for x in range(0,thesize):
            marinerect = pygame.Rect(100,500 + x*30,50,50)
            entity1 = Marine.Marine(15,marinesurf,marinerect)
            self._entitylist.append(entity1)

        #Initialize and fill the entity QuadTree
        self._entityquadtree = Quadtree.Quadtree()
        for x in range(0,len(self._entitylist)):
            self._entityquadtree.insertstart(self._entitylist[x])

        #Fill enemy List structure
        self._enemyentitylist = []
        for x in range(0,thesize):
            marinerect = pygame.Rect(400,250 + x*30,50,50)
            entity1 = Marauder.Marauder(15,maraudersurf,marinerect)
            self._enemyentitylist.append(entity1)

        #Initialize and fill the enemy QuadTree
        self._enemyentityquadtree = Quadtree.Quadtree()
        for x in range(0,len(self._enemyentitylist)):
            self._enemyentityquadtree.insertstart(self._enemyentitylist[x])

    def load_media(self):
        # (from: on_execute-> on_init)
        # Load general sounds and images
        self._mineralimg = pygame.image.load(os.path.join(self._cwdpath, "Images", "mineralt.png")).convert_alpha()

        # Background Map (stored in map object)
        self.map._mapimage = pygame.image.load(
            os.path.join(self._cwdpath, "Images", "NeoPlanetSx2.png")).convert()  # bigmap3.jpg
        self._commandcenterimg = pygame.image.load(
            os.path.join(self._cwdpath, "Images", "commandcentert.png")).convert_alpha()
        
        # Directional Green Cursor
        self._mouseimg1 = pygame.image.load(os.path.join(self._cwdpath, "Images", "mouse1t.png")).convert_alpha()
        self._mouseimg2 = pygame.image.load(os.path.join(self._cwdpath, "Images", "mouse2t.png")).convert_alpha()
        self._mouseimg3 = pygame.image.load(os.path.join(self._cwdpath, "Images", "mouse3t.png")).convert_alpha()
        self._mouseimg4 = pygame.image.load(os.path.join(self._cwdpath, "Images", "mouse4t.png")).convert_alpha()
        self._mouseimg5 = pygame.image.load(os.path.join(self._cwdpath, "Images", "mouse5t.png")).convert_alpha()
        self._mouseimgoffset = np.array([10, 10])
        self._mouseimglist = [self._mouseimg1, self._mouseimg2, self._mouseimg3, self._mouseimg4, self._mouseimg5]
        self._mouseimgcurrent = self._mouseimg1
        self.sound_esketit = pygame.mixer.Sound(os.path.join(self._cwdpath, "Sounds", "esketit.wav"))
        
    def on_update(self):
        #KEEP input update at top
        #update input
        self._input.update()
        self.worldgraph.clicklocationfound = False
        #update map and mouse information
        mouseinfo = self.map.handleinput(self._input, self._display_surf,self._mouseimgcurrent, self._mouseimglist, self.worldgraph_editmode)
        self._mouseimgcurrent = self._mouseimglist[mouseinfo[0]]
        self._mouseimgoffset[0] = mouseinfo[1]
        self._mouseimgoffset[1] = mouseinfo[2]

        #update playerinformation
        self._playerinfo.update(self._input, self._entitylist,self.map,self._display_surf, self._building_list,self._enemyentitylist,
                                self._entityquadtree,self._enemyentityquadtree)


        #update graph creating
        if self.worldgraph_editmode:
            self.worldgraph.update(self._input, self.map, self._display_surf, self._cwdpath,self._playerinfo)

        #if self._input.keys[pygame.K_y]:
            #self.worldgraph.GetShortestPath()

        """if self._input.leftclickframe:
            self.clickcount = self.clickcount + 1
            self.clickpoints.append(self.map.windowtoworldtransform(self._input.mouseposition[0],self._input.mouseposition[1],self._display_surf))
            if self.clickcount >= 4:
                if mathfuncs.mathfuncs.segsegintersection(self.clickpoints[0],self.clickpoints[1],self.clickpoints[2],self.clickpoints[3]):
                    print("intersection!")
                else:
                    print("no intersection!")
                self.clickcount = 0
                self.clickpoints.clear()"""

        """
        quad tree update iterate implementation (slower)
        frametime = time.time()
        for unit in self._entitylist:
            pass
        print(time.time() - frametime)
        frametime = time.time()
        gen = self._entityquadtree.iterategen()
        for unit in gen:
            pass
        print(time.time() - frametime)
        """

        #units
        starttime = time.time()
        for units in self._entitylist:
            units.update(self._input,self.minerallist, self.map,self._display_surf, self._enemyentitylist, self._entitylist, self._enemyentityquadtree, self._entityquadtree,
                         self.worldgraph)
        #print(time.time() - starttime)
        #remove dead units
        count = 0
        for x in range(0,len(self._entitylist)):
            if self._entitylist[x - count].alive == False:
                self._entityquadtree.deletestart(self._entitylist[x - count])
                self._entitylist.pop(x - count)
                count = count + 1

        #enemy units
        for units in self._enemyentitylist:
            units.update(self._input,self.minerallist, self.map,self._display_surf, self._entitylist, self._enemyentitylist, self._entityquadtree, self._enemyentityquadtree,
                          self.worldgraph)

        #remove dead enemy units
        count = 0
        for x in range(0,len(self._enemyentitylist)):
            if self._enemyentitylist[x - count].alive == False:
                self._enemyentityquadtree.deletestart(self._enemyentitylist[x - count])
                self._enemyentitylist.pop(x - count)
                count = count + 1


        #buildings
        for buildings in self._building_list:
            buildings.update(self._input)


        """
        just here to remember sound syntax
        if not pygame.mixer.music.get_busy():
            pygame.mixer.music.load(os.path.join(self._cwdpath,"Sounds","100 on my wrist.wav"))
            pygame.mixer.music.set_volume(0.5)
            pygame.mixer.music.play()
            self.sound_esketit.set_volume(.05)
            self.sound_esketit.play();
        """

    def on_render(self):
        # (from: on_execute)

        """ About Render
        Pretty much we have an x by y resolution image, self._display_surfrender, this
        is the resolution of the world we render and can change. This is where you render the "world" on.
        So thats everything in the world like, minerals, units, buildings, etc. Then
        Once the resolution image is filled you remap it to the screen size, resized_screen. After that
        you can do UI stuff because it would be weird to remap the UI when it just
        needs to spread over the screen size.
        """

        #map (set up camera dimensions on map to avoid going out of bounds)
        self.map.render(self._display_surfrender)

        #units
        for x in self._entitylist:
            x.render(self)

        #enemy units
        for x in self._enemyentitylist:
            x.render(self)

        #buildings
        for buildings in self._building_list:
            buildings.render(self)

        #minerals
        for x in self.minerallist:
            x.render(self)

        #for x in self.clickpoints:
            #pygame.draw.circle(self._display_surfrender,(0,0,0), (int(x[0] - self.map._cameraposition[0]),int(x[1] - self.map._cameraposition[1])), 5, 1)

        #graph
        if self._input.keysframe[pygame.K_i][0]:
            self.bspgraph_render = not self.bspgraph_render
        if self.bspgraph_render:
            self.worldgraph.renderbsp(self._display_surfrender, self.map)
        if self._input.keysframe[pygame.K_o][0]:
            self.worldgraph_render = not self.worldgraph_render
        if self.worldgraph_render:
            self.worldgraph.render(self._display_surfrender, self.map)
        #map cont. - render map to fit window size
        # MUST BE AFTER rendering units and minerals or they will not appear!
        #transform surface to fit screen size
        resized_screen = pygame.transform.scale(self._display_surfrender, (self._display_surf.get_width(),self._display_surf.get_height()))
        self._display_surf.blit(resized_screen, (0, 0))

        #UI - ORDER MATTERS!
        #bottom Overlay
        if self._input.keysframe[pygame.K_MINUS][0]:
            self.overlay_enable = not self.overlay_enable
        if self.overlay_enable:
            self.overlay.renderBottomOverlay(self._display_surf)
            self.overlay.renderResources(self._display_surf, self._playerinfo)
            self.overlay.renderGameClock(self._display_surf)
            self.overlay.renderSelectedItem(self._display_surf, self._playerinfo._selectedlist, self._playerinfo._selectedbuildinglist)
            #self.overlay.renderTemplate(self._display_surf) #If you want to see boxes

        #UI
        #mini map
            self.map.renderminimap(self._display_surf)
        #green box
        self._playerinfo.render(self._display_surf)

        #cursor - Ignore cursor for now need to figure out a way to do it on the OS probably because it lags
        mousesize = 44
        #self.drawimagerectgui(pygame.Rect(self._input.mouseposition[0] - int(mousesize/2) + self._mouseimgoffset[0],
          #self._input.mouseposition[1] - int(mousesize/2) + self._mouseimgoffset[1],mousesize,mousesize),self._mouseimgcurrent)

        #self.drawimagerectgui(pygame.Rect(self._input.mouseposition[0] - int(mousesize/2) + self._mouseimgoffset[0],
          #self._input.mouseposition[1] - int(mousesize/2) + self._mouseimgoffset[1],mousesize,mousesize),self._mouseimgcurrent)


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
        #(from: on_execute)
        #Quit Mixer and PyGames
        pygame.quit()
        pygame.mixer.quit()

    def draw_text(self, text, size, width_loc, height_loc, c):
        font = pygame.font.Font(pygame.font.get_default_font(), size)
        text_surface = font.render(text, True, c)
        self._display_surf.blit(text_surface, (width_loc, height_loc))

    def draw_rect(self, fill_color, border_color, rect, border=1):
        self._display_surf.fill(border_color, rect)
        self._display_surf.fill(fill_color, rect.inflate(-border * 2, -border * 2))

    def menu(self):
        # Display Start Menu

        title = pygame.image.load(os.path.join(self._cwdpath, "Images", "Title.png")).convert_alpha()
        background = pygame.image.load(os.path.join(self._cwdpath, "Images", "StartMenu.png")).convert()
        background_rect = background.get_rect()

        self._display_surf.blit(background, background_rect)
        self._display_surf.blit(title, (250, 40))

        # Menu Options
        # pygame.draw.rect(screen, [red, green, blue], [left, top, width, height], filled)
        top_rect = pygame.draw.rect(self._display_surf, (0, 0, 255), (240, 294, 321, 35))
        bottom_rect = pygame.draw.rect(self._display_surf, (0, 0, 255), (280, 345, 240, 35))
        self.draw_rect((0, 0, 255), (255, 255, 255), top_rect, 2)
        self.draw_rect((0, 0, 255), (255, 255, 255), bottom_rect, 2)
        self.draw_text("PRESS [ENTER] TO BEGIN", 24, 245, 299, (255, 255, 255))
        self.draw_text("PRESS [Q] TO QUIT", 24, 285, 350, (255, 255, 255))

        pygame.display.update()

        while True:
            event = pygame.event.poll()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    break
                elif event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()
            elif event.type == QUIT:
                pygame.quit()
                sys.exit()

    def help(self):
        title = pygame.image.load(os.path.join(self._cwdpath, "Images", "HelpScreenTitle.png")).convert_alpha()

        while True:
            event = pygame.event.poll()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    break
                elif event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()
            elif event.type == QUIT:
                pygame.quit()
                sys.exit()

            self._display_surf.fill((0, 0, 0))
            self._display_surf.blit(title, (250, 40))

            # Menu Options
            # pygame.draw.rect(screen, [red, green, blue], [left, top, width, height], filled)
            top_rect = pygame.draw.rect(self._display_surf, (0, 0, 255), (240, 214, 380, 35))
            bottom_rect = pygame.draw.rect(self._display_surf, (0, 0, 255), (280, 265, 240, 35))
            self.draw_rect((0, 0, 255), (255, 255, 255), top_rect, 2)
            self.draw_rect((0, 0, 255), (255, 255, 255), bottom_rect, 2)
            self.draw_text("PRESS [ENTER] TO CONTINUE", 24, 245, 219, (255, 255, 255))
            self.draw_text("PRESS [Q] TO QUIT", 24, 285, 270, (255, 255, 255))

            self.draw_text("Here are the instructions", 24, 145, 330, (255, 255, 255))

            pygame.display.update()

    def pause(self):
        paused = True
        title = pygame.image.load(os.path.join(self._cwdpath, "Images", "PauseTitle.png")).convert_alpha()

        while paused:
            event = pygame.event.poll()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    paused = False
                elif event.key == pygame.K_h:
                    self.help()
                elif event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()
            elif event.type == QUIT:
                pygame.quit()
                sys.exit()

            self._display_surf.fill((0, 0, 0))
            self._display_surf.blit(title, (250, 40))

            # Menu Options
            # pygame.draw.rect(screen, [red, green, blue], [left, top, width, height], filled)
            top_rect = pygame.draw.rect(self._display_surf, (0, 0, 255), (240, 294, 380, 35))
            help_rect = pygame.draw.rect(self._display_surf, (0, 0, 255), (280, 345, 260, 35))
            bottom_rect = pygame.draw.rect(self._display_surf, (0, 0, 255), (280, 395, 240, 35))
            self.draw_rect((0, 0, 255), (255, 255, 255), top_rect, 2)
            self.draw_rect((0, 0, 255), (255, 255, 255), help_rect, 2)
            self.draw_rect((0, 0, 255), (255, 255, 255), bottom_rect, 2)
            self.draw_text("PRESS [ENTER] TO CONTINUE", 24, 245, 299, (255, 255, 255))
            self.draw_text("PRESS [H] FOR HELP", 24, 285, 350, (255, 255, 255))
            self.draw_text("PRESS [Q] TO QUIT", 24, 285, 400, (255, 255, 255))

            pygame.display.update()

    def on_execute(self):
        #Initialize the window, camera, media and other entities. Return false if
        #there is an error on initiating Mixer.
        if self.on_init() == False:
            self._running = False

        start = True
            self._input.reset()
            for event in pygame.event.get():
                self.on_event(event)

            # Start Game Menu
            if start:
                self.menu()
                start = False

            self.on_update()
            self.on_render()
            self.handlefps()

        # Quit Mixer and PyGames
        self.on_cleanup()

    def handlefps(self):
        #(from: on_execute)
        #Display user's FPS in upper right-hand corner of the screen
        frametime = pygame.time.get_ticks() - self._lasttime
        if frametime != 0:
            fps = 1000 / frametime #1000 miliseconds = 1 second, so
            pygame.display.set_caption("Scuffed StarCraft fps: %f" % fps)
            if frametime < 17:
                pygame.time.delay(17 - frametime)
        self._lasttime = pygame.time.get_ticks()

    def on_event(self, event):
        #(from: on_execute)

        #INPUT HANDLING FUNCTION
        #Change _running to false to get out of infinite loop and exit program
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
            self._input.keysframe[event.key] = (self._input.keysframe[event.key][0],False)

        elif event.type == KEYDOWN: #event.key (pygame.K_x) event.mod == pygame.KMOD_LSHIFT
            speed = 10
            self._input.keys[event.key] = 1
            self._input.keysframe[event.key] = (True,True)

            if event.key == pygame.K_1:
                pygame.display.set_mode((800, 600),  pygame.RESIZABLE)
            if event.key == pygame.K_2:
                pygame.display.set_mode((1350,750),  pygame.RESIZABLE)
                pygame.display.update()
            if event.key == pygame.K_ESCAPE:
                self.on_exit()
            if event.key == pygame.K_p:
                self.pause()

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
