'''
Created on Aug 17, 2016

@author: Nao
'''
from ImportList import *
from ImportListForCell import *
from Cells import *
from CellsComparor import *

top =  'C:\Users\Lee\Downloads\OFF_SAC.xml'
bot = 'C:\Users\Lee\Downloads\ON_SAC.xml'

AII = 'C:\Users\Lee\Downloads\AII.xml'
CB = 'C:\Users\Lee\Downloads\CB.xml'

CBcell= Cells(CB)

CBcell.toVTK()
"""
CBcell = Cells(CB)
AIIcell = Cells(AII)

topCell = Cells(top)
botCell = Cells(bot)

coef = topCell.getCoefInfo().values()[0]

CBcell.changeCoordinate(coef)

CBcell.normalizeX(botCell, topCell, False)

CBcell.toXML("C:/Users/Lee/Downloads/modifiedCB.xml")
"""
"""
synapseAnalyzer("C:/Users/Lee/Downloads", top, bot, CB, AII, 'ibbon', 'nput', 'nput', 'utput')

connectionAnalyzer("C:/Users/Lee/Downloads", top, bot, CB, AII, 'ibbon', 'nput', 'nput', 'utput')

printConvexHull("C:/Users/Lee/Downloads", top, bot, AII, True)
printConvexHull("C:/Users/Lee/Downloads", top, bot, AII, False, 'utput')
printConvexHull("C:/Users/Lee/Downloads", top, bot, CB, True, 'ibbon')

CBsAnalyzer('C:/Users/Lee/Downloads' ,top, bot, CB, AII, 'ibbon', 'nput', 'nput', 'utput')
"""