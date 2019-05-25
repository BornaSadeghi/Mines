import math

def distance (p1, p2):
    return math.hypot(p2[0]-p1[0], p2[1]-p1[1])

# return true if a point is within a rectangle (x,y,w,h)
def inRect(pos, rect, inclusive=True):
    x, y = pos
    rX, rY, rW, rH = rect
    return rX <= x <= rX+rW and rY <= y <= rY+rH

def inCircle(pos, circlePos, circleRadius, inclusive=True):
    if distance(pos, circlePos) <= circleRadius:
        return True
    return False

def vertRectCollision(rect1, rect2):
    x,y,w,h = rect1
    verts = (x,y), (x+w,y), (x,y+h), (x+w,y+h)
    
    for v in verts:
        if inRect(v, rect2):
            return True

def rectCollision(rect1, rect2, getSide=False):
    (r1x, r1y, r1w, r1h), (r2x, r2y, r2w, r2h) = rect1, rect2 
    w,h = (r1w + r2w)/2, (r1h + r2h)/2 # average width and height
    diffX, diffY = (r1x+r1w/2 - r2x+r2w/2), (r1y+r1h/2 - r2y+r2h/2) # x and y difference between centers
    
    if abs(diffX) <= w and abs(diffY) <= h:
        if getSide: # gets the side of the first rectangle which the second rectangle intersects
            wy,hx = w * diffY, h * diffX
            if wy > hx:
                if wy > -hx:
                    return "top"
                else:
                    return "left"
            else:
                if wy > -hx:
                    return "right"
                else:
                    return "bottom"
        else:
            return True

def circleCollision (pos1, radius1, pos2, radius2):
    if distance(pos1, pos2) <= radius1+radius2:
        return True
    return False

def circleCollidesRect(circlePos, radius, rect):
    diffX, diffY = abs(circlePos[0] - rect[0]), abs(circlePos[1] - rect[1])

    if diffX > rect[2]/2+radius or diffY > rect[3]/2+radius:
        return False
    elif diffX <= rect[2]/2 or diffY <= rect[3]/2:
        return True
    
    cornerDistance = (diffX - rect[2]/2)**2 + (diffY - rect[3]/2)**2

    return cornerDistance <= radius**2

# check if two lines intersect
# takes in two lines (x,y), (x,y)
def linesCollide(line1, line2):
    l1p1, l1p2, l2p1, l2p2 = line1[0], line1[1], line2[0], line2[1]
    
    q = (l1p1[1] - l2p1[1]) * (l2p2[0] - l2p1[0]) - (l1p1[0] - l2p1[0]) * (l2p2[1] - l2p1[1])
    d = (l1p2[0] - l1p1[0]) * (l2p2[1] - l2p1[1]) - (l1p2[1] - l1p1[1]) * (l2p2[0] - l2p1[0])
    if d == 0:
        return False
    
    r = q / d
    q = (l1p1[1] - l2p1[1]) * (l1p2[0] - l1p1[0]) - (l1p1[0] - l2p1[0]) * (l1p2[1] - l1p1[1]) 
    
    s = q / d
    if r < 0 or r > 1 or s < 0 or s > 1:
        return False

    return True

# checks if a line intersects a rectangle
# takes in line (x,y), rect (x,y,w,h)
def lineCollidesRect(line, rect):
    rectTop = (rect[0], rect[1]), (rect[0] + rect[2], rect[1])
    rectRight = (rect[0] + rect[2], rect[1]), (rect[0] + rect[2], rect[1] + rect[3])
    rectBottom = (rect[0], rect[1] + rect[3]), (rect[0] + rect[2], rect[1] + rect[3])
    rectLeft = (rect[0], rect[1]), (rect[0], rect[1] + rect[3])
    
    if linesCollide(line, rectTop) or linesCollide(line, rectRight) or linesCollide(line, rectBottom) or linesCollide(line, rectLeft):
        return True
    return False
