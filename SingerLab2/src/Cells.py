'''
Created on Aug 17, 2016

@author: Nao
'''
from ImportList import *
from ImportListForCell import *

class Cells(object):
    """
    condition boolean list: [node comment edge branch]
   hellooooo change~
   Nodes { cell: [z y x id cellName]}
   Comments { cell: [z y x id cellName comment]}
   Edges { cell: [target source]}
   Branches { cell: [z y x id cellName branchpoint]}
   Names [name of cell]
   MinMax non-used
   Parameter xml.parameter
   scale: [z y x]
   
    """    
    def __init__(self, cellAddress , keywordForCell = None, NCBEboolean = [True, True, True, True], makeitEmpty = False):
        
        """
        Excpetion check
        """
        """
        if cellAddress == None:
            raise Exception('No address specified.')
        
        if not os.path.isfile(cellAddress):
            raise Exception('The file does not exist.')
        """

        if len(NCBEboolean) > 4 :
            raise Exception('Too many parameters for boolean array.')
        
        if len(NCBEboolean) < 4 :
            raise Exception('Too few parameters for boolean array.')
        ####
        self.NCBEboolean = None
        
        self.Nodes = None
        self.Comments = None
        self.Edges = None
        self.Branches = None
        self.MinMax = None
        
        self.XMLfile = None
        self.Names = None
        self.Parameter = None
        self.scale = None
        
        if not makeitEmpty:
            self.NCBEboolean = NCBEboolean        
            self.XMLfile = ET.parse(cellAddress)  
             
            self.Names = self.nameExtract()     
            self.Names = self.__getNameOfCells(keywordForCell)     
                
            self.Parameter = self.parameterExtract()    
            self.scale = self.scaleExtract()
            
            if NCBEboolean[0]:
                self.Nodes = self.nodesExtract()
                
            if NCBEboolean[1]:
                self.Comments = self.commentExtract()
            
            if NCBEboolean[2]:
                self.Edges = self.edgesExtract()
            
            if NCBEboolean[3]:
                Branch = self.branchExtract() 
            
            
    """
    return xml.parameter
    """
    def parameterExtract(self):
        parameter = self.XMLfile.find("parameters") 
        
        if parameter == None:
            raise Exception('Parameter does not exist.')
        
        return parameter       
    """
    return scale [z y x]
    currently it is [26 13.2 13.2]
    """
    def scaleExtract(self):
        things= self.XMLfile.getroot()
        children = things.find('parameters/scale')
        
        scale =[]
        z = float(children.get("z"))
        y = float(children.get("y"))
        x = float(children.get("x"))
        
        if z == None or y == None or x == None:
            raise Exception('x or y or z does not exist.')
        
        #scale.append(26)
        #scale.append(13.2)
        #scale.append(13.2)
        return scale
    """
    return nodes in dictionary form
    { cell: [z y x id cellName]}
    """
    def nodesExtract(self):
        NonNamedCellIndex = 1
        Nodes = {}
        things = self.XMLfile.getroot()
        #children = things.getchildren()  
        children = things.iterfind('thing')
        for child in children:
            thingCellName = child.get('comment')
            if thingCellName == None:
                
                print "WARNING. There is a cell with no name!" 
                
                thingCellName = "Jane Doe" + str(NonNamedCellIndex)
                NonNamedCellIndex = NonNamedCellIndex+1
            
            if not thingCellName in self.Names:
                continue
           
            Nodes.setdefault(thingCellName)
            Nodes[thingCellName] = []
            for elem in child.iterfind('nodes/node'):
                node = []
                a=int(self.scale[0]*int(elem.get('z')))
                b=int(self.scale[1]*int(elem.get('y')))
                c=int(self.scale[2]*int(elem.get('x')))
                d=int(elem.get('id'))
                node.append(a)
                node.append(b)
                node.append(c)
                node.append(d)
                node.append(thingCellName)
                Nodes[thingCellName].append(node)            
    """
    return min and max node number in a cell
    [min max]
    """
    def minmaxExtract(self):
        minmax = {}
        things = self.XMLfile.getroot()
        children = things.iterfind('thing')
        for child in children:
            thingCellName = child.get('comment')
            
            if not thingCellName in self.Names:
                continue
            
            minmax.setdefault(thingCellName)
            minmax[thingCellName] = []
            mini = 1000000000
            maxi = 0
            for elem in child.iterfind('nodes/node'):
                a = int(elem.get('id'))
                if( a> maxi):
                    maxi = a
                if(a < mini):
                    mini = a        
            minmax[thingCellName].append(mini)
            minmax[thingCellName].append(maxi)
        return minmax
    """
    return list of comments
    [node content]
    """
    def commentExtract(self, indexnumber = 2):
        NonNamedCellIndex = 1
        Comments = []
        things = self.XMLfile.getroot()
        children = things.getchildren()  
        for child in children:
            for elem in child.iterfind('comment'):
                comment1 = []
                
                nodeId = int(elem.get('node'))
                content = elem.get('content')
                
                if nodeId == None:
                    # cannot identify the node, so why use it?
                    print "WARNING. There is a comment without ID."
                    continue                
                
                if content == None:
                    print "WARNING. There is a comment without content."
                    content = "John Doe" + str(NonNamedCellIndex)
                    NonNamedCellIndex = NonNamedCellIndex + 1

                
                comment1.append(nodeId)
                comment1.append(content)
                Comments.append(comment1)
            
        """ extract raw comments, then sort them out"""

        CommentSet = set(x[indexnumber] for x in Comments)
        comment = {}

        for key in self.Nodes:
            comment.setdefault(key)
            indivCellNode = self.Nodes[key]
            indivCellNodSet = set(x[3] for x in indivCellNode)
            intersection = indivCellNodSet & CommentSet
            #intersection_list = [item for item in indivCellNode if item[3] in intersection]
            
            int_list = []
            for item in indivCellNode:
                if item[3] in intersection:
                    temp = item
                    for commenta in Comments:
                        if commenta[0] == item[3]:
                            temp.append(commenta[1])
                            break;
                    int_list.append(temp)
            #int_list.sort(key = lambda x:x[3])
            comment[key] = int_list
            
            
        return comment
    """
    return list of branchpoints
    [branchpoints]
    """
    def branchExtract(self):
        Branches = []
        things = self.XMLfile.getroot()
        children = things.getchildren()  
        for child in children:
            for elem in child.iterfind('branchpoint'):
                a = int(elem.get('id'))
                Branches.append(a)
                
        Keys = self.Nodes.keys()
        EdgeNode = {}
        for key in Keys:
            EdgeNode.setdefault(key)
            indivCellNode = self.Nodes[key]
            
            indivEdge = set(Branches)
            EdgeNode[key] = [item for item in indivCellNode if item[3] in indivEdge]
                       

        return EdgeNode
    """
    return edge in dictionary form
    { cell: [target source]}
    """
    def edgesExtract(self):
        Edges = {}
        NonNamedCellIndex = 1
        things = self.XMLfile.getroot()
        #children = things.getchildren()
        children = things.iterfind('thing')  
        for child in children:
            thingCellName = child.get('comment')
            if thingCellName == None:
                thingCellName = "Jane Doe" + str(NonNamedCellIndex)
                NonNamedCellIndex = NonNamedCellIndex+1

            if not thingCellName in self.Names:
                continue
                
            Edges.setdefault(thingCellName)
            Edges[thingCellName] = []
            for elem in child.iterfind('edges/edge'):
                edge = []
                a=int(elem.get('target'))
                b=int(elem.get('source'))
                edge.append(a)
                edge.append(b)
                edge.append(thingCellName)
                Edges[thingCellName].append(edge)
        return Edges
    """
    return list of names of cells
    [cellname]
    """
    def nameExtract(self):
        Names = []
        NonNamedCellIndex = 1
        things = self.XMLfile.getroot()
        children = things.iterfind('thing')  
        for child in children:
            Cellname = child.get('comment')
            if Cellname == None:
                Cellname = "Jane Doe" + str(NonNamedCellIndex)
                NonNamedCellIndex = NonNamedCellIndex +1
            Names.append(Cellname)
        return Names
    def getNameOfCells(self, KeyTerm):
        if (KeyTerm == None):
            return self.Names
        else:
            newCellNames = []
            for cellName in self.Names:
                if cellName.find(KeyTerm) != -1:
                    newCellNames.append(cellName)
            if (len(newCellNames)== 0):
                raise Exception('there is no cell with the name of ' + KeyTerm)
            return newCellNames    
        
    """
    /
    /
    /
    /
    """

   
    def __edgeNodeExtract(self):
        Keys = self.Nodes.keys()
        EdgeNode = {}
        for key in Keys:
            EdgeNode.setdefault(key)
            indivCellNode = self.Nodes[key]
            indivEdge = self.Edges[key]
            indEdSource = set(x[1] for x in indivEdge)
            EdgeNode[key] = [item for item in indivCellNode if item[3] in indEdSource]
       
        return EdgeNode
    def __allCommentComnined(self):
        allComments = []
        for comments in self.Comments.values():
            allComments = allComments + comments
        return allComments
    """
    return edges in dictionary form
    { cell: [z y x id cellName]}
    id is the source only! 
    """
    def sortEdgeExtract(self):
        Keys = self.Nodes.keys()
        EdgeNode = {}
        for key in Keys:
            EdgeNode.setdefault(key)
            indivCellNode = self.Nodes[key]
            indivEdge = self.Edges[key]
            indEdSource = set(x[1] for x in indivEdge)
            EdgeNode[key] = [item for item in indivEdge if item[0] in indEdSource]
       
        return EdgeNode
    """
    return nodes in list form
    you have freedome to sort this however you want. 0 -z 1- y 2-x 
    {[z y x id cellName]}
    """
    def allNodesExtract(self, sortIndex = 2):
        allNodes = []
        for nodes in self.Nodes.values():
            allNodes = allNodes + nodes
        allNodes.sort(key = lambda x:x[sortIndex])
        return allNodes
    """
    return edges in list form
    you have freedome to sort this however you want. 0 -z 1- y 2-x 
    {[z y x id cellName]}
     id is the source only! 
    """
    def allEdgesExtract(self,sortIndex):
        EdgeNode = self.__edgeNodeExtract()      
        allEdges = []
        for edges in EdgeNode.values():
            allEdges = allEdges + edges
        allEdges.sort(key = lambda x:x[sortIndex]) 
            
        return allEdges
    """
    return nodes without comments in dictionary form
     You should use this with commentWithKeywordExtract 
    {[z y x id cellName]} 
    """
    def allNodesNotCommentedExtract(self, Comment):
        AllNodes = self.Nodes
        #Comment = self.__allCommentComnined()
        CommentSet = set(x[3] for x in Comment)
        UncommentedNodes = {}
        for key in AllNodes:
            UncommentedNodes.setdefault(key)
            indivCellNode = AllNodes[key]
            indivCellNodSet = set(x[3] for x in indivCellNode)
            indivCellNodSet.difference_update(CommentSet)
            UncommentedNodes[key] = [item for item in indivCellNode if item[3] in indivCellNodSet]
        return UncommentedNodes
    """
    return nodes with specific comments in list form
     You can use comment
    {[z y x id cellName comment]} 
    """
    def commentWithKeywordExtract(self,*args):
        Comments = self.__allCommentComnined()
        newComments = []
        for comment in Comments:
            for keyword in args:
                if comment[5].find(keyword) != -1:
                    newComments.append(comment)
                    break
        return newComments
    def commentWithKeywordExtractDict(self, key1):
        newComment = {}
        for item1 in self.Comments.keys():
            newComment.setdefault(item1)
            newComment[item1] = []
            
            
        for item2 in self.Comments.keys():
            
            for comment in self.Comments[item2]:
                
                #print comment[5]
                if comment[5].find(key1) != -1:
                    newComment[item2].append(comment)
                    
        newNewComment = {}
        
        for item3 in newComment.keys():
            if len(newComment[item3]) != 0:
                
                newNewComment.setdefault(item3)
                newNewComment[item3] = newComment[item3]
            
        
        return newNewComment
    def allCommentExtracted(self):
        returner   = []
        for item in  self.Comments.keys():
            returner = returner + self.Comments[item]
        return returner            
    def allBranchExtracted(self):
        returner   = []
        for item in  self.Branches.keys():
            returner = returner + self.Branches[item]        
        return returner 
    def findStartingPoints(self):
        returner = {}
        for item in self.Comments.keys():
            count = 0
            thePoint= 0
            for item1 in self.Comments[item]:
                if item1[5] == "Soma":
                    count= count +1
                    thePoint = item1[3]
            if count > 1:
                raise Exception('more than 1 soma at ' +  str(item)+ '... Evan you gotta do a better job')        
            elif count < 1:
                raise Exception('no soma at '+ str(item) + '... Evan you gotta do a better job')
            else:
                returner.setdefault(item)
                returner[item] = thePoint                               
    def findStartingPointsVar(self):
        returner = {}
       
        SOMA = "SOMA"
        for item in self.Comments.keys():
            count = 0
            thePoint= 0
            for item1 in self.Comments[item]:
                if item1[5].lower() == SOMA.lower():
                    
                    count= count +1
                    thePoint = item1[3]
            if count == 1:
                
                returner.setdefault(item)
                returner[item] = thePoint
           # returner.setdefault(item)
            #returner[item] = count  
        return returner
    def toXML(self, filename):
        CellPrinter(self, filename)
        print "File created."
    def toMultiXML(self, saveDir):
        if not os.path.isdir(saveDir):
            raise Exception(saveDir + "is not a directory.")
        
        
        Names = self.Names
        for Name in Names:
            separtor(self, saveDir + "/" + Name)    
        
    def toVTK(self):
        print "todo"
        
    def toManyCells(self, NCBEboolean):
        cellDict = {}
        for name in self.Names:
            cellDict.setdefault(name)
            temp = Cells(None, None, NCBEboolean, True)
            
            if NCBEboolean[0]:
                nodeDict = {}
                nodeDict.setdefault(name)
                nodeDict[name] = self.Nodes[name]
                temp.Nodes = nodeDict
            if NCBEboolean[2]:
                edgeDict = {}
                edgeDict.setdefault(name)
                edgeDict[name] = self.Edges[name]
                temp.Edges = edgeDict
            
            if NCBEboolean[1]:
                commentDict = {}
                commentDict.setdefault(name)
                commentDict[name] = self.Comments[name]
                temp.Comments = commentDict
            if NCBEboolean[3]:
                branchDict = {}
                branchDict.setdefault(name)
                branchDict[name] = self.Branches[name]
                temp.Branches = branchDict        
            
            temp.NCBEboolean = NCBEboolean
            
            nameList = []
            nameList.append(name)
            temp.Names = nameList
            
            temp.Parameter = self.Parameter
            temp.scale = self.scale
            
            cellDict[name] = temp
        return cellDict
    def addCells(self):
        print "todo"
    def extractCells(self, cellnames):
        print "todo"

    def getEllipse(self):
        print "todo"
    
    def toArea(self, Nodes = True, keyword = None):
        polyDict = self.toPolygon(Nodes, keyword)
        areaDict = {}
        for name in polyDict.keys():
            areaDict.setdefault(name)
            areaDict[name] = polyDict[name].area
        return areaDict
    def toPolygon(self, Nodes = True, keyword = None):
        NodeDict = {}
        if Nodes:
            if self.NCBEboolean[0]:
                NodeDict = self.Nodes
            else:
                raise Exception("The cell does not have Nodes.")
        else:
            if self.NCBEboolean[1]:
                if keyword == None:
                    NodeDict = self.Comments
                else:
                    NodeDict = self.commentWithKeywordExtractDict(keyword)
            else:
                raise Exception("The cell does not have Comments.")
            
        hullDict = self.toConvexHull(Nodes)
        polyDict = {}
        for name in NodeDict.keys():
            polyDict.setdefault(name)
            polyDict[name] = Polygon(vertexToPoly(hullDict[name], yzExtract(NodeDict[name])))
        
        return polyDict
    def toConvexHull(self, Nodes = True, keyword = None, printCSV = False, saveLocation = None):
        if printCSV:
            if saveLocation == None:
                raise Exception("The file name is not specified.")
            if not os.path.isdir(os.path.dirname(saveLocation)):
                raise Exception(os.path.dirname(saveLocation) + "does not exist.")
            if os.path.exists(saveLocation):
                raise Exception(saveLocation + " already exists.")
        
        NodeDict = {}
        if Nodes:
            if self.NCBEboolean[0]:
                NodeDict = self.Nodes
            else:
                raise Exception("The cell does not have Nodes.")
        else:
            if self.NCBEboolean[1]:
                if keyword == None:
                    NodeDict = self.Comments
                else:
                    NodeDict = self.commentWithKeywordExtractDict(keyword)
            else:
                raise Exception("The cell does not have Comments.")
        
        hullDict = {}
        for name in NodeDict.keys():
            nodeList = self.Nodes[name]
            
            if len(nodeList) < 3:
                raise name + " list have less than 3 nodes; not enough for convex hull. "
            
            yzList = yzExtract(nodeList)
            
            hullDict.setdefault(name)
            hullDict[name] = ConvexHull(yzList)


        return hullDict
        
        
        
        print "todo"
    def changeCoordinate(self, coordinateCoefficient):
        if self.NCBEboolean[0]:
            for nodeList in self.Nodes.values():
                nodeList = convertCoord(coordinateCoefficient, nodeList)
        if self.NCBEboolean[1]:
            for commentList in self.Comments.values():
                commentList = convertCoord(coordinateCoefficient, commentList)
        if self.NCBEboolean[3]:    
            for branchList in self.Branches.values():
                branchList = convertCoord(coordinateCoefficient, branchList)
    
    def normalizeX(self, botPlaneCell, topPlaneCell):
        
        if (not botPlaneCell.NCBEboolean[0]) or (not topPlaneCell.NCBEboolean[0]) :
            raise Exception("Bot cell or Top cell does not have nodes.")
            
            
        topX = topPlaneCell.getMidPoint().values()[0][2]
        botX = botPlaneCell.getMidPoint().values()[0][2]
        
        if self.NCBEboolean[0]:
            for nodeList in self.Nodes.values():
                for node in nodeList:
                    node[2] = (topX - node[2])/( topX - botX)
        
        if self.NCBEboolean[1]:
            for commentList in self.Comments.values():
                for comment in commentList:
                    comment[2] = (topX - comment[2])/(topX - botX)
        
        if self.NCBEboolean[3]:
            for branchList in self.Branches.values():
                for branch in branchList:
                    branch[2] = (topX - branch[2])/(topX - botX)        
    """
    get plane vector. 
    """
    
    """###################FIX IT FIX IT#####################""" 
    
    
    def getCoefInfo(self, Node = True, keyword = None):
        if not (self.NCBEboolean[0]):
            raise Exception("This cell does not have nodes.")
        coefDict = {}
        nodeDict = {}
        if Node:
            nodeDict = self.Nodes
        else:
            if keyword == None:
                nodeDict = self.Comments
            else:
                nodeDict = self.commentWithKeywordExtractDict(keyword)
        
        for name in nodeDict.keys():
            nodeList = nodeDict[name]
            
            coefDict.setdefault(name)
            coefDict[name] = getPlaneCoef2(nodeList)  
        
        return coefDict
    def getMidPoint(self, Average = True, Node = True, keyword = None):
        if not (self.NCBEboolean[0]):
            raise Exception("This cell does not have nodes.")
        avgDict = {}
        nodeDict = {}
        if Node:
            nodeDict = self.Nodes
        else:
            if keyword == None:
                nodeDict = self.Comments
            else:
                nodeDict = self.commentWithKeywordExtractDict(keyword)
        
        for name in nodeDict.keys():
            nodeList = nodeDict[name]
            
            avgDict.setdefault(name)
            
            if Average:
                avgDict[name] = getAvgPoint(nodeList)  
            else:
                avgDict[name] = getMedianPoint(nodeList)

        return avgDict
    
        
    def getDeviation(self, StandardDeviation = True, Node = True, keyword = None):
        if not (self.NCBEboolean[0]):
            raise Exception("This cell does not have nodes.")
        devDict = {}
        nodeDict = {}
        if Node:
            nodeDict = self.Nodes
        else:
            if keyword == None:
                nodeDict = self.Comments
            else:
                nodeDict = self.commentWithKeywordExtractDict(keyword)
            
        for name in nodeDict.keys():
            nodeList = nodeDict[name]
            
            devDict.setdefault(name)
            if StandardDeviation:
                devDict[name] = stdev1D(nodeList)
            else:
                devDict[name] = abstdev1D(nodeList)
        
        return devDict

                     
    