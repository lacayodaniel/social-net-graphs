# unused file. Reference for algorithm
from PriorityQueue import *

def dijkstra(aGraph, start, end):
    pq = PriorityQueue()
    start.setDistance(0)
    pq.buildHeap([(v.getDistance(), v) for v in aGraph])
    while not pq.isEmpty():
        currentVert = pq.delMin()
        for nextVert in currentVert.getConnections():
            newDist = currentVert.getDistance() + currentVert.getWeight(nextVert)
            if newDist > nextVert.getDistance():
                nextVert.setDistance(newDist)
                nextVert.setPrev(currentVert)
                pq.decreaseKey(nextVert, newDist)

