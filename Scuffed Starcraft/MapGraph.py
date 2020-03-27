#This class handles the graph of vertices and edges over the world which is used for the unit movement algorithms
import AdjacencyList
import pygame
import mathfuncs
import os
import PriorityQueue
import time
import BSP
import copy

"""
This class holds the world graph, bsp graph, and the actual bsp tree
This class also can create the graphs with a basic input system
This class is what the units call when they move, UnitPath, which gives them
their path to go
Also holds the dijkstra algorithm
"""

""" MapGraph Instructions
**make sure self.worldgraph_editmode is True in main.py

-editing map-
v - press v then click to place vertex

d - press d then click to delete vertex and every edge with it

w - press w then click two vertices and if they are valid create edge for bspgraph

e - press e then click two vertices and if they are valid create edge between them for worldgraph

r - press r then click two vertices to delete the edge between them for both graphs

p - will print graph information to file mapgraph.txt

n - create box 2 clicks

m - delete box

b - bind physics vertex with normal vertex

-rendering-
o - to toggle rendering the world graph

i - to toggle rendering the bsp graph

-algorithms-
y - press y then click two vertices to highlight the shortest path between them!

c - press c and click to see all visible vertices from clicked point

u - press you and click any two locations, will highlight vertices unit will walk to, if any
"""

