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


def CBgroupAnalyzer(saveLoc, top, bot, CBsCells,CBgroupDict):
    def addArea(dict):
        sum = 0
        for key in dict.keys():
            sum = sum + dict[key]
        return sum
    def avg(dict):
        if len(dict.keys()) == 0:
            return "All Zero"
        
        return addArea(dict)/len(dict.keys())
    
    def std(dict):
        if len(dict.keys()) ==0:
            return "All Zero"
        
        avg = addArea(dict)/len(dict.keys())
        sum = 0.0
        for item in dict.values():
            sum = sum + (item - avg) * (item -avg)
        return ( math.sqrt(sum/len(dict.keys())) )
    
    def omit_zero(dict):
        dic = {}
        for key in dict.keys():
            if dict[key] == 0:
                continue
            else:
                dic.setdefault(key)
                dic[key] = dict[key]
        return dic
    
    cellDict = {}
    CB = Cells(CBsCells)
    
    topCell = Cells(top)
    botCell = Cells(bot)
    
    coef = topCell.getCoefInfo().values()[0]
    
    CB.changeCoordinate(coef)

    for n in CBgroupDict.keys():
        cellDict.setdefault(n)
        cellDict[n] = CB.toCellsWithSpecificNames(CBgroupDict[n])
    
    for n1 in CBgroupDict.keys():
        for n2 in CBgroupDict.keys():
            if n1 == n2:
                continue
            else:
                dicdic = cellDict[n1].findOverlapArea(cellDict[n2], 500, False, "ibbon",False, "ibbon") 

                with open( saveLoc + "/" + n1 + "_" + n2 + ".csv", 'wb') as csvfile:
                    
                    fieldnames = ['name1', 'name2', 'overlap_area']
                    writer = csv.DictWriter(csvfile, fieldnames = fieldnames )
                    writer.writerow({'name1': 'name1', 'name2':'name2', 'overlap_area':'overlap_area' })
                    
                    for key1 in dicdic.keys():
                        dic = dicdic[key1]
                        for key2 in dic.keys():
                        
                            writer.writerow({'name1': key1, 'name2': key2, 'overlap_area': dic[key2] })
                    
            


def CBsAnalyzer( saveLoc, top, bot,CBsCells, AIIsCells, keyword1 = 'ibbon', keyword3 ='nput' , keyword2 = 'nput' ,keyword4= 'utput', savename = "CBsAnalyzer", passByCell = False):
    
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

    CB = None
    AIIs = None
    if passByCell:
        CB = copy.copy(CBsCells)
        AIIs = copy.copy(AIIsCells)
    else:
        CB = Cells(CBsCells)
        AIIs = Cells(AIIsCells)
    
    topCell = Cells(top)
    botCell = Cells(bot)
    
    
    
    coef = topCell.getCoefInfo().values()[0]
    
    CB.changeCoordinate(coef)
    AIIs.changeCoordinate(coef)
    
    #CB.normalizeX(botCell, topCell, False)
    #AIIs.normalizeX(botCell, topCell, False)
    
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
   
   
    with open( saveLoc + "/" + savename + ".csv", 'wb') as csvfile:
        
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
    
    #CB.normalizeX(botCell, topCell, False)
    #AIIs.normalizeX(botCell, topCell, False) 
        
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
    
    #CB.normalizeX(botCell, topCell, False)
    #AIIs.normalizeX(botCell, topCell, False)
        
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
        
        
def CBsAnalyzer2( saveLoc, top, bot,CBsCells):
    
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
    
    topCell = Cells(top)
    botCell = Cells(bot)
    
    coef = topCell.getCoefInfo().values()[0]
    
    CB.changeCoordinate(coef)


    CB.edgeOnlyNode()
    median = CB.getMidPoint(True, False)
    deviation = CB.getDeviation(False)

   
   
    with open( saveLoc + "/CBsSkeletonDepth.csv", 'wb') as csvfile:
        
        fieldnames = ['name', 'median', 'AD', ]
        writer = csv.DictWriter(csvfile, fieldnames = fieldnames )
        writer.writerow({'name': 'name', 'median' : 'median', 'AD' : 'AD'})
        
        for name in CB.Names:
            writer.writerow({'name': name, 'median' : printer(name, median), 'AD' : printer(name, deviation) })
        

    