import sys
class Point(object):
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.L = []
        self.U = []
        self.C = []

class Line(object):
    def __init__(self,startPoint,endPoint,slope):
        self.startPoint=startPoint
        self.endPoint=endPoint
        self.slope = slope
    
    def is_startPoint(self, point):
        return point.x == self.startPoint.x and point.y == self.startPoint.y

    def is_endPoint(self, point):
        return point.x == self.endPoint.x and point.y == self.endPoint.y

class Polygon(object):
    def __init__(self,vertices):
        self.vertices = vertices

def dFunction(line, point,slope):
    result = 0
    if line.slope is not None:
        term1 = (slope*point.x) - (line.slope * line.startPoint.x)
        term2 = (line.startPoint.y - point.y)
        term3 = term1+term2

        result = (1/(slope - line.slope))*term3#(((slope*point.x) - (line.slope * line.startPoint.x)) + (line.startPoint.y - point.y)) 
    else:
        result = line.startPoint.x
    # print("Dfunction value:",result)
    return result


def find_intersection(line1,line2):
    x1 = line1.startPoint.x
    y1 = line1.startPoint.y
    x2 = line1.endPoint.x
    y2 = line1.endPoint.y
    x3 = line2.startPoint.x
    y3 = line2.startPoint.y
    x4 = line2.endPoint.x
    y4 = line2.endPoint.y
    # Calculate the cross product
    cross_product = (x2 - x1) * (y4 - y3) - (y2 - y1) * (x4 - x3)

    # Check if the line segments are collinear or parallel
    if cross_product == 0:
        return None

    # Calculate the parameters t1 and t2
    t1 = ((x4 - x3) * (y1 - y3) - (y4 - y3) * (x1 - x3)) / cross_product
    t2 = ((x2 - x1) * (y1 - y3) - (y2 - y1) * (x1 - x3)) / cross_product

    # Check if the intersection point lies within both line segments
    if 0 <= t1 <= 1 and 0 <= t2 <= 1:
        intersection_x = x1 + t1 * (x2 - x1)
        intersection_y = y1 + t1 * (y2 - y1)
        return Point(intersection_x, intersection_y)

    return None

class EPTreeNode(object):
    def __init__(self,point):
        self.point = point
        self.left=None
        self.right=None
        self.height=1