class MapGraph():
    def __init__(self):
        #helper attributes
        self.key = -1 # -1:None, 0:v, 1:d, 2:e, 3:c
        self.keyletgo = -1
        self.clicky = False
        self.vertexindex = -1

        self.adjlist = AdjacencyList.AdjacencyList()    #world adjlist
        self.adjlistbsp = AdjacencyList.AdjacencyList() #bsp adjlist
        self.adjlistphysics = AdjacencyList.AdjacencyList()
        self.physicsboxes = [] #holds tuples(nparray box, list of vertex indices referencing adjlistbsp)
        self.createmap() #loads both adjlist
        self.adjlistbsptree = AdjacencyList.AdjacencyList()
        """for x in self.adjlistbsp.vtable:
            self.adjlistbsptree.addvertex(x.pos[0],x.pos[1])
        for x in range(0,len(self.adjlistbsp.adjlist)):
            for y in range(0,len(self.adjlistbsp.adjlist[x])):
                if y > x:
                    self.adjlistbsptree.addedge(x,self.adjlistbsp.adjlist[x][y][0])"""
        self.adjlistbsptree = copy.deepcopy(self.adjlistbsp)
        self.bsp = BSP.BSP(self.adjlistbsptree) #creates bsp tree
        """l = len(self.adjlist.vtable)
        for x in range(len(self.adjlistbsp.vtable) - 1, l - 1, -1):
            self.adjlistbsp.deletevertex(x)"""

        self.clicklocationfound = False #resets at start of every frame, lets other units know not to calculate clickpoly
        self.clicknewlocation = (0,0)
        self.pathlocation = []
        #print(len(self.adjlistbsp.vtable))
        #print(len(self.adjlist.vtable))
        #self.createadjlist()

    def createadjlist(self):
        originalsize = len(self.adjlist.vtable)
        for x in range(0,len(self.adjlist.vtable)):
            visiblelist = []
            self.bsp.closestnodes((self.adjlist.vtable[x].pos[0],self.adjlist.vtable[x].pos[1]), visiblelist)
            for y in visiblelist:
                if y < originalsize:
                    self.adjlist.addedge(x,y)

    def update(self, input, map, displaysurf, cwdpath, playerinfo):
        if input.keys[pygame.K_z]:
            self.key = -1
        elif input.keys[pygame.K_v]:
            self.key = 0
        elif input.keys[pygame.K_d]:
            self.key = 1
        elif input.keys[pygame.K_e]:
            self.key = 2
        elif input.keys[pygame.K_r]:
            self.key = 3
        elif input.keys[pygame.K_p]:
            self.key = 4
        elif input.keys[pygame.K_y]:
            self.key = 5
        elif input.keys[pygame.K_c]:
            self.key = 6
        elif input.keys[pygame.K_w]:
            self.key = 7
        elif input.keys[pygame.K_u]:
            self.key = 8
        elif input.keys[pygame.K_q]:
            self.key = 9
        elif input.keys[pygame.K_b]:
            self.key = 10
        elif input.keys[pygame.K_n]:
            self.key = 11
        elif input.keys[pygame.K_m]:
            self.key = 12


        #clicked
        if input.leftclickframe:
            dontreset = False
            worldcoords = map.windowtoworldtransform(input.mouseposition[0],input.mouseposition[1], displaysurf)
            #v
            if self.key == 0:
                self.adjlist.addvertex(worldcoords[0],worldcoords[1])
                self.adjlistbsp.addvertex(worldcoords[0],worldcoords[1])
            #m
            if self.key == 12:
                counter = 0
                print("m")
                for x in range(0,len(self.physicsboxes)):
                    if mathfuncs.mathfuncs.pointrectanycollision(worldcoords, self.physicsboxes[x - counter][0]):
                        self.physicsboxes.pop(x - counter)
                        counter = counter + 1
            #n
            elif self.key == 11:
                dontreset = True
                if self.clicky:
                    box = pygame.Rect(self.vertexindex[0],self.vertexindex[1], abs(worldcoords[0] - self.vertexindex[0]), abs(self.vertexindex[1] - worldcoords[1]))
                    l = []
                    for x in range(0,len(self.adjlistbsp.vtable)):
                        if mathfuncs.mathfuncs.pointrectanycollision(self.adjlistbsp.vtable[x].pos, box):
                            l.append(x)
                    self.physicsboxes.append((box,l))
                    dontreset = False
                    self.vertexindex = -1
                    self.clicky = False
                else:
                    self.vertexindex = worldcoords
                    self.clicky = True
            #b
            elif self.key == 10:
                dontreset = True
                if self.clicky:
                    index2 = self.indexclicked(worldcoords)
                    if index2 == -1:
                        pass
                    else:
                        v = PriorityQueue.Vertex(self.vertexindex[0], self.vertexindex[1])
                        if len(self.adjlistphysics.vtable) > index2:
                            self.adjlistphysics.vtable[index2] = v
                        else:
                            self.adjlistphysics.addsize(index2)
                            self.adjlistphysics.vtable[index2] = v

                    self.vertexindex = -1
                    self.clicky = False
                else:
                    self.vertexindex = worldcoords
                    self.clicky = True
            #c
            elif self.key == 6:
                for vertex in self.adjlist.vtable:
                    vertex.highlight = False
                l = []
                starttime = time.time()
                for x in range(0,2):
                    self.bsp.closestnodes((worldcoords[0],worldcoords[1]), l)
                #print("total time %f" % (time.time() - starttime))
                for x in l:
                    if x < len(self.adjlist.vtable):
                        self.adjlist.vtable[x].highlight = True
            #d
            elif self.key == 1:
                clickcircle = (worldcoords[0],worldcoords[1], 20)
                for x in range(0,len(self.adjlist.vtable)):
                    if mathfuncs.mathfuncs.pointcirclecollision((self.adjlist.vtable[x].pos[0],self.adjlist.vtable[x].pos[1]), clickcircle):
                        self.adjlist.deletevertex(x)
                        break
                for x in range(0,len(self.adjlistbsp.vtable)):
                    if mathfuncs.mathfuncs.pointcirclecollision((self.adjlistbsp.vtable[x].pos[0],self.adjlistbsp.vtable[x].pos[1]), clickcircle):
                        self.adjlistbsp.deletevertex(x)
                        self.adjlistphysics.vtable[x] = None
                        break
            #e
            elif self.key == 2:
                dontreset = True
                if self.clicky:
                    index2 = self.indexclicked(worldcoords)
                    if self.vertexindex == -1 or index2 == -1:
                        pass
                    elif self.vertexindex == index2:
                        pass
                    else:
                        self.adjlist.addedge(self.vertexindex,index2)

                    self.vertexindex = -1
                    self.clicky = False
                else:
                    self.vertexindex = self.indexclicked(worldcoords)
                    self.clicky = True
            #w
            elif self.key == 7:
                dontreset = True
                if self.clicky:
                    index2 = self.indexclicked(worldcoords)
                    if self.vertexindex == -1 or index2 == -1:
                        pass
                    elif self.vertexindex == index2:
                        pass
                    else:
                        self.adjlistbsp.addedgenormal(self.vertexindex,index2)

                    self.vertexindex = -1
                    self.clicky = False
                else:
                    self.vertexindex = self.indexclicked(worldcoords)
                    self.clicky = True
            #q
            elif self.key == 9:
                dontreset = True
                if self.clicky:
                    index2 = self.indexclicked(worldcoords)
                    if self.vertexindex == -1 or index2 == -1:
                        pass
                    elif self.vertexindex == index2:
                        pass
                    else:
                        #swap delete normal and on order normal will switch
                        self.adjlistbsp.deleteedge(self.vertexindex,index2)
                        self.adjlistbsp.addedgenormal(self.vertexindex,index2)

                    self.vertexindex = -1
                    self.clicky = False
                else:
                    self.vertexindex = self.indexclicked(worldcoords)
                    self.clicky = True
            #r
            elif self.key == 3:
                dontreset = True
                if self.clicky:
                    index2 = self.indexclicked(worldcoords)
                    if self.vertexindex == -1 or index2 == -1:
                        pass
                    elif self.vertexindex == index2:
                        pass
                    else:
                        self.adjlist.deleteedge(self.vertexindex,index2)
                        self.adjlistbsp.deleteedge(self.vertexindex,index2)
                    self.vertexindex = -1
                    self.clicky = False
                else:
                    self.vertexindex = self.indexclicked(worldcoords)
                    self.clicky = True
            #u
            elif self.key == 8:
                dontreset = True
                if self.clicky:
                    index2 = (worldcoords[0],worldcoords[1])
                    if self.vertexindex == -1 or index2 == -1:
                        pass
                    elif self.vertexindex == index2:
                        pass
                    else:
                        starttime = time.time()
                        #call binary tree operation to get a list of visible vertices
                        unitlist = []
                        clicklist = []
                        self.bsp.closestnodes((self.vertexindex[0],self.vertexindex[1]), unitlist)
                        self.bsp.closestnodes((index2[0],index2[1]), clicklist)
                        #now add 2 vertices and all edges connecting visible vertices to main graph
                        originalsize = len(self.adjlist.vtable)
                        self.adjlist.addvertex(self.vertexindex[0],self.vertexindex[1])
                        self.adjlist.addvertex(index2[0],index2[1])
                        size = len(self.adjlist.vtable) - 1
                        size2 = len(self.adjlist.vtable) - 2
                        for x in unitlist:
                            if x < originalsize:
                                self.adjlist.addedge(size2,x)
                        for x in clicklist:
                            if x < originalsize:
                                self.adjlist.addedge(size,x)

                        #vertices added to graph call shortest path algorithm
                        l = []
                        l = self.GetShortestPath(size2, size, l)

                        #remove from graph
                        self.adjlist.deletevertex(size)
                        self.adjlist.deletevertex(size2)

                        #print(time.time() - starttime)

                    self.vertexindex = -1
                    self.clicky = False
                else:
                    self.vertexindex = (worldcoords[0],worldcoords[1])
                    self.clicky = True
            #y
            elif self.key == 5:
                dontreset = True
                if self.clicky:
                    index2 = self.indexclicked(worldcoords)
                    if self.vertexindex == -1 or index2 == -1:
                        pass
                    elif self.vertexindex == index2:
                        pass
                    else:
                        l = []
                        self.GetShortestPath(self.vertexindex,index2, l)

                    self.vertexindex = -1
                    self.clicky = False
                else:
                    self.vertexindex = self.indexclicked(worldcoords)
                    self.clicky = True
            if not dontreset:
                self.key = -1
        #not clicked
        else:
            #p
            if input.keys[pygame.K_p]:
                #os.path.join(self._cwdpath,"Images","sc2.png")
                f = open("mapgraph.txt", 'w')
                f.write("#copy and past into MapGraph.MapGraph.createmap() functions\n")
                for vertex in self.adjlist.vtable:
                    f.write("        self.adjlist.addvertex(%f, %f)\n" % (vertex.pos[0],vertex.pos[1]))
                for x in range(0,len(self.adjlist.adjlist)):
                    for node in self.adjlist.adjlist[x]:
                        if node[0] > x:
                            f.write("        self.adjlist.addedge(%d, %d)\n" % (x,node[0]))
                l = len(self.adjlist.vtable)
                f.write("#BSP adjacency list\n")
                for vertex in range(0,l):
                    f.write("        self.adjlistbsp.addvertex(%f, %f)\n" % (self.adjlistbsp.vtable[vertex].pos[0],self.adjlistbsp.vtable[vertex].pos[1]))
                for x in range(0,l):
                    for node in self.adjlistbsp.adjlist[x]:
                        if node[0] > x and node[0] < l:
                            f.write("        self.adjlistbsp.addedgenormal(%d, %d, (%f, %f))\n" % (x,node[0], node[1][0], node[1][1]))
                f.write("#Physics adjacency list\n")
                for vertex in range(0,len(self.adjlistphysics.vtable)):
                    if self.adjlistphysics.vtable[vertex] is not None:
                        f.write("        self.adjlistphysics.addvertex(%f, %f)\n" % (self.adjlistphysics.vtable[vertex].pos[0],self.adjlistphysics.vtable[vertex].pos[1]))
                f.write("#Physics boxes\n")
                for box in self.physicsboxes:
                    f.write("        l = [];")
                    for x in box[1]:
                        f.write("        l.append(%d);" % x)
                    f.write("\n        self.physicsboxes.append((pygame.Rect(%d,%d,%d,%d), l))\n" % (box[0][0],box[0][1],box[0][2],box[0][3]))
                f.close()
                print("File saved")

    def UnitPath(self, unitlocation, clicklocation):
        starttime = time.time()
        unitlist = []
        clicklist = []
        #see if clickpoint is visible from unitlist

        #see if we clicked in a restricted area and redirect click
        if self.clicklocationfound == False:
            self.clicklocationfound = True
            self.pathlocation = []
            self.clicknewlocation = (clicklocation[0], clicklocation[1])
            farpoint = (-1000,-1000)
            for box in self.physicsboxes:
                #check if clickpoint is inside a box
                leave = False
                if mathfuncs.mathfuncs.pointrectanycollision(clicklocation,box[0]):
                    #print("box found")
                    #check if clickpoint is inside the polygon
                    p1 = (self.adjlistbsp.vtable[box[1][0]].pos[0],self.adjlistbsp.vtable[box[1][0]].pos[1])
                    visited = [box[1][0]]
                    lastvertexindex = box[1][0]
                    currentvertexindex = box[1][0]
                    collisions = 0
                    v = box[1][0]
                    #print("start")
                    for a in range(0,len(box[1])):#v is current poly vertex index of bsp vtable
                        #print("%d, %d" % (currentvertexindex, lastvertexindex), end=', ')
                        for l in self.adjlistbsp.adjlist[currentvertexindex]: #l is tuple(vtable index, weight)
                            if l[0] in box[1] and l[0] != lastvertexindex:#l[0] != lastvertexindex
                                p2 = (self.adjlistbsp.vtable[l[0]].pos[0], self.adjlistbsp.vtable[l[0]].pos[1])
                                visited.append(l[0])
                                lastvertexindex = currentvertexindex
                                currentvertexindex = l[0]
                                break
                        #print("%d, %d" % (currentvertexindex, lastvertexindex))
                        #print("(%f, %f), (%f, %f)" % (p1[0],p1[1], p2[0], p2[1]))
                        if mathfuncs.mathfuncs.segsegintersection(p1,p2,clicklocation,farpoint):
                            #print("collided")
                            collisions = collisions + 1
                        p1 = (p2[0],p2[1])
                    #print("visited: ", end=' ')
                    #print("collisions = %d" % collisions)
                    if collisions % 2 == 1:
                        #print("poly found")
                        #choose closest vertex in polygon
                        closest = -1
                        closestvalue = 100000
                        for polyindex in box[1]:
                            distance = (clicklocation[0] - self.adjlistbsp.vtable[polyindex].pos[0])**2 + (clicklocation[1] - self.adjlistbsp.vtable[polyindex].pos[1])**2
                            if distance < closestvalue:
                                closest = polyindex
                                closestvalue = distance
                        if closest == -1:
                            #print("error")
                            pass
                        else:
                            #swap clicklocations
                            #print("swapped")
                            #print("inside poly")
                            clicklocation = (self.adjlistphysics.vtable[closest].pos[0],self.adjlistphysics.vtable[closest].pos[1])
                            self.clicknewlocation = (self.adjlistphysics.vtable[closest].pos[0],self.adjlistphysics.vtable[closest].pos[1])
                            leave = True
                if leave:
                    break
        else:
            clicklocation = self.clicknewlocation
            values = copy.deepcopy(self.pathlocation)
            return values



        clicklocation2 = (clicklocation[0] + 1, clicklocation[1] + 1)
        self.bsp.graph.addvertex(clicklocation[0],clicklocation[1])
        self.bsp.graph.addvertex(clicklocation2[0],clicklocation2[1])
        sizey = len(self.bsp.graph.vtable)
        seg = BSP.BSPNode(sizey - 2,sizey - 1, self.bsp.calculatenormal(sizey - 2,sizey - 1))
        i = []
        self.bsp.addsegment(1, seg, i)
        #print("start")
        self.bsp.closestnodes((unitlocation[0],unitlocation[1]), unitlist)

        self.bsp.graph.deletevertex(sizey - 1)
        self.bsp.graph.deletevertex(sizey - 2)
        if len(i) == 0:
            print("cut our small click yikes error")
        self.bsp.tree[i[0]] = None

        for x in unitlist:
            if x == sizey - 1 or x == sizey - 2:
                #print("click visible")
                values = []
                values.append(((clicklocation[0],clicklocation[1]), (0,0), False, (0,0)))
                #print(time.time() - starttime)
                self.pathlocation = copy.deepcopy(values)
                return values
        self.bsp.closestnodes((clicklocation[0],clicklocation[1]), clicklist)
        #now add 2 vertices and all edges connecting visible vertices to main graph
        originalsize = len(self.adjlist.vtable)
        self.adjlist.addvertex(unitlocation[0],unitlocation[1])
        self.adjlist.addvertex(clicklocation[0],clicklocation[1])
        size = len(self.adjlist.vtable) - 1
        size2 = len(self.adjlist.vtable) - 2
        for x in unitlist:
            if x < originalsize:
                self.adjlist.addedge(size2,x)
        for x in clicklist:
            if x < originalsize:
                self.adjlist.addedge(size,x)

        #vertices added to graph call shortest path algorithm
        l = []
        self.GetShortestPath(size2, size, l)

        #l has the indices to path vertices in vtable
        #values is a tuple (vertexdestination, vertexbefore, true or false whether its valid)
        values = []
        firsttime = True
        oldvertex = (0,0)
        oldindex = 0
        sizev = len(self.adjlistbsp.vtable) - 1
        for x in l:
            if firsttime:
                if x > sizev:#if clickposition
                    val = ((self.adjlist.vtable[x].pos[0],self.adjlist.vtable[x].pos[1]),(0,0), False, (0,0))
                else:
                    val = ((self.adjlistphysics.vtable[x].pos[0],self.adjlistphysics.vtable[x].pos[1]),(0,0), False, (0,0))
                firsttime = False
            else:
                if x > sizev:
                    val = ((self.adjlist.vtable[x].pos[0],self.adjlist.vtable[x].pos[1]), oldvertex, self.adjlistbsp.doesedgeexist(x,oldindex),
                            self.adjlistbsp.getedgeweightnormal(x,oldindex))
                else:
                    val = ((self.adjlistphysics.vtable[x].pos[0],self.adjlistphysics.vtable[x].pos[1]), oldvertex, self.adjlistbsp.doesedgeexist(x,oldindex),
                            self.adjlistbsp.getedgeweightnormal(x,oldindex))
                #mathfuncs.mathfuncs.calculatenormal(self.adjlist.vtable[x].pos[0],self.adjlist.vtable[x].pos[1], oldvertex[0], oldvertex[1])
            if x > sizev:
                oldvertex = (self.adjlist.vtable[x].pos[0],self.adjlist.vtable[x].pos[1])
            else:
                oldvertex = (self.adjlistphysics.vtable[x].pos[0],self.adjlistphysics.vtable[x].pos[1])
            oldindex = x
            values.append(val)
        #remove from graph
        self.adjlist.deletevertex(size)
        self.adjlist.deletevertex(size2)
        #print(time.time() - starttime)
        self.pathlocation = copy.deepcopy(values)
        return values

    def indexclicked(self, worldcoords):
        clickcircle = (worldcoords[0],worldcoords[1], 20)
        for x in range(0,len(self.adjlist.vtable)):
            if mathfuncs.mathfuncs.pointcirclecollision((self.adjlist.vtable[x].pos[0],self.adjlist.vtable[x].pos[1]), clickcircle):
                return x
        return -1

    def renderbsp(self, display_render, map):
        #draw bsp vertices
        color = (0,0,0)
        for vertex in self.adjlistbsp.vtable:
            color = (0,0,0)
            if vertex.highlight:
                color = (0,0,255)
            pygame.draw.circle(display_render, color,(int(round(vertex.pos[0])) - map._cameraposition[0],
                                int(round(vertex.pos[1])) - map._cameraposition[1]), 10, 0)
        #draw bsp edges and normals
        color = (0,0,0)
        for y in range(0,len(self.adjlistbsp.adjlist)):
            p1 = (self.adjlistbsp.vtable[y].pos[0] - map._cameraposition[0], self.adjlistbsp.vtable[y].pos[1] - map._cameraposition[1])
            for x in range(0,len(self.adjlistbsp.adjlist[y])):
                p2 = (self.adjlistbsp.vtable[self.adjlistbsp.adjlist[y][x][0]].pos[0] - map._cameraposition[0],
                      self.adjlistbsp.vtable[self.adjlistbsp.adjlist[y][x][0]].pos[1] - map._cameraposition[1])
                color = (0,0,0)
                if self.adjlistbsp.vtable[y].highlight and self.adjlistbsp.vtable[self.adjlistbsp.adjlist[y][x][0]].highlight:
                    color = (0,0,255)
                pygame.draw.line(display_render,color, p1, p2, 2)
                color = (50,150,50)
                p3 = (int(round((p2[0] + p1[0]) / 2)), int(round((p2[1] + p1[1]) / 2)))
                pygame.draw.line(display_render,color, p3, (p3[0] + int(round(self.adjlistbsp.adjlist[y][x][1][0] * 15)), int(p3[1] + round(self.adjlistbsp.adjlist[y][x][1][1] * 15))), 5)

        #physics tree vertex and connections
        color = (100,100,100)
        for vertex in self.adjlistphysics.vtable:
            if vertex is not None:
                pygame.draw.circle(display_render, color,(int(round(vertex.pos[0])) - map._cameraposition[0],
                                    int(round(vertex.pos[1])) - map._cameraposition[1]), 10, 1)

        #physics boxes
        for x in self.physicsboxes:
            camerarect = pygame.Rect(x[0][0] - map._cameraposition[0], x[0][1] - map._cameraposition[1],x[0][2],x[0][3])
            pygame.draw.rect(display_render,(0,0,255),camerarect, 2)
            for z in x[1]:
                    color = (255,0,0)
                    pygame.draw.circle(display_render, color,(int(round(self.adjlistbsp.vtable[z].pos[0])) - map._cameraposition[0],
                                    int(round(self.adjlistbsp.vtable[z].pos[1])) - map._cameraposition[1]), 10, 1)
        #self.bsp.render(display_render, map

    def render(self, display_render, map):
        #draw vertices
        color = (255,255,0)
        for vertex in self.adjlist.vtable:
            color = (255,255,0)
            if vertex.highlight:
                color = (0,0,255)
            pygame.draw.circle(display_render, color,(int(round(vertex.pos[0])) - map._cameraposition[0],
                                int(round(vertex.pos[1])) - map._cameraposition[1]), 10, 0)
        #draw edges
        color = (255,255,0)
        for y in range(0,len(self.adjlist.adjlist)):
            p1 = (self.adjlist.vtable[y].pos[0] - map._cameraposition[0], self.adjlist.vtable[y].pos[1] - map._cameraposition[1])
            for x in range(0,len(self.adjlist.adjlist[y])):
                p2 = (self.adjlist.vtable[self.adjlist.adjlist[y][x][0]].pos[0] - map._cameraposition[0],
                      self.adjlist.vtable[self.adjlist.adjlist[y][x][0]].pos[1] - map._cameraposition[1])
                color = (255,255,0)
                if self.adjlist.vtable[y].highlight and self.adjlist.vtable[self.adjlist.adjlist[y][x][0]].highlight:
                    color = (0,0,255)
                pygame.draw.line(display_render,color, p1, p2)

    def GetShortestPath(self, s, e, l):
        #clear highlight for new path
        for vertex in self.adjlist.vtable:
            vertex.highlight = False

        #s = 10
        #e = 15
        #starttime = time.time_ns()
        self.Astar(self.adjlist,s,e)
        #print(time.time_ns() - starttime)
        #self.adjlist.print()
        #starttime = time.time_ns()
        #self.Astar(self.adjlist,s,e)
        #print(time.time_ns() - starttime)
        #self.adjlist.print()

        index = self.adjlist.vtable[e].parent
        l.append(e)
        while index != s:
            l.append(index)
            index = self.adjlist.vtable[index].parent
        l.reverse()
        #print(l)

        #highlight vertex on path
        self.adjlist.vtable[s].highlight = True
        for x in l:
            self.adjlist.vtable[x].highlight = True

    def Dijkstra(self, G, s, e):
        #initialize everything
        for x in G.vtable:
            x.found = False
            x.finished = False
            x.parent = None
            x.d = 10000000
        G.vtable[s].d = 0

        #set up queue
        Q = PriorityQueue.PriorityQueue()
        Q.MaxHeapInsert(G.vtable[s])

        #main loop
        while Q.heapsize > 0:
            V = Q.HeapExtractMax()
            G.vtable[V.index].finished = True

            #the end is finished thats all we need to know, leave
            if V.index == e:
                return

            for neighbor in G.adjlist[V.index]: #neighbor = tuple(index, weight)
                if G.vtable[neighbor[0]].finished == False:
                    if G.vtable[neighbor[0]].d > V.d + neighbor[1]:
                        G.vtable[neighbor[0]].d = V.d + neighbor[1]
                        G.vtable[neighbor[0]].parent = V.index
                        if G.vtable[neighbor[0]].found:
                            a = Q.VtoH.get(neighbor[0], -1)
                            if a != -1:
                                Q.HeapIncreaseKey(Q.VtoH[neighbor[0]],G.vtable[neighbor[0]])
                            else:
                                print("dictionary key error")
                        else:
                            Q.MaxHeapInsert(G.vtable[neighbor[0]])
                            G.vtable[neighbor[0]].found = True

    #same as dijkstra but is smarter about distance, 1 line difference
    def Astar(self, G, s, e):
        endpos = G.vtable[e].pos
        #initialize everything
        for x in G.vtable:
            x.found = False
            x.finished = False
            x.parent = None
            x.d = 10000000
        G.vtable[s].d = 0

        #set up queue
        Q = PriorityQueue.PriorityQueue()
        Q.MaxHeapInsert(G.vtable[s])

        #main loop
        while Q.heapsize > 0:
            V = Q.HeapExtractMax()
            G.vtable[V.index].finished = True

            #the end is finished thats all we need to know, leave
            if V.index == e:
                return

            for neighbor in G.adjlist[V.index]: #neighbor = tuple(index, weight)
                if G.vtable[neighbor[0]].finished == False:
                    #store distance in vertex, if its -1 then use the magnitude function else just use that number, also see if i dont have to sqrt it?
                    if G.vtable[neighbor[0]].d > V.d + neighbor[1] + mathfuncs.mathfuncs.Magnitude((G.vtable[neighbor[0]].pos[0] - endpos[0],G.vtable[neighbor[0]].pos[1] - endpos[1])):
                        G.vtable[neighbor[0]].d = V.d + neighbor[1]
                        G.vtable[neighbor[0]].parent = V.index
                        if G.vtable[neighbor[0]].found:
                            a = Q.VtoH.get(neighbor[0], -1)
                            if a != -1:
                                Q.HeapIncreaseKey(Q.VtoH[neighbor[0]],G.vtable[neighbor[0]])
                            else:
                                print("dictionary key error")
                        else:
                            Q.MaxHeapInsert(G.vtable[neighbor[0]])
                            G.vtable[neighbor[0]].found = True


    def createmap(self):
