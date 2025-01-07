import random

nodes = []
size = 0; wSize = 0
diameter = 0
centerPos = 0

class Node:
    def __init__(self, _index, _wPos, _pos):
        self.index = _index
        self.wPosition = _wPos
        self.position = _pos
        self.walkable = True

    def IsWalkable(self, b):
        self.walkable = b

def Initialize(_size, _wSize, _diameter = 1):
    global size; global wSize; global diameter; global centerPos
    size = _size
    wSize = _wSize
    diameter = _diameter
    Create()
    centerPos = NodeFromPos((wSize[0]/2, wSize[1]/2)).position

def Create():
    for x in range(int(size / diameter)):
        for y in range(int(size / diameter)):
            avgXPos = x * diameter + diameter/size + wSize[0]/2-size/2
            avgYPos = y * diameter + diameter/size + wSize[1]/2-size/2
            node = Node((x, y), (avgXPos, avgYPos), (avgXPos+diameter/2, avgYPos+diameter/2))
            nodes.append(node)
            #print(f"index: {node.index} and Pos: {node.wPosition}")

def NodeFromPos(pos):
    wTopLeft = next(node for node in nodes if node.index == (0, 0)).position
    perX = Clamp01((pos[0]-wTopLeft[0])/ size)
    perY = Clamp01((pos[1]-wTopLeft[1])/size)
    x = int((size//diameter) * perX +1)
    y = int((size//diameter) * perY +1)
    x = min(max(x, 0), int(size // diameter) - 1)
    y = min(max(y, 0), int(size // diameter) - 1)
    return next(node for node in nodes if node.index == (x, y))

def SnapToGrid(obj, pos = None):
    if(pos == None): pos = obj.position
    for node in nodes:
        if(node.index == NodeFromPos(pos).index):
            obj.UpdatePosition(node.position)

def GetRandAvailNode(l = set()):
    node = random.choice(list(set(nodes).difference(l)))
    if(not node.walkable):
        l.add(node)
        node = GetRandAvailNode(l)
    return node

def Clamp01(n):
    if(n >= 1):
        n = 1
    elif(n <= 0):
        n = 0
    return n
