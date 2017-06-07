'''
Created on Aug 17, 2016

@author: Nao
'''
from ImportList import *
from ImportListForCell import *
from Cells import *
from CellsComparor import *
from os import listdir
top=  'C:\Users\Lee\Downloads\check\OFF.xml'
bot = 'C:\Users\Lee\Downloads\check\ON.xml'

AII = 'C:\Users\Lee\Downloads\chek2\pCRHs.xml'
AIIvtk = 'C:\Users\Lee\Downloads\chek2\AIIu_pres.xml'
CB =  'C:\Users\Lee\Downloads/annotation.xml'

p1 = 'C:\Users\Lee\Downloads\pCRH1.nml'
p2 = 'C:\Users\Lee\Downloads\pCRH2.nml'

saveLoc = "C:\Users\Lee\Downloads\chek2"

#Cells(CB).toMultiXML(saveLoc)
#printConvexHull(saveLoc, top, bot, CB, True)
#groupDict = {"group1":["OFF_CBn","OFF_CBb","OFF_CBk","OFF_CBa","OFF_CBo","OFF_CBp","OFF_CBd","OFF_CBf","OFF_CBi","OFF_CBr","OFF_CBtt","OFF_CBq","OFF_CBl","OFF_CBx","OFF_CBg","OFF_CBh"], "group2":["OFF_CBuu","OFF_CBrr","OFF_CBbbb","OFF_CBs","OFF_CBaaa","OFF_CBkk","OFF_CBlll","OFF_CBoo","OFF_CBjjj","OFF_CBq","OFF_CBqq","OFF_CBjj"], "group3":["OFF_CBw","OFF_CBll","OFF_CBee","OFF_CBj","OFF_CBy","OFF_CBpp","OFF_CByy","OFF_CBkkk","OFF_CBaa","OFF_CBmm","OFF_CBfff","OFF_CBe","OFF_CBbb","OFF_CBdd"], "group4":["OFF_CBc","OFF_CBxx","OFF_CBcc","OFF_CBii","OFF_CBww"]  }

#CBsAnalyzer2(saveLoc, top, bot, CB)
#CBgroupAnalyzer(saveLoc, top, bot, CB, groupDict)
"""
CBsAnalyzer(saveLoc ,top, bot, CB, AII, 'ibbon', 'nput', 'nput', 'utput')
synapseAnalyzer(saveLoc, top, bot, CB, AII, 'ibbon', 'nput', 'nput', 'utput')
connectionAnalyzer(saveLoc, top, bot, CB, AII, 'ibbon', 'nput', 'nput', 'utput')
"""
#topCell= Cells(top)
#print topCell.getCoefInfo()

"""


printConvexHull(saveLoc , top, bot, AII, False, 'utput')
printConvexHull(saveLoc , top, bot, CB, True, 'ibbon')

CBsAnalyzer(saveLoc ,top, bot, CB, AII, 'ibbon', 'nput', 'nput', 'utput')

connectionAnalyzer(saveLoc, top, bot, CB, AII, 'ibbon', 'nput', 'nput', 'utput')

"""

#Cells(CB).toMultiXML(saveLoc)
#AIIcell = Cells(AIIvtk)
CBcell = Cells(CB)



CBcell.toMultiXML(saveLoc)

#topCell = Cells(top)
#botCell = Cells(bot)

#coef = topCell.getCoefInfo().values()[0]

#topCell.changeCoordinate(coef)
#botCell.changeCoordinate(coef)
#CBcell.changeCoordinate(coef)
#AIIcell.changeCoordinate(coef)

#CBcell.normalizeX(botCell, topCell, False, 500)
#AIIcell.normalizeX(botCell, topCell, False, 500)

#saveLoc1 = "C:\Users\Lee\Downloads\check\skeleton"
#saveLoc2 = "C:\Users\Lee\Downloads\check\comment"

#topCell.toVTK(saveLoc, False)
#botCell.toVTK(saveLoc, False)

#CBcell.toVTK(saveLoc1, False)
#AIIcell.toVTK(saveLoc, False)

#CBcell.toVTK(saveLoc2, True, "ibbon", "0.500000", "0.700000")
#AIIcell.toVTK(saveLoc, True, "utput", "0.500000", "0.700000")
"""
"""
"""
tt1 = Cells(top)
tt2 = Cells(bot)

#p1C.toVTK(saveLoc, False, None, "0.500000", "0.700000" )
#p2C.toVTK(saveLoc, False,None,  "0.500000", "0.700000" )
#topCell.toVTK(saveLoc, False)
#botCell.toVTK(saveLoc, False)


coef = topCell.getCoefInfo().values()[0]

topCell.changeCoordinate(coef)
botCell.changeCoordinate(coef)
tt1.changeCoordinate(coef)
tt2.changeCoordinate(coef)
AIIcell

tt1.normalizeX(botCell, topCell, False, 1000)
tt2.normalizeX(botCell, topCell, False, 1000)

tt1.toVTK(saveLoc, False, None, "0.500000" )
tt2.toVTK(saveLoc, False, None, "0.500000")
"""
