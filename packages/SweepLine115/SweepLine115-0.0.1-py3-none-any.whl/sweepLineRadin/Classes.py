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
