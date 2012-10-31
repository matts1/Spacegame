import math
ANGLE = 4
def rotate_movement(angle, x, y, dr = 1):
    angle = math.radians(angle)
    x += dr * ANGLE * math.sin(angle)
    y += dr * ANGLE * math.cos(angle)
    return [x, y]

def in_bounds(obj, h, w, xdis = 0, ydis = 0):
    x, y = obj.x, obj.y
    if 0 - xdis >= obj.x: x = 0 - xdis
    if obj.x >= w + xdis: x = w + xdis
    if 0 - ydis >= obj.y: y = 0 - ydis
    if obj.y >= h + ydis: y = h + ydis
    if y == obj.y and x == obj.x: return [1]
    return [0, x, y]

def highscore(score):
    highfile = open('high.txt', 'rU')
    high = int(highfile.read())
    highfile.close()
    print high, "was the highscore"
    print "Your score was", score
    if score > high:
        print "You beat the highscore"
        highfile = open('high.txt', 'w')
        highfile.write(str(score))
        highfile.close()
        
def detect_collision(obj1, obj2):
    if obj1.x + obj1.width / 2.0 > obj2.x - obj2.width:
        if obj1.x - obj1.width / 2.0 < obj2.x + obj2.width:
            if obj1.y + obj1.height / 2.0 > obj2.y - obj2.height:
                if obj1.y - obj1.height / 2.0 < obj2.y + obj2.height:
                    return 1
    return 0
