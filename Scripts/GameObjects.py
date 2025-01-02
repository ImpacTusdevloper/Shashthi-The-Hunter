import pygame, random, math
import GridSystem as grid
import SpriteLoader as sprites

enemies = []
boundaries = []
# Screen shake parameters
shake_duration = 0
shake_intensity = 5
#Directional vectors
lFRB = [(-1, 0), (0, -1), (1, 0), (0, 1)]

#!Classes
class StaticObj:
    def __init__(self, _position, _scale, _sprite):
        self.position = _position
        self.scale = _scale
        self.sprite = _sprite
        self.wPosition = VecSum(self.position, (-self.scale/2, -self.scale/2))
        self.rect = pygame.Rect(self.wPosition[0], self.wPosition[1], self.scale, self.scale)

class DynObj:
    def __init__(self, _position, _orientation, _scale, _sprite, _target = (0, 0)):
        self.position = _position
        self.orientation = _orientation
        self.scale = _scale
        self.sprite = _sprite
        self.target = _target
        self.wPosition = VecSum(self.position, (-self.scale/2, -self.scale/2))
        self.prePos = self.position
        self.rect = pygame.Rect(self.wPosition[0], self.wPosition[1], self.scale, self.scale)
        self.UpdatePosition(self.position)

    def UpdatePosition(self, pos):
        self.position = pos
        self.wPosition = VecSum(self.position, (-self.scale/2, -self.scale/2))
        self.rect.center = self.position

    def UpdateOrientation(self, orientation, forced = False):
        #?No change in orientation
        if(self.orientation == orientation and not forced): return
        x = orientation[1]*self.orientation[0] - orientation[0]*self.orientation[1]
        y = orientation[0]*self.orientation[0] + orientation[1]*self.orientation[1]
        angle = -math.degrees(math.atan2(x, y))
        self.sprite = pygame.transform.rotate(self.sprite, angle)
        self.rect = self.sprite.get_rect(center=self.rect.center)

        self.orientation = orientation
        
class SpawnEnemies():
    def LadyBug():
        import Objects.Enemy.EnemyBase as enemy
        ladyBug = enemy.LadyBug((0, 0), lFRB[1], grid.diameter)
        enemies.append(ladyBug)

#!Functions
def CreatePlayer():
    import Objects.Player as pObj
    return pObj.Player(grid.diameter)

def CreateBoundaries():
    for node in grid.nodes:
        ind = node.index; maxInd = int(grid.size/grid.diameter)-1
        if ind[0] in [0, maxInd] or ind[1] in [0, maxInd]:
            node.walkable = False
            boundaries.append(StaticObj(node.position, grid.diameter, sprites.test_Wall))

def apply_screen_shake():
    global shake_duration
    if shake_duration > 0:
        shake_duration -= 1
        shake_x = random.randint(-shake_intensity, shake_intensity)
        shake_y = random.randint(-shake_intensity, shake_intensity)
        return shake_x, shake_y
    return 0, 0

def trigger_screen_shake(duration):
    global shake_duration
    shake_duration = duration

#Mathematical functions
def ExponentialFunc(x, pow = 2):
        return x**pow

def AddFunc(x, const):
     return x + const
def SmoothFunc(t):
    return t * (2 - t)

#Vector logic
def VecSum(v1, v2, mult = 1):
    return (v1[0] + v2[0]*mult, v1[1] + v2[1]*mult)

def VecMult(v1, v2):
    if(type(v2) == tuple):
        return (v1[0] * v2[0], v1[1] * v2[1])
    return (v1[0] * v2, v1[1] * v2)

def MagOfVec(v):
    return (v[0]**2 + v[1]**2)**(1/2)

def NormalOfVec(v):
    if(MagOfVec(v) == 0): return (0, 0)
    return VecMult(v, 1/MagOfVec(v))
     