class EPAVLTree(object):
    #insertion Function
    def insertNode(self,root,key):
        if not root:
            return EPTreeNode(key) #if the root is empty add the current point as the root
            Pprint("Treenode")
        if key.y < root.point.y:
            # print("left,root", (root.point.x, root.point.y))
            # print("left,key,", (key.x, key.y))
            root.left = self.insertNode(root.left,key) #if the current node y-coordinate is smaller than the root go to the left subtree

        elif key.y > root.point.y:
            # print("right,root,", (root.point.x, root.point.y))
            # print("right,key,", (key.x, key.y))
            root.right = self.insertNode(root.right,key)#if the current node y-coordinate is bigger than the root go to the right subtree

        else: #y-coordinates are equal
            if key.x > root.point.x:
                # print("spleft,root,", (root.point.x, root.point.y))
                # print("spleft,key,", (key.x, key.y))
                root.left = self.insertNode(root.left,key) #if the current node x-coordinate is smaller than the root go to the left subtree

            elif key.x < root.point.x:
                root.right = self.insertNode(root.right,key) #if the current node x-coordinate is bigger than the root go to the right subtree
                # print("spRIGHT1,", (root.point.x, root.point.y))
                # print("spRIGHT2,", (key.x, key.y))
            else:
                pass
        #check if the tree is balanced
        root.height = 1 +  max(self.getHeight(root.left),self.getHeight(root.right))
        balance_factor = self.getBalance(root)

        #balancing the tree
        if balance_factor > 1 :
            if self.getBalance(root.left) >= 0:
                return self.rightRotate(root)
            else:
                root.left = self.leftRotate(root.left)
                return self.rightRotate(root)
        if balance_factor < -1:
            if self.getBalance(root.right) <=0:
                return self.leftRotate(root)
            else:
                root.right = self.rightRotate(root.right)
                return self.leftRotate(root)
        return root
    def getHeight(self,root):
        if not root:
            return 0
        return root.height

    def getBalance(self,root):
        if not root:
            return 0
        return self.getHeight(root.left) - self.getHeight(root.right)

    #delete function
    def deleteNode(self, root, key):
        if not root:
            return root

        # Special case: if the key matches the root's key
        if key.y > root.point.y:
            root.right = self.deleteNode(root.right,key)
        elif key.y < root.point.y:
            root.left = self.deleteNode(root.left,key)
        elif key.y == root.point.y:
            if key.x < root.point.x:
                root.right = self.deleteNode(root.right,key)
            elif key.x > root.point.x:
                root.left = self.deleteNode(root.left,key)
            else:
                if not root.left:
                        temp = root.right
                        root = None
                        return temp
                elif not root.right:
                        temp = root.left
                        root = None
                        return temp
                temp = self.getMinValueNode(root.right)
                root.point = temp.point
                root.right = self.deleteNode(root.right, temp.point)
        if not root:
            return root
            #update nodes height
        root.height = 1 + max(self.getHeight(root.left),
                              self.getHeight(root.right))

        balanceFactor = self.getBalance(root)

        # Balance the tree
        if balanceFactor > 1:
            if self.getBalance(root.left) >= 0:
                return self.rightRotate(root)
            else:
                root.left = self.leftRotate(root.left)
                return self.rightRotate(root)
        if balanceFactor < -1:
            if self.getBalance(root.right) <= 0:
                return self.leftRotate(root)
            else:
                root.right = self.rightRotate(root.right)
                return self.leftRotate(root)
        return root

    #function for perforing left rotation
    def leftRotate(self, z):
        y = z.right
        T2 = y.left
        y.left = z
        z.right = T2
        z.height = 1 + max(self.getHeight(z.left),
                           self.getHeight(z.right))
        y.height = 1 + max(self.getHeight(y.left),
                           self.getHeight(y.right))
        return y

    #function to perform right rotation
    def rightRotate(self, z):
        y = z.left
        T3 = y.right
        y.right = z
        z.left = T3
        z.height = 1 + max(self.getHeight(z.left),
                           self.getHeight(z.right))
        y.height = 1 + max(self.getHeight(y.left),
                           self.getHeight(y.right))
        return y

    #getting min value
    def getMinValueNode(self, root):
        if root is None or root.left is None:
            return root
        return self.getMinValueNode(root.left)

    #traverse the Tree in an in-order traversal
    def inorderTraversal(self,root):
        result = []
        if root:
            result.extend(self.inorderTraversal(root.left))
            result.append(root.point)
            result.extend(self.inorderTraversal(root.right))
        return result
    #the name describes what will do
    def printHelper(self, currPtr, indent, last):
        if currPtr is not None:
            sys.stdout.write(indent)
            if last:
                sys.stdout.write("R----")
                indent += "     "
            else:
                sys.stdout.write("L----")
                indent += "|    "
            print((currPtr.point.x),(currPtr.point.y))
            self.printHelper(currPtr.left, indent, False)
            self.printHelper(currPtr.right, indent, True)



class ALTreeNode(object):
    def __init__(self,line):
        self.line = line
        self.left=None
        self.right=None
        self.height=1


