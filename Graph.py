from Vertex import *

class Graph:
    def __init__(self):
        self.vertList = {} # key is the name, value is the Vertex
        self.numVertices = 0
        self.last = None

    def addVertex(self, key):
        self.numVertices += 1
        newVertex = Vertex(key)
        self.vertList[key] = newVertex
        self.last = newVertex
        return newVertex

    def getVertex(self, n):
        if n in self.vertList:
            return self.vertList[n]
        else:
            return None

    def __contains__(self, n):
        return n in self.vertList

    def addEdge(self, f, t, cost=0):
        if f not in self.vertList:
            nv = self.addVertex(f)
        if t not in self.vertList:
            nv = self.addVertex(t)
        self.vertList[f].addNeighbor(self.vertList[t], cost)
        self.vertList[t].addNeighbor(self.vertList[f], cost)


    def getVertices(self):
        return self.vertList.keys()

    def __iter__(self):
        return iter(self.vertList.values())

def testGraph_():
    g = Graph()
    for i in range(6):
        g.addVertex(i)

    # vertList is a dictionary, keys are i (ints), values are Vertices
    for k in g.vertList:
        print(g.vertList[k])

    g.addEdge(0,1,5)
    g.addEdge(0,5,2)
    g.addEdge(1,2,4)
    g.addEdge(2,3,9)
    g.addEdge(3,4,7)
    g.addEdge(3,5,3)
    g.addEdge(4,0,1)
    g.addEdge(5,4,8)
    g.addEdge(5,2,1)
    for v in g:
        # v = vertList.values which is an array of Vertices
        for w in v.getConnections():

            print("( %s , %s )" % (v.getId(), w.getId()))

    for k in g.vertList:
        print(g.vertList[k])