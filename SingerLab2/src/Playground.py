'''
Created on Aug 17, 2016

@author: Nao
'''
from ImportList import *
from ImportListForCell import *
from Cells import *

CB = Cells("D:/Download/CBs.xml")
AII = Cells("D:/Download/AIIs.xml")
Up = Cells("D:/Download/ON_SAC.xml")
Down = Cells("D:/Download/OFF_SAC.xml")

CB.changeCoordinate(Up.getCoefInfo().values()[0])
AII.changeCoordinate(Up.getCoefInfo().values()[0])

print CB.findClosePoints(AII, 500)

print CB.findClosePointsDict(AII, 500)
