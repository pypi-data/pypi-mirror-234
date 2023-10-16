from DFunction import dFunction
from Classes import  Line
from Classes import  Point
import sys

class TreeNode(object):
    def __init__(self,line):
        self.line = line
        self.left=None
        self.right=None
        self.height=1


class AVLTree(object):
    #insertion Function
    def insert_node(self, root, key,point,slslope):
        # Find the correct location and insert the node
        if not root:
            return TreeNode(key)
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
