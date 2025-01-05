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
        for enemy in gObj.enemies:
            if(enemy != self): tmp.add(grid.NodeFromPos(enemy.position))
        self.UpdatePosition(grid.GetRandAvailNode(tmp).position)
        self.SetOrientation()

    def DoDamage(self, damage = 1):
        if(self.CannotBlockAttack()):
            self.health -= damage
        else:
            self.Move()

        if(self.health <= 0): self.Death()
        self.Move()

    def Death(self):
        grid.NodeFromPos(self.position).walkable = True
        gObj.player.ExtendBody()
        gObj.enemies.remove(self)

    def CannotBlockAttack(self):
        playerHead = gObj.player.parts[0]
        vec = gObj.VecMult(gObj.NormalOfVec(gObj.VecSum(self.position, playerHead.position, -1)), -1)
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
        _animatedSprite = sprites.AnimatedSprite("Enemies/LadyBug/", 1)
        #?Blocked from front
        self.blocksFromDir = [gObj.lFRB[1]]
        super().__init__(_position, _orientation, _scale, _animatedSprite)
        self.health = 3

class Fly(Base):
    def __init__(self, _position, _orientation, _scale):
        _animatedSprite = sprites.AnimatedSprite("Enemies/Fly/", 1)
        #?Blocked from left, right and back
        self.blocksFromDir = [gObj.lFRB[3], gObj.lFRB[0], gObj.lFRB[2]]
        super().__init__(_position, _orientation, _scale, _animatedSprite)
        self.health = 1

class Spider(Base):
    def __init__(self, _position, _orientation, _scale):
        _animatedSprite = sprites.AnimatedSprite("Enemeis/Spider/", 1)
        #?Blocked from left and right
        self.blocksFromDir = [gObj.lFRB[1], gObj.lFRB[3]]
        super().__init__(_position, _orientation, _scale, _animatedSprite)
        self.health = 2