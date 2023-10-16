from Classes import Line
from Classes import Point

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