#copy and past into MapGraph.MapGraph.createmap() functions
        self.adjlist.addvertex(457.500000, 608.000000)
        self.adjlist.addvertex(322.500000, 846.000000)
        self.adjlist.addvertex(438.000000, 992.000000)
        self.adjlist.addvertex(583.500000, 834.000000)
        self.adjlist.addvertex(571.500000, 746.000000)
        self.adjlist.addvertex(370.500000, 700.000000)
        self.adjlist.addvertex(685.500000, 410.000000)
        self.adjlist.addvertex(805.500000, 356.000000)
        self.adjlist.addvertex(1113.000000, 360.000000)
        self.adjlist.addvertex(1200.000000, 350.000000)
        self.adjlist.addvertex(1281.000000, 502.000000)
        self.adjlist.addvertex(1498.500000, 534.000000)
        self.adjlist.addvertex(1495.500000, 592.000000)
        self.adjlist.addvertex(1191.000000, 552.000000)
        self.adjlist.addvertex(745.500000, 528.000000)
        self.adjlist.addvertex(769.500000, 1034.000000)
        self.adjlist.addvertex(645.000000, 1206.000000)
        self.adjlist.addvertex(817.500000, 1642.000000)
        self.adjlist.addvertex(937.500000, 1780.000000)
        self.adjlist.addvertex(1297.500000, 1796.000000)
        self.adjlist.addvertex(1378.500000, 1728.000000)
        self.adjlist.addvertex(1234.500000, 1680.000000)
        self.adjlist.addvertex(994.500000, 1602.000000)
        self.adjlist.addvertex(952.500000, 1162.000000)
        self.adjlist.addvertex(898.500000, 1072.000000)
        self.adjlist.addvertex(862.500000, 1510.000000)
        self.adjlist.addvertex(783.000000, 1364.000000)
        self.adjlist.addvertex(849.000000, 1236.000000)
        self.adjlist.addvertex(1053.000000, 924.000000)
        self.adjlist.addvertex(1314.000000, 880.000000)
        self.adjlist.addvertex(1540.500000, 904.000000)
        self.adjlist.addvertex(1669.500000, 1060.000000)
        self.adjlist.addvertex(1792.500000, 1496.000000)
        self.adjlist.addvertex(1714.500000, 1616.000000)
        self.adjlist.addvertex(1548.000000, 1556.000000)
        self.adjlist.addvertex(1593.000000, 1450.000000)
        self.adjlist.addvertex(1663.500000, 1332.000000)
        self.adjlist.addvertex(1570.500000, 1148.000000)
        self.adjlist.addvertex(1122.000000, 1000.000000)
        self.adjlist.addvertex(1665.000000, 1220.000000)
        self.adjlist.addvertex(532.500000, 148.000000)
        self.adjlist.addvertex(405.000000, 268.000000)
        self.adjlist.addvertex(343.500000, 208.000000)
        self.adjlist.addvertex(406.500000, 26.000000)
        self.adjlist.addvertex(534.000000, 42.000000)
        self.adjlist.addvertex(472.500000, 0.000000)
        self.adjlist.addvertex(474.000000, 110.000000)
        self.adjlist.addvertex(1134.000000, 100.000000)
        self.adjlist.addvertex(1242.000000, 8.000000)
        self.adjlist.addvertex(526.500000, 4.000000)
        self.adjlist.addvertex(304.500000, 384.000000)
        self.adjlist.addvertex(267.000000, 426.000000)
        self.adjlist.addvertex(69.000000, 552.000000)
        self.adjlist.addvertex(231.000000, 316.000000)
        self.adjlist.addvertex(0.000000, 436.000000)
        self.adjlist.addvertex(1.500000, 502.000000)
        self.adjlist.addvertex(1642.500000, 378.000000)
        self.adjlist.addvertex(1680.000000, 110.000000)
        self.adjlist.addvertex(1930.500000, 208.000000)
        self.adjlist.addvertex(1934.000000, 340.000000)
        self.adjlist.addvertex(2121.500000, 686.000000)
        self.adjlist.addvertex(2165.000000, 758.000000)
        self.adjlist.addvertex(1940.000000, 788.000000)
        self.adjlist.addvertex(1535.000000, 52.000000)
        self.adjlist.addvertex(1857.500000, 538.000000)
        self.adjlist.addvertex(1854.500000, 674.000000)
        self.adjlist.addvertex(1914.500000, 728.000000)
        self.adjlist.addvertex(1788.500000, 714.000000)
        self.adjlist.addvertex(1737.500000, 484.000000)
        self.adjlist.addvertex(1584.500000, 2.000000)
        self.adjlist.addvertex(1884.500000, 4.000000)
        self.adjlist.addvertex(2010.500000, 6.000000)
        self.adjlist.addvertex(2019.500000, 1652.000000)
        self.adjlist.addvertex(1895.000000, 1828.000000)
        self.adjlist.addvertex(1901.000000, 1936.000000)
        self.adjlist.addvertex(2009.000000, 2084.000000)
        self.adjlist.addvertex(2150.000000, 1952.000000)
        self.adjlist.addvertex(2177.000000, 1790.000000)
        self.adjlist.addvertex(2030.000000, 962.000000)
        self.adjlist.addvertex(1979.000000, 1138.000000)
        self.adjlist.addvertex(2196.500000, 1378.000000)
        self.adjlist.addvertex(2375.000000, 1360.000000)
        self.adjlist.addvertex(2475.500000, 1482.000000)
        self.adjlist.addvertex(2477.000000, 962.000000)
        self.adjlist.addvertex(2321.000000, 1120.000000)
        self.adjlist.addvertex(2136.500000, 1134.000000)
        self.adjlist.addvertex(2186.030151, 628.000000)
        self.adjlist.addvertex(2261.407035, 704.000000)
        self.adjlist.addvertex(2416.683417, 716.000000)
        self.adjlist.addvertex(2476.984925, 770.000000)
        self.adjlist.addvertex(2475.465995, 618.000000)
        self.adjlist.addvertex(2416.523929, 686.000000)
        self.adjlist.addvertex(2336.423174, 692.000000)
        self.adjlist.addvertex(2223.073048, 600.000000)
        self.adjlist.addedge(0, 4)
        self.adjlist.addedge(0, 5)
        self.adjlist.addedge(0, 50)
        self.adjlist.addedge(0, 6)
        self.adjlist.addedge(1, 2)
        self.adjlist.addedge(1, 5)
        self.adjlist.addedge(1, 52)
        self.adjlist.addedge(2, 3)
        self.adjlist.addedge(2, 16)
        self.adjlist.addedge(3, 4)
        self.adjlist.addedge(3, 15)
        self.adjlist.addedge(4, 14)
        self.adjlist.addedge(5, 51)
        self.adjlist.addedge(6, 7)
        self.adjlist.addedge(6, 14)
        self.adjlist.addedge(6, 41)
        self.adjlist.addedge(7, 8)
        self.adjlist.addedge(7, 40)
        self.adjlist.addedge(8, 9)
        self.adjlist.addedge(8, 47)
        self.adjlist.addedge(9, 10)
        self.adjlist.addedge(9, 48)
        self.adjlist.addedge(9, 68)
        self.adjlist.addedge(10, 11)
        self.adjlist.addedge(11, 12)
        self.adjlist.addedge(11, 68)
        self.adjlist.addedge(12, 13)
        self.adjlist.addedge(12, 67)
        self.adjlist.addedge(12, 29)
        self.adjlist.addedge(13, 14)
        self.adjlist.addedge(13, 28)
        self.adjlist.addedge(14, 16)
        self.adjlist.addedge(15, 24)
        self.adjlist.addedge(15, 16)
        self.adjlist.addedge(15, 28)
        self.adjlist.addedge(16, 17)
        self.adjlist.addedge(17, 18)
        self.adjlist.addedge(18, 19)
        self.adjlist.addedge(18, 75)
        self.adjlist.addedge(19, 20)
        self.adjlist.addedge(20, 21)
        self.adjlist.addedge(20, 74)
        self.adjlist.addedge(20, 73)
        self.adjlist.addedge(20, 33)
        self.adjlist.addedge(20, 34)
        self.adjlist.addedge(21, 22)
        self.adjlist.addedge(22, 25)
        self.adjlist.addedge(23, 24)
        self.adjlist.addedge(23, 27)
        self.adjlist.addedge(23, 38)
        self.adjlist.addedge(24, 28)
        self.adjlist.addedge(24, 38)
        self.adjlist.addedge(25, 26)
        self.adjlist.addedge(26, 27)
        self.adjlist.addedge(28, 29)
        self.adjlist.addedge(28, 38)
        self.adjlist.addedge(29, 30)
        self.adjlist.addedge(30, 31)
        self.adjlist.addedge(30, 62)
        self.adjlist.addedge(30, 31)
        self.adjlist.addedge(31, 39)
        self.adjlist.addedge(31, 78)
        self.adjlist.addedge(32, 33)
        self.adjlist.addedge(32, 39)
        self.adjlist.addedge(32, 80)
        self.adjlist.addedge(33, 34)
        self.adjlist.addedge(33, 73)
        self.adjlist.addedge(34, 35)
        self.adjlist.addedge(35, 36)
        self.adjlist.addedge(36, 37)
        self.adjlist.addedge(37, 38)
        self.adjlist.addedge(40, 41)
        self.adjlist.addedge(40, 44)
        self.adjlist.addedge(41, 42)
        self.adjlist.addedge(41, 50)
        self.adjlist.addedge(42, 46)
        self.adjlist.addedge(42, 53)
        self.adjlist.addedge(43, 46)
        self.adjlist.addedge(44, 47)
        self.adjlist.addedge(48, 63)
        self.adjlist.addedge(50, 51)
        self.adjlist.addedge(50, 53)
        self.adjlist.addedge(50, 53)
        self.adjlist.addedge(51, 52)
        self.adjlist.addedge(52, 55)
        self.adjlist.addedge(53, 54)
        self.adjlist.addedge(56, 57)
        self.adjlist.addedge(56, 68)
        self.adjlist.addedge(57, 63)
        self.adjlist.addedge(58, 59)
        self.adjlist.addedge(58, 71)
        self.adjlist.addedge(59, 64)
        self.adjlist.addedge(60, 61)
        self.adjlist.addedge(60, 66)
        self.adjlist.addedge(60, 86)
        self.adjlist.addedge(61, 62)
        self.adjlist.addedge(61, 78)
        self.adjlist.addedge(61, 87)
        self.adjlist.addedge(62, 67)
        self.adjlist.addedge(64, 65)
        self.adjlist.addedge(65, 66)
        self.adjlist.addedge(67, 68)
        self.adjlist.addedge(72, 73)
        self.adjlist.addedge(72, 77)
        self.adjlist.addedge(72, 80)
        self.adjlist.addedge(73, 74)
        self.adjlist.addedge(74, 75)
        self.adjlist.addedge(75, 76)
        self.adjlist.addedge(76, 77)
        self.adjlist.addedge(78, 85)
        self.adjlist.addedge(78, 79)
        self.adjlist.addedge(78, 88)
        self.adjlist.addedge(79, 80)
        self.adjlist.addedge(80, 81)
        self.adjlist.addedge(81, 82)
        self.adjlist.addedge(83, 84)
        self.adjlist.addedge(84, 85)
        self.adjlist.addedge(86, 93)
        self.adjlist.addedge(86, 87)
        self.adjlist.addedge(87, 88)
        self.adjlist.addedge(88, 89)
        self.adjlist.addedge(90, 91)
        self.adjlist.addedge(91, 92)
        self.adjlist.addedge(92, 93)
