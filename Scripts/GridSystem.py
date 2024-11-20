nodes = []
size = 0
diameter = 0
centerPos = 0

def Initialize(_size, _diameter = 1):
    global size; global diameter; global centerPos
    size = _size
    diameter = _diameter
    Create()
    centerPos = NodeFromPos((size/2, size/2)).position

def Create():
    for x in range(int(size / diameter)):
        for y in range(int(size / diameter)):
            avgXPos = x * diameter + diameter/size
            avgYPos = y * diameter + diameter/size
            nodes.append(Node((x, y), (avgXPos, avgYPos), (avgXPos + diameter/2,avgYPos + diameter/2)))

def NodeFromPos(pos):
    perX = Clamp01((pos[0])/ size)
    perY = Clamp01((pos[1])/ size)
    x = int((size//diameter) * perX)
    y = int((size//diameter) * perY)
    return next(node for node in nodes if node.index == (x, y))

def SnapToGrid(obj, pos = None):
    if(pos == None): pos = obj.position
    for node in nodes:
        if(node.index == NodeFromPos(pos).index):
            obj.position = node.position

class Node:
    def __init__(self, _index, _wPos, _pos):
        self.index = _index
        self.wPosition = _wPos
        self.position = _pos


def Clamp01(n):
    if(n >= 1):
        n = 1
    elif(n <= 0):
        n = 0
    return n
