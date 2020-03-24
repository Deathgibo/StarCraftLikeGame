"""
This has the priority queue class that the shortest path algorithms use. Its a binary heap
that uses dictionaries for help. The dictionaries map the Heap indices to the vertex table indices.
For shortest path algorithm the queue recieves vertices in the adjacencylist vertex table. These vertices
hold their own .index in them which is used for the mapping. Every time the Heap swap array indices it also swaps
the mappings. The Queue compares .d which represents the distance of the vertices currently.

The vertex class is what the adjacencylist stores as vertices
"""


# This class holds the vertex information for the adjacency List
class Vertex():
    def __init__(self):
        self.pos = (-100, -100)  # position of vertex
        self.found = False  # used for shortest path algorithm / currently in queue
        self.finished = False  # used for shortest path algorithm / popped off queue
        self.parent = None  # used to track path back
        self.index = -1  # its own index in the adjacency lists vtable
        self.d = 0  # variable used for shortest path and also bsp algorithm
        self.highlight = False  # renders it different color

    def __init__(self, x, y):
        self.pos = (x, y)
        self.found = False
        self.finished = False
        self.parent = None
        self.index = -1
        self.d = 0
        self.highlight = False


# This class is the priority queue used for the dijkstra algorithm
class PriorityQueue():
    def __init__(self):
        self.heapsize = 0
        self.A = [Vertex(0, 0)]  # heap starts with junk value at index 0
        self.A[0].d = -10000000  # set it to any value
        self.HtoV = {}  # Heap to Vtable mapping
        self.VtoH = {}  # Vtable to Heap mapping

    def verifymaps(self):
        for H in self.HtoV:
            if self.VtoH[self.HtoV[H]] != H:
                print("error, maps not verified")
                return
        print("correct, maps verified")

    def printmaps(self):
        print("HASH TO VERTEX")
        print(self.HtoV)
        print("VERTEX TO HASH")
        print(self.VtoH)

    def Parent(self, i):
        return i >> 1;

    def Left(self, i):
        return i << 1

    def Right(self, i):
        return (i << 1) + 1

    def MaxHeapify(self, i):
        l = self.Left(i)
        r = self.Right(i)
        largest = 0
        if l <= self.heapsize and self.A[l].d < self.A[i].d:  # self.A[l].d #comparison
            largest = l
        else:
            largest = i
        if r <= self.heapsize and self.A[r].d < self.A[largest].d:  # comparison
            largest = r
        if largest != i:
            self.A[i], self.A[largest] = self.A[largest], self.A[i]
            # map
            self.VtoH[self.HtoV[i]] = largest
            self.VtoH[self.HtoV[largest]] = i
            self.HtoV[i], self.HtoV[largest] = self.HtoV[largest], self.HtoV[i]

            self.MaxHeapify(largest)

    def HeapMaximum(self):
        if len(self.A) > 1:
            return self.A[1]

    def HeapExtractMax(self):
        if self.heapsize < 1:
            print("heap underflow")
            return self.A[0]
        max = self.A[1]
        self.A[1], self.A[self.heapsize] = self.A[self.heapsize], self.A[1]
        self.A[self.heapsize] = Vertex(0, 0)
        self.A[self.heapsize].d = 10000001
        # map
        self.VtoH[self.HtoV[1]] = self.heapsize
        self.VtoH[self.HtoV[self.heapsize]] = 1
        self.HtoV[1], self.HtoV[self.heapsize] = self.HtoV[self.heapsize], self.HtoV[1]

        self.heapsize = self.heapsize - 1
        self.MaxHeapify(1)
        return max

    def HeapIncreaseKey(self, i, val):
        if val.d > self.A[i].d:  # comparison
            print("new key is larger than current key")
            return
        # print(val.d)
        self.A[i] = val
        while i > 1 and self.A[self.Parent(i)].d > self.A[i].d:  # comparison
            self.A[i], self.A[self.Parent(i)] = self.A[self.Parent(i)], self.A[i]

            # map
            self.VtoH[self.HtoV[i]] = self.Parent(i)
            self.VtoH[self.HtoV[self.Parent(i)]] = i
            self.HtoV[i], self.HtoV[self.Parent(i)] = self.HtoV[self.Parent(i)], self.HtoV[i]

            i = self.Parent(i)

    def MaxHeapInsert(self, val):
        self.heapsize = self.heapsize + 1
        # print(self.heapsize + 1)
        # print(len(self.A))
        if self.heapsize + 1 <= len(self.A):
            pass
            # self.A[self.heapsize].d = 10000001
        else:
            self.A.append(val)
        # map
        self.HtoV[self.heapsize] = val.index
        self.VtoH[val.index] = self.heapsize

        self.HeapIncreaseKey(self.heapsize, val)

    def print(self):
        print("heapsize: %d heaplength: %d" % (self.heapsize, len(self.A)))
        for x in range(1, self.heapsize + 1):
            print("%f | %d" % (self.A[x].pos[0], self.A[x].d))


"""
Q = PriorityQueue()
Q.MaxHeapInsert(5)
Q.MaxHeapInsert(3)
Q.MaxHeapInsert(4)
Q.HeapIncreaseKey(2,8)
Q.HeapExtractMax()
Q.HeapExtractMax()
Q.print()
"""
