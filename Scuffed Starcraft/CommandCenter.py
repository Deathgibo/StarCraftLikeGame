import Building
import Worker
import pygame
import numpy as np

class CommandCenter(Building.Building):
    def __init__(self, x, y, imgsurf):
        super().__init__(x, y, imgsurf)
        #render
        xsize = 200
        ysize = 200
        self.rect = pygame.Rect(x - xsize/2,y - ysize/2,xsize,ysize)
        self.img = imgsurf
        #stats
        self.health = 1500
        self.maxhealth = 1500
        #physics
        self.circlecenter = np.array([int(x),int(y)])
        self.radius = int(xsize/5)

    def update(self, input):
        self.handle_input(input)

    def handle_input(self, input):
        if self.selected:
            if input.keys[pygame.K_s]:
                print("creating worker!")

    def buildWorker(self, entityList, scvsurf, entityquadtree):
        #Create units and enemies and set up data structures
        # (1,2) = x,y coords on background surface, (3,4) = image size
        for x in range(50, 1000, 20):
            spotTaken = False
            for entity in entityList:
                #Some entity is already in that location
                if self.x + x == entity.rect[0]:
                    spotTaken = True

            # If we try to place a worker in the same spot of another the game will crash, here we have found an empty spot
            if spotTaken == False:
                # print(self.x + x, self.y + x)
                workerrect = pygame.Rect(self.x + x,self.y + x,45,45)
                worker1 = Worker.Worker(15,scvsurf,workerrect)
                entityList.append(worker1)
                entityquadtree.insertstart(worker1)  #W/out Node is none error
                #Stop looping
                return
