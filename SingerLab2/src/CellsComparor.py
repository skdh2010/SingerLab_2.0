'''
Created on Aug 20, 2016

@author: Nao
'''
from ImportList import *
from ImportListForCell import *
from Cells import *

def printConvexHull(saveLoc, top, bot, cellAddress, Node =True, keyword = None):
    cells = Cells(cellAddress)

    topCell = Cells(top)
    botCell = Cells(bot)

    coef = topCell.getCoefInfo().values()[0]

    cells.changeCoordinate(coef)


    cells.normalizeX(botCell, topCell, False)
    cells.toConvexHull(Node, keyword, True, saveLoc )






def CBsAnalyzer( saveLoc, top, bot,CBsCells, AIIsCells , keyword1 = 'ibbon', keyword3 ='nput' , keyword2 = 'nput' ,keyword4= 'utput'):
    
    def printer(name, dict):
        nameList = dict.keys()
        if not name in nameList:
            return "N/A"
        else:
            return str(dict[name])
    
    def toLengthDict(dict, isitDD = False):
        newDict = {}
        for name in dict.keys():
            newDict.setdefault(name)
            
            if not isitDD:
                newDict[name] = len(dict[name])
            else: 
                newDict[name] = len(dict[name].keys())
        return newDict

    
    CB = Cells(CBsCells)
    AIIs = Cells(AIIsCells)
    
    topCell = Cells(top)
    botCell = Cells(bot)
    
    coef = topCell.getCoefInfo().values()[0]
    
    CB.changeCoordinate(coef)
    AIIs.changeCoordinate(coef)
    
    CB.normalizeX(botCell, topCell, False)
    AIIs.normalizeX(botCell, topCell, False)
    
    comments = CB.commentWithKeywordExtractDict(keyword1)
    area = CB.toArea(False, keyword1)
    median = CB.getMidPoint(True, False, False, keyword1)
    deviation = CB.getDeviation(False, False, keyword1)
    ribbonToAII = CB.findClosePoints(AIIs, 500, False, keyword1, False, keyword2, False)
    
    ribtoAIIdd = CB.findClosePointsDict(AIIs, 500, False, keyword1, False, keyword2)
    
    inputToAII = CB.findClosePoints(AIIs, 500, False, keyword3, False, keyword4, False )
    
    inptoAIIdd = CB.findClosePointsDict(AIIs, 500, False, keyword3, False, keyword4)
    commentLengthDict = toLengthDict(comments)
    ribToAIILengthDict = toLengthDict(ribbonToAII)
    inpToAIILengthDict = toLengthDict(inputToAII)
    ribDDLengDict = toLengthDict(ribtoAIIdd, True)
    inpDDLengDict = toLengthDict(inptoAIIdd, True)    
   
   
    with open( saveLoc + "/CBsAnalysis.csv", 'wb') as csvfile:
        
        fieldnames = ['name', 'median', 'AD', 'ribbon total', 'ribbons to AII', 'AIIs contacted', 'AII input', 'AIIs providing input', 'hull area']
        writer = csv.DictWriter(csvfile, fieldnames = fieldnames )
        writer.writerow({'name': 'name', 'median' : 'median', 'AD' : 'AD', 'ribbon total': 'ribbon total', 'ribbons to AII': 'ribbons to AII', 'AIIs contacted': "AIIs contacted", 'AII input': 'AII input', 'AIIs providing input': 'AIIs providing input', 'hull area' : 'hull area' })
        
        for name in CB.Names:
            writer.writerow({'name': name, 'median' : printer(name, median), 'AD' : printer(name, deviation), 'ribbon total': printer(name, commentLengthDict), 'ribbons to AII': printer(name, ribToAIILengthDict), 'AIIs contacted': printer(name, ribDDLengDict), 'AII input':  printer(name, inpToAIILengthDict), 'AIIs providing input': printer(name, inpDDLengDict), 'hull area' : printer(name, area) })
        
        
