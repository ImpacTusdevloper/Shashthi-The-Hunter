import GameObjects as gObj

grid = gObj.grid
random = gObj.random
lFRB = gObj.lFRB
sprites = gObj.sprites

class Base(gObj.DynObj):
    def __init__(self, _position, _orientation, _scale, _animatedSprite):
        super().__init__(_position, _orientation, _scale, _animatedSprite)
        self.pointer = 1
        self.health = 1
        self.Move()
        
    def Move(self):
        tmp = set()
        tmp.add(gObj.player.parts[0].target)
        for enemy in gObj.enemies:
            tmp.add(grid.NodeFromPos(enemy.position))
        for part in gObj.player.parts:
            tmp.add(grid.NodeFromPos(part.position))
        self.UpdatePosition(grid.GetRandAvailNode(tmp).position)
        self.SetOrientation()

    def TakeDamage(self, damage = 1):
        if(self.CannotBlockAttack()):
            self.health -= damage
        else:
            effect = sprites.SpecialEffect("Cross/", self.wPosition, 3)
            gObj.animations.append(effect)
            gObj.specialFx.append(effect)
            
            self.Move()

        if(self.health <= 0): self.Death()
        self.Move()

    def Death(self):
        gObj.player.ExtendBody()
        gObj.enemies.remove(self)

    def CannotBlockAttack(self):
        playerHead = gObj.player.parts[0]
        vec = gObj.VecMult(playerHead.orientation, -1)
        for blockDir in self.blocksFromDir:
            if(blockDir == vec): return False
        return True

    def SetOrientation(self):
        allowed = []
        for dir in lFRB:
            if(grid.NodeFromPos(gObj.VecSum(self.position, gObj.VecMult(dir, self.scale))).walkable):
                allowed.append(dir)
        if(len(allowed) == 0): #SetAgain(recursive)
            self.Move(); return
        unBlocked = []
        for dir in lFRB:
            if(dir not in self.blocksFromDir): unBlocked.append(dir)
        #?Orientation = LFRB[pointer + index(target) - index(position)]
        ind = self.pointer + lFRB.index(random.choice(allowed)) - lFRB.index(random.choice(unBlocked))
        ind = ind if ind < 4 else ind-4
        ind = ind if ind >= 0 else ind+4
        tmp = []
        for dir in self.blocksFromDir:
            i = lFRB.index(dir) + ind - self.pointer
            if(i >= 4): i -= 4
            tmp.append(lFRB[i])
        self.blocksFromDir = tmp
        self.pointer = ind
        self.UpdateOrientation(lFRB[ind])
        
#!Enemy types
class LadyBug(Base):
    def __init__(self, _position, _orientation, _scale):
        self.normalSprite = sprites.AnimatedSprite("Enemies/LadyBugNormal/", 5, self)
        self.psychoSprite = sprites.AnimatedSprite("Enemies/LadyBugPsycho/", 2, self)
        #?Blocked from front
        self.blocksFromDir = [gObj.lFRB[1]]
        super().__init__(_position, _orientation, _scale, self.normalSprite)
        self.health = 3

    def TakeDamage(self, damage=1):
        super().TakeDamage(damage)
        if(self.health <= 1):
            gObj.animations.remove(self.animatedSprite)
            self.animatedSprite = self.psychoSprite
            gObj.animations.append(self.animatedSprite)
            self.blocksFromDir = []
            self.UpdateSpriteRotation(gObj.GetAngleFromVector(lFRB[0], random.choice(lFRB)))


class Fly(Base):
    def __init__(self, _position, _orientation, _scale):
        _animatedSprite = sprites.AnimatedSprite("Enemies/Fly/", 3, self)
        #?Blocked from left, right and back
        self.blocksFromDir = [gObj.lFRB[3], gObj.lFRB[0], gObj.lFRB[2]]
        super().__init__(_position, _orientation, _scale, _animatedSprite)
        self.health = 1

class Spider(Base):
    def __init__(self, _position, _orientation, _scale):
        _animatedSprite = sprites.AnimatedSprite("Enemies/Spider/", 8, self)
        #?Blocked from left and right
        self.blocksFromDir = [gObj.lFRB[1], gObj.lFRB[3]]
        super().__init__(_position, _orientation, _scale, _animatedSprite)
        self.health = 2