class ALAVLTree(object):
    #insertion Function
    def insert_node(self, root, key,point,slslope):
        # Find the correct location and insert the node
        if not root:
            return ALTreeNode(key)
        elif dFunction(key, Point(point.x,point.y - 0.0001),slslope) < dFunction(root.line, Point(point.x,point.y - 0.0001),slslope):
            # print("1 key,left",(key.startPoint.x,key.startPoint.y),(key.endPoint.x,key.endPoint.y))
            # print("1 root",(root.line.startPoint.x,root.line.startPoint.y),(root.line.endPoint.x,root.line.endPoint.y))
            root.left = self.insert_node(root.left, key,point,slslope)
        elif dFunction(key, Point(point.x,point.y - 0.0001),slslope) > dFunction(root.line, Point(point.x,point.y - 0.0001),slslope):
            # print("2 key,right",(key.startPoint.x,key.startPoint.y),(key.endPoint.x,key.endPoint.y))
            # print("2 root",(root.line.startPoint.x,root.line.startPoint.y),(root.line.endPoint.x,root.line.endPoint.y))
            root.right = self.insert_node(root.right, key,point,slslope)
        else:   
            if root.line.slope != key.slope:
                if dFunction(key, Point(point.x,point.y - 0.0001),slslope) < dFunction(root.line, Point(point.x,point.y - 0.0001),slslope):
                    # print("3 key,left",(key.startPoint.x,key.startPoint.y),(key.endPoint.x,key.endPoint.y))
                    # print("3 root",(root.line.startPoint.x,root.line.startPoint.y),(root.line.endPoint.x,root.line.endPoint.y))
                    root.left = self.insert_node(root.left, key,point,slslope)
                else:
                    # print("4 key,right",(key.startPoint.x,key.startPoint.y),(key.endPoint.x,key.endPoint.y))
                    # print("4 root",(root.line.startPoint.x,root.line.startPoint.y),(root.line.endPoint.x,root.line.endPoint.y))
                    root.right = self.insert_node(root.right, key,point,slslope)
            else:#m1=m2!=0
                if root.line.slope !=0:
                    if root.line.endPoint.y > key.endPoint.y:
                        # print("5 key,right",(key.startPoint.x,key.startPoint.y),(key.endPoint.x,key.endPoint.y))
                        # print("5 root",(root.line.startPoint.x,root.line.startPoint.y),(root.line.endPoint.x,root.line.endPoint.y))
                        root.right = self.insert_node(root.right, key,point,slslope) #m1=m2!=0, the one with lowest y-coordinate of end point goes right
                    else:
                        pass
                else:
                    if root.line.endPoint.x < key.endPoint.x:
                        # print("6 key,right",(key.startPoint.x,key.startPoint.y),(key.endPoint.x,key.endPoint.y))
                        # print("6 root",(root.line.startPoint.x,root.line.startPoint.y),(root.line.endPoint.x,root.line.endPoint.y))
                        root.right = self.insert_node(root.right, key,point,slslope) #m1=m2=0, the one with highst x-coordinate of end point goes right
                    else:
                        pass
        root.height = 1 +  max(self.getHeight(root.left),self.getHeight(root.right))
        balance_factor = self.getBalance(root)

        #balancing the tree
        if balance_factor > 1 :
            if self.getBalance(root.left) >= 0:
                return self.rightRotate(root)
            else:
                root.left = self.leftRotate(root.left)
                return self.rightRotate(root)
        if balance_factor < -1:
            if self.getBalance(root.right) <=0:
                return self.leftRotate(root)
            else:
                root.right = self.rightRotate(root.right)
                return self.leftRotate(root)
        return root
    def getHeight(self,root):
        if not root:
            return 0
        return root.height

    def getBalance(self,root):
        if not root:
            return 0
        return self.getHeight(root.left) - self.getHeight(root.right)

    #delete function
    def deleteNode(self, root, key,point,slSlope):

        # Find the node to be deleted and remove it
        if not root:
            return root
        elif dFunction(key, Point(point.x,point.y + 0.01),slSlope) < dFunction(root.line, Point(point.x,point.y + 0.01),slSlope):
            # print("1 key,left",(key.startPoint.x,key.startPoint.y),(key.endPoint.x,key.endPoint.y),dFunction(key, point,slSlope))
            # print("1 root",(root.line.startPoint.x,root.line.startPoint.y),(root.line.endPoint.x,root.line.endPoint.y),dFunction(root.line, point,slSlope))
            root.left = self.deleteNode(root.left, key,point,slSlope)
        elif dFunction(key, Point(point.x,point.y + 0.01),slSlope) > dFunction(root.line, Point(point.x,point.y + 0.01),slSlope):
            # print("2 key,right",(key.startPoint.x,key.startPoint.y),(key.endPoint.x,key.endPoint.y),dFunction(key, point,slSlope))
            # print("2 root",(root.line.startPoint.x,root.line.startPoint.y),(root.line.endPoint.x,root.line.endPoint.y),dFunction(root.line, point,slSlope))
            root.right = self.deleteNode(root.right, key,point,slSlope)
        else :
            if root.line.slope != key.slope:
                if dFunction(key, Point(point.x,point.y + 0.01),slSlope) < dFunction(root.line, Point(point.x,point.y + 0.01),slSlope):
                    # print("3 key,left",(key.startPoint.x,key.startPoint.y),(key.endPoint.x,key.endPoint.y),dFunction(key, point,slSlope))
                    # print("3 root",(root.line.startPoint.x,root.line.startPoint.y),(root.line.endPoint.x,root.line.endPoint.y),dFunction(root.line, point,slSlope))
                    root.left = self.deleteNode(root.left, key,point,slSlope)
                elif dFunction(key, Point(point.x,point.y + 0.01),slSlope) > dFunction(root.line, Point(point.x,point.y + 0.01),slSlope):
                    # print("4 key,right",(key.startPoint.x,key.startPoint.y),(key.endPoint.x,key.endPoint.y),dFunction(key, point,slSlope),dFunction(root.line, point,slSlope))
                    # print("4 root",(root.line.startPoint.x,root.line.startPoint.y),(root.line.endPoint.x,root.line.endPoint.y))
                    root.right = self.deleteNode(root.right, key,point,slSlope)
            elif root.line.slope == key.slope and root.line.slope !=0:
                if root.line.endPoint.y > key.endPoint.y: #m1=m2!=0, look for the lowest y-coordinate of end point in the right subtree
                    # print("5 key,right",(key.startPoint.x,key.startPoint.y),(key.endPoint.x,key.endPoint.y))
                    # print("5 root",(root.line.startPoint.x,root.line.startPoint.y),(root.line.endPoint.x,root.line.endPoint.y))    
                    root.right = self.deleteNode(root.right, key,point,slSlope)   
                else:
                    # print("4")
                    if root.left is None:
                        temp = root.right
                        root = None
                        return temp
                    elif root.right is None:
                        temp = root.left
                        root = None
                        return temp
                    temp = self.getMinValueNode(root.right)
                    root.line = temp.line
                    root.right = self.deleteNode(root.right,
                                                temp.line,point,slSlope)
            elif root.line.slope == key.slope and root.line.slope ==0:
                if root.line.endPoint.x < key.endPoint.x:
                    # print("6 key,right",(key.startPoint.x,key.startPoint.y),(key.endPoint.x,key.endPoint.y))
                    # print("6 root",(root.line.startPoint.x,root.line.startPoint.y),(root.line.endPoint.x,root.line.endPoint.y))
                    root.right = self.deleteNode(root.right, key,point,slSlope)   
                elif root.line.endPoint.x > key.endPoint.x:
                    root.left = self.deleteNode(root.left, key,point,slSlope)
                else:
                    # print("7")
                    if root.left is None:
                        temp = root.right
                        root = None
                        return temp
                    elif root.right is None:
                        temp = root.left
                        root = None
                        return temp
                    temp = self.getMinValueNode(root.right)
                    root.line = temp.line
                    root.right = self.deleteNode(root.right,
                                                temp.line,point,slSlope)
            else:
                # print("8")
                if root.left is None:
                    temp = root.right
                    root = None
                    return temp
                elif root.right is None:
                    temp = root.left
                    root = None
                    return temp
                temp = self.getMinValueNode(root.right)
                root.line = temp.line
                root.right = self.deleteNode(root.right,
                                            temp.line,point,slSlope)
        if root is None:
            return root

            #update nodes height
        root.height = 1 + max(self.getHeight(root.left),
                              self.getHeight(root.right))

        balanceFactor = self.getBalance(root)

        # Balance the tree
        if balanceFactor > 1:
            if self.getBalance(root.left) >= 0:
                return self.rightRotate(root)
            else:
                root.left = self.leftRotate(root.left)
                return self.rightRotate(root)
        if balanceFactor < -1:
            if self.getBalance(root.right) <= 0:
                return self.leftRotate(root)
            else:
                root.right = self.rightRotate(root.right)
                return self.leftRotate(root)
        return root
    #function for perforing left rotation
    def leftRotate(self, z):
        y = z.right
        T2 = y.left
        y.left = z
        z.right = T2
        z.height = 1 + max(self.getHeight(z.left),
                           self.getHeight(z.right))
        y.height = 1 + max(self.getHeight(y.left),
                           self.getHeight(y.right))
        return y

    #function to perform right rotation
    def rightRotate(self, z):
        y = z.left
        T3 = y.right
        y.right = z
        z.left = T3
        z.height = 1 + max(self.getHeight(z.left),
                           self.getHeight(z.right))
        y.height = 1 + max(self.getHeight(y.left),
                           self.getHeight(y.right))
        return y

    #getting min value
    def getMinValueNode(self, root):
        if root is None or root.left is None:
            return root
        return self.getMinValueNode(root.left)

    #traverse the Tree in an in-order traversal

    def inorderTraversal(self,root):
        result = []
        if root:
            result.extend(self.inorderTraversal(root.left))
            result.append(((root.line.startPoint),(root.line.endPoint)))
            result.extend(self.inorderTraversal(root.right))
        return result
    
    #the name describes what will do
    def printHelper(self, currPtr, indent, last):
        if currPtr is not None:
            sys.stdout.write(indent)
            if last:
                sys.stdout.write("R----")
                indent += "     "
            else:
                sys.stdout.write("L----")
                indent += "|    "
            print((currPtr.line.startPoint.x,currPtr.line.startPoint.y),(currPtr.line.endPoint.x,currPtr.line.endPoint.y))
            self.printHelper(currPtr.left, indent, False)
            self.printHelper(currPtr.right, indent, True)

