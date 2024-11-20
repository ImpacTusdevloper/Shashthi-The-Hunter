import pygame
import GridSystem

import math

def CreatePlayer():
    import Objects.Player as pObj
    return pObj.Player(GridSystem.diameter)

class DynObj:
    refVec = 0
    def __init__(self, _position, _orientation, _scale, _sprite, _target = 0):
        self.position = _position
        self.orientation = _orientation
        self.scale = _scale
        self.sprite = _sprite
        self.target = _target
        self.wPosition = VecSum(self.position, (-self.scale/2, -self.scale/2))

    def UpdatePosition(self, pos):
        self.position = pos
        self.wPosition = VecSum(self.position, (-self.scale/2, -self.scale/2))


def ExponentialFunc(x, pow = 2):
        return x**pow

def MultyFunc(x, const):
    return x * const

def AddFunc(x, const):
     return x + const

#Vector logic
def VecSum(v1, v2):
    return (v1[0] + v2[0], v1[1] + v2[1])

def VecMult(v, c):
    return (v[0] * c, v[1] * c)

def MagOfVec(v):
    return (v[0]**2 + v[1]**2)**(1/2)
def NormalOfVec(v):
    return VecMult(v, 1/MagOfVec(v))
     