#BSP adjacency list
        self.adjlistbsp.addvertex(457.500000, 608.000000)
        self.adjlistbsp.addvertex(322.500000, 846.000000)
        self.adjlistbsp.addvertex(438.000000, 992.000000)
        self.adjlistbsp.addvertex(583.500000, 834.000000)
        self.adjlistbsp.addvertex(571.500000, 746.000000)
        self.adjlistbsp.addvertex(370.500000, 700.000000)
        self.adjlistbsp.addvertex(685.500000, 410.000000)
        self.adjlistbsp.addvertex(805.500000, 356.000000)
        self.adjlistbsp.addvertex(1113.000000, 360.000000)
        self.adjlistbsp.addvertex(1200.000000, 350.000000)
        self.adjlistbsp.addvertex(1281.000000, 502.000000)
        self.adjlistbsp.addvertex(1498.500000, 534.000000)
        self.adjlistbsp.addvertex(1495.500000, 592.000000)
        self.adjlistbsp.addvertex(1191.000000, 552.000000)
        self.adjlistbsp.addvertex(745.500000, 528.000000)
        self.adjlistbsp.addvertex(769.500000, 1034.000000)
        self.adjlistbsp.addvertex(645.000000, 1206.000000)
        self.adjlistbsp.addvertex(817.500000, 1642.000000)
        self.adjlistbsp.addvertex(937.500000, 1780.000000)
        self.adjlistbsp.addvertex(1297.500000, 1796.000000)
        self.adjlistbsp.addvertex(1378.500000, 1728.000000)
        self.adjlistbsp.addvertex(1234.500000, 1680.000000)
        self.adjlistbsp.addvertex(994.500000, 1602.000000)
        self.adjlistbsp.addvertex(952.500000, 1162.000000)
        self.adjlistbsp.addvertex(898.500000, 1072.000000)
        self.adjlistbsp.addvertex(862.500000, 1510.000000)
        self.adjlistbsp.addvertex(783.000000, 1364.000000)
        self.adjlistbsp.addvertex(849.000000, 1236.000000)
        self.adjlistbsp.addvertex(1053.000000, 924.000000)
        self.adjlistbsp.addvertex(1314.000000, 880.000000)
        self.adjlistbsp.addvertex(1540.500000, 904.000000)
        self.adjlistbsp.addvertex(1669.500000, 1060.000000)
        self.adjlistbsp.addvertex(1792.500000, 1496.000000)
        self.adjlistbsp.addvertex(1714.500000, 1616.000000)
        self.adjlistbsp.addvertex(1548.000000, 1556.000000)
        self.adjlistbsp.addvertex(1593.000000, 1450.000000)
        self.adjlistbsp.addvertex(1663.500000, 1332.000000)
        self.adjlistbsp.addvertex(1570.500000, 1148.000000)
        self.adjlistbsp.addvertex(1122.000000, 1000.000000)
        self.adjlistbsp.addvertex(1665.000000, 1220.000000)
        self.adjlistbsp.addvertex(532.500000, 148.000000)
        self.adjlistbsp.addvertex(405.000000, 268.000000)
        self.adjlistbsp.addvertex(343.500000, 208.000000)
        self.adjlistbsp.addvertex(406.500000, 26.000000)
        self.adjlistbsp.addvertex(534.000000, 42.000000)
        self.adjlistbsp.addvertex(472.500000, 0.000000)
        self.adjlistbsp.addvertex(474.000000, 110.000000)
        self.adjlistbsp.addvertex(1134.000000, 100.000000)
        self.adjlistbsp.addvertex(1242.000000, 8.000000)
        self.adjlistbsp.addvertex(526.500000, 4.000000)
        self.adjlistbsp.addvertex(304.500000, 384.000000)
        self.adjlistbsp.addvertex(267.000000, 426.000000)
        self.adjlistbsp.addvertex(69.000000, 552.000000)
        self.adjlistbsp.addvertex(231.000000, 316.000000)
        self.adjlistbsp.addvertex(0.000000, 436.000000)
        self.adjlistbsp.addvertex(1.500000, 502.000000)
        self.adjlistbsp.addvertex(1642.500000, 378.000000)
        self.adjlistbsp.addvertex(1680.000000, 110.000000)
        self.adjlistbsp.addvertex(1930.500000, 208.000000)
        self.adjlistbsp.addvertex(1934.000000, 340.000000)
        self.adjlistbsp.addvertex(2121.500000, 686.000000)
        self.adjlistbsp.addvertex(2165.000000, 758.000000)
        self.adjlistbsp.addvertex(1940.000000, 788.000000)
        self.adjlistbsp.addvertex(1535.000000, 52.000000)
        self.adjlistbsp.addvertex(1857.500000, 538.000000)
        self.adjlistbsp.addvertex(1854.500000, 674.000000)
        self.adjlistbsp.addvertex(1914.500000, 728.000000)
        self.adjlistbsp.addvertex(1788.500000, 714.000000)
        self.adjlistbsp.addvertex(1737.500000, 484.000000)
        self.adjlistbsp.addvertex(1584.500000, 2.000000)
        self.adjlistbsp.addvertex(1884.500000, 4.000000)
        self.adjlistbsp.addvertex(2010.500000, 6.000000)
        self.adjlistbsp.addvertex(2019.500000, 1652.000000)
        self.adjlistbsp.addvertex(1895.000000, 1828.000000)
        self.adjlistbsp.addvertex(1901.000000, 1936.000000)
        self.adjlistbsp.addvertex(2009.000000, 2084.000000)
        self.adjlistbsp.addvertex(2150.000000, 1952.000000)
        self.adjlistbsp.addvertex(2177.000000, 1790.000000)
        self.adjlistbsp.addvertex(2030.000000, 962.000000)
        self.adjlistbsp.addvertex(1979.000000, 1138.000000)
        self.adjlistbsp.addvertex(2196.500000, 1378.000000)
        self.adjlistbsp.addvertex(2375.000000, 1360.000000)
        self.adjlistbsp.addvertex(2475.500000, 1482.000000)
        self.adjlistbsp.addvertex(2477.000000, 962.000000)
        self.adjlistbsp.addvertex(2321.000000, 1120.000000)
        self.adjlistbsp.addvertex(2136.500000, 1134.000000)
        self.adjlistbsp.addvertex(2186.030151, 628.000000)
        self.adjlistbsp.addvertex(2261.407035, 704.000000)
        self.adjlistbsp.addvertex(2416.683417, 716.000000)
        self.adjlistbsp.addvertex(2476.984925, 770.000000)
        self.adjlistbsp.addvertex(2475.465995, 618.000000)
        self.adjlistbsp.addvertex(2416.523929, 686.000000)
        self.adjlistbsp.addvertex(2336.423174, 692.000000)
        self.adjlistbsp.addvertex(2223.073048, 600.000000)
        self.adjlistbsp.addedgenormal(0, 4, (-0.770962, 0.636881))
        self.adjlistbsp.addedgenormal(0, 5, (-0.726575, -0.687087))
        self.adjlistbsp.addedgenormal(1, 2, (0.784264, -0.620428))
        self.adjlistbsp.addedgenormal(1, 5, (-0.949977, -0.312321))
        self.adjlistbsp.addedgenormal(2, 3, (-0.735606, -0.677409))
        self.adjlistbsp.addedgenormal(3, 4, (-0.990830, 0.135113))
        self.adjlistbsp.addedgenormal(6, 7, (-0.410365, -0.911922))
        self.adjlistbsp.addedgenormal(6, 14, (0.891385, -0.453247))
        self.adjlistbsp.addedgenormal(7, 8, (0.013007, -0.999915))
        self.adjlistbsp.addedgenormal(8, 9, (0.114191, 0.993459))
        self.adjlistbsp.addedgenormal(9, 10, (-0.882514, 0.470287))
        self.adjlistbsp.addedgenormal(10, 11, (-0.145559, 0.989350))
        self.adjlistbsp.addedgenormal(11, 12, (-0.998665, -0.051655))
        self.adjlistbsp.addedgenormal(12, 13, (0.130244, -0.991482))
        self.adjlistbsp.addedgenormal(13, 14, (0.053794, -0.998552))
        self.adjlistbsp.addedgenormal(15, 24, (0.282569, -0.959247))
        self.adjlistbsp.addedgenormal(15, 16, (-0.810058, -0.586350))
        self.adjlistbsp.addedgenormal(16, 17, (0.929867, -0.367895))
        self.adjlistbsp.addedgenormal(17, 18, (-0.754606, 0.656179))
        self.adjlistbsp.addedgenormal(18, 19, (-0.044401, 0.999014))
        self.adjlistbsp.addedgenormal(19, 20, (0.642970, 0.765891))
        self.adjlistbsp.addedgenormal(20, 21, (0.316228, -0.948683))
        self.adjlistbsp.addedgenormal(21, 22, (0.309086, -0.951034))
        self.adjlistbsp.addedgenormal(22, 25, (-0.571793, 0.820398))
        self.adjlistbsp.addedgenormal(23, 24, (0.857493, -0.514496))
        self.adjlistbsp.addedgenormal(23, 27, (-0.581610, -0.813468))
        self.adjlistbsp.addedgenormal(25, 26, (-0.878240, 0.478220))
        self.adjlistbsp.addedgenormal(26, 27, (-0.888803, -0.458289))
        self.adjlistbsp.addedgenormal(28, 38, (0.740381, -0.672188))
        self.adjlistbsp.addedgenormal(28, 29, (0.166237, 0.986086))
        self.adjlistbsp.addedgenormal(29, 30, (-0.105370, 0.994433))
        self.adjlistbsp.addedgenormal(30, 31, (-0.770645, 0.637264))
        self.adjlistbsp.addedgenormal(31, 39, (-0.999605, -0.028114))
        self.adjlistbsp.addedgenormal(32, 33, (-0.838444, -0.544988))
        self.adjlistbsp.addedgenormal(32, 39, (-0.907815, 0.419371))
        self.adjlistbsp.addedgenormal(33, 34, (0.339020, -0.940779))
        self.adjlistbsp.addedgenormal(34, 35, (0.920487, 0.390773))
        self.adjlistbsp.addedgenormal(35, 36, (0.858454, 0.512890))
        self.adjlistbsp.addedgenormal(36, 37, (0.892479, -0.451090))
        self.adjlistbsp.addedgenormal(37, 38, (0.313368, -0.949632))
        self.adjlistbsp.addedgenormal(40, 41, (-0.685365, -0.728200))
        self.adjlistbsp.addedgenormal(40, 44, (0.999900, 0.014150))
        self.adjlistbsp.addedgenormal(41, 42, (-0.698324, 0.715782))
        self.adjlistbsp.addedgenormal(42, 46, (0.600490, 0.799632))
        self.adjlistbsp.addedgenormal(43, 45, (-0.366525, -0.930408))
        self.adjlistbsp.addedgenormal(43, 46, (0.779509, -0.626391))
        self.adjlistbsp.addedgenormal(44, 45, (0.563962, -0.825801))
        self.adjlistbsp.addedgenormal(44, 47, (0.096218, -0.995360))
        self.adjlistbsp.addedgenormal(44, 49, (0.981074, -0.193633))
        self.adjlistbsp.addedgenormal(47, 48, (0.648466, 0.761243))
        self.adjlistbsp.addedgenormal(48, 49, (0.005590, -0.999984))
        self.adjlistbsp.addedgenormal(50, 51, (-0.745938, -0.666016))
        self.adjlistbsp.addedgenormal(50, 53, (-0.679109, 0.734037))
        self.adjlistbsp.addedgenormal(51, 52, (-0.536875, -0.843661))
        self.adjlistbsp.addedgenormal(52, 55, (0.595228, -0.803557))
        self.adjlistbsp.addedgenormal(53, 54, (0.460990, 0.887405))
        self.adjlistbsp.addedgenormal(54, 55, (0.999742, -0.022721))
        self.adjlistbsp.addedgenormal(56, 57, (-0.990352, -0.138575))
        self.adjlistbsp.addedgenormal(56, 68, (0.744690, -0.667411))
        self.adjlistbsp.addedgenormal(57, 63, (0.371391, -0.928477))
        self.adjlistbsp.addedgenormal(58, 59, (0.999649, -0.026506))
        self.adjlistbsp.addedgenormal(58, 71, (0.929741, 0.368214))
        self.adjlistbsp.addedgenormal(59, 64, (0.932798, 0.360399))
        self.adjlistbsp.addedgenormal(60, 61, (0.855916, -0.517116))
        self.adjlistbsp.addedgenormal(60, 66, (-0.198847, -0.980031))
        self.adjlistbsp.addedgenormal(61, 62, (0.132164, 0.991228))
        self.adjlistbsp.addedgenormal(62, 67, (0.438891, -0.898540))
        self.adjlistbsp.addedgenormal(63, 69, (-0.710651, -0.703545))
        self.adjlistbsp.addedgenormal(64, 65, (0.999757, 0.022053))
        self.adjlistbsp.addedgenormal(65, 66, (0.668965, -0.743294))
        self.adjlistbsp.addedgenormal(67, 68, (0.976287, -0.216481))
        self.adjlistbsp.addedgenormal(69, 70, (0.006667, -0.999978))
        self.adjlistbsp.addedgenormal(70, 71, (0.015871, -0.999874))
        self.adjlistbsp.addedgenormal(72, 77, (0.659012, -0.752133))
        self.adjlistbsp.addedgenormal(72, 73, (-0.816389, -0.577502))
        self.adjlistbsp.addedgenormal(73, 74, (-0.998460, 0.055470))
        self.adjlistbsp.addedgenormal(74, 75, (-0.807791, 0.589469))
        self.adjlistbsp.addedgenormal(75, 76, (0.683424, 0.730021))
        self.adjlistbsp.addedgenormal(76, 77, (0.986394, 0.164399))
        self.adjlistbsp.addedgenormal(78, 79, (0.960488, 0.278323))
        self.adjlistbsp.addedgenormal(78, 85, (0.850212, -0.526440))
        self.adjlistbsp.addedgenormal(79, 80, (0.740987, -0.671519))
        self.adjlistbsp.addedgenormal(80, 81, (-0.100332, -0.994954))
        self.adjlistbsp.addedgenormal(81, 82, (0.771839, -0.635818))
        self.adjlistbsp.addedgenormal(82, 83, (-0.999996, -0.002885))
        self.adjlistbsp.addedgenormal(83, 84, (-0.711596, -0.702589))
        self.adjlistbsp.addedgenormal(84, 85, (-0.075663, -0.997133))
        self.adjlistbsp.addedgenormal(86, 93, (-0.602998, -0.797743))
        self.adjlistbsp.addedgenormal(86, 87, (-0.710011, 0.704190))
        self.adjlistbsp.addedgenormal(87, 88, (-0.077052, 0.997027))
        self.adjlistbsp.addedgenormal(88, 89, (-0.667111, 0.744959))
        self.adjlistbsp.addedgenormal(89, 90, (-0.999950, 0.009992))
        self.adjlistbsp.addedgenormal(90, 91, (-0.755641, -0.654986))
        self.adjlistbsp.addedgenormal(91, 92, (-0.074696, -0.997206))
        self.adjlistbsp.addedgenormal(92, 93, (0.630192, -0.776439))
