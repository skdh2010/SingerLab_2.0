'''
Created on Aug 17, 2016

@author: Nao
'''
from ImportList import *
from ImportListForCell import *
from Cells import *
from CellsComparor import *
from os import listdir

saveLoc = 'C:\\Users\\skdh2\\Downloads\\chek2'


top=  'C:\\Users\\skdh2\\Downloads\\OFF_SAC.xml'
bot = 'C:\\Users\\skdh2\\Downloads\\ON_SAC.xml'

AII = 'C:\\Users\\skdh2\\Downloads\\AII\\annotation.xml'

NOS = 'C:\\Users\\skdh2\\Downloads\\nNOS\\annotation.xml'

Delta = 'C:\\Users\\skdh2\\Downloads\\OFF_Deltas.xml'
CB = 'C:\\Users\\skdh2\\Downloads\\CBs.xml'



"""
##AIICell = Cells(AII)
NOSCell = Cells(NOS)

##AIIcells =  AIICell.toManyCells()
NOScells = NOSCell.toManyCells()

##for aName in AIIcells.keys():
##	AIIcells[aName].toVTK(saveLoc)

for nName in NOScells.keys():
	NOScells[nName].toVTK(saveLoc)

"""
###########################################


#synapseAnalyzer2(saveLoc,top, bot,  Delta, CB )

CBsAnalyzer2(saveLoc, top, bot, NOS)
commentLister1(saveLoc, top, bot, NOS)

