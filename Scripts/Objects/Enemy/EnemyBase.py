import GameObjects as gObj

grid = gObj.grid
random = gObj.random
lFRB = gObj.lFRB

class Base(gObj.DynObj):
    def __init__(self, _position, _orientation, _scale, _sprite, _target = (0, 0)):
        super().__init__(_position, _orientation, _scale, _sprite, _target)
        self.pointer = 1
        self.blocksFromDir = [0, 0]
        self.health = 1
        
    def Move(self):
        self.UpdatePosition(grid.GetRandAvailNode().position)
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
        

class LadyBug(Base):
    def __init__(self, _position, _orientation, _scale, _sprite = None, _target=(0, 0)):
        _sprite = gObj.sprites.test_Head
        super().__init__( _position, _orientation, _scale, _sprite, _target)
        self.health = 2
        self.blocksFromDir = [gObj.lFRB[3], gObj.lFRB[0], gObj.lFRB[2]]
        self.Move()