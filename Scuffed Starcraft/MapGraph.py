#This class handles the graph of vertices and edges over the world which is used for the unit movement algorithms
import AdjacencyList
import pygame
import mathfuncs
import os
import PriorityQueue
import time
import BSP

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
        self.clicky = False
        self.vertexindex = -1

        self.adjlist = AdjacencyList.AdjacencyList()    #world adjlist
        self.adjlistbsp = AdjacencyList.AdjacencyList() #bsp adjlist
        self.createmap() #loads both adjlist
        self.bsp = BSP.BSP(self.adjlistbsp) #creates bsp tree

    def update(self, input, map, displaysurf, cwdpath):
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


        #clicked
        if input.leftclickframe:
            dontreset = False
            worldcoords = map.windowtoworldtransform(input.mouseposition[0],input.mouseposition[1], displaysurf)
            #v
            if self.key == 0:
                self.adjlist.addvertex(worldcoords[0],worldcoords[1])
                self.adjlistbsp.addvertex(worldcoords[0],worldcoords[1])
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
                        self.adjlistbsp.addedge(self.vertexindex,index2)

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

                f.write("#BSP adjacency list\n")
                for vertex in self.adjlistbsp.vtable:
                    f.write("        self.adjlistbsp.addvertex(%f, %f)\n" % (vertex.pos[0],vertex.pos[1]))
                for x in range(0,len(self.adjlistbsp.adjlist)):
                    for node in self.adjlistbsp.adjlist[x]:
                        if node[0] > x:
                            f.write("        self.adjlistbsp.addedge(%d, %d)\n" % (x,node[0]))
                f.close()
                print("File saved")

    def UnitPath(self, unitlocation, clicklocation):
        starttime = time.time()
        unitlist = []
        clicklist = []
        #see if clickpoint is visible from unitlist
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
                values.append((clicklocation[0],clicklocation[1]))
                #print(time.time() - starttime)
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
        values = []
        for x in l:
            val = (self.adjlist.vtable[x].pos[0],self.adjlist.vtable[x].pos[1])
            values.append(val)
        #remove from graph
        self.adjlist.deletevertex(size)
        self.adjlist.deletevertex(size2)
        #print(time.time() - starttime)
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
        for vertex in self.adjlist.vtable:
            color = (0,0,0)
            if vertex.highlight:
                color = (0,0,255)
            pygame.draw.circle(display_render, color,(int(round(vertex.pos[0])) - map._cameraposition[0],
                                int(round(vertex.pos[1])) - map._cameraposition[1]), 10, 0)
        #draw bsp edges
        color = (0,0,0)
        for y in range(0,len(self.adjlistbsp.adjlist)):
            p1 = (self.adjlistbsp.vtable[y].pos[0] - map._cameraposition[0], self.adjlistbsp.vtable[y].pos[1] - map._cameraposition[1])
            for x in range(0,len(self.adjlistbsp.adjlist[y])):
                p2 = (self.adjlistbsp.vtable[self.adjlistbsp.adjlist[y][x][0]].pos[0] - map._cameraposition[0],
                      self.adjlistbsp.vtable[self.adjlistbsp.adjlist[y][x][0]].pos[1] - map._cameraposition[1])
                color = (0,0,0)
                if self.adjlistbsp.vtable[y].highlight and self.adjlistbsp.vtable[self.adjlistbsp.adjlist[y][x][0]].highlight:
                    color = (0,0,255)
                pygame.draw.line(display_render,color, p1, p2)

        #self.bsp.render(display_render, map)

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
                            Q.HeapIncreaseKey(Q.VtoH[neighbor[0]],G.vtable[neighbor[0]])
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
                            Q.HeapIncreaseKey(Q.VtoH[neighbor[0]],G.vtable[neighbor[0]])
                        else:
                            Q.MaxHeapInsert(G.vtable[neighbor[0]])
                            G.vtable[neighbor[0]].found = True


    def createmap(self):

        self.adjlist.addvertex(463.500000, 578.000000)
        self.adjlist.addvertex(327.000000, 694.000000)
        self.adjlist.addvertex(291.000000, 880.000000)
        self.adjlist.addvertex(444.000000, 1040.000000)
        self.adjlist.addvertex(616.500000, 784.000000)
        self.adjlist.addvertex(753.000000, 546.000000)
        self.adjlist.addvertex(654.000000, 384.000000)
        self.adjlist.addvertex(817.500000, 318.000000)
        self.adjlist.addvertex(1126.500000, 326.000000)
        self.adjlist.addvertex(1170.000000, 516.000000)
        self.adjlist.addvertex(340.500000, 210.000000)
        self.adjlist.addvertex(511.500000, 60.000000)
        self.adjlist.addvertex(301.500000, 2.000000)
        self.adjlist.addvertex(10.500000, 28.000000)
        self.adjlist.addvertex(7.500000, 450.000000)
        self.adjlist.addvertex(237.000000, 320.000000)
        self.adjlist.addvertex(312.000000, 394.000000)
        self.adjlist.addvertex(81.000000, 558.000000)
        self.adjlist.addvertex(412.500000, 278.000000)
        self.adjlist.addvertex(534.000000, 146.000000)
        self.adjlist.addvertex(721.500000, 64.000000)
        self.adjlist.addvertex(1120.500000, 102.000000)
        self.adjlist.addvertex(1117.500000, 218.000000)
        self.adjlist.addvertex(93.000000, 870.000000)
        self.adjlist.addvertex(4.500000, 998.000000)
        self.adjlist.addvertex(21.000000, 1264.000000)
        self.adjlist.addvertex(277.500000, 1300.000000)
        self.adjlist.addvertex(634.500000, 1208.000000)
        self.adjlist.addvertex(760.500000, 1032.000000)
        self.adjlist.addvertex(967.500000, 1120.000000)
        self.adjlist.addvertex(787.500000, 1414.000000)
        self.adjlist.addvertex(1056.000000, 922.000000)
        self.adjlist.addvertex(1269.000000, 858.000000)
        self.adjlist.addvertex(1107.000000, 998.000000)
        self.adjlist.addvertex(1432.500000, 1102.000000)
        self.adjlist.addvertex(1521.000000, 886.000000)
        self.adjlist.addvertex(1494.000000, 608.000000)
        self.adjlist.addedge(0, 4)
        self.adjlist.addedge(0, 1)
        self.adjlist.addedge(0, 6)
        self.adjlist.addedge(0, 16)
        self.adjlist.addedge(0, 18)
        self.adjlist.addedge(1, 2)
        self.adjlist.addedge(1, 17)
        self.adjlist.addedge(1, 23)
        self.adjlist.addedge(2, 3)
        self.adjlist.addedge(2, 23)
        self.adjlist.addedge(2, 24)
        self.adjlist.addedge(3, 4)
        self.adjlist.addedge(3, 24)
        self.adjlist.addedge(3, 26)
        self.adjlist.addedge(3, 25)
        self.adjlist.addedge(3, 27)
        self.adjlist.addedge(3, 28)
        self.adjlist.addedge(4, 5)
        self.adjlist.addedge(4, 27)
        self.adjlist.addedge(4, 28)
        self.adjlist.addedge(5, 9)
        self.adjlist.addedge(5, 6)
        self.adjlist.addedge(5, 28)
        self.adjlist.addedge(5, 29)
        self.adjlist.addedge(6, 7)
        self.adjlist.addedge(6, 18)
        self.adjlist.addedge(6, 19)
        self.adjlist.addedge(7, 8)
        self.adjlist.addedge(7, 19)
        self.adjlist.addedge(7, 20)
        self.adjlist.addedge(7, 21)
        self.adjlist.addedge(8, 20)
        self.adjlist.addedge(8, 22)
        self.adjlist.addedge(9, 36)
        self.adjlist.addedge(9, 28)
        self.adjlist.addedge(9, 29)
        self.adjlist.addedge(9, 32)
        self.adjlist.addedge(9, 31)
        self.adjlist.addedge(10, 18)
        self.adjlist.addedge(10, 11)
        self.adjlist.addedge(10, 15)
        self.adjlist.addedge(10, 15)
        self.adjlist.addedge(10, 12)
        self.adjlist.addedge(10, 13)
        self.adjlist.addedge(11, 12)
        self.adjlist.addedge(11, 14)
        self.adjlist.addedge(12, 13)
        self.adjlist.addedge(12, 15)
        self.adjlist.addedge(13, 14)
        self.adjlist.addedge(13, 15)
        self.adjlist.addedge(14, 15)
        self.adjlist.addedge(15, 16)
        self.adjlist.addedge(15, 18)
        self.adjlist.addedge(16, 17)
        self.adjlist.addedge(16, 18)
        self.adjlist.addedge(17, 23)
        self.adjlist.addedge(18, 19)
        self.adjlist.addedge(19, 20)
        self.adjlist.addedge(20, 21)
        self.adjlist.addedge(21, 22)
        self.adjlist.addedge(23, 24)
        self.adjlist.addedge(24, 25)
        self.adjlist.addedge(25, 26)
        self.adjlist.addedge(26, 27)
        self.adjlist.addedge(26, 30)
        self.adjlist.addedge(27, 30)
        self.adjlist.addedge(27, 28)
        self.adjlist.addedge(28, 29)
        self.adjlist.addedge(29, 33)
        self.adjlist.addedge(29, 31)
        self.adjlist.addedge(29, 34)
        self.adjlist.addedge(31, 33)
        self.adjlist.addedge(31, 32)
        self.adjlist.addedge(32, 35)
        self.adjlist.addedge(32, 36)
        self.adjlist.addedge(33, 34)
        self.adjlist.addedge(35, 36)
        #BSP adjacency list
        self.adjlistbsp.addvertex(463.500000, 578.000000)
        self.adjlistbsp.addvertex(327.000000, 694.000000)
        self.adjlistbsp.addvertex(291.000000, 880.000000)
        self.adjlistbsp.addvertex(444.000000, 1040.000000)
        self.adjlistbsp.addvertex(616.500000, 784.000000)
        self.adjlistbsp.addvertex(753.000000, 546.000000)
        self.adjlistbsp.addvertex(654.000000, 384.000000)
        self.adjlistbsp.addvertex(817.500000, 318.000000)
        self.adjlistbsp.addvertex(1126.500000, 326.000000)
        self.adjlistbsp.addvertex(1170.000000, 516.000000)
        self.adjlistbsp.addvertex(340.500000, 210.000000)
        self.adjlistbsp.addvertex(511.500000, 60.000000)
        self.adjlistbsp.addvertex(301.500000, 2.000000)
        self.adjlistbsp.addvertex(10.500000, 28.000000)
        self.adjlistbsp.addvertex(7.500000, 450.000000)
        self.adjlistbsp.addvertex(237.000000, 320.000000)
        self.adjlistbsp.addvertex(312.000000, 394.000000)
        self.adjlistbsp.addvertex(81.000000, 558.000000)
        self.adjlistbsp.addvertex(412.500000, 278.000000)
        self.adjlistbsp.addvertex(534.000000, 146.000000)
        self.adjlistbsp.addvertex(721.500000, 64.000000)
        self.adjlistbsp.addvertex(1120.500000, 102.000000)
        self.adjlistbsp.addvertex(1117.500000, 218.000000)
        self.adjlistbsp.addvertex(93.000000, 870.000000)
        self.adjlistbsp.addvertex(4.500000, 998.000000)
        self.adjlistbsp.addvertex(21.000000, 1264.000000)
        self.adjlistbsp.addvertex(277.500000, 1300.000000)
        self.adjlistbsp.addvertex(634.500000, 1208.000000)
        self.adjlistbsp.addvertex(760.500000, 1032.000000)
        self.adjlistbsp.addvertex(967.500000, 1120.000000)
        self.adjlistbsp.addvertex(787.500000, 1414.000000)
        self.adjlistbsp.addvertex(1056.000000, 922.000000)
        self.adjlistbsp.addvertex(1269.000000, 858.000000)
        self.adjlistbsp.addvertex(1107.000000, 998.000000)
        self.adjlistbsp.addvertex(1432.500000, 1102.000000)
        self.adjlistbsp.addvertex(1521.000000, 886.000000)
        self.adjlistbsp.addvertex(1494.000000, 608.000000)
        self.adjlistbsp.addedge(0, 4)
        self.adjlistbsp.addedge(0, 1)
        self.adjlistbsp.addedge(1, 2)
        self.adjlistbsp.addedge(2, 3)
        self.adjlistbsp.addedge(3, 4)
        self.adjlistbsp.addedge(5, 6)
        self.adjlistbsp.addedge(5, 9)
        self.adjlistbsp.addedge(6, 7)
        self.adjlistbsp.addedge(7, 8)
        self.adjlistbsp.addedge(9, 36)
        self.adjlistbsp.addedge(10, 11)
        self.adjlistbsp.addedge(10, 18)
        self.adjlistbsp.addedge(11, 12)
        self.adjlistbsp.addedge(12, 13)
        self.adjlistbsp.addedge(13, 14)
        self.adjlistbsp.addedge(14, 15)
        self.adjlistbsp.addedge(15, 16)
        self.adjlistbsp.addedge(16, 17)
        self.adjlistbsp.addedge(17, 23)
        self.adjlistbsp.addedge(18, 19)
        self.adjlistbsp.addedge(19, 20)
        self.adjlistbsp.addedge(20, 21)
        self.adjlistbsp.addedge(21, 22)
        self.adjlistbsp.addedge(23, 24)
        self.adjlistbsp.addedge(24, 25)
        self.adjlistbsp.addedge(25, 26)
        self.adjlistbsp.addedge(27, 28)
        self.adjlistbsp.addedge(27, 30)
        self.adjlistbsp.addedge(28, 29)
        self.adjlistbsp.addedge(31, 33)
        self.adjlistbsp.addedge(31, 32)
        self.adjlistbsp.addedge(32, 35)
        self.adjlistbsp.addedge(33, 34)

        """self.adjlist.addvertex(418.500000, 464.000000)
        self.adjlist.addvertex(331.500000, 754.000000)
        self.adjlist.addvertex(573.000000, 942.000000)
        self.adjlist.addvertex(675.000000, 602.000000)
        self.adjlist.addvertex(357.000000, 196.000000)
        self.adjlist.addvertex(85.500000, 252.000000)
        self.adjlist.addvertex(639.000000, 406.000000)
        self.adjlist.addvertex(531.000000, 284.000000)
        self.adjlist.addedge(0, 1)
        self.adjlist.addedge(0, 7)
        self.adjlist.addedge(1, 2)
        self.adjlist.addedge(2, 3)
        self.adjlist.addedge(3, 6)
        self.adjlist.addedge(4, 5)
        self.adjlist.addedge(4, 7)
        self.adjlist.addedge(6, 7)"""


        #BSP graph
        """self.adjlist.addvertex(459.000000, 568.000000)
        self.adjlist.addvertex(322.500000, 702.000000)
        self.adjlist.addvertex(286.500000, 878.000000)
        self.adjlist.addvertex(451.500000, 1034.000000)
        self.adjlist.addvertex(610.500000, 790.000000)
        self.adjlist.addvertex(762.000000, 548.000000)
        self.adjlist.addvertex(669.000000, 386.000000)
        self.adjlist.addvertex(415.500000, 270.000000)
        self.adjlist.addvertex(348.000000, 212.000000)
        self.adjlist.addvertex(240.000000, 310.000000)
        self.adjlist.addvertex(301.500000, 386.000000)
        self.adjlist.addvertex(271.500000, 422.000000)
        self.adjlist.addvertex(57.000000, 558.000000)
        self.adjlist.addvertex(529.500000, 144.000000)
        self.adjlist.addvertex(537.000000, 38.000000)
        self.adjlist.addvertex(1114.500000, 348.000000)
        self.adjlist.addvertex(1111.500000, 90.000000)
        self.adjlist.addvertex(1108.500000, 206.000000)
        self.adjlist.addvertex(1210.500000, 200.000000)
        self.adjlist.addvertex(1209.000000, 104.000000)
        self.adjlist.addvertex(370.500000, 186.000000)
        self.adjlist.addvertex(451.500000, 180.000000)
        self.adjlist.addvertex(505.500000, 130.000000)
        self.adjlist.addvertex(504.000000, 48.000000)
        self.adjlist.addvertex(108.000000, 438.000000)
        self.adjlist.addvertex(12.000000, 458.000000)
        self.adjlist.addvertex(27.000000, 814.000000)
        self.adjlist.addvertex(100.500000, 868.000000)
        self.adjlist.addvertex(1179.000000, 518.000000)
        self.adjlist.addvertex(400.500000, 20.000000)
        self.adjlist.addvertex(3.000000, 50.000000)
        self.adjlist.addvertex(130.500000, 6.000000)
        self.adjlist.addvertex(277.500000, 6.000000)
        self.adjlist.addvertex(897.000000, 518.000000)
        self.adjlist.addvertex(807.000000, 328.000000)
        self.adjlist.addvertex(1122.000000, 314.000000)
        self.adjlist.addvertex(1200.000000, 310.000000)
        self.adjlist.addvertex(1224.000000, 340.000000)
        self.adjlist.addvertex(1224.000000, 412.000000)
        self.adjlist.addvertex(1284.000000, 478.000000)
        self.adjlist.addvertex(1366.500000, 468.000000)
        self.adjlist.addvertex(1411.500000, 526.000000)
        self.adjlist.addvertex(1492.500000, 520.000000)
        self.adjlist.addvertex(1512.000000, 606.000000)
        self.adjlist.addvertex(1395.000000, 602.000000)
        self.adjlist.addvertex(1201.500000, 566.000000)
        self.adjlist.addedge(0, 4)
        self.adjlist.addedge(0, 1)
        self.adjlist.addedge(1, 2)
        self.adjlist.addedge(2, 3)
        self.adjlist.addedge(3, 4)
        self.adjlist.addedge(5, 6)
        self.adjlist.addedge(5, 33)
        self.adjlist.addedge(6, 34)
        self.adjlist.addedge(7, 8)
        self.adjlist.addedge(7, 13)
        self.adjlist.addedge(8, 20)
        self.adjlist.addedge(9, 10)
        self.adjlist.addedge(9, 24)
        self.adjlist.addedge(10, 11)
        self.adjlist.addedge(11, 12)
        self.adjlist.addedge(12, 26)
        self.adjlist.addedge(13, 14)
        self.adjlist.addedge(14, 16)
        self.adjlist.addedge(15, 34)
        self.adjlist.addedge(15, 35)
        self.adjlist.addedge(16, 17)
        self.adjlist.addedge(17, 18)
        self.adjlist.addedge(18, 19)
        self.adjlist.addedge(20, 21)
        self.adjlist.addedge(21, 22)
        self.adjlist.addedge(22, 23)
        self.adjlist.addedge(23, 29)
        self.adjlist.addedge(24, 25)
        self.adjlist.addedge(25, 30)
        self.adjlist.addedge(26, 27)
        self.adjlist.addedge(28, 33)
        self.adjlist.addedge(28, 45)
        self.adjlist.addedge(29, 32)
        self.adjlist.addedge(30, 31)
        self.adjlist.addedge(31, 32)
        self.adjlist.addedge(35, 36)
        self.adjlist.addedge(36, 37)
        self.adjlist.addedge(37, 38)
        self.adjlist.addedge(38, 39)
        self.adjlist.addedge(39, 40)
        self.adjlist.addedge(40, 41)
        self.adjlist.addedge(41, 42)
        self.adjlist.addedge(42, 43)
        self.adjlist.addedge(43, 44)
        self.adjlist.addedge(44, 45)"""


        """ map graph
        self.adjlist.addvertex(456.000000, 567.000000)
        self.adjlist.addvertex(324.000000, 688.000000)
        self.adjlist.addvertex(294.000000, 874.000000)
        self.adjlist.addvertex(411.000000, 1021.000000)
        self.adjlist.addvertex(464.000000, 1025.000000)
        self.adjlist.addvertex(598.000000, 848.000000)
        self.adjlist.addvertex(594.000000, 738.000000)
        self.adjlist.addvertex(659.625000, 385.000000)
        self.adjlist.addvertex(684.000000, 492.500000)
        self.adjlist.addvertex(762.750000, 552.500000)
        self.adjlist.addvertex(1180.875000, 515.000000)
        self.adjlist.addvertex(982.125000, 1125.000000)
        self.adjlist.addvertex(884.625000, 1052.500000)
        self.adjlist.addvertex(764.625000, 1035.000000)
        self.adjlist.addvertex(639.000000, 1195.000000)
        self.adjlist.addvertex(809.625000, 1292.500000)
        self.adjlist.addvertex(775.875000, 1407.500000)
        self.adjlist.addvertex(1250.250000, 855.000000)
        self.adjlist.addvertex(1042.125000, 915.000000)
        self.adjlist.addvertex(1109.625000, 997.500000)
        self.adjlist.addvertex(1242.750000, 1005.000000)
        self.adjlist.addvertex(813.375000, 315.000000)
        self.adjlist.addvertex(1126.500000, 332.500000)
        self.adjlist.addvertex(69.000000, 524.000000)
        self.adjlist.addvertex(301.500000, 380.000000)
        self.adjlist.addvertex(238.500000, 308.000000)
        self.adjlist.addvertex(33.000000, 472.000000)
        self.adjlist.addvertex(405.000000, 278.000000)
        self.adjlist.addvertex(343.500000, 212.000000)
        self.adjlist.addvertex(439.500000, 186.000000)
        self.adjlist.addvertex(505.500000, 118.000000)
        self.adjlist.addvertex(490.500000, 22.000000)
        self.adjlist.addvertex(537.000000, 134.000000)
        self.adjlist.addvertex(534.000000, 50.000000)
        self.adjlist.addvertex(720.000000, 62.000000)
        self.adjlist.addvertex(1.500000, 372.000000)
        self.adjlist.addvertex(12.000000, 34.000000)
        self.adjlist.addvertex(216.000000, 12.000000)
        self.adjlist.addvertex(1117.500000, 98.000000)
        self.adjlist.addvertex(31.500000, 812.000000)
        self.adjlist.addvertex(100.500000, 874.000000)
        self.adjlist.addedge(0, 1)
        self.adjlist.addedge(0, 6)
        self.adjlist.addedge(0, 7)
        self.adjlist.addedge(0, 8)
        self.adjlist.addedge(0, 24)
        self.adjlist.addedge(1, 2)
        self.adjlist.addedge(2, 3)
        self.adjlist.addedge(2, 40)
        self.adjlist.addedge(2, 40)
        self.adjlist.addedge(2, 40)
        self.adjlist.addedge(2, 40)
        self.adjlist.addedge(2, 40)
        self.adjlist.addedge(3, 4)
        self.adjlist.addedge(4, 5)
        self.adjlist.addedge(4, 14)
        self.adjlist.addedge(4, 13)
        self.adjlist.addedge(5, 6)
        self.adjlist.addedge(5, 13)
        self.adjlist.addedge(6, 8)
        self.adjlist.addedge(6, 9)
        self.adjlist.addedge(7, 8)
        self.adjlist.addedge(7, 21)
        self.adjlist.addedge(7, 27)
        self.adjlist.addedge(8, 9)
        self.adjlist.addedge(9, 10)
        self.adjlist.addedge(9, 18)
        self.adjlist.addedge(9, 13)
        self.adjlist.addedge(9, 12)
        self.adjlist.addedge(10, 17)
        self.adjlist.addedge(10, 18)
        self.adjlist.addedge(11, 12)
        self.adjlist.addedge(11, 19)
        self.adjlist.addedge(11, 20)
        self.adjlist.addedge(12, 13)
        self.adjlist.addedge(12, 18)
        self.adjlist.addedge(12, 19)
        self.adjlist.addedge(13, 14)
        self.adjlist.addedge(14, 15)
        self.adjlist.addedge(14, 16)
        self.adjlist.addedge(15, 16)
        self.adjlist.addedge(17, 18)
        self.adjlist.addedge(18, 19)
        self.adjlist.addedge(19, 20)
        self.adjlist.addedge(21, 22)
        self.adjlist.addedge(21, 34)
        self.adjlist.addedge(22, 38)
        self.adjlist.addedge(23, 24)
        self.adjlist.addedge(23, 39)
        self.adjlist.addedge(24, 25)
        self.adjlist.addedge(24, 27)
        self.adjlist.addedge(25, 26)
        self.adjlist.addedge(26, 35)
        self.adjlist.addedge(27, 32)
        self.adjlist.addedge(27, 28)
        self.adjlist.addedge(28, 29)
        self.adjlist.addedge(29, 30)
        self.adjlist.addedge(30, 31)
        self.adjlist.addedge(31, 37)
        self.adjlist.addedge(32, 33)
        self.adjlist.addedge(33, 34)
        self.adjlist.addedge(34, 38)
        self.adjlist.addedge(35, 36)
        self.adjlist.addedge(36, 37)
        self.adjlist.addedge(39, 40)
        """
