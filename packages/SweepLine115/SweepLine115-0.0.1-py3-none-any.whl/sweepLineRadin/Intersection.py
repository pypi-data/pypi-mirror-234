from Classes import Point
from Classes import Line

# def find_intersection(line1,line2):
#     if line1.slope is not None:
#         m1 = line1.slope * line1.startPoint.x
#         l1 = line1.startPoint.y - m1
    
#     if line2.slope is not None:
#         m2 = line2.slope * line2.startPoint.x
#         l2 = line2.startPoint.y - m2

    
#     if line1.slope == line2.slope:
#         # The line segments are parallel and will not intersect.
#         return None
#     temp1 = l2 - l1 
#     x_intersect = temp1 / (line1.slope - line2.slope)
#     y_intersect = line1.slope * x_intersect + l1 

#     if (
#         min(line1.startPoint.x, line1.endPoint.x) <= x_intersect <= max(line1.startPoint.x, line1.endPoint.x) and
#         min(line2.startPoint.x, line2.endPoint.x) <= x_intersect <= max(line2.startPoint.x, line2.endPoint.x) and
#         min(line1.startPoint.y, line1.endPoint.y) <= y_intersect <= max(line1.startPoint.y, line1.endPoint.y) and
#         min(line2.startPoint.y, line2.endPoint.y) <= y_intersect <= max(line2.startPoint.y, line2.endPoint.y)
#     ):
#         return (Point(x_intersect, y_intersect))
#     else:
#         return None


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