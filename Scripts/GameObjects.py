import pygame
import GridSystem as grid
import Load as sprites

import math

enemies = []
boundaries = []
def CreatePlayer():
    import Objects.Player as pObj
    return pObj.Player(grid.diameter)

def CreateBoundaries():
    for node in grid.nodes:
        ind = node.index; maxInd = int(grid.size/grid.diameter)-1
        if ind[0] in [0, maxInd] or ind[1] in [0, maxInd]:
            node.walkable = False
            boundaries.append(StaticObj(node.position, grid.diameter, sprites.test))

class SpawnEnemies():
    def LadyBug():
        import Objects.Enemy.EnemyBase as enemy
        ladyBug = enemy.LadyBug(grid.GetRandAvailNode().position, [0, -1], grid.diameter)
        enemies.append(ladyBug)

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

    def UpdatePosition(self, pos):
        self.position = pos
        self.wPosition = VecSum(self.position, (-self.scale/2, -self.scale/2))

#Mathematical functions
def ExponentialFunc(x, pow = 2):
        return x**pow

def AddFunc(x, const):
     return x + const
def SmoothFunc(t):
    return t * (2 - t)

#Vector logic
def VecSum(v1, v2):
    return (v1[0] + v2[0], v1[1] + v2[1])

def VecMult(v, c):
    return (v[0] * c, v[1] * c)

def MagOfVec(v):
    return (v[0]**2 + v[1]**2)**(1/2)
def NormalOfVec(v):
    return VecMult(v, 1/MagOfVec(v))
     