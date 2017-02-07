'''
Created on Aug 19, 2016

@author: Nao
'''
from ImportList import *


def CellPrinter(Cellcoin, filename):
    nodes = Cellcoin.Nodes
    edges = Cellcoin.Edges
    print Cellcoin.allCommentExtracted
    comments = Cellcoin.allCommentExtracted()
    branches = Cellcoin.allBranchExtracted()
    Parameter = Cellcoin.Parameter
    scaler = Cellcoin.scale
    root = ET.Element("things")
    root.append(Parameter)
    rgb_t="-1." 
    a_t="1." 
    nodeide = 1
    Cellnames = nodes.keys()
    for itemz in Cellnames:
        node = nodes[itemz]
        edge = edges[itemz]
        thing=ET.SubElement(root, "thing", id=str(nodeide), colorr='%s' %rgb_t, colorg='%s' %rgb_t, colorb='%s' %rgb_t, colora='%s' %a_t, comment= itemz)
        node1 = ET.SubElement(thing, "nodes") 
        nodeide = nodeide +1
        for item1 in node:
            a = str(int(item1[0]/scaler[0]))
            b = str(int(item1[1]/scaler[1]))
            c = str(int(item1[2] * 1000/scaler[2]))
            d = str(item1[3])
            e = item1[4]
            node=ET.SubElement(node1, "node", id= d, radius="10", x=c, y=b, z=a, inVP="1", inMag="1", time="0")    
        edge1 = ET.SubElement(thing, "edges")
        for item2 in edge:
            a = str(item2[0])
            b = str(item2[1])
        
            node=ET.SubElement(edge1, "edge", target = a, source = b )
        
    comment1 =ET.SubElement(root, "comments")
    for item3 in comments:
        a = str(item3[3])
        b = str(item3[4])
        node=ET.SubElement(comment1, "comment", node = a, content = b )
    
    branch1 =ET.SubElement(root, "branchpoints")
    for item3 in branches:
        a = str(item3[3])
        node=ET.SubElement(branch1, "branchpoint", id = a)
    
    newfile = filename
    pile = open(newfile, "w")
    pile.writelines(ET.tostring(root, pretty_print=True, xml_declaration=True, encoding='UTF-8'))
    pile.close()    
    

""" Separator Printer  """
def separtor(Cellcoin, cellname, saveLoc):
    node = Cellcoin.Nodes[cellname]
    edge = Cellcoin.Edges[cellname]
    comment = Cellcoin.Comments[cellname]
    branch = Cellcoin.Branches[cellname]
    Parameter = Cellcoin.Parameter
    scale = Cellcoin.scale
    
    root = ET.Element("things")
    root.append(Parameter)
    rgb_t="-1." 
    a_t="1." 
    ij = 1
    nodeide = 1
    thing=ET.SubElement(root, "thing", id=str(ij), colorr='%s' %rgb_t, colorg='%s' %rgb_t, colorb='%s' %rgb_t, colora='%s' %a_t, comment=cellname)
    node1 = ET.SubElement(thing, "nodes")
    ij = ij+1
    for item1 in node:
            
        a = str(int(item1[0]/scale[0]))
        b = str(int(item1[1]/scale[1]))
        c = str(int(item1[2]/scale[2]))
        d = str(item1[3])
        e = item1[4]
        nodeide = nodeide +1
        node=ET.SubElement(node1, "node", id= d, radius="10", x=c, y=b, z=a, inVP="1", inMag="1", time="0")    
    edge1 = ET.SubElement(thing, "edges")
    for item2 in edge:
        a = str(item2[0])
        b = str(item2[1])
        
        node=ET.SubElement(edge1, "edge", target = a, source = b )
        
    comment1 =ET.SubElement(root, "comments")
    for item3 in comment:
        a = str(item3[3])
        b = str(item3[4])
        node=ET.SubElement(comment1, "comment", node = a, content = b )
    
    branch1 =ET.SubElement(root, "branchpoints")
    for item3 in branch:
        a = str(item3[3])
        node=ET.SubElement(branch1, "branchpoint", id = a)
    
    print("done")
    newfile = saveLoc + "/" + cellname + ".xml"
    pile = open(newfile, "w")
    pile.writelines(ET.tostring(root, pretty_print=True, xml_declaration=True, encoding='UTF-8'))
    pile.close()    
    


def convertToVTK(Cells, saveLocation):

    head1 = "# vtk DataFile Version 3.0\n"
    head2 = "vtk output\n"
    head3 = "ASCII\n"
    head4 = "DATASET POLYDATA\n\n"
    head = head1 + head2 + head3 + head4
    
    for name in Cells.Names:
        with open(saveLocation + "/" + name + ".vtk", 'w') as f:
            f.write(head)
            
    
    
    
    
    
    
