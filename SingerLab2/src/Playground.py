'''
Created on Aug 17, 2016

@author: Nao
'''
from ImportList import *
from ImportListForCell import *
from Cells import *

point = ((0, 0), (0, 1), (1, 1), (1, 0), (0,0))
#poly = ConvexHull(point)

#print vertexToPoly(poly, point)
poly = Polygon(point)


x,y = poly.exterior.xy
print x, y
print len(x)