#Physics adjacency list
        self.adjlistphysics.addvertex(457.500000, 562.000000)
        self.adjlistphysics.addvertex(282.000000, 870.000000)
        self.adjlistphysics.addvertex(436.500000, 1036.000000)
        self.adjlistphysics.addvertex(612.000000, 844.000000)
        self.adjlistphysics.addvertex(610.500000, 736.000000)
        self.adjlistphysics.addvertex(342.000000, 668.000000)
        self.adjlistphysics.addvertex(653.000000, 402.000000)
        self.adjlistphysics.addvertex(810.000000, 312.000000)
        self.adjlistphysics.addvertex(1113.000000, 318.000000)
        self.adjlistphysics.addvertex(1218.000000, 324.000000)
        self.adjlistphysics.addvertex(1299.000000, 454.000000)
        self.adjlistphysics.addvertex(1512.000000, 516.000000)
        self.adjlistphysics.addvertex(1507.500000, 618.000000)
        self.adjlistphysics.addvertex(1191.000000, 582.000000)
        self.adjlistphysics.addvertex(744.000000, 556.000000)
        self.adjlistphysics.addvertex(771.000000, 1008.000000)
        self.adjlistphysics.addvertex(616.500000, 1210.000000)
        self.adjlistphysics.addvertex(783.000000, 1650.000000)
        self.adjlistphysics.addvertex(922.500000, 1808.000000)
        self.adjlistphysics.addvertex(1308.000000, 1830.000000)
        self.adjlistphysics.addvertex(1416.000000, 1706.000000)
        self.adjlistphysics.addvertex(1242.000000, 1644.000000)
        self.adjlistphysics.addvertex(1005.000000, 1576.000000)
        self.adjlistphysics.addvertex(982.500000, 1186.000000)
        self.adjlistphysics.addvertex(909.000000, 1046.000000)
        self.adjlistphysics.addvertex(876.000000, 1476.000000)
        self.adjlistphysics.addvertex(810.000000, 1370.000000)
        self.adjlistphysics.addvertex(865.500000, 1262.000000)
        self.adjlistphysics.addvertex(1033.500000, 920.000000)
        self.adjlistphysics.addvertex(1314.000000, 840.000000)
        self.adjlistphysics.addvertex(1548.000000, 876.000000)
        self.adjlistphysics.addvertex(1701.000000, 1042.000000)
        self.adjlistphysics.addvertex(1846.500000, 1492.000000)
        self.adjlistphysics.addvertex(1716.000000, 1668.000000)
        self.adjlistphysics.addvertex(1521.000000, 1576.000000)
        self.adjlistphysics.addvertex(1578.000000, 1420.000000)
        self.adjlistphysics.addvertex(1639.500000, 1334.000000)
        self.adjlistphysics.addvertex(1557.000000, 1174.000000)
        self.adjlistphysics.addvertex(1110.000000, 1016.000000)
        self.adjlistphysics.addvertex(1687.500000, 1208.000000)
        self.adjlistphysics.addvertex(550.500000, 160.000000)
        self.adjlistphysics.addvertex(403.500000, 298.000000)
        self.adjlistphysics.addvertex(319.500000, 202.000000)
        self.adjlistphysics.addvertex(388.500000, 40.000000)
        self.adjlistphysics.addvertex(556.500000, 60.000000)
        self.adjlistphysics.addvertex(379.500000, 12.000000)
        self.adjlistphysics.addvertex(456.000000, 108.000000)
        self.adjlistphysics.addvertex(1117.500000, 122.000000)
        self.adjlistphysics.addvertex(1116.000000, 116.000000)
        self.adjlistphysics.addvertex(555.000000, 58.000000)
        self.adjlistphysics.addvertex(327.000000, 390.000000)
        self.adjlistphysics.addvertex(282.000000, 448.000000)
        self.adjlistphysics.addvertex(75.000000, 576.000000)
        self.adjlistphysics.addvertex(234.000000, 290.000000)
        self.adjlistphysics.addvertex(12.000000, 402.000000)
        self.adjlistphysics.addvertex(31.500000, 554.000000)
        self.adjlistphysics.addvertex(1619.000000, 386.000000)
        self.adjlistphysics.addvertex(1655.000000, 124.000000)
        self.adjlistphysics.addvertex(1950.500000, 212.000000)
        self.adjlistphysics.addvertex(1959.500000, 338.000000)
        self.adjlistphysics.addvertex(2123.000000, 656.000000)
        self.adjlistphysics.addvertex(2181.500000, 778.000000)
        self.adjlistphysics.addvertex(1938.500000, 812.000000)
        self.adjlistphysics.addvertex(1514.000000, 66.000000)
        self.adjlistphysics.addvertex(1884.500000, 542.000000)
        self.adjlistphysics.addvertex(1877.000000, 660.000000)
        self.adjlistphysics.addvertex(1922.000000, 688.000000)
        self.adjlistphysics.addvertex(1770.500000, 728.000000)
        self.adjlistphysics.addvertex(1707.500000, 496.000000)
        self.adjlistphysics.addvertex(1500.500000, 44.000000)
        self.adjlistphysics.addvertex(2009.000000, 70.000000)
        self.adjlistphysics.addvertex(2028.500000, 40.000000)
        self.adjlistphysics.addvertex(2013.500000, 1620.000000)
        self.adjlistphysics.addvertex(1866.500000, 1820.000000)
        self.adjlistphysics.addvertex(1871.000000, 1938.000000)
        self.adjlistphysics.addvertex(2000.000000, 2114.000000)
        self.adjlistphysics.addvertex(2166.500000, 1966.000000)
        self.adjlistphysics.addvertex(2196.500000, 1778.000000)
        self.adjlistphysics.addvertex(2025.500000, 930.000000)
        self.adjlistphysics.addvertex(1944.500000, 1144.000000)
        self.adjlistphysics.addvertex(2181.500000, 1408.000000)
        self.adjlistphysics.addvertex(2366.000000, 1380.000000)
        self.adjlistphysics.addvertex(2451.500000, 1504.000000)
        self.adjlistphysics.addvertex(2456.000000, 924.000000)
        self.adjlistphysics.addvertex(2307.500000, 1068.000000)
        self.adjlistphysics.addvertex(2150.000000, 1090.000000)
        self.adjlistphysics.addvertex(2170.176322, 636.000000)
        self.adjlistphysics.addvertex(2245.743073, 736.000000)
        self.adjlistphysics.addvertex(2413.501259, 742.000000)
        self.adjlistphysics.addvertex(2461.863980, 792.000000)
        self.adjlistphysics.addvertex(2466.397985, 588.000000)
        self.adjlistphysics.addvertex(2408.967254, 660.000000)
        self.adjlistphysics.addvertex(2339.445844, 666.000000)
        self.adjlistphysics.addvertex(2221.561713, 580.000000)