def connectionAnalyzer(saveLoc, top, bot,CBsCells, AIIsCells , keyword1 = 'ibbon', keyword3 ='nput' , keyword2 = 'nput' ,keyword4= 'utput'):
    
    def printer(name1, name2, DD, isitList):
        if not name1 in DD.keys():
            return str(0)
        else:
            if not name2 in DD[name1].keys():
                return str(0)
            else:
                if isitList:
                    return str(len(DD[name1][name2]))
                else:
                    return str(DD[name1][name2])
        

    
    CB = Cells(CBsCells)
    AIIs = Cells(AIIsCells)
    
    topCell = Cells(top)
    botCell = Cells(bot)
    
    coef = topCell.getCoefInfo().values()[0]
    
    CB.changeCoordinate(coef)
    AIIs.changeCoordinate(coef)
    
    CB.normalizeX(botCell, topCell, False)
    AIIs.normalizeX(botCell, topCell, False)
        
    ribtoAIIdd = CB.findClosePointsDict(AIIs, 500, False, keyword1, False, keyword2)
    inptoAIIdd = CB.findClosePointsDict(AIIs, 500, False, keyword3, False, keyword4)
    
    ribIntersectPolydd = CB.findOverlapArea(AIIs, 500, False, keyword1, False, keyword2)
    inpIntersectPolydd = CB.findOverlapArea(AIIs, 500, False, keyword3, False, keyword4)
    

    
    with open( saveLoc + "/overlap_vs_connections.csv", 'wb') as csvfile:
        
        fieldnames = ['CBname', 'AIIname', 'CBtoAIIcontacts', 'overlapCBtoAII' ,'AIItoCBcontacts', 'overlapAIItoCB']
        writer = csv.DictWriter(csvfile, fieldnames = fieldnames )
        writer.writerow({'CBname': 'CBname', 'AIIname': 'AIIname', 'CBtoAIIcontacts': 'CBtoAIIcontacts','overlapCBtoAII':'overlapCBtoAII', 'AIItoCBcontacts': 'AIItoCBcontacts','overlapAIItoCB':'overlapAIItoCB' }) 
        for name1 in CB.Names:
            for name2 in AIIs.Names:
                writer.writerow({'CBname': name1, 'AIIname': name2, 'CBtoAIIcontacts': printer(name1, name2, ribtoAIIdd, True),'overlapCBtoAII': printer(name1, name2, ribIntersectPolydd, False), 'AIItoCBcontacts': printer(name1, name2, inptoAIIdd, True),'overlapAIItoCB': printer(name1, name2, inpIntersectPolydd, False ) })
                
def synapseAnalyzer(saveLoc, top, bot,CBsCells, AIIsCells , keyword1 = 'ibbon', keyword3 ='nput' , keyword2 = 'nput' ,keyword4= 'utput'):
    
    CB = Cells(CBsCells)
    AIIs = Cells(AIIsCells)
    
    topCell = Cells(top)
    botCell = Cells(bot)
    
    coef = topCell.getCoefInfo().values()[0]
    
    CB.changeCoordinate(coef)
    AIIs.changeCoordinate(coef)
    
    CB.normalizeX(botCell, topCell, False)
    AIIs.normalizeX(botCell, topCell, False)
        
    ribtoAIIdd = CB.findClosePointsDict(AIIs, 500, False, keyword1, False, keyword2)
    inptoAIIdd = CB.findClosePointsDict(AIIs, 500, False, keyword3, False, keyword4)
    

    
                
    with open( saveLoc + "/synapses.csv", 'wb') as csvfile:
        
        fieldnames = ['CBname', 'AIIname', 'CBtoAII' ,'AIItoCB', 'x', 'y', 'z']
        writer = csv.DictWriter(csvfile, fieldnames = fieldnames )
        writer.writerow({'CBname': 'CBname', 'AIIname': 'AIIname', 'CBtoAII': 'CBtoAII', 'AIItoCB' : 'AIItoCB', 'x': 'x', 'y': 'y', 'z':'z' }) 
        for name1 in ribtoAIIdd.keys():
            for name2 in ribtoAIIdd[name1].keys():
                for node in ribtoAIIdd[name1][name2]:
                    writer.writerow({'CBname': name1, 'AIIname': name2, 'CBtoAII': 'Y', 'AIItoCB' : 'N', 'x': node[2] ,'y': node[1], 'z': node[0]})

        for name1 in inptoAIIdd.keys():
            for name2 in inptoAIIdd[name1].keys():
                for node in inptoAIIdd[name1][name2]:
                    writer.writerow({'CBname': name1, 'AIIname': name2, 'CBtoAII': 'N', 'AIItoCB' : 'Y', 'x': node[2] ,'y': node[1], 'z': node[0]})
        
        
        
    