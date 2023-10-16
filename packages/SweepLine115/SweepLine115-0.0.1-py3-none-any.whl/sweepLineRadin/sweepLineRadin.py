
from EPAVLTree import AVLTree
from ALAVLTree import AVLTree as AL
from ALAVLTree import findPreSuc
from Intersection import find_intersection

eventPoint = AVLTree()
activeLine = AL()
findPreSuc.pre = None
findPreSuc.suc = None
EProot = None
ALroot = None


def findNewEvent(left,right,p,root):
    if left is None or right is None:
        return
    else:
        intersection = find_intersection(left,right)
        if intersection is None:
            pass
        else:
            if (intersection.y < p.y and intersection.x < p.x) or (intersection.y <= p.y and intersection.x >= p.x )  and not (intersection.y == p.y and intersection.x == p.x):
                root =  eventPoint.insertNode(root,intersection)
                if intersection.x != left.endPoint.x or intersection.y != left.endPoint.y:
                    intersection.C.append(left)
                if intersection.x != right.endPoint.x or intersection.y != right.endPoint.y:
                    intersection.C.append(right)

def findMostLeft(l,list,p,SL_Slope):
    newList = list[:]
    newList.pop(newList.index(l))
    findPreSuc(ALroot,l,p,SL_Slope)
    left = findPreSuc.pre
    if len(newList) == 0:
        return l
    else:
        if left is not None:
            for line in newList:
                if left.startPoint.x == line.startPoint.x and left.startPoint.y == line.startPoint.y and left.endPoint.x == line.endPoint.x and left.endPoint.y == line.endPoint.y:
                    return findMostLeft(line,newList,p,SL_Slope)
                else:
                    return l
        else:
            return l

def findMostRight(l,list,p,SL_Slope):
    newList = list[:]
    newList.pop(newList.index(l))
    findPreSuc(ALroot,l,p,SL_Slope)
    right = findPreSuc.suc
    if len(newList) == 0:
        return l
    else:
        if right is not None:
            for line in newList:
                if right.startPoint.x == line.startPoint.x and right.startPoint.y == line.startPoint.y and right.endPoint.x == line.endPoint.x and right.endPoint.y == line.endPoint.y:
                    return findMostRight(line,newList,p,SL_Slope)
                else:
                    return l
        else:
            return l

def handleEvent(point,SL_Slope,root):
    global ALroot
    intersection = []
    findPreSuc.pre = None
    findPreSuc.suc = None
    if(len(point.U) + len(point.L) + len(point.C)) > 1:
        intersection.append(point)
    temp1 = point.L + point.C
    temp2 = point.U + point.C
    for line in temp1:
        ALroot = activeLine.deleteNode(ALroot,line,point,SL_Slope)
    for line in temp2:
        ALroot = activeLine.insert_node(ALroot,line,point,SL_Slope)
    if len(temp2) == 0:
        left = findPreSuc.pre
        right = findPreSuc.suc
        findNewEvent(left,right,point,root) 
    else:
        left = findMostLeft(temp2[0],temp2,point,SL_Slope)
        findPreSuc.pre = None
        findPreSuc.suc = None
        findPreSuc(ALroot,left,point,SL_Slope)
        mostLeft = findPreSuc.pre
        findNewEvent(mostLeft,left,point,root)
        right = findMostRight(temp2[-1],temp2,point,SL_Slope)
        findPreSuc.pre = None
        findPreSuc.suc = None
        findPreSuc(ALroot,right,point,SL_Slope)
        mostRight = findPreSuc.suc
        findNewEvent(mostRight,right,point,root)
    return intersection



def sweepLine(pointList,edgesList):
    global EProot
    SL_Slope = 0.0001
    for line in edgesList:
        if(line.slope == SL_Slope):
            SL_Slope = SL_Slope + (SL_Slope/100)

    for point in pointList:
        for line in edgesList:
            if(line.is_startPoint(point)):
                point.U.append(line)
            elif(line.is_endPoint(point)):
                point.L.append(line)

    #filling the event point AVLTree
    for point in pointList:
        EProot =  eventPoint.insertNode(EProot,point)
    inorder = eventPoint.inorderTraversal(EProot)
    reversed_inorder = list(reversed(inorder))
    root= EProot
    result = []
    filteredResult = []
    while len(reversed_inorder) >= 1:
        reversed_inorder = list(reversed(eventPoint.inorderTraversal(root)))
        p = reversed_inorder[0]
        root = eventPoint.deleteNode(root,p)
        reversed_inorder = list(reversed(eventPoint.inorderTraversal(root)))
        result.extend(handleEvent(p,SL_Slope,root))
    filteredResult = [tuple for tuple in result if tuple not in (pointList)]
    return filteredResult

