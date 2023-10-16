import math
from fractions import Fraction
import numpy as np

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Line(object):
    def __init__(self,startPoint,endPoint,slope):
        self.startPoint = startPoint
        self.endPoint = endPoint
        self.slope = slope

    def is_startPoint(self, point):
        return point.x == self.startPoint.x and point.y == self.startPoint.y

    def is_endPoint(self, point):
        return point.x == self.endPoint.x and point.y == self.endPoint.y
    
def find_intersection(line1,line2):
    x1 = Fraction(line1.startPoint.x)
    y1 = Fraction(line1.startPoint.y)
    x2 = Fraction(line1.endPoint.x)
    y2 = Fraction(line1.endPoint.y)
    x3 = Fraction(line2.startPoint.x)
    y3 = Fraction(line2.startPoint.y)
    x4 = Fraction(line2.endPoint.x)
    y4 = Fraction(line2.endPoint.y)
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
        return Point(intersection_x,intersection_y)

    return None

def point_checker(point,polygon):
    for p in polygon:
        if((point.x == p[0]) and(point.y == p[1])):
            return True

def left_or_right(segment,point):
    # print("Point:",(point.x,point.y))
    A = (segment.startPoint.x - segment.endPoint.x) * (segment.startPoint.y - point.y)
    B = (segment.startPoint.y - segment.endPoint.y) * (segment.startPoint.x - point.x)
    # Calculate the cross product of the direction vectors
    cross_product = (A) - (B)
    # print("cp:",cross_product)
    if cross_product > 0:
        return "left"
    elif cross_product < 0:
        return "right"
    else:
        return "parallel"
def angle_finder(line1,line2):
    A = np.array([line1.startPoint.x, line1.startPoint.y])
    B = np.array([line1.endPoint.x, line1.endPoint.y])
    C = np.array([line2.startPoint.x, line2.startPoint.y])
    D = np.array([line2.endPoint.x, line2.endPoint.y])

    # Calculate the direction vectors
    AB = B - A
    CD = D - C

    # Calculate the dot product and cross product
    dot_product = np.dot(AB, CD)
    cross_product = np.cross(AB, CD)

    # Calculate the angle in radians
    theta = np.arctan2(cross_product, dot_product)

    # Convert the angle to degrees
    theta_degrees = np.degrees(theta)

    # Ensure the angle is positive and represents counter-clockwise direction
    if theta_degrees < 0:
        theta_degrees += 360.0

    return theta_degrees

def vector_angle(line):
# Define the coordinates of the two points
    # Calculate the vector components
    vector_x = line[0]
    vector_y = line[1]

    # Calculate the angle (in radians) relative to the x-axis
    angle_rad = math.atan2(vector_y, vector_x)
    if angle_rad < 0:
        angle_rad += 2 * math.pi

    # Convert the angle to degrees if needed
    angle_deg = math.degrees(angle_rad)
    return angle_deg


pointsA=[]
pointsB=[]
edgesA=[]
edgesB=[]

cond1 = True
cond2 = False

def lowest_key(polygon):
    lowest_key = min((point[1], point[0]) for point in polygon)
    lowest_key_points = next(filter(lambda point: (point[1], point[0]) == lowest_key, polygon))
    return lowest_key_points

def highest_key(polygon):
    highest_key = max((point[1], point[0]) for point in polygon)
    highest_key_points = next(filter(lambda point: (point[1], point[0]) == highest_key, polygon))
    return highest_key_points

def tVectorFinder(p,edgesA,edgesB,l=None):
    if (cond1):
        edgeA= next(filter(lambda e: e.is_startPoint(p)  , edgesA))
        edgeB= next(filter(lambda e: e.is_startPoint(p)  , edgesB))
        # print("edgeA:",(edgeA.startPoint.x,edgeA.startPoint.y),(edgeA.endPoint.x,edgeA.endPoint.y))
        # print("edgeB:",(edgeB.startPoint.x,edgeB.startPoint.y),(edgeB.endPoint.x,edgeB.endPoint.y))
        if(left_or_right(edgeA,edgeB.endPoint) == "left"):
            return (edgeB.startPoint.x - edgeB.endPoint.x, edgeB.startPoint.y - edgeB.endPoint.y),edgeA.startPoint
        elif ((left_or_right(edgeA,edgeB.endPoint) == "right")):
            return (edgeA.endPoint.x - edgeA.startPoint.x, edgeA.endPoint.y - edgeA.startPoint.y),edgeA.endPoint
        else:
            return((edgeB.startPoint.x - edgeB.endPoint.x) + (edgeA.endPoint.x - edgeA.startPoint.x),(edgeB.startPoint.y - edgeB.endPoint.y) + (edgeA.endPoint.y - edgeA.startPoint.y)),edgeA.endPoint
    else:   
        if (cond2):
            return(l.endPoint.x - p.x, l.endPoint.y - p.y),l.endPoint 
        else: 
            return(p.x - l.endPoint.x , p.y - l.endPoint.y),p

