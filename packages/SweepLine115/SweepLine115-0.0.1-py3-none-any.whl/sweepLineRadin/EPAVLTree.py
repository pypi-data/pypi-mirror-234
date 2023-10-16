from Classes import Point
from Classes import Line
import sys
class TreeNode(object):
    def __init__(self,point):
        self.point = point
        self.left=None
        self.right=None
        self.height=1

class AVLTree(object):
    #insertion Function
    def insertNode(self,root,key):
        if not root:
            return TreeNode(key) #if the root is empty add the current point as the root
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