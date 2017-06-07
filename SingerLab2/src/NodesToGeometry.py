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

def printVertice(filename, vertice):
    with open(filename + ".csv", 'wb') as csvfile:
        newName=os.path.split(filename)[1]
        
        fieldnames = [newName+'_x',newName+'_y']
        writer = csv.DictWriter(csvfile, fieldnames =fieldnames)
        writer.writerow({newName+'_x': newName+'_x', newName+'_y': newName+'_y'})
        for vertex in vertice:
            writer.writerow({ newName+'_x': vertex[0], newName+'_y': vertex[1]})

       
        
    
    

    