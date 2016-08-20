'''
Created on Aug 17, 2016

@author: Nao
'''
from ImportList import *


 
def cross(a, b):
    comp1 = a[1]*b[2] - a[2]*b[1]
    comp2 = a[2]*b[0] - a[0]*b[2]
    comp3 = a[0]*b[1] - a[1]*b[0]

    normalization = math.sqrt(comp1 * comp1 + comp2 * comp2 + comp3 * comp3)
    
    comp1 = comp1/normalization
    comp2 = comp2/normalization
    comp3 = comp3/normalization    
    
    c = []
    c.append(comp1)
    c.append(comp2)
    c.append(comp3)
    
    return c
    
    

def generateVector(coordinate1, coordinate2):
    zcor = coordinate1[0] - coordinate2[0]
    ycor = coordinate1[1] - coordinate2[1]
    xcor = coordinate1[2] - coordinate2[2]
    vector = []
    
    vector.append(zcor)
    vector.append(ycor)
    vector.append(xcor)
    return vector


def getAvgPoint(aList):
    xsum = 0
    ysum = 0
    zsum = 0
    length = len(aList)
    
    for item in aList:
        zsum = zsum + item[0]
        ysum = ysum + item[1]
        xsum = xsum + item[2]
        
    xsum = xsum/length
    ysum = ysum/length
    zsum = zsum/length
    #lets keep them z, y, x
    avgPoint = []
    avgPoint.append(zsum)
    avgPoint.append(ysum)
    avgPoint.append(xsum)
    
    return avgPoint



def getMedianPoint(aList):

    
    xArray =  sorted(aList, key = lambda x:x[2])
    
    
    
    
    yArray =  sorted(aList, key = lambda y:y[1])
    zArray =  sorted(aList, key = lambda z:z[0])
    
    returnList = []

    returnList.append(zArray[len(aList)/2][0])
    returnList.append(yArray[len(aList)/2][1])
    returnList.append(xArray[len(aList)/2][2])
    
    return returnList



def getPlaneCoef2(allNodes):
    
    # 3d square fitting
    length = len(allNodes)
    sum_zz = 0.0
    sum_z = 0.0
    sum_zy = 0.0
    sum_yy = 0.0
    sum_y = 0.0
    
    sum_zx = 0.0
    sum_yx = 0.0
    sum_x = 0.0
    for item in allNodes:
        z_cor = item[0]
        y_cor = item[1]
        x_cor = item[2]
    
        sum_zz = sum_zz + z_cor*z_cor
        sum_z = sum_z + z_cor
        sum_zy = sum_zy + z_cor*y_cor
        sum_yy = sum_yy + y_cor*y_cor
        sum_y = sum_y + y_cor
        
        sum_zx = sum_zx + z_cor*x_cor
        sum_yx = sum_yx + y_cor*x_cor
        sum_x = sum_x + x_cor
    Matrix = []
    firstrow = []
    firstrow.append(sum_zz)
    firstrow.append(sum_zy)
    firstrow.append(sum_z)
    
    secondrow = []
    secondrow.append(sum_zy)
    secondrow.append(sum_yy)
    secondrow.append(sum_y)
    
    thirdrow = []
    thirdrow.append(sum_z)
    thirdrow.append(sum_y)
    thirdrow.append(length)
    
    Matrix.append(firstrow)
    Matrix.append(secondrow)
    Matrix.append(thirdrow)
    
    vector = []
    vector.append(sum_zx)
    vector.append(sum_yx)
    vector.append(sum_x)

    Amatrix = np.array(Matrix)
    Ainverse= inv(Amatrix)
    Avector = np.array(vector)
    Coef = (np.dot(Ainverse, Avector)).tolist()
    #print Coef;
    c = []
    
    c.append(Coef[0])
    c.append(Coef[1])
    c.append(-1)
    c.append(Coef[2])
    
    return c;
    """
    comp1 = Coef[0]
    comp2 = Coef[1]
    comp3 = Coef[2]
    
    normalization = math.sqrt(comp1 * comp1 + comp2 * comp2 + comp3 * comp3)
    
    comp1 = comp1/normalization
    comp2 = comp2/normalization
    comp3 = comp3/normalization    
    
    c = []
    c.append(comp1)
    c.append(comp2)
    c.append(comp3)
    #print c
    
    return c
    """
    
    
    
"""
[z,y,x ...


"""

def stdev1D (aList):
    sum = 0
    for item in aList:
        sum = sum + item[2]
    avg = sum/len(aList)
    
    
    var = 0
    for item in aList:
        var = var + (item[2] - avg) * (item[2] - avg)
        
    var = var/len(aList)  # it should be n - 1, but it make no difference
    
    return math.sqrt(var)


def abstdev1D (aList):
    avgVal = getAvgPoint(aList)[2]
    newList = []
    
    for item in aList:
        newList.append(math.fabs(item[2]-avgVal))
    
    newList.sort()
    print newList
    val = newList[len(newList)/2]
    
    return val

    

def getNewCoord(allNodes):
    #preTop = XMLinterpreter(addressTop)
    #condition  = [True, False, False, False]
    Plane = getPlaneCoef2(allNodes)
    
    coord = getAvgPoint(allNodes)
    
    Plane.append(getPlaneConst(Plane, coord))
    
    return Plane

def getPlaneConst(coef, coord):
    d = -(coef[0]*coord[0] + coef[1] * coord[1] + coef[2] * coord[2])
    return d


def convertCoord(coef, allNodes):
    """
    change to x y z then convert to z y x. disaster from my old mistake.
    """
    FirstCol = []
    
    norm1 = coef[2] * coef[2] + coef[1] * coef[1] + coef[0] * coef[0]
    
    FirstCol.append(-coef[2]/norm1)
    FirstCol.append(-coef[1]/norm1)
    FirstCol.append(-coef[0]/norm1)


    tempY = []
    tempY.append(0)
    tempY.append(0)
    tempY.append(1)
    SecCol = cross(tempY, FirstCol )
            
    ThrCol = cross(FirstCol, SecCol)
    
    
    Matrix = []
    Matrix.append(FirstCol)
    Matrix.append(SecCol)
    Matrix.append(ThrCol)
       
    aMatrix = np.array(Matrix)
    aMatrix = np.transpose(aMatrix)
    invMat = inv(aMatrix)
    
    returner = []
    
    for item in allNodes:
        temper = []
        temper.append(item[2])
        temper.append(item[1])
        temper.append(item[0])
        Avector = np.array(temper)
        newCoord = (np.dot(invMat, Avector)).tolist()
        
        #print item
        item[2] = newCoord[0]
        item[1] = newCoord[1]
        item[0] = newCoord[2]
        
        returner.append(item)
        #print item
        
    return returner
 
    