#finding predecessor and successor
def findPreSuc(root, key,point,slSlope):
# Base Case
    if root is None:
        return

    # If key is present at root
    if key.startPoint.x == root.line.startPoint.x and key.startPoint.y == root.line.startPoint.y and key.endPoint.x == root.line.endPoint.x and key.endPoint.y == root.line.endPoint.y:

        # the maximum value in left subtree is predecessor
        if root.left is not None:
            tmp = root.left
            while(tmp.right):
                tmp = tmp.right
            findPreSuc.pre = tmp.line


        # the minimum value in right subtree is successor
        if root.right is not None:
            tmp = root.right
            while(tmp.left):
                tmp = tmp.left
            findPreSuc.suc = tmp.line

        return

    # If key is smaller than root's key, go to left subtree
    if dFunction(root.line,Point(point.x,point.y - 0.01),slSlope) > dFunction(key,Point(point.x,point.y - 0.01),slSlope):
        findPreSuc.suc = root.line
        findPreSuc(root.left, key,point,slSlope)

    elif dFunction(root.line,Point(point.x,point.y - 0.01),slSlope) < dFunction(key,Point(point.x,point.y - 0.01),slSlope):
        findPreSuc.pre = root.line
        findPreSuc(root.right, key,point, slSlope)
    else:

        if root.line.slope != key.slope:
            if root.line.endPoint.x < key.endPoint.x:
                findPreSuc.pre = root.line
                findPreSuc(root.right, key,point, slSlope)
            else:
                findPreSuc.suc = root.line
                findPreSuc(root.left, key,point,slSlope)



eventPoint = EPAVLTree()
activeLine = ALAVLTree()
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

