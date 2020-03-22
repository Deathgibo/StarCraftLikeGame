import AdjacencyList
import math
import pygame
import numpy as np
import time

"""
This is a BSP data structure used to see what vertices on the graph are visible from other
vertices. It works like basic BSP trees and stores line segments, it doesnt use pointer nodes though the tree
is implemented as an array. To see whats visible it has a buffer it fills for 360
degrees. It all starts out as false. Then in the bsp order it gets segments, calculates angle between vertex and input point,
if the angle in the buffer is false its visible, after that you set the angles covered by the line to true in the buffer, repeat.
The bsp tree holds its own adjacencylist it uses and is seperate from the world one.

The bspnode stores segments, but the points are indexes to the bsp trees adjacency list vtable, the n is the normal.

"""

class BSPNode():
    def __init__(self, p1, p2, n):
        self.p1index = p1   #index to vertex in its adjacencylist vtable
        self.p2index = p2   #index to vertex in its adjacencylist vtable
        self.n = n          #normal to segment

    #f(p) = n * (p - p1) = 0
    def f(self, pindex, graph):
        return (self.n[0] * (graph.vtable[pindex].pos[0] - graph.vtable[self.p1index].pos[0])) + (self.n[1] * (graph.vtable[pindex].pos[1] - graph.vtable[self.p1index].pos[1]))

    def fpos(self, p, graph, bsp):
        #starttime = time.time()
        #a = (self.n[0] * (p[0] - graph.vtable[self.p1index].pos[0])) + (self.n[1] * (p[1] - graph.vtable[self.p1index].pos[1]))
        #bsp.planetimer = bsp.planetimer + (time.time() - starttime)
        return (self.n[0] * (p[0] - graph.vtable[self.p1index].pos[0])) + (self.n[1] * (p[1] - graph.vtable[self.p1index].pos[1]))

    def angles(self, e, graph):
        return (round(self.angle(self.p1index, e, graph)), round(self.angle(self.p2index, e, graph)))

    def angle(self, p, e, graph, bsp):
        #starttime = time.clock()
        pvec = graph.vtable[p].pos
        dist = math.sqrt((pvec[0] - e[0])**2 + (pvec[1] - e[1])**2)
        if dist == 0:
            print("distance 0")
            return 0.0
        a = math.degrees(math.acos((pvec[0] - e[0]) / dist))
        if pvec[1] > e[1]:
            a = 360 - a
        #bsp.angletimer = bsp.angletimer + (time.clock() - starttime)
        return a

    def intersection(self, other, graph):
        p1 = np.array([graph.vtable[self.p1index].pos[0],graph.vtable[self.p1index].pos[1]])
        p2 = np.array([graph.vtable[self.p2index].pos[0],graph.vtable[self.p2index].pos[1]])
        p3 = np.array([graph.vtable[other.p1index].pos[0],graph.vtable[other.p1index].pos[1]])
        p4 = np.array([graph.vtable[other.p2index].pos[0],graph.vtable[other.p2index].pos[1]])

        d1 = p2 - p1
        d2 = p4 - p3
        D = np.array([[d1[0],d2[0]],[d1[1],d2[1]]])
        b = p3-p1
        det = np.linalg.det(D)
        if det == 0:
            return None
        else:
            Dinv = np.linalg.inv(D)
            t = Dinv.dot(b)
            answer = p1 + t[0]*d1
            return (answer[0],answer[1])


