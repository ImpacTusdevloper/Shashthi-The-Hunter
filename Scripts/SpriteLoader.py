import pygame, os, sys, random
import numpy as np
import GridSystem as grid
from PIL import Image, ImageFilter

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
        spriteFiles = sorted(os.listdir(resourcePath("Data/Sprites/" + self.path)))
        for sprite in spriteFiles:
            if(sprite.endswith(".png")):
                self.sprites.append(Loader(self.path + sprite, self.scale))
        self.curSprite = self.sprites[self.pointer]
    
    def Update(self):
        if(not self.canAnimate): return
        if(self.obj != None):
            self.CorrectSpriteRotation()
        if(len(self.sprites) <=1):
            return
        self.tick += 1
        if(self.tick >= self.tickRate):

            self.tick = 0
            self.pointer += 1
            if(self.pointer >= len(self.sprites)):
                if(self.loop):
                    self.pointer = 0
                    if(self.randomizeOnEnd):
                        self.RandomizeSprites()
                else:
                    import GameObjects as gObj
                    self.pointer -= 1
                    if(self in gObj.animations):
                        gObj.animations.remove(self)
                    if(self.exitToAnimation != None):
                        if(self.obj != None):
                            self.obj.animatedSprite = self.exitToAnimation
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

import GameObjects as gObj
class SpecialEffect(AnimatedSprite):
    def __init__(self, _path, _pos, _tickRate=1, _scale=(0, 0), _loop=False):
        super().__init__(_path, _tickRate, _scale=_scale, _loop=_loop)
        self.pos = _pos
    def Update(self):
        if(self.pointer >= len(self.sprites)-1):
            gObj.specialFx.remove(self)
            gObj.animations.remove(self)
        return super().Update()

def Loader(path, _scale = (0, 0)):
    global scale
    if(_scale == (0, 0)):
        _scale = (scale, scale)
    path = resourcePath("Data/Sprites/" + path)
    image = pygame.image.load(path).convert_alpha()  # Use convert_alpha() for better quality
    scaledImage = pygame.transform.smoothscale(image, _scale)

    pil_image = pygame_to_pil(scaledImage)
    #pil_image = apply_bloom_effect(pil_image)
    # Apply chromatic aberration effect
    pil_image = apply_all_effects(pil_image)
    pil_image = pil_image.filter(ImageFilter.DETAIL)
    scaledImage = pil_to_pygame(pil_image)

    return scaledImage

def resourcePath(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, *relative_path.split("/"))

#?Effects
def apply_all_effects(image, offset=0.6):
    # Create a mask from the alpha channel
    alpha = image.split()[-1]
    
    # Apply chromatic aberration effect
    eImage = apply_chromatic_aberration(image, offset)
    # Apply grain effect with larger grain size and cyberpunkish color tint
    eImage = apply_grain_effect(eImage, intensity=0.02, grain_size=3)
    
    
    # Combine the effects with the original image using the alpha mask
    combined_image = Image.composite(eImage, image, alpha)
    
    return combined_image

def apply_chromatic_aberration(image, offset=0.6):
    # Split the image into red, green, and blue channels
    r, g, b, a = image.split()
    # Offset the red channel
    r = r.transform(image.size, Image.AFFINE, (1, 0, offset, 0, 1, 0))
    # Offset the blue channel in the opposite direction
    b = b.transform(image.size, Image.AFFINE, (1, 0, -offset, 0, 1, 0))
    # Merge the channels back together
    image = Image.merge('RGBA', (r, g, b, a))

    return image

def generate_noise(width, height, intensity=0.2, grain_size=4):
    """
    Generate random noise.
    
    :param width: Width of the image
    :param height: Height of the image
    :param intensity: Intensity of the noise
    :param grain_size: Size of the grain effect
    :return: Noise image
    """
    noise = np.random.normal(0, 255 * intensity, (height // grain_size, width // grain_size, 4)).astype(np.uint8)
    noise_image = Image.fromarray(noise, 'RGBA')
    noise_image = noise_image.resize((width, height), resample=Image.NEAREST)
    return noise_image

def apply_grain_effect(image, intensity=0.2, grain_size=4):
    """
    Apply a grain effect to an image while preserving transparency.
    
    :param image: PIL.Image object
    :param intensity: Intensity of the grain effect
    :param grain_size: Size of the grain effect
    :return: PIL.Image object with grain effect applied
    """
    width, height = image.size
    noise_image = generate_noise(width, height, intensity, grain_size)
    
    # Split the original image into RGB and alpha channels
    r, g, b, a = image.split()
    
    # Split the noise image into RGB and alpha channels
    nr, ng, nb, na = noise_image.split()
    
    # Blend the RGB channels of the original image and the noise image
    blended_r = Image.blend(r, nr, intensity)
    blended_g = Image.blend(g, ng, intensity)
    blended_b = Image.blend(b, nb, intensity)
    
    # Combine the blended RGB channels with the original alpha channel
    grain_image = Image.merge('RGBA', (blended_r, blended_g, blended_b, a))
    
    return grain_image

#?Conversion
def pygame_to_pil(image):
    """Convert a Pygame surface to a PIL image"""
    return Image.frombytes("RGBA", image.get_size(), pygame.image.tostring(image, "RGBA", False))

def pil_to_pygame(image):
    """Convert a PIL image to a Pygame surface"""
    if image.mode != "RGBA":
        image = image.convert("RGBA")
    return pygame.image.fromstring(image.tobytes(), image.size, image.mode)

#!Testing
'''Test_120x120 = Loader("Test/test_120x120.png")
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
'''