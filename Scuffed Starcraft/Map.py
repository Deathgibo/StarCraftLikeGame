#contains map and mini map
#the map is responsible for rendering the map, moving the map, zooming in or out of the map
#the map will also hold physics which will be for now an array of segments
#map will hold camera information like position, zoom
import numpy as np
import pygame
from pygame.locals import *

class Map:
    def __init__(self, x, y):
        #render stuff
        self._renderdimensions = np.array([x,y]) # 800,600
        self._mapimage = None #is pygame image so holds dimensions as well
        #camera stuff
        self._cameraposition = np.array([0,0])
        self._cameraspeed = 12
        self._camerazoom = 1.0

    def handleinput(self, input, displaysurf, mouseimg, mouseimglist, editmode): #returns tuple(mouseimgvalue, mousexoffset,mouseyoffset)
        #handle camera changes
        movelength = 20
        val = 0
        xdir = False
        ydir = False
        left = False
        up = False
        offset = np.array([10,10])
        if input.mouseposition[0] < movelength:
            xdir = True
            left = True
            self._cameraposition[0] = self._cameraposition[0] - self._cameraspeed
        if input.mouseposition[0] > displaysurf.get_width() - movelength:
            xdir = True
            self._cameraposition[0] = self._cameraposition[0] + self._cameraspeed
        if input.mouseposition[1] < movelength:
            ydir = True
            up = True
            self._cameraposition[1] = self._cameraposition[1] - self._cameraspeed
        if input.mouseposition[1] > displaysurf.get_height() - movelength:
            ydir = True
            self._cameraposition[1] = self._cameraposition[1] + self._cameraspeed

        if xdir and ydir:
            if left and up or not left and not up:
                val = 4
            else:
                val = 3
            if left:
                offset[0] = 10
            else:
                offset[0] = -10
            if up:
                offset[1] = 10
            else:
                offset[1] = -10
        elif xdir:
            val = 2
            if left:
                offset[0] = 10
            else:
                offset[0] = -10
            offset[1] = 0
        elif ydir:
            val = 1
            if up:
                offset[1] = 10
            else:
                offset[1] = -10
            offset[0] = 0

        #handle minimouse clicks
        #if your mouse is in mini map and you click move the camera position accordingly
        if not editmode:
            if self.ispointonminimap(input.mouseclickposition[0],input.mouseclickposition[1], displaysurf):
                if input.leftclick == True:
                    #get percent and move percent
                    #x (13,118)
                    xpercent = float((input.mouseposition[0] - 13) / 105.0)#MINI
                    ypercent = float((input.mouseposition[1] - (displaysurf.get_height() - 150.0)) / 150.0)#MINI
                    self._cameraposition[0] = int(self._mapimage.get_width() * xpercent) - (self._renderdimensions[0]/2)
                    self._cameraposition[1] = int(self._mapimage.get_height() * ypercent) - (self._renderdimensions[1]/2)

        if self._cameraposition[0] < 0:
            self._cameraposition[0] = 0
        if self._cameraposition[0] > self._mapimage.get_width() - self._renderdimensions[0]: #displaysurf.get_width()
            self._cameraposition[0] = self._mapimage.get_width() - self._renderdimensions[0]
        if self._cameraposition[1] < 0:
            self._cameraposition[1] = 0
        if self._cameraposition[1] > self._mapimage.get_height() - self._renderdimensions[1]: #displaysurf.get_height()
            self._cameraposition[1] = self._mapimage.get_height() - self._renderdimensions[1]

        #camera zoom
        if input.mousewheel == -1:
            self._camerazoom = self._camerazoom - 0.01;
        if input.mousewheel == 1:
            self._camerazoom = self._camerazoom + 1.0;

        #self._renderdimensions[0] = self._renderdimensions[0] * self._camerazoom
        #self._renderdimensions[1] = self._renderdimensions[1] * self._camerazoom

        return (val,offset[0],offset[1])

    def render(self, displaysurf):
        #calculate clip rectangle if it goes out of bounds make sure to fix that
        widthclip = 0
        heightclip = 0
        #displaysurf.get_width()
        if self._cameraposition[0] + self._renderdimensions[0] > self._mapimage.get_width():
            widthclip = self._cameraposition[0] + self._renderdimensions[0] - self._mapimage.get_width()
        if self._cameraposition[1] + self._renderdimensions[1] > self._mapimage.get_height():
            heightclip = self._cameraposition[1] + self._renderdimensions[1] - self._mapimage.get_height()

        rectclip = pygame.Rect(self._cameraposition[0],self._cameraposition[1],self._renderdimensions[0] - widthclip, self._renderdimensions[1] - heightclip)

        subimage = self._mapimage.subsurface(rectclip)
        #newimage = pygame.transform.scale(subimage,(displaysurf.get_width(),displaysurf.get_height()))
        displaysurf.blit(subimage,(0,0))

    #ORIGINAL
    # def renderminimap(self, displaysurf):
    #     miniheight = 150
    #     miniwidth = 150
    #     minimapimg = pygame.transform.scale(self._mapimage,(miniheight,miniwidth))
    #     displaysurf.blit(minimapimg,(displaysurf.get_width() - miniwidth,displaysurf.get_height() - miniheight))

    def renderminimap(self, displaysurf):
        #Set-up Minimap dimensions based on screen size
        if displaysurf.get_rect().size == (800,600):
            #Minimap dimensions for 800x600
            miniheight = 150
            miniwidth = 105
            minimapimg = pygame.transform.scale(self._mapimage,(miniwidth,miniheight))
            displaysurf.blit(minimapimg,(13, displaysurf.get_height() - miniheight - 10, miniwidth, miniheight))

        elif displaysurf.get_rect().size == (1350,750):
            #Minimap dimensions for 1350x750
            miniheight = 180
            miniwidth = 180
            minimapimg = pygame.transform.scale(self._mapimage,(miniwidth,miniheight))
            displaysurf.blit(minimapimg, (22, displaysurf.get_height() - miniheight - 12, miniwidth, miniheight))

    def windowtoworldtransform(self, x, y, displaysurf):
        if (x < 0 or x > displaysurf.get_width()) or (y < 0 or y > displaysurf.get_height()):
            print("not given window coordinates in Map.py windowtoworldtransform...")
        xpercent = float(x / displaysurf.get_width())
        ypercent = float(y / displaysurf.get_height())
        return (self._cameraposition[0] + (xpercent * self._renderdimensions[0]), self._cameraposition[1] + (ypercent * self._renderdimensions[1]))

    def worldtowindowtransform(self, x, y):
        pass
        #subtract cameraposition

    def ispointonminimap(self, px, py, displaysurf):#MINI
        if px > 12 and px < 105 + 13 and py > displaysurf.get_height() - 150 - 10:
            return True
        return False
