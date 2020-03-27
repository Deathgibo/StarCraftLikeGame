import queue
import random
import mathfuncs
import pygame
from pygame.locals import *
#import Marine

#QuadTree is a spatial data structure that helps with optimizing the entity functions
#like finding near enemies, and near teammates when colliding
#its not too good because it pays of when N is higher around 100+ but it still beats the N^2 method

class Quadnode():
    def __init__(self):
        self.square = (0.0,0.0,0.0,0.0) #rect (x,y,w,h)
        self.info = []       #data type
        self.topleft = None     #Quadnode
        self.topright = None    #Quadnode
        self.bottomleft = None  #Quadnode
        self.bottomright = None #Quadnode
        self.parent = None      #(Quadnode,int)
    def __init__(self,sq):
        self.square = sq
        self.info = []       #data type
        self.topleft = None     #Quadnode
        self.topright = None    #Quadnode
        self.bottomleft = None  #Quadnode
        self.bottomright = None #Quadnode
        self.parent = None      #(Quadnode,int)
    def isleaf(self):
        #print(self.topleft, self.topright, self.bottomleft,self.bottomright)
        if self.topleft is None and self.topright is None and self.bottomleft is None and self.bottomright is None:
            return True
        return False

class Quadtree():
    def __init__(self):
        self.root = Quadnode((-300.0,-300.0,3000.0,3000.0))

    def boundary(self, node, data):
        #print("x: %f y: %f w: %f h: %f data: (%f,%f)" % (node.square[0],node.square[1],node.square[2],node.square[3], data[0],data[1]))
        if data[0] < node.square[0] or data[0] > (node.square[0] + node.square[2]):
            return False
        if data[1] < node.square[1] or data[1] > (node.square[1] + node.square[3]):
            return False
        return True

    def slot(self, node, data):#(value, cx, cy)
        center = (node.square[0] + (node.square[2]/2.0), node.square[1] + (node.square[3]/2.0))
        if data[0] <= center[0]:
            #bottomleft
            if data[1] <= center[1]:
                return (0,center[0],center[1])
            #topleft
            else:
                return (1,center[0],center[1])
        else:
            #bottomright
            if data[1] <= center[1]:
                return (3,center[0],center[1])
             #topright
            else:
                return (2,center[0],center[1])

    def insertstart(self, data):
        self.insert(self.root,data,False)

    def insert(self, node, data, reinsert = False):
        if node is None:
            print("node is None")
            return

        if not self.boundary(node,data.circlecenter):
            print("node out of boundary")
            return

        if (node.square[2] < 0.05 and node.square[3] < 0.05):
            node.info.append(data)
            #print("square too small")
            return


        slot = self.slot(node, data.circlecenter)
        #bottomleft
        if slot[0] == 0:
            if node.bottomleft is not None:
                self.insert(node.bottomleft,data)
            else:
                isleaf = node.isleaf()
                #see if theres a data in child if not insert else insert both again
                if isleaf and len(node.info) == 0:
                    node.info.append(data)
                else:
                    node.bottomleft = Quadnode((node.square[0],node.square[1],node.square[2]/2.0,node.square[3]/2.0))
                    node.bottomleft.parent = (node,0)
                    if reinsert is False and isleaf:
                        self.insert(node,node.info[0],True)
                        node.info.clear()
                    self.insert(node.bottomleft,data)
        #topleft
        elif slot[0] == 1:
            if node.topleft is not None:
                self.insert(node.topleft,data)
            else:
                isleaf = node.isleaf()
                if isleaf and len(node.info) == 0:
                    node.info.append(data)
                else:
                    node.topleft = Quadnode((node.square[0],slot[2],node.square[2]/2.0,node.square[3]/2.0))
                    node.topleft.parent = (node,1)
                    if reinsert is False and isleaf:
                        self.insert(node,node.info[0],True)
                        node.info.clear()
                    self.insert(node.topleft,data)
        #topright
        elif slot[0] == 2:
            if node.topright is not None:
                self.insert(node.topright,data)
            else:
                isleaf = node.isleaf()
                if isleaf and len(node.info) == 0:
                    node.info.append(data)
                else:
                    node.topright = Quadnode((slot[1],slot[2],node.square[2]/2.0,node.square[3]/2.0))
                    node.topright.parent = (node,2)
                    if reinsert is False and isleaf:
                        self.insert(node,node.info[0],True)
                        node.info.clear()
                    self.insert(node.topright,data)
        #bottomright
        elif slot[0] == 3:
            if node.bottomright is not None:
                self.insert(node.bottomright,data)
            else:
                isleaf = node.isleaf()
                if isleaf and len(node.info) == 0:
                    node.info.append(data)
                else:
                    node.bottomright = Quadnode((slot[1],node.square[1],node.square[2]/2.0,node.square[3]/2.0))
                    node.bottomright.parent = (node,3)
                    if reinsert is False and isleaf:
                        self.insert(node,node.info[0],True)
                        node.info.clear()
                    self.insert(node.bottomright,data)

    def deletestart(self, data):
        self.delete(self.root,data)

    def delete(self, node, data):
        if node is None:
            print("node is None cant delete ")
            return

        if not self.boundary(node,data.circlecenter):
            print("node out of boundary cant delete")
            return

        if node.isleaf():
            #remove from list, if list is empty also remove node from parent
            for x in range(0,len(node.info)):
                if node.info[x] == data:
                    node.info.pop(x)
                    break
            if len(node.info) == 0 and node.parent is not None:
             condition = True
             quadrant = node.parent[1]
             pnode = node.parent[0]
             while condition:
                if quadrant == 0:
                    pnode.bottomleft = None
                elif quadrant == 1:
                    pnode.topleft = None
                elif quadrant == 2:
                    pnode.topright = None
                elif quadrant == 3:
                    pnode.bottomright = None
                condition = pnode.isleaf()
                if pnode.parent is None:
                    condition = False
                else:
                    quadrant = pnode.parent[1]
                    pnode = pnode.parent[0]
            return

        slot = self.slot(node, data.circlecenter)
        if slot[0] == 0:
            self.delete(node.bottomleft, data)
        elif slot[0] == 1:
            self.delete(node.topleft, data)
        elif slot[0] == 2:
            self.delete(node.topright, data)
        elif slot[0] == 3:
            self.delete(node.bottomright, data)



    def print(self):
        if self.root is None:
            print("empty")
            return
        r = (self.root,0, 'R')
        q = queue.Queue()
        q.put(r)
        depth = 0
        highestsize = 0
        while not q.empty():
            top = q.get()
            depth = top[1]

            if top[2] == 'BL':
                print("next")
            if top[0] is None:
                print("(NA, %f, %s)" % (top[1], top[2]))
            else:
                if len(top[0].info) > highestsize:
                    highestsize = len(top[0].info)
                if len(top[0].info) == 0:
                    print("(node, %f, %s)" % (top[1], top[2]))
                else:
                    print("(leaf, %f, %f, %f, %s)" % (top[0].info[0].circlecenter[0],top[0].info[0].circlecenter[1],top[1], top[2]))

                if top[0].bottomleft is not None:
                    q.put((top[0].bottomleft,top[1] + 1, 'BL'))
                else:
                    q.put((None,top[1] + 1, 'BL'))

                if top[0].topleft is not None:
                    q.put((top[0].topleft,top[1] + 1, 'TL'))
                else:
                    q.put((None,top[1] + 1, 'TL'))

                if top[0].topright is not None:
                    q.put((top[0].topright,top[1] + 1, 'TR'))
                else:
                    q.put((None,top[1] + 1, 'TR'))

                if top[0].bottomright is not None:
                    q.put((top[0].bottomright,top[1] + 1, 'BR'))
                else:
                    q.put((None,top[1] + 1, 'BR'))

        print("max depth: %d highest list size: %d" % (depth,highestsize))

    def iterategen(self):
            if self.root is None:
                return None
            q = queue.Queue()
            q.put(self.root)

            while not q.empty():
                top = q.get()

                if top.bottomleft is not None:
                    q.put(top.bottomleft)

                if top.topleft is not None:
                    q.put(top.topleft)

                if top.topright is not None:
                    q.put(top.topright)

                if top.bottomright is not None:
                    q.put(top.bottomright)

                if top.isleaf():
                    for info in top.info:
                        yield info

    def PointsInBoxStart(self, box, l):    #box should be a pygame.Rect
        self.PointsInBox(self.root,box, l, False)

    def PointsInBox(self, node, box, l, inside):
        if node.isleaf():
            if inside:
                for x in range(0,len(node.info)):
                    l.append(node.info[x])
            else:
                for x in range(0,len(node.info)):
                    if mathfuncs.mathfuncs.rectcirclecollision(box[0],box[1],box[2],box[3],node.info[x].circlecenter[0],node.info[x].circlecenter[1],node.info[x].radius):
                        l.append(node.info[x])
                    #if box.collidepoint(node.info[x].circlecenter[0],node.info[x].circlecenter[1]):
                        #l.append(node.info[x])
            return

        if node.bottomleft is not None:
            if inside:
                self.PointsInBox(node.bottomleft, box, l, True)

            if box.colliderect(node.bottomleft.square):
                self.PointsInBox(node.bottomleft, box, l, box.contains(node.bottomleft.square))#False
        if node.topleft is not None:
            if inside:
                self.PointsInBox(node.topleft, box, l, True)

            if box.colliderect(node.topleft.square):
                self.PointsInBox(node.topleft, box, l, box.contains(node.topleft.square))
        if node.topright is not None:
            if inside:
                self.PointsInBox(node.topright, box, l, True)

            if box.colliderect(node.topright.square):
                self.PointsInBox(node.topright, box, l, box.contains(node.topright.square))
        if node.bottomright is not None:
            if inside:
                self.PointsInBox(node.bottomright, box, l, True)

            if box.colliderect(node.bottomright.square):
                self.PointsInBox(node.bottomright, box, l, box.contains(node.bottomright.square))

    def PointsInCircleStart(self, circle, l, unitrepeat):    #box should be a pygame.Rect
        return self.PointsInCircle(self.root,circle, l, False, unitrepeat)

    def PointsInCircle(self, node, circle, l, inside, unitrepeat):
        if node.isleaf():
            if inside:
                for x in range(0,len(node.info)):
                    if node.info[x] not in unitrepeat:
                        return node.info[x]
                    """if len(unitrepeat) == 0:
                        return node.info[x]
                    else:
                        for y in unitrepeat:
                            if node.info[x] != y:
                                return node.info[x]"""
            else:
                for x in range(0,len(node.info)):
                    if mathfuncs.mathfuncs.pointcirclecollision(node.info[x].circlecenter,circle) and node.info[x] not in unitrepeat:
                        return node.info[x]
                        """if len(unitrepeat) == 0:
                            return node.info[x]
                        else:
                            for y in unitrepeat:
                                if node.info[x] != y:
                                    return node.info[x]"""
                    #l.append(node.info[x])
            return None

        if node.bottomleft is not None:
            if inside:
                self.PointsInCircle(node.bottomleft, circle, l, True, unitrepeat)
            if mathfuncs.mathfuncs.rectcirclecollision(node.bottomleft.square[0],node.bottomleft.square[1],node.bottomleft.square[2],node.bottomleft.square[3],circle[0],circle[1],circle[2]):
                unit = self.PointsInCircle(node.bottomleft, circle, l,mathfuncs.mathfuncs.boxincircle(node.bottomleft.square[0],node.bottomleft.square[1],node.bottomleft.square[2],node.bottomleft.square[3],circle[0],circle[1],circle[2]), unitrepeat)
                if unit is not None:
                    return unit

        if node.topleft is not None:
            if inside:
                self.PointsInCircle(node.topleft, circle, l, True, unitrepeat)
            if mathfuncs.mathfuncs.rectcirclecollision(node.topleft.square[0],node.topleft.square[1],node.topleft.square[2],node.topleft.square[3],circle[0],circle[1],circle[2]):
                unit = self.PointsInCircle(node.topleft, circle, l, mathfuncs.mathfuncs.boxincircle(node.topleft.square[0],node.topleft.square[1],node.topleft.square[2],node.topleft.square[3],circle[0],circle[1],circle[2]), unitrepeat)
                if unit is not None:
                    return unit

        if node.topright is not None:
            if inside:
                self.PointsInCircle(node.topright, circle, l, True, unitrepeat)
            if mathfuncs.mathfuncs.rectcirclecollision(node.topright.square[0],node.topright.square[1],node.topright.square[2],node.topright.square[3],circle[0],circle[1],circle[2]):
                unit = self.PointsInCircle(node.topright, circle, l, mathfuncs.mathfuncs.boxincircle(node.topright.square[0],node.topright.square[1],node.topright.square[2],node.topright.square[3],circle[0],circle[1],circle[2]), unitrepeat)
                if unit is not None:
                    return unit

        if node.bottomright is not None:
            if inside:
                self.PointsInCircle(node.bottomright, circle, l, True, unitrepeat)
            if mathfuncs.mathfuncs.rectcirclecollision(node.bottomright.square[0],node.bottomright.square[1],node.bottomright.square[2],node.bottomright.square[3],circle[0],circle[1],circle[2]):
                unit = self.PointsInCircle(node.bottomright, circle, l, mathfuncs.mathfuncs.boxincircle(node.bottomright.square[0],node.bottomright.square[1],node.bottomright.square[2],node.bottomright.square[3],circle[0],circle[1],circle[2]), unitrepeat)
                if unit is not None:
                    return unit

        return None

    def PointslistInCircleStart(self, circle, l):    #box should be a pygame.Rect
        return self.PointslistInCircle(self.root,circle, l, False)

    def PointslistInCircle(self, node, circle, l, inside):
        if node.isleaf():
            if inside:
                for x in range(0,len(node.info)):
                    l.append(node.info[x])
            else:
                for x in range(0,len(node.info)):
                    if mathfuncs.mathfuncs.pointcirclecollision(node.info[x].circlecenter,circle):
                        l.append(node.info[x])

        if node.bottomleft is not None:
            if inside:
                self.PointslistInCircle(node.bottomleft, circle, l, True)
            if mathfuncs.mathfuncs.rectcirclecollision(node.bottomleft.square[0],node.bottomleft.square[1],node.bottomleft.square[2],node.bottomleft.square[3],circle[0],circle[1],circle[2]):
                self.PointslistInCircle(node.bottomleft, circle, l,mathfuncs.mathfuncs.boxincircle(node.bottomleft.square[0],node.bottomleft.square[1],node.bottomleft.square[2],node.bottomleft.square[3],circle[0],circle[1],circle[2]))

        if node.topleft is not None:
            if inside:
                self.PointslistInCircle(node.topleft, circle, l, True)
            if mathfuncs.mathfuncs.rectcirclecollision(node.topleft.square[0],node.topleft.square[1],node.topleft.square[2],node.topleft.square[3],circle[0],circle[1],circle[2]):
                self.PointslistInCircle(node.topleft, circle, l, mathfuncs.mathfuncs.boxincircle(node.topleft.square[0],node.topleft.square[1],node.topleft.square[2],node.topleft.square[3],circle[0],circle[1],circle[2]))

        if node.topright is not None:
            if inside:
                self.PointslistInCircle(node.topright, circle, l, True)
            if mathfuncs.mathfuncs.rectcirclecollision(node.topright.square[0],node.topright.square[1],node.topright.square[2],node.topright.square[3],circle[0],circle[1],circle[2]):
                self.PointslistInCircle(node.topright, circle, l, mathfuncs.mathfuncs.boxincircle(node.topright.square[0],node.topright.square[1],node.topright.square[2],node.topright.square[3],circle[0],circle[1],circle[2]))

        if node.bottomright is not None:
            if inside:
                self.PointsInCircle(node.bottomright, circle, l, True)
            if mathfuncs.mathfuncs.rectcirclecollision(node.bottomright.square[0],node.bottomright.square[1],node.bottomright.square[2],node.bottomright.square[3],circle[0],circle[1],circle[2]):
                self.PointsInCircle(node.bottomright, circle, l, mathfuncs.mathfuncs.boxincircle(node.bottomright.square[0],node.bottomright.square[1],node.bottomright.square[2],node.bottomright.square[3],circle[0],circle[1],circle[2]))



"""
#x = input("quad tree")
entitylist = []
for x in range(0,10):
    marinerect = pygame.Rect(100,300 + x*30,50,50)
    entity1 = Marine.Marine(15,None,marinerect)
    entitylist.append(entity1)

Q = Quadtree()
for entity in entitylist:
    Q.insertstart(entity)

#Q.print()
#Q.insertstart((0.66,9.55))
#Q.insertstart((0.71,1.1))
#Q.insertstart((3,5))
gen = Q.iterategen()
for leaf in gen:
    leaf
    print("(%f,%f)" % (leaf.circlecenter[0],leaf.circlecenter[1]))

print("------------------")
for x in range(0,5):
    Q.deletestart(entitylist[x])
    print("deleting (%f, %f)" % (entitylist[x].circlecenter[0],entitylist[x].circlecenter[1]))
print("------------------")

gen = Q.iterategen()
for leaf in gen:
    leaf
    print("(%f,%f)" % (leaf.circlecenter[0],leaf.circlecenter[1]))
#Q.print()
"""
