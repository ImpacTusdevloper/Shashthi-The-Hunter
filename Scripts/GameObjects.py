import pygame, random, math, json, os
import GridSystem as grid
import SpriteLoader as sprites

#GameObjects
enemies = []
animations = []
specialFx = []
boundaries = []
infoSprite = sprites.Loader("Info.png", (grid.size, grid.size))
infoSprite.set_alpha(240)
#Screen shake parameters
shake_duration = 0
shake_intensity = 8
shake_x = 0
shake_y = 0
#Zoom parameters
zoom_factor = 1.49
target_zoom_in = 1.5
target_zoom_out = 1.0
zoom_speed = 0.01
zoom_in = False
zoom_triggered = False
#Directional vectors
lFRB = [(-1, 0), (0, -1), (1, 0), (0, 1)]

score = 0
fixedTime = 0

HIGH_SCORE_FILE = sprites.resourcePath("Data/high_score.json")
highScore = 0

#!Classes
class StaticObj:
    def __init__(self, _position, _scale, _sprite = None):
        self.position = _position
        self.scale = _scale
        self.sprite = _sprite
        self.wPosition = VecSum(self.position, (-self.scale/2, -self.scale/2))
        self.rect = pygame.Rect(self.wPosition[0], self.wPosition[1], self.scale, self.scale)
        node = grid.NodeFromPos(self.position)

class DynObj:
    def __init__(self, _position, _orientation, _scale, _animatedSprite = None, _target = (0, 0)):
        self.position = _position
        self.orientation = _orientation
        self.scale = _scale
        self.target = _target
        self.wPosition = VecSum(self.position, (-self.scale/2, -self.scale/2))
        self.prePos = self.position
        self.rect = pygame.Rect(self.wPosition[0], self.wPosition[1], self.scale, self.scale)
        self.UpdatePosition(self.position)
        self.animatedSprite = _animatedSprite
        self.animatedSprite.obj = self
        self.animatedSprite.scale = self.scale
        animations.append(self.animatedSprite)

    def UpdatePosition(self, pos):
        self.position = pos
        self.wPosition = VecSum(self.position, (-self.scale/2, -self.scale/2))
        self.rect.center = self.position

    def UpdateOrientation(self, orientation, forced = False):
        #?No change in orientation
        if(self.orientation == orientation and not forced): return
        angle = GetAngleFromVector(self.orientation, orientation)
        self.orientation = orientation
        self.UpdateSpriteRotation(angle)
    
    def UpdateSpriteRotation(self, angle):
        tmp = []
        for sprite in self.animatedSprite.sprites:
            tmp.append(pygame.transform.rotate(sprite, angle))
        self.animatedSprite.sprites = tmp
        self.animatedSprite.orientation = self.orientation
        self.animatedSprite.curSprite = self.animatedSprite.sprites[self.animatedSprite.pointer]
        self.rect = self.animatedSprite.curSprite.get_rect(center=self.rect.center)

import Objects.EnemyBase as enemy
class SpawnEnemies():
    def SpawnRandEnemy():
        num = random.choice([0, 1, 2])
        enemyType={
            0: SpawnEnemies.LadyBug,
            1: SpawnEnemies.Fly,
            2: SpawnEnemies.Spider
        }
        enemyType[num]()
    def LadyBug():
        ladyBug = enemy.LadyBug((0, 0), lFRB[1], grid.diameter)
        enemies.append(ladyBug)
    def Fly():
        fly = enemy.Fly((0, 0), lFRB[1], grid.diameter)
        enemies.append(fly)
    def Spider():
        spider = enemy.Spider((0, 0), lFRB[1], grid.diameter)
        enemies.append(spider)


#!Functions
def CreatePlayer():
    import Objects.Player as pObj
    return pObj.Player(grid.diameter * 1.02)

def CreateBoundaries():
    for node in grid.nodes:
        ind = node.index; maxInd = int(grid.size/grid.diameter)-1
        if ind[0] in [0, maxInd] or ind[1] in [0, maxInd]:
            grid.notWalkable.add(node)
            node.walkable = False
            boundaries.append(StaticObj(node.position, grid.diameter))

#?screen shake functions
def apply_screen_shake(deltaTime):
    global shake_duration, shake_x, shake_y
    if shake_duration > 0:
        shake_duration -= 1 * deltaTime/10
        _shake_x = random.randint(-shake_intensity, shake_intensity)
        _shake_y = random.randint(-shake_intensity, shake_intensity)
        shake_x, shake_y = _shake_x, _shake_y
    elif(shake_duration < 0):
        shake_x, shake_y =  0, 0

def trigger_screen_shake(duration, intensity = 8):
    global shake_duration, shake_intensity
    shake_intensity = intensity
    shake_duration = duration
#?Zoom functions
def SmoothZoom(target_in=1.1, target_out=1.0, speed=0.5):
    global target_zoom_in, target_zoom_out, zoom_speed, zoom_in, zoom_triggered
    target_zoom_in = target_in
    target_zoom_out = target_out
    zoom_speed = speed
    zoom_in = True  # Start by zooming in
    zoom_triggered = True  # Set the zoom trigger

def UpdateZoom(deltaTime):
    global zoom_factor, target_zoom_in, target_zoom_out, zoom_speed, zoom_in, zoom_triggered
    if not zoom_triggered:
        return  # Do nothing if zoom is not triggered

    zoom_change = zoom_speed * deltaTime

    if zoom_in:
        if zoom_factor < target_zoom_in:
            zoom_factor += zoom_change
            if zoom_factor >= target_zoom_in:
                zoom_factor = target_zoom_in
                zoom_in = False  # Switch to zooming out
    else:
        if zoom_factor > target_zoom_out:
            zoom_factor -= zoom_change
            if zoom_factor <= target_zoom_out:
                zoom_factor = target_zoom_out
                zoom_triggered = False  # Stop zooming once original position is reached

def ScaleSpriteToZoom(sprite):
    scaled_sprite = pygame.transform.scale(sprite, (int(sprite.get_width() * zoom_factor), int(sprite.get_height() * zoom_factor)))
    offset_x = (scaled_sprite.get_width() - sprite.get_width()) // 2
    offset_y = (scaled_sprite.get_height() - sprite.get_height()) // 2
    return scaled_sprite, offset_x, offset_y

#?High score functions
def load_high_score():
    if os.path.exists(HIGH_SCORE_FILE):
        with open(HIGH_SCORE_FILE, "r") as file:
            data = json.load(file)
            return data.get("high_score", 0)
    return 0

def save_high_score(high_score):
    with open(HIGH_SCORE_FILE, "w") as file:
        json.dump({"high_score": high_score}, file)

def update_high_score():
    global highScore
    high_score = highScore
    if score > high_score:
        save_high_score(score)
        highScore = score
        return
    highScore = high_score 

#!Mathematical functions
def GetAngleFromVector(init, target):
        x = target[1]*init[0] - target[0]*init[1]
        y = target[0]*init[0] + target[1]*init[1]
        angle = -math.degrees(math.atan2(x, y))
        return angle

def AddFunc(x, const):
     return x + const

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