class Grid:
    nodes = []
    def __init__(self, _size, _diameter = 1):
        self.size = _size
        self.diameter = _diameter
        self.Create()
    
    def Create(self):
        for x in range(self.size // self.diameter):
            for y in range(self.size // self.diameter):
                avgPos = self.diameter/self.size
                node = {
                    "xIndex": x, "yIndex": y,
                    "wXPos": x * self.diameter + avgPos, "wYPos": y * self.diameter + avgPos,
                    "xPos": x * self.diameter + avgPos + self.diameter/2,
                    "yPos": y * self.diameter + avgPos + self.diameter/2
                }
                self.nodes.append(node)
    
    def NodeFromPos(self, pos):
        diameter = self.diameter
        perX = Clamp01((pos[0])/ self.size)
        perY = Clamp01((pos[1])/ self.size)

        x = int((self.size//diameter) * perX)
        y = int((self.size//diameter) * perY)
        return(x, y)


grid = Grid().self

def SnapToGrid(obj, grid):
    nodePos = grid.NodeFromPos((obj.x+obj.width/2, obj.y+obj.height/2))
    for node in grid.nodes:
        if node["xIndex"] == nodePos[0]:
            if node["yIndex"] == nodePos[1]:
                obj.x = node["xPos"]-obj.width/2
                obj.y = node["yPos"]-obj.height/2

def Clamp01(n):
    if(n >= 1):
        n = 1
    elif(n <= 0):
        n = 0
    return n