class BSP():
    def __init__(self, adjlist):
        self.angletimer = 0
        self.planetimer = 0
        self.bufferfull = False #lets algorithm know if were done
        self.buffer = [] #holds tuples of ranges from (0,360)
        self.tree = [None] #list holds BSPNodes
        self.graph = adjlist #holds a adjlist with vtable and adjlist
        self.createtree() #function to create tree from given adjlist

    def render(self, display_render, map):
        self.printindex(1, display_render, map)

    def printindex(self, i, display_render, map):
        if len(self.tree) <= i or self.tree[i] is None:
            return
        self.printindex(self.Left(i), display_render, map)

        color = (0,0,0)
        pygame.draw.line(display_render,color, (self.graph.vtable[self.tree[i].p1index].pos[0] - map._cameraposition[0],self.graph.vtable[self.tree[i].p1index].pos[1] - map._cameraposition[1]),
        (self.graph.vtable[self.tree[i].p2index].pos[0] - map._cameraposition[0] ,self.graph.vtable[self.tree[i].p2index].pos[1] - map._cameraposition[1]))
        l = 50
        normalvec = (self.graph.vtable[self.tree[i].p1index].pos[0] + self.tree[i].n[0]*l - map._cameraposition[0],
        self.graph.vtable[self.tree[i].p1index].pos[1] + self.tree[i].n[1] * l - map._cameraposition[1])
        color = (255,255,255)
        pygame.draw.line(display_render,color, (self.graph.vtable[self.tree[i].p1index].pos[0] - map._cameraposition[0],self.graph.vtable[self.tree[i].p1index].pos[1] - map._cameraposition[1])
        , normalvec)

        self.printindex(self.Right(i), display_render, map)

    def Parent(self, i):
        return i>>1;

    def Left(self, i):
        return i<<1

    def Right(self, i):
        return (i<< 1) + 1

    def calculatenormal(self, p1, p2):
        vec = (self.graph.vtable[p1].pos[0] - self.graph.vtable[p2].pos[0],self.graph.vtable[p1].pos[1] - self.graph.vtable[p2].pos[1])
        vecrotate = (-vec[1], vec[0])
        return self.normalize(vecrotate)

    def normalize(self, vec):
        length = math.sqrt(vec[0]**2 + vec[1]**2)

        return (vec[0] / length, vec[1] / length)

    def createtree(self):
        if len(self.graph.vtable) <= 0:
            return
        for x in range(0,len(self.graph.adjlist)):
            for y in range(0,len(self.graph.adjlist[x])):
                if self.graph.adjlist[x][y][0] < x:
                    seg = BSPNode(x,self.graph.adjlist[x][y][0], self.calculatenormal(x,self.graph.adjlist[x][y][0]))
                    self.addsegment(1, seg)

    def addsegment(self, i, seg, x = []):
        if len(self.tree) <= 1:
            self.tree.append(seg)
            x.append(1)
            return
        if self.tree[i] is None:
            self.tree[i] = seg
            x.append(i)
            return
        f1 = self.tree[i].f(seg.p1index, self.graph)
        f2 = self.tree[i].f(seg.p2index, self.graph)
        epsilon = 1
        if abs(f1) < epsilon:
            f1 = 0
        if abs(f2) < epsilon:
            f2 = 0
        if f1 <= 0 and f2 <= 0:
            if len(self.tree) <= self.Left(i):
                self.addsize(self.Left(i))
                self.tree[self.Left(i)] = seg
                x.append(self.Left(i))
            else:
                self.addsegment(self.Left(i), seg, x)
        elif f1 >= 0 and f2 >= 0:
            if len(self.tree) <= self.Right(i):
                self.addsize(self.Right(i))
                self.tree[self.Right(i)] = seg
                x.append(self.Right(i))
            else:
                self.addsegment(self.Right(i), seg, x)
        else:
            #print("cutting")
            intersection = self.tree[i].intersection(seg, self.graph)
            self.graph.deleteedge(seg.p1index,seg.p2index)
            self.graph.addvertex(intersection[0],intersection[1])
            size = len(self.graph.vtable) - 1
            self.graph.addedge(seg.p1index, size)
            self.graph.addedge(seg.p2index, size)

            seg1 = BSPNode(seg.p1index, size, self.calculatenormal(seg.p1index, size))
            seg2 = BSPNode(seg.p2index, size, self.calculatenormal(seg.p2index, size))
            if f1 <= 0:
                if len(self.tree) <= self.Left(i):
                    self.addsize(self.Left(i))
                    self.tree[self.Left(i)] = seg1
                else:
                    self.addsegment(self.Left(i), seg1, x)
                if len(self.tree) <= self.Right(i):
                    self.addsize(self.Right(i))
                    self.tree[self.Right(i)] = seg2
                else:
                    self.addsegment(self.Right(i), seg2, x)
            else:
                if len(self.tree) <= self.Left(i):
                    self.addsize(self.Left(i))
                    self.tree[self.Left(i)] = seg2
                else:
                    self.addsegment(self.Left(i), seg2, x)
                if len(self.tree) <= self.Right(i):
                    self.addsize(self.Right(i))
                    self.tree[self.Right(i)] = seg1
                else:
                    self.addsegment(self.Right(i), seg1, x)


    def addsize(self, indexneeded): #adds size to tree list if needed and sets everything to None
        indexneeded + 1
        len(self.tree)
        for x in range(0, indexneeded + 1 - len(self.tree)):
            self.tree.append(None)

    def isinrange(self, rangez, num):
        if num >= rangez[0] and num <= rangez[1]:
            return True
        return False

    """
    function to see whats visible, recursively sees what side e is on and goes in the order
    closest middle farthest. handlefunction gets the angles, sees if vertex is visible, then
    updates the buffer. For efficiency make a quicker angle function
    """
    def closestnodes(self, e, l):
        self.buffer.clear()
        self.bufferfull = False
        self.angletimer = 0
        self.planetimer = 0
        for x in range(0,len(self.graph.vtable)):
            self.graph.vtable[x].d = -1
        #print("---------")
        self.closestnodesindex(1, e, l)

    def closestnodesindex(self, i , e, l):
        if len(self.tree) <= i or self.tree[i] is None:
            return
        if self.tree[i].fpos(e,self.graph,self) < 0:
            self.closestnodesindex(self.Left(i), e, l)
            self.handlefunction(i, e, l)
            self.closestnodesindex(self.Right(i), e, l)
        else:
            self.closestnodesindex(self.Right(i), e, l)
            self.handlefunction(i, e, l)
            self.closestnodesindex(self.Left(i), e, l)

    def handlefunction(self, i, e, l):
        if self.bufferfull:
            return
        #calculate angles
        anglep1 = self.graph.vtable[self.tree[i].p1index].d
        if anglep1 == -1:
            anglep1 = round(self.tree[i].angle(self.tree[i].p1index, e, self.graph, self))
            self.graph.vtable[self.tree[i].p1index].d = anglep1

        anglep2 = self.graph.vtable[self.tree[i].p2index].d
        if anglep2 == -1:
            anglep2 = round(self.tree[i].angle(self.tree[i].p2index, e, self.graph, self))
            self.graph.vtable[self.tree[i].p2index].d = anglep2
        anglerange = (anglep1, anglep2)

        #see if vertices are visible
        visible = True
        for rangez in self.buffer:
            if self.isinrange(rangez, anglerange[0]):
                visible = False
                break
        if visible:
            l.append(self.tree[i].p1index)

        visible = True
        for rangez in self.buffer:
            if self.isinrange(rangez, anglerange[1]):
                visible = False
                break
        if visible:
            l.append(self.tree[i].p2index)

        #figure out if its cw or ccw
        if anglerange[0] > anglerange[1]:
            anglerange = (anglerange[1], anglerange[0])
        l = []
        if anglerange[1] - anglerange[0] > 180:
            anglerange1 = (0,anglerange[0])
            anglerange2 = (anglerange[1], 360)
            l.append(anglerange1)
            l.append(anglerange2)
        else:
            l.append(anglerange)

        #merge each range
        for x in range(0,len(l)):
            counter =  0
            for y in range(0,len(self.buffer)):
                #check collision
                if l[x][1] < self.buffer[y - counter][0]:
                    continue
                if l[x][0] > self.buffer[y - counter][1]:
                    continue
                #see which has farthest left and right side
                if l[x][0] > self.buffer[y - counter][0]:
                    l[x] = (self.buffer[y - counter][0], l[x][1])
                if l[x][1] < self.buffer[y - counter][1]:
                    l[x] = (l[x][0], self.buffer[y - counter][1])
                self.buffer.pop(y - counter)
                counter = counter + 1
            self.buffer.append(l[x])

        if not self.bufferfull:
            if self.buffer[0][0] == 0 and self.buffer[0][1] == 360:
                self.bufferfull = True
