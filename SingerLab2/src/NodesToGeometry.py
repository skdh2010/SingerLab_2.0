'''
Created on Aug 19, 2016

@author: Nao
'''

from ImportList import *


def yzExtract(arrNode):
    aList = []
    for item in arrNode:
        newNode = []
        newNode.append(item[1])
        newNode.append(item[0])
        aList.append(newNode)
    return aList



def vertexToPoly(hull, points):
    returnList = []
    vertex = hull.vertices
    
    for item in vertex:
        returnList.append(points[item])
        
    returnList.append(returnList[0])
        
    return returnList

def printVertex(filename, ):
    with open(filename + ".csv", 'wb') as csvfile:
        fieldnames = ['x','y']
        writer = csv.DictWriter(csvfile, fieldnames =fieldnames)
        
        for item5 in DicPolyV.keys():
            if item5 in VAreaSet:
                writer.writerow({'connectTo': item5, '# of connection': str(len(CBACsorted1[item3][item5])), 'intersecting area':str((DicPolyC[item3].intersection(DicPolyV[item5])).area)})
            else:
                writer.writerow({'connectTo': item5, '# of connection': str(0), 'intersecting area':str((DicPolyC[item3].intersection(DicPolyV[item5])).area)})
       
        
    
    

    