def rotate_point(point,angle):
    # Angle of rotation in radians
    x = point.x
    y = point.y
    alpha = math.radians(angle)  # Rotate the coordinate system by 45 degrees counterclockwise
    # Apply the rotation transformation
    x_rotated = x * math.cos(alpha) + y * math.sin(alpha)
    y_rotated = -x * math.sin(alpha) + y * math.cos(alpha)
    return (y_rotated)

def bounding(edge, tVector):    
    if (
        ((tVector.startPoint.x >= min(edge.startPoint.x,edge.endPoint.x) and tVector.startPoint.x <= max(edge.startPoint.x,edge.endPoint.x))
        and
        (tVector.startPoint.y >= min(edge.startPoint.y,edge.endPoint.y) and tVector.startPoint.y <= max(edge.startPoint.y,edge.endPoint.y)))
        or
        ((tVector.endPoint.x >= min(edge.startPoint.x,edge.endPoint.x) and tVector.endPoint.x <= max(edge.startPoint.x,edge.endPoint.x))
        and
        (tVector.endPoint.y >= min(edge.startPoint.y,edge.endPoint.y) and tVector.endPoint.y <= max(edge.startPoint.y,edge.endPoint.y)))
        or
        ((edge.startPoint.x >= min(tVector.startPoint.x,tVector.endPoint.x) and edge.startPoint.x <= max(tVector.startPoint.x,tVector.endPoint.x))
        and
        (edge.startPoint.y >= min(tVector.startPoint.y,tVector.endPoint.y) and edge.startPoint.y <= max(tVector.startPoint.x,tVector.endPoint.y)))
        or
        ((edge.endPoint.x >= min(tVector.startPoint.x,tVector.endPoint.x) and edge.endPoint.x <= max(tVector.startPoint.x,tVector.endPoint.x))
        and
        (edge.endPoint.y >= min(tVector.startPoint.y,tVector.endPoint.y) and edge.endPoint.y <= max(tVector.startPoint.y,tVector.endPoint.y)))  
        ):
        return True
    else:
        return False

def trimFunc(Points,translateVector,filteredEdges,p,contactP):
    global cond1
    global cond2
    tVectors = []
    nTVec = translateVector
    fEdge= None
    intersection = None
    for point in Points:
        tVectors.append((Line(Point(point[0],point[1]),Point(point[0] + translateVector[0],point[1] + translateVector[1]),
        (((point[1] + translateVector[1] - point[1]))/((point[0] + translateVector[0]) - point[0])) if ((point[0] + translateVector[0]) - point[0]) != 0 else None)))
    for tVec in tVectors:
        for edge in filteredEdges:
            intersect = find_intersection(tVec,edge)
            if (intersect is not None):
                if not(edge.is_startPoint(intersect) or edge.is_endPoint(intersect)):
                    if(not(tVec.is_startPoint(intersect) and  left_or_right(edge,tVec.endPoint)=="right") and (intersect.x != (tVec.startPoint.x + translateVector[0]) and intersect.y != (tVec.startPoint.y + translateVector[1]))):
                        cond1 = False
                        cond2 = p
                        nTVec = ((intersect.x - tVec.startPoint.x), (intersect.y - tVec.startPoint.y))
                        if(p):
                            intersection = Point(intersect.x,intersect.y)
                            fEdge = edge 
                        else:
                            intersection = Point(intersect.x - nTVec[0],intersect.y - nTVec[1])
                            fEdge = Line(Point(edge.startPoint.x -  nTVec[0],edge.startPoint.y - nTVec[1]),Point(edge.endPoint.x -  nTVec[0],edge.endPoint.y - nTVec[1]),((edge.endPoint.y - nTVec[1]) -(edge.startPoint.y + nTVec[1]) /(edge.endPoint.x + nTVec[0]) -(edge.startPoint.x + nTVec[0])) if ((edge.endPoint.x + nTVec[0]) -(edge.startPoint.x + nTVec[0]) != 0) else None)
                        trimFunc(Points,nTVec,filteredEdges,p,contactP)
                        break
    return (nTVec,intersection,fEdge)


def boundry(polygonA,polygonB,vector):
    angle = vector_angle(vector)
    edgesA = [Line(Point(a[0],a[1]),Point(b[0],b[1]),((b[1] - a[1])/(b[0] - a[0])) if (b[0] - a[0]) != 0 else None)  for a, b in zip(polygonA, polygonA[1:] + [polygonA[0]])] 

    rotated_points =[]

    for point in polygonB:
        rotated_points.append(rotate_point(Point(point[0],point[1]),angle))

    minVal = polygonB[rotated_points.index(min(rotated_points))]
    maxVal = polygonB[rotated_points.index(max(rotated_points))]
    seg1 = Line(Point(minVal[0],minVal[1]),Point(minVal[0] + vector[0],minVal[1] + vector[1]),0)
    seg2 = Line(Point(maxVal[0],maxVal[1]),Point(maxVal[0] + vector[0],maxVal[1] + vector[1]),0)
    filtered_edges = []
    for edge in edgesA:
        if(not 
           ((((left_or_right(seg1,edge.startPoint) == "left") and (left_or_right(seg1,edge.endPoint) == "left")) and ((left_or_right(seg2,edge.startPoint) == "left") and (left_or_right(seg2,edge.endPoint) == "left"))) 
           or
           (((left_or_right(seg1,edge.startPoint) == "right") and (left_or_right(seg1,edge.endPoint) == "right")) and ((left_or_right(seg2,edge.startPoint) == "right") and (left_or_right(seg2,edge.endPoint) == "right")))
           )):
            filtered_edges.append(edge)
    return filtered_edges

def NFP(polygonA,polygonB):
    global cond1
    x = Point(-1,1)
    L=None
    nfp = []
    polygonB2=polygonB[:]
    a_RefPoint = Point(lowest_key(polygonA)[0],lowest_key(polygonA)[1])
    b_highPoint = Point(highest_key(polygonB2)[0],highest_key(polygonB2)[1])
    edgesA = [Line(Point(a[0],a[1]),Point(b[0],b[1]),((b[1] - a[1])/(b[0] - a[0])) if (b[0] - a[0]) != 0 else None)  for a, b in zip(polygonA, polygonA[1:] + [polygonA[0]])] 
    dVec = [a_RefPoint.x - b_highPoint.x,a_RefPoint.y - b_highPoint.y ]
    polygonB2= [[x+dVec[0], y +dVec[1]] for x,y in polygonB2]
    contactPoint = a_RefPoint
    y = 0
    # (x.x  != a_RefPoint.x) or (x.y != a_RefPoint.y)
    while((x.x  != a_RefPoint.x) or (x.y != a_RefPoint.y) or y<2):
        b_RefPoint = (lowest_key(polygonB2)[0],lowest_key(polygonB2)[1])
        nfp.append(b_RefPoint)
        edgesB = [Line(Point(a[0],a[1]),Point(b[0],b[1]),((b[1] - a[1])/(b[0] - a[0])) if (b[0] - a[0]) != 0 else None)  for a, b in zip(polygonB2, polygonB2[1:] + [polygonB2[0]])]
        tvec = tVectorFinder(contactPoint,edgesA,edgesB,L)[0]
        firstTVec = tvec
        nextCP = tVectorFinder(contactPoint,edgesA,edgesB,L)[1]
        filteredEdgesA = boundry(polygonA,polygonB2,tvec)
        filteredEdgesB = boundry(polygonB2,polygonA,(-tvec[0],-tvec[1]))
        Trimresult = trimFunc(polygonB2,tvec,filteredEdgesA,True,contactPoint)
        tvec = Trimresult[0]
        result = trimFunc(polygonA,(-tvec[0],-tvec[1]),filteredEdgesB,False,contactPoint)
        if ((result[0] != (-tvec[0],-tvec[1])) and (result[0][0] != 0 and result[0][1] != 0)):
            tvec = result[0]
            L=result[2]
            polygonB2= [[x - (tvec[0]), y - (tvec[1])] for x,y in polygonB2]
            if (result[1] == None):
                contactPoint = nextCP
            else:
                contactPoint = result[1]
        elif((Trimresult[0] != (firstTVec[0],firstTVec[1])) and (Trimresult[0][0] != 0 and Trimresult[0][1] != 0)):
            L= Trimresult[2]
            polygonB2= [[x + (tvec[0]), y + (tvec[1])] for x,y in polygonB2]
            if (Trimresult[1] == None):
                contactPoint = nextCP
            else:
                contactPoint = Trimresult[1]
        else:
            cond1 = True
            polygonB2= [[x + (tvec[0]), y + (tvec[1])] for x,y in polygonB2]
            if (Trimresult[1] ==  None):
                contactPoint = nextCP
            else:
                contactPoint = Trimresult[1]
        x= contactPoint
        y +=1        
    return nfp