#Physics boxes
        l = [];        l.append(0);        l.append(1);        l.append(2);        l.append(3);        l.append(4);        l.append(5);
        self.physicsboxes.append((pygame.Rect(286,606,322,398), l))
        l = [];        l.append(6);        l.append(7);        l.append(8);        l.append(9);        l.append(10);        l.append(11);        l.append(12);        l.append(13);        l.append(14);
        self.physicsboxes.append((pygame.Rect(679,318,853,318), l))
        l = [];        l.append(15);        l.append(16);        l.append(17);        l.append(18);        l.append(19);        l.append(20);        l.append(21);        l.append(22);        l.append(23);        l.append(24);        l.append(25);        l.append(26);        l.append(27);
        self.physicsboxes.append((pygame.Rect(580,1032,820,794), l))
        l = [];        l.append(28);        l.append(29);        l.append(30);        l.append(31);        l.append(32);        l.append(33);        l.append(34);        l.append(35);        l.append(36);        l.append(37);        l.append(38);        l.append(39);
        self.physicsboxes.append((pygame.Rect(1027,856,784,778), l))
        l = [];        l.append(40);        l.append(41);        l.append(42);        l.append(43);        l.append(44);        l.append(45);        l.append(46);
        self.physicsboxes.append((pygame.Rect(341,0,250,322), l))
        l = [];        l.append(44);        l.append(47);        l.append(48);        l.append(49);
        self.physicsboxes.append((pygame.Rect(510,2,739,118), l))
        l = [];        l.append(50);        l.append(51);        l.append(52);        l.append(53);        l.append(54);        l.append(55);
        self.physicsboxes.append((pygame.Rect(0,288,313,278), l))
        l = [];        l.append(56);        l.append(57);        l.append(58);        l.append(59);        l.append(60);        l.append(61);        l.append(62);        l.append(63);        l.append(64);        l.append(65);        l.append(66);        l.append(67);        l.append(68);        l.append(69);        l.append(70);        l.append(71);
        self.physicsboxes.append((pygame.Rect(1518,2,663,788), l))
        l = [];        l.append(72);        l.append(73);        l.append(74);        l.append(75);        l.append(76);        l.append(77);
        self.physicsboxes.append((pygame.Rect(1853,1634,345,502), l))
        l = [];        l.append(78);        l.append(79);        l.append(80);        l.append(81);        l.append(82);        l.append(83);        l.append(84);        l.append(85);
        self.physicsboxes.append((pygame.Rect(1952,916,526,590), l))
        l = [];        l.append(86);        l.append(87);        l.append(88);        l.append(89);        l.append(90);        l.append(91);        l.append(92);        l.append(93);
        self.physicsboxes.append((pygame.Rect(2176,526,302,266), l))
