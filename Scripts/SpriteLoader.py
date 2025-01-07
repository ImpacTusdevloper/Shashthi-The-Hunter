import pygame, os, sys
from os import listdir
import GridSystem as grid

scale = grid.diameter

class AnimatedSprite():
    def __init__(self, _path, _tickRate = 1, _pointer = 0):
        self.path = _path
        self.obj = None
        self.tickRate = _tickRate
        self.pointer = _pointer
        self.tick = 0
        self.canAnimate = True
        #Load Sprites
        self.sprites = []
        for sprite in listdir(resource_path("Sprites/" + self.path)):
            if(sprite.endswith(".png")):
                self.sprites.append(Loader(self.path + sprite))
        self.curSprite = self.sprites[self.pointer]
    
    def Update(self):
        if(not self.canAnimate): return
        self.tick += 1
        if(self.tick >= self.tickRate):
            self.tick = 0
            self.pointer += 1
            if(self.pointer >= len(self.sprites)):
                self.pointer = 0
            self.curSprite = self.sprites[self.pointer]

def Loader(path, _scale = 0):
    global scale
    if(_scale == 0):
        _scale = scale
    path = resource_path("Sprites/" + path)
    return pygame.transform.scale(pygame.image.load(path), (_scale, _scale))

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


#!Testing
Test_120x120 = Loader("Test/test_120x120.png")
Test_240x240 = Loader("Test/test_240x240.png")
Test_50x50 = Loader("Test/test_50x50.png")

#Main
test_Head = Loader("Test/test_Head.png")
test_Body_Solid = Loader("Test/test_Body_Solid.png")
test_Body_Dotted = Loader("Test/test_Body_Dotted.png")
test_Tail = Loader("Test/test_Tail.png")
test_Wall = Loader("Test/test_Wall.png")
test_Food = Loader("Test/test_Food.png")

#Squares
test = Loader("Test/test.png")
test01 = Loader("Test/test01.png")
test02 = Loader("Test/test02.png")
test03 = Loader("Test/test03.png")
test04 = Loader("Test/test04.png")
#Circles
testR = Loader("Test/testR.png")
testR01 = Loader("Test/testR01.png")
