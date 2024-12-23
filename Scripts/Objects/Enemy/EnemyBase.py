import GameObjects as gObj

class Base(gObj.DynObj):
    def __init__(self, _position, _orientation, _scale, _sprite, _target = (0, 0)):
        super().__init__(_position, _orientation, _scale, _sprite, _target)
        self.collider = gObj.pygame.Rect(self.wPosition[0], self.wPosition[1], self.scale, self.scale)
        
    def Death():
        pass

    def DoDamage(self, other, damage = 1):
        if(self.CannotBlockAttack(self, other)):
            self.health -= damage
        if(self.health <= 0): self.Death(); gObj.player.ExtendBody()

    def CannotBlockAttack(self, other):
        vec = gObj.VecMult(gObj.NormalOfVec(gObj.VecSum(self.position, other.position)), -1)
        for blockDir in self.blocksFromDir:
            if(blockDir == vec): return False
        return True


class LadyBug(Base):
    def __init__(self, _position, _orientation, _scale, _sprite = None, _target=(0, 0)):
        _sprite = gObj.sprites.testR
        super().__init__( _position, _orientation, _scale, _sprite, _target)