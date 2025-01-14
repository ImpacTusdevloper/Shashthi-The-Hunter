import pygame, os, sys, random
from os import listdir
import GridSystem as grid
from PIL import Image, ImageFilter, ImageEnhance

scale = grid.diameter

class AnimatedSprite():
    def __init__(self, _path, _tickRate = 1, _obj = None, _scale = (0, 0), _loop = True):
        self.obj = _obj
        self.path = _path
        self.tickRate = _tickRate
        self.pointer = 0
        self.tick = 0
        self.canAnimate = True
        self.scale = _scale
        self.loop = _loop
        self.exitToAnimation = None
        self.randomizeOnEnd = False
        self.orientation = (0, -1)

        #Load Sprites
        self.sprites = []
        spriteFiles = sorted(os.listdir(resource_path("Sprites/" + self.path)))
        for sprite in spriteFiles:
            if(sprite.endswith(".png")):
                self.sprites.append(Loader(self.path + sprite, self.scale))
        self.curSprite = self.sprites[self.pointer]
    
    def Update(self):
        if(not self.canAnimate): return
        self.tick += 1
        if(self.tick >= self.tickRate):
            if(self.obj != None):
                self.CorrectSpriteRotation()

            self.tick = 0
            self.pointer += 1
            if(self.pointer >= len(self.sprites)):
                if(self.loop):
                    self.pointer = 0
                    if(self.randomizeOnEnd):
                        self.RandomizeSprites()

                else:
                    import GameObjects as gObj
                    self.obj.animatedSprite = self.exitToAnimation
                    gObj.animations.remove(self)
                    gObj.animations.append(self.exitToAnimation)
                    
            self.curSprite = self.sprites[self.pointer]
    
    def CorrectSpriteRotation(self):
        import GameObjects as gObj
        targetOrientation = self.obj.orientation
        if(self.orientation != targetOrientation):
            angle = gObj.GetAngleFromVector(self.orientation, targetOrientation)
            self.obj.UpdateSpriteRotation(angle)

    
    def RandomizeSprites(self):
        random.shuffle(self.sprites)
        self.curSprite = self.sprites[self.pointer]

    def SetRandomPointer(self):
        self.pointer = random.choice([0, len(self.sprites)-1])

def Loader(path, _scale = (0, 0)):
    global scale
    if(_scale == (0, 0)):
        _scale = (scale, scale)
    path = resource_path("Sprites/" + path)
    image = pygame.image.load(path).convert_alpha()  # Use convert_alpha() for better quality
    scaledImage = pygame.transform.smoothscale(image, _scale)

    pil_image = pygame_to_pil(scaledImage)
       # Enhance color saturation to make the image more vibrant
    enhancer = ImageEnhance.Color(pil_image)
    pil_image = enhancer.enhance(1.5)  # Increase the factor to make it more vibrant
    #pil_image = pil_image.filter(ImageFilter.SHARPEN)
    #pil_image = pil_image.filter(ImageFilter.CONTOUR)
    #pil_image = pil_image.filter(ImageFilter.EDGE_ENHANCE)
    pil_image = pil_image.filter(ImageFilter.DETAIL)
    scaledImage = pil_to_pygame(pil_image)

    return scaledImage

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

def pygame_to_pil(image):
    """Convert a Pygame surface to a PIL image"""
    return Image.frombytes("RGBA", image.get_size(), pygame.image.tostring(image, "RGBA", False))

def pil_to_pygame(image):
    """Convert a PIL image to a Pygame surface"""
    return pygame.image.fromstring(image.tobytes(), image.size, image.mode)

#!Testing
Test_120x120 = Loader("Test/test_120x120.png")
Test_240x240 = Loader("Test/test_240x240.png")
Test_50x50 = Loader("Test/test_50x50.png")

test_Background = Loader("Test/Background.png", (grid.size, grid.size))

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
