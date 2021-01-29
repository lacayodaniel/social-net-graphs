from OSN import *

if __name__ == '__main__':
    osn = OSN()
    osn2 = OSN()
    osn.buildGraph('facebook_network.csv')
    # osn._buildGraph()

    # should be 1287
    print("OSN Network number of vertices", osn.network.numVertices)
    osn.buildMST()
    # should be 1287
    print("MST number of vertices", osn.MST.numVertices)

    count = 0
    for vertName in osn.MST.getVertices():
        for neiborVert in osn.MST.getVertex(vertName).connectedTo:
            count += osn.MST.getVertex(vertName).connectedTo[neiborVert]
    # should be 92546
    print("Edges in MST", count/2)
    # should be 3
    print(osn.findDistance("Murray", "Clark"))
    # should be Murray -> Wilson -> Nguyen -> Silva -> Maldonado -> Jenkins -> Burton -> Hoffman -> Lambert -> Clark
    print(osn.findPath("Murray", "Clark"))
    # should be Murray -> Howell -> Stewart -> Clark (190)
    print(osn.findClosePath("Murray", "Clark"))







