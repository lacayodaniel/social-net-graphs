import sys
class Vertex:
    def __init__(self, key):
        self.id = key
        self.connectedTo = {} # key is Vertex, value is weight
        self.dist = sys.maxsize
        self.prev = None
        self.color = 'white'
        self.closeness = 0

    def addNeighbor(self, nbr, weight=0):
        self.connectedTo[nbr] = weight

    def numberOfNeighbors(self):
        return len(self.connectedTo)

    def neighborsIsEmpty(self):
        return self.numberOfNeighbors() == 0

    def setDistance(self, d):
        self.dist = d

    def setPrev(self, prev):
        self.prev = prev

    def setCloseness(self, score):
        self.closeness = score

    def setColor(self, color):
        self.color = color

    def getDistance(self):
        return self.dist

    def getPrev(self):
        return self.prev

    def getCloseness(self):
        return self.closeness

    def getColor(self):
        return self.color

    def getConnections(self):
        return self.connectedTo.keys()

    def getId(self):
        return self.id

    def getWeight(self, nbr):
        return self.connectedTo[nbr]

    def __str__(self):
        return str(self.id) + " connectedTo: " + str([x.id for x in self.connectedTo])