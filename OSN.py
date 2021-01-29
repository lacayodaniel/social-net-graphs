from Graph import *
from QueueE import *
import sys
from PriorityQueue import *

class OSN:
    def __init__(self):
        self.network = Graph()
        self.MST = Graph()

    # get the size of the network
    def size(self):
        return self.network.numVertices

    # build a network from a csv file
    def buildGraph(self, filename): # load data file and build graph
        raw_data = open(filename, "r") # , encoding='utf-8-sig'
        list_data = raw_data.readlines()
        raw_data.close()
        # parse list_data, create node objects
        for each_line in list_data:
            row = each_line.split(',')
            self.network.addEdge(row[0], row[1], int(row[2]))

    # build a test graph for debugging
    def _buildGraph(self):
        # From A
        self.network.addEdge("A", "B", 8)
        self.network.addEdge("A", "C", 2)
        self.network.addEdge("A", "D", 5)
        self.network.addEdge("A", "Z", 1)
        # From B
        self.network.addEdge("B", "D", 2)
        self.network.addEdge("B", "F", 13)
        # From C
        self.network.addEdge("C", "D", 2)
        self.network.addEdge("C", "E", 5)
        # From D
        self.network.addEdge("D", "F", 6)
        self.network.addEdge("D", "G", 3)
        self.network.addEdge("D", "E", 1)
        # From E
        self.network.addEdge("E", "G", 1)
        # From F
        self.network.addEdge("F", "G", 2)
        self.network.addEdge("F", "H", 3)
        # From G
        self.network.addEdge("G", "H", 6)
        # From Z
        self.network.addEdge("Z", "E", 10)
        self.network.addEdge("Z", "D", 10)
        self.network.addEdge("Z", "Y", 8)
        # From

    # return the number of friends between two users in the network
    def findDistance(self, user1, user2):
        # if the users are not in the network return 0
        if not self.network.__contains__(user1) or not self.network.__contains__(user2):
            return 0

        # convert user1 and user2 from names to their respective vertex from
        u1Vertex = self.network.getVertex(user1)
        u2Vertex = self.network.getVertex(user2)

        # create the queue for BFS and queue user1
        vertQ = Queue()
        vertQ.enqueue(u1Vertex)
        while vertQ.size() > 0:
            currentVert = vertQ.dequeue()

            # user found, return distance
            if currentVert == u2Vertex:
                # since the nodes start at sys.maxsize, the distance is the difference
                dist = sys.maxsize - currentVert.getDistance()
                self.resetNetwork()
                return dist

            # visit all neighboring nodes, set their prev to currentVert, queue them to do the same for their neighbors
            for nbr in currentVert.getConnections():
                if nbr.getDistance() == sys.maxsize:
                    nbr.setDistance(currentVert.getDistance() - 1)
                    nbr.setPrev(currentVert)
                    vertQ.enqueue(nbr)

    # build a maximum spanning tree using BFS
    def buildMST(self):
        # create a node to start from and set its distance to 0
        start = self.network.getVertex(list(self.network.vertList.keys())[0])
        start.setDistance(0)

        # create the PriorityQueue and fill it with the vertices in the network
        pq = PriorityQueue()
        pq.buildHeap([(v.getDistance(), v) for v in self.network])
        while not pq.isEmpty():
            currentVert = pq.delMin()

            for nextVert in currentVert.getConnections():
                # by making the cost negative, the algorithm creates a maximum spanning tree
                newCost = -currentVert.getWeight(nextVert)
                if nextVert in pq and newCost < nextVert.getDistance():
                    nextVert.setPrev(currentVert)
                    nextVert.setDistance(newCost)
                    pq.decreaseKey(nextVert, newCost)

        for vertex in self.network:
            for connections in vertex.getConnections():
                if connections == vertex.getPrev():
                    self.MST.addEdge(connections.getId(), vertex.getId(), vertex.getWeight(connections))
        self.resetNetwork()

    # return the path of user IDs between two users in MST
    def findPath(self, user1, user2):
        # if user1 or user2 are not in MST then return 0
        if not self.MST.__contains__(user1) or not self.MST.__contains__(user2):
            return 0

        # convert names to vertices
        u1Vertex = self.MST.getVertex(user1)
        u2Vertex = self.MST.getVertex(user2)

        # create the queue for BFS and queue user1
        vertQueue = Queue()
        vertQueue.enqueue(u1Vertex)
        while vertQueue.size() > 0:
            currentVert = vertQueue.dequeue()
            for nbr in currentVert.getConnections():
                if nbr.getColor() == 'white':
                    nbr.setColor('gray')
                    nbr.setPrev(currentVert)
                    vertQueue.enqueue(nbr)
            currentVert.setColor('black')

        # go backwards to user1 from user2 using prev and append each id along the way
        final = [u2Vertex.getId()]
        while u2Vertex.getPrev():
            u2Vertex = u2Vertex.getPrev()
            final.append(u2Vertex.getId())
        self.resetMST()

        # flip the path and return
        return " -> ".join(final[::-1])

    # return the heaviest path of user IDs with the least number of friends between two users in the network
    # currentVert looks ahead and has the nbrs decide who their previous should be
    def _findClosePath(self, user1, user2):
        # if the users are not in the network return 0
        if not self.network.__contains__(user1) or not self.network.__contains__(user2):
            return 0
        # convert user1 and user2 from names to their respective vertex from
        u1Vertex = self.network.getVertex(user1)
        u2Vertex = self.network.getVertex(user2)
        u1Vertex.setDistance(0)
        vertQ = Queue()
        vertQ.enqueue(u1Vertex)
        minDist = sys.maxsize
        maxCloseness = 0
        while vertQ.size() > 0:
            currentVert = vertQ.dequeue()
            # if we dequeued u2Vertex, all nbrs between it and u1Vertex have been visited so nothing left to do
            if currentVert == u2Vertex:
                break

            # if u2Vertex is a nbr to currentVert
            if u2Vertex in currentVert.getConnections():
                currentVert.setCloseness(currentVert.getWeight(u2Vertex) + currentVert.getCloseness())

                # if currentVert has the path with the least amount of friends
                if currentVert.getDistance() <= minDist:
                    minDist = currentVert.getDistance()

                    # if currentVert has the path with the largest closeness, set prev for u2Vertex and enqueue it
                    if currentVert.getCloseness() > maxCloseness:
                        maxCloseness = currentVert.getCloseness()
                        u2Vertex.setPrev(currentVert)
                        vertQ.enqueue(u2Vertex)

                # no need to visit the other neighbors of currentVert, just dequeue the next vertex
                continue
            # visit all neighboring nodes
            for nbr in currentVert.getConnections():
                # keep track of the closeness from the u1Vertex up to this nbr
                closeness = currentVert.getWeight(nbr) + currentVert.getCloseness()

                # if the nbr is undiscovered
                if nbr.getColor() == 'white':
                    nbr.setColor('gray')
                    nbr.setPrev(currentVert)
                    nbr.setCloseness(closeness)
                    nbr.setDistance(currentVert.getDistance() + 1)
                    vertQ.enqueue(nbr)

                # if there exists a path with greater closeness, and the nbr is in front of currentVert
                elif nbr.getCloseness() < closeness and nbr.getDistance() > currentVert.getDistance():
                    nbr.setCloseness(closeness)
                    nbr.setPrev(currentVert)

            currentVert.setColor('black')

        # go from user2 to user1 using prev and append each id along the way
        final = [u2Vertex.getId()+" (" + str(maxCloseness) + ")"]
        while u2Vertex.getPrev():
            u2Vertex = u2Vertex.getPrev()
            final.append(u2Vertex.getId())

        self.resetNetwork()
        # flip the path and return
        final = final[::-1]
        return " -> ".join(final)

    # return the heaviest path of user IDs with the least number of friends between two users in the network
    # currentVert looks backwards and decides which nbr should be its previous
    def findClosePath(self, user1, user2):
        # if the users are not in the network return 0
        if not self.network.__contains__(user1) or not self.network.__contains__(user2):
            return 0
        # convert user1 and user2 from names to their respective vertex from
        u1Vertex = self.network.getVertex(user1)
        u2Vertex = self.network.getVertex(user2)

        # create the queue for BFS and queue u1Vertex
        u1Vertex.setDistance(0)
        vertQ = Queue()
        vertQ.enqueue(u1Vertex)
        while vertQ.size() > 0:
            currentVert = vertQ.dequeue()
            # visit all neighboring nodes
            for nbr in currentVert.getConnections():
                # keep track of the closeness from the u1Vertex up to this nbr
                closeness = currentVert.getWeight(nbr) + currentVert.getCloseness()
                if nbr.getDistance() == sys.maxsize: # nbrs that are undiscovered
                    nbr.setPrev(currentVert)
                    nbr.setCloseness(closeness)
                    nbr.setDistance(currentVert.getDistance() + 1)
                    vertQ.enqueue(nbr)
                elif nbr.getDistance() < currentVert.getDistance(): # nbrs that were discovered before currentVert
                    if nbr.getCloseness() + nbr.getWeight(currentVert) > currentVert.getCloseness():
                        currentVert.setCloseness(nbr.getCloseness() + nbr.getWeight(currentVert))
                        currentVert.setPrev(nbr)
            if currentVert == u2Vertex:
                break
        # go from user2 to user1 using prev and append each id along the way
        final = [u2Vertex.getId() + " (" + str(u2Vertex.getCloseness()) + ")"]
        while u2Vertex.getPrev():
            u2Vertex = u2Vertex.getPrev()
            final.append(u2Vertex.getId())

        self.resetNetwork()
        # flip the path and return
        final = final[::-1]
        return " -> ".join(final)

    # set the network vertices to default, undiscovered values
    def resetNetwork(self):
        # reset vertices in the network to an undiscovered state
        for vertex in self.network:
            vertex.setColor("white")
            vertex.setPrev(None)
            vertex.setDistance(sys.maxsize)
            vertex.setCloseness(0)

    # set the MST vertices to default, undiscovered values
    def resetMST(self):
        # reset vertices in MST to an undiscovered state
        for vertex in self.MST:
            vertex.setColor("white")
            vertex.setPrev(None)
            vertex.setDistance(sys.maxsize)
            vertex.setCloseness(0)