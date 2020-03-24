import mathfuncs
import PriorityQueue
import time

"""
Adjacencylist is the data structure for holding the graphs. It has a list called vtable
which holds all the actual vertex data. adjlist holds all the edge information in the form
of a tuple(index, weight) index is the index in the vtable and weight is any value needed.
A lot of the time references are made to vtable passing indices around.

"""


# This is a data structure to hold graphs
class AdjacencyList():
    def __init__(self):
        self.vtable = []  # list that holds vertices
        self.adjlist = []  # list that holds edge indexes, adjlist[0] gives list of vertices connected to vtable[0]

    def addvertex(self, x, y):
        v = PriorityQueue.Vertex(x, y)
        self.vtable.append(v)
        v.index = len(self.vtable) - 1
        self.adjlist.append([])

    def deletevertex(self, index):
        self.vtable.pop(index)
        self.adjlist.pop(index)
        for list in self.adjlist:
            counter = 0
            for x in range(0, len(list)):
                if list[x - counter][0] == index:
                    list.pop(x)
                    counter = counter + 1
                elif list[x - counter][0] > index:
                    list[x - counter] = (list[x - counter][0] - 1, list[x - counter][1])

    def addedge(self, index1, index2):
        distance = mathfuncs.mathfuncs.Magnitude((self.vtable[index1].pos[0] - self.vtable[index2].pos[0],
                                                  self.vtable[index1].pos[1] - self.vtable[index2].pos[1]))
        self.adjlist[index1].append((index2, distance))
        self.adjlist[index2].append((index1, distance))

    def deleteedge(self, index1, index2):
        # go to index1 in adjlist and delete index2, then vice versa
        check1 = False
        counter = 0
        for x in range(0, len(self.adjlist[index1])):
            if self.adjlist[index1][x - counter][0] == index2:
                check1 = True
                self.adjlist[index1].pop(x - counter)
                counter = counter + 1
        check2 = False
        counter = 0
        for x in range(0, len(self.adjlist[index2])):
            if self.adjlist[index2][x - counter][0] == index1:
                self.adjlist[index2].pop(x - counter)
                check2 = True
                counter = counter + 1

        if not check1 or not check2:
            print("delete edge didnt delete both")
        if not check1 and not check2:
            print("edge doesnt exist")

    def print(self):
        print("---------------VTable---------------")
        counter = 0
        for x in self.vtable:
            print("[%d | (%f, %f) | %s | %d | " % (counter, x.pos[0], x.pos[1], x.finished, x.d), end='')
            if x.parent is None:
                print("None ]")
            else:
                print("%d ]" % x.parent)
            counter = counter + 1
        print("---------------AdjList---------------")
        counter = 0
        for l in self.adjlist:
            print("[%d ]" % counter, end='')
            for x in l:
                print("| (%d, %f) " % (x[0], x[1]), end='')
            print("")
            counter = counter + 1


"""
def Dijkstra(G, s, e):
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


A = AdjacencyList()
A.addvertex(100,100)
A.addvertex(120,120)
A.addvertex(150,140)
A.addvertex(400,80)
A.addvertex(450,60)
A.addvertex(150,200)
A.addvertex(110,250)
A.addvertex(80,80)
A.addvertex(140,110)
A.addvertex(130,40)
A.addedge(0,1)
A.addedge(1,2)
A.addedge(2,4)
A.addedge(3,4)
A.addedge(6,0)
A.addedge(6,5)
A.addedge(2,5)
A.addedge(8,1)
A.addedge(8,2)
A.addedge(9,7)
A.addedge(9,3)
#A.print()


#shortest path from 0, 2 answer should be 0,1,2
#A.print()
starttime = time.time_ns()
s = 0
e = 1
Dijkstra(A,s,e)
print(time.time_ns() - starttime)
index = A.vtable[e].parent
l = [e]
while index != s:
    l.append(index)
    index = A.vtable[index].parent
l.reverse()
print(l)
A.print()
"""
