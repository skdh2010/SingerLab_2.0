'''
Created on Aug 17, 2016

@author: Nao
'''
from ImportList import *
from ImportListForCell import *
from _ast import Num
from netbios import NCBENUM

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
            self.Names = self.getNameOfCells(keywordForCell)     
                
            self.Parameter = self.parameterExtract()    
            self.scale = self.scaleExtract()
            
            if NCBEboolean[0]:
                self.Nodes = self.nodesExtract()
                
            if NCBEboolean[1]:
                self.Comments = self.commentExtract()
            
            if NCBEboolean[2]:
                self.Edges = self.edgesExtract()
            
            if NCBEboolean[3]:
                self.Branches = self.branchExtract() 
            
            
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
        
        scale.append(z)
        scale.append(y)
        scale.append(x)
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
        return Nodes      
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
    def commentExtract(self, indexnumber = 0):
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
                    temp = copy.copy(item)
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
                       

        return copy.copy(EdgeNode)
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
            indEdArr = set(x[0] for x in indivEdge)
            indEdSource = indEdSource.union(indEdArr)
            EdgeNode[key] = [item for item in indivCellNode if item[3] in indEdSource]
       
        return copy.copy(EdgeNode)
    
    def edgeOnlyNode(self):
        self.Nodes = self.__edgeNodeExtract()
        
    
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
    def allEdgesExtract(self):
        allEdges = []
        for edges in self.Edges.values():
            allEdges = allEdges + edges
        return allEdges
    
    """
    return edges in list form
    you have freedome to sort this however you want. 0 -z 1- y 2-x 
    {[z y x id cellName]}
     id is the source only! 
    """
    def allEdgeNodesExtract(self,sortIndex):
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
        Comments = self.allCommentExtracted()
        newComments = []
        for comment in Comments:
            for keyword in args:
                if comment[5].lower().find(keyword.lower()) != -1:
                    newComments.append(comment)
                    break
        return newComments
    def commentWithKeywordExtractDict(self, key1):
        if key1 == None:
            return self.Comments
        newComment = {}
        
        
        
        for item1 in self.Comments.keys():
            newComment.setdefault(item1)
            newComment[item1] = []
        
        if isinstance(key1, str):
            for item2 in self.Comments.keys():
                
                for comment in self.Comments[item2]:
                    
                    #print comment[5]
                    if comment[5].lower().find(key1.lower()) != -1:
                        newComment[item2].append(comment)
                        
                        
        elif isinstance(key1, list) and (len(key1) == 0):
            return self.Comments
        
        
        elif isinstance(key1, list) and (len(key1) != 0) and isinstance(key1[0],str) :
            for item2 in self.Comments.keys():
                for comment in self.Comments[item2]:
                    #print comment[5]
                    for akey in key1:
                        if comment[5].lower().find(akey.lower()) != -1:
                            newComment[item2].append(comment)
                            break
                        
        else:
            raise "key1 is either a single string or a list of strings"
        
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
            separtor(self, Name, saveDir)    
        
    def toVTK(self, fileLoc, commentonlyToo = True, keyForComment = None, Commentcolor = "0.500000", skeletonColor = "0.000000"):
        
        newCell = copy.copy(self)
        newCell.reorderNodeID(keyForComment)
        
        
        head1 = "# vtk DataFile Version 3.0\n"
        head2 = "vtk output\n"
        head3 = "ASCII\n"
        head4 = "DATASET POLYDATA\n\n"
        head = head1 + head2 + head3 + head4
        for name in newCell.Names:
            nodes = newCell.Nodes[name]
            self.Comments[name].sort(key = lambda comment: comment[4])
            self.Edges[name].sort(key = lambda edge:edge[1] )
            
            comments = newCell.Comments[name]
            edges = newCell.Edges[name]
            
        
            with open(fileLoc + "/" + name + ".vtk", 'w') as f:
                f.write(head)
                f.write("POINTS " + str(len(nodes)) + " float\n")
                
                for node in nodes:
                    f.write(str(node[2])+ " " + str(node[1])+ " " + str(node[0]) + "\n")
                
                f.write("\nLINES " + str(len(edges)) + " " + str( 3* len(edges)) + "\n")
                for edge in edges:
                    f.write("2 " + str(edge[1]) +" " + str(edge[0]) + "\n")
                    
                f.write("\nVERTICES "+ str(len(nodes)) + " " + str(len(nodes) * 2) + "\n")
                
                for node in nodes:
                    f.write("1 " + str(node[3]) + "\n")
                
                f.write("\nPOINT_DATA " + str(len(nodes)) + "\n") 
                f.write("SCALARS scalars float 1\n")
                f.write("LOOKUP_TABLE default\n")
                for node in nodes:
                    f.write(skeletonColor + "\n")
                
            if not commentonlyToo:
                continue
            
            varname = ""
            if keyForComment != None:
                varname = str(keyForComment)
            
            with open(fileLoc + "/" + name +"_"+ varname +"_comments.vtk", 'w') as f:
                f.write(head)
                f.write("POINTS " + str(len(comments)) + " float\n")
                
                for node in comments:
                    f.write(str(node[2])+ " " + str(node[1])+ " " + str(node[0]) + "\n")
                
                f.write("\nVERTICES "+ str(len(comments)) + " " + str(len(comments) * 2) + "\n")
                count = 0
                for comment in comments:
                    f.write("1 " + str(count) + "\n")
                    count = count + 1
                
                f.write("\nPOINT_DATA " + str(len(comments)) + "\n") 
                f.write("SCALARS scalars float 1\n")
                f.write("LOOKUP_TABLE default\n")
                for comment in comments:
                    f.write(Commentcolor+"\n")
         
        
    def toManyCells(self, NCBEboolean = [True, True, True, True]):
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
    
    def toCellsWithSpecificNames(self, comment = None):
        if comment == None:
            return self
    
        cell = Cells(None, None, [True, True, True, True], True)
        nodeDict = {}
        edgeDict = {}
        commentDict = {}
        branchDict = {}
        nameList = []
 
        for name in self.Names:
            skip = True
            for sname in comment:
                s2 = sname.lower()
                s1 = name.lower()
                if s1 == s2:
                    skip = False
            if skip:
                continue
                    
            nodeDict.setdefault(name)
            nodeDict[name] = self.Nodes[name]
            
            edgeDict.setdefault(name)
            edgeDict[name] = self.Edges[name]
            
            commentDict.setdefault(name)
            commentDict[name] = self.Comments[name]
      
            branchDict.setdefault(name)
            branchDict[name] = self.Branches[name]
                
            nameList.append(name)
       
        cell.Nodes = nodeDict
        cell.Edges = edgeDict
        cell.Comments = commentDict
        cell.Branches = branchDict
        cell.NCBEboolean = [True, True, True, True]
        cell.Names = nameList  
        cell.Parameter = self.Parameter
        cell.scale = self.scale
        
        return cell
    
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
            
        hullDict = self.toConvexHull(Nodes, keyword)
        polyDict = {}
        for name in NodeDict.keys():
            if hullDict[name] == None:
                continue
            polyDict.setdefault(name)
            polyDict[name] = Polygon(vertexToPoly(hullDict[name], yzExtract(NodeDict[name])))
        
        return polyDict
    def toConvexHull(self, Nodes = True, keyword = None, printCSV = False, saveLocation = None):
        if printCSV:
            if saveLocation == None:
                raise Exception("The file name is not specified.")
            if not os.path.isdir(os.path.dirname(saveLocation)):
                raise Exception(os.path.dirname(saveLocation) + "does not exist.")
            #if os.path.exists(saveLocation):
            #    raise Exception(saveLocation + " already exists.")
        
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
            nodeList = NodeDict[name]
            
            if len(nodeList) < 3:
                #raise Exception( name + " list have less than 3 nodes; not enough for convex hull. ")
                print name + " has less than 3 nodes"
                hullDict[name] = None
            else:
                yzList = yzExtract(nodeList)
                
                hullDict.setdefault(name)
                hullDict[name] = ConvexHull(yzList)
                
                if printCSV:
                    vertice = vertexToPoly(hullDict[name], yzList)
                    if keyword == None:
                        keyword = ''
                    
                    printVertice(saveLocation + "/" + name  + "_"+str(keyword), vertice)

        return hullDict
        
        
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
    
    def normalizeX(self, botPlaneCell, topPlaneCell, zeroToOne, extraFactor = 1):
        
        if (not botPlaneCell.NCBEboolean[0]) or (not topPlaneCell.NCBEboolean[0]) :
            raise Exception("Bot cell or Top cell does not have nodes.")
            
            
        topX = topPlaneCell.getMidPoint().values()[0][2]
        botX = botPlaneCell.getMidPoint().values()[0][2]
        
        if self.NCBEboolean[0]:
            for nodeList in self.Nodes.values():
                for node in nodeList:
                    
                    node[2] = (topX - node[2])/( topX - botX)
                    
                    if not zeroToOne:
                        node[2] = (node[2] * 45 + 27.5) * extraFactor
        
        
        if self.NCBEboolean[1]:
            for commentList in self.Comments.values():
                for comment in commentList:
                   
                    comment[2] = (topX - comment[2])/(topX - botX)
                    
                    if not zeroToOne:
                        comment[2] = (comment[2] * 45 + 27.5) * extraFactor
                    
        if self.NCBEboolean[3]:
            for branchList in self.Branches.values():
                for branch in branchList:
                    branch[2] = (topX - branch[2])/(topX - botX)
                    
                    if not zeroToOne:
                        branch[2] = (branch[2] * 45 + 27.5) * extraFactor
    """
    get plane vector. 
    """
    def reorderNodeID(self, keys = None):    
        
        def findMapping(nodeList):
            returnList = []
            count = 0
            
            for node in nodeList:
                newNode = []
                newNode.append(node[3])
                newNode.append(count)
                returnList.append(newNode)
                count = count + 1
            
            return returnList
        
        def changeIndex(mapings, nodeList, index):
            newNodeList = []
            
            for map in mapings:
                for node in nodeList:
                    if map[0] == node[index]:
                        newNode = copy.copy(node)
                        newNode[index] = map[1]
                        
                        newNodeList.append(newNode)
            
            return newNodeList
        newNodes = {}
        newEdges = {}
        newComments = {}
        newBranches = {}
        COMMENTS = self.commentWithKeywordExtractDict(keys)
        
        
        for name in self.Names:
        
            self.Nodes[name].sort(key = lambda node:node[2])
            
            
            Nodes = self.Nodes[name]
            Edges = self.Edges[name]
            Comments = COMMENTS[name]
            Branches = self.Branches[name]        
            
            
            nodeID = set([item[3] for item in Nodes])
            commentID = set(item[3] for item in Comments)
            nodeID.difference_update(commentID)
            Nodes = [item for item in Nodes if item[3] in nodeID]

            maping1 = findMapping(Nodes)
            maping2 = findMapping(Comments)
            newNodes.setdefault(name)
            newNodes[name] = changeIndex(maping1, Nodes, 3)
            newEdges.setdefault(name)
            newEdges[name] = changeIndex(maping1, changeIndex(maping1, Edges, 1), 0)
            newComments.setdefault(name)
            newComments[name] = changeIndex(maping2, Comments, 3)
            newBranches.setdefault(name)
            newBranches[name] = changeIndex(maping1, Branches, 3)
            
            print name
            print len(Edges)
            print len(newEdges[name])
            
        self.Nodes = newNodes
        self.Edges = newEdges
        self.Comments = newComments
        self.Branches = newBranches
        
            
    
    
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
    def getMidPoint(self, onlyX = False, Average = True, Node = True, keyword = None):
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
                if onlyX:
                    avgDict[name] = getAvgPoint(nodeList)[2]
                else:
                    avgDict[name] = getAvgPoint(nodeList)  
            else:
                if onlyX:
                    avgDict[name] = getMedianPoint(nodeList)[2]
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

    def findClosePoints(self, otherCell, threshold = 500, useNodeForSelf = True, keywordForSelf = None, useNodeForOther = True, keywordForOther = None, toCell = False):
        def compareNodeCube(nodeA, nodeB):
            if (math.fabs((nodeA[0] - nodeB[0])) < threshold) and (math.fabs((nodeA[1] - nodeB[1])) < threshold) and (math.fabs((nodeA[2] - nodeB[2])) < threshold):
                return True
            else:
                return False
            
        def compareNode(nodeA, nodeB):
            dist = (nodeA[0] - nodeB[0])*(nodeA[0] - nodeB[0])+(nodeA[1] - nodeB[1])*(nodeA[1] - nodeB[1])+(nodeA[2] - nodeB[2])*(nodeA[2] - nodeB[2])
            thsq = threshold * threshold
            if dist < thsq:
                return True
            else:
                return False
        
        selfNodeDict = {}
        if useNodeForSelf:
            if self.NCBEboolean[0]:
                
                selfNodeDict = self.Nodes
            else:
                raise Exception("The cell does not have Nodes.")
        else:
            if self.NCBEboolean[1]:
                if keywordForSelf == None:
                    selfNodeDict = self.Comments()
                else:
                    selfNodeDict = self.commentWithKeywordExtractDict(keywordForSelf)
                    
        otherNodeList = []      
        if useNodeForOther:
            if otherCell.NCBEboolean[0]:
                otherNodeList = otherCell.allNodesExtract()
            else:
                raise Exception("The cell does not have Nodes.")
        else:
            if otherCell.NCBEboolean[1]:
                if keywordForOther == None:
                    otherNodeList = otherCell.allCommentExtracted()
                else:
                    otherNodeList = otherCell.commentWithKeywordExtract(keywordForOther)
                    
        newNodeDict = {}            
        for name in selfNodeDict.keys():
            
            newNodeDict.setdefault(name)
            newNodeDict[name] = []
            
            nodeList = selfNodeDict[name]
            for selfNode in nodeList:
                newNode = copy.copy(selfNode)
                for otherNode in otherNodeList:
                    if compareNode(newNode, otherNode):
                        newNode.append(otherNode[3])
                        newNode.append(otherNode[4])
                        newNodeDict[name].append(newNode)
                        break
        if toCell:
                
                
            newCell = Cells(None, None, [False, True, False, False], True)
            newCell.NCBEboolean = [False, True, False, False]
            newCell.Names = newNodeDict.keys()
            newCell.Parameter = self.Parameter
            newCell.scale = self.scale
            newCell.Comments =  newNodeDict
            
            return newCell
        
        else:
            return newNodeDict
    
    
    def findClosePointsDict(self, otherCell, threshold = 500, useNodeForSelf = True, keywordForSelf = None, useNodeForOther = True, keywordForOther = None):
        listDict = self.findClosePoints(otherCell, threshold, useNodeForSelf, keywordForSelf, useNodeForOther, keywordForOther)
        
        newDictDict = {}
        for name1 in self.Names:
            newDictDict.setdefault(name1)
            newDict = {}
            for name2 in otherCell.Names:
                newDict.setdefault(name2)
                newDict[name2] = []
            newDictDict[name1] = newDict
        
        for name in listDict:
            for node in listDict[name]:
                newDictDict[node[4]][node[len(node) - 1]].append(node)
        
        for name in newDictDict.keys():
            for name2 in newDictDict[name].keys():
                if len(newDictDict[name][name2]) ==0:
                    del newDictDict[name][name2]
        
        for name in newDictDict.keys():
            if len(newDictDict[name].keys()) == 0:
                del newDictDict[name]
        
        
        
        return newDictDict
    
    def findOverlapArea(self, otherCell, threshold = 500, useNodeForSelf = True, keywordForSelf = None, useNodeForOther = True, keywordForOther = None):
        selfPolygonDict = self.toPolygon(useNodeForSelf, keywordForSelf)
        otherPolygonDict = otherCell.toPolygon(useNodeForOther, keywordForOther)

        newDictDict = {}
        for name1 in selfPolygonDict.keys():
            newDictDict.setdefault(name1)
            newDict = {}
            for name2 in otherPolygonDict.keys():
                newDict.setdefault(name2)
                
                if selfPolygonDict[name1].intersects(otherPolygonDict[name2]):
                    newDict[name2] = (selfPolygonDict[name1].intersection(otherPolygonDict[name2])).area
                else:
                    newDict[name2] = 0 
                
            newDictDict[name1] = newDict
        
        return newDictDict
            
        
        
             
    def filterComments(self):
        print "todo"       
        
    def filterNodes(self):
        print "todo"
                    
                    
                    
        
                    
                    
    