import GameObjects as gObj

class Base(gObj.DynObj):
    def __init__(self, _health, _blocksFromDir, _position, _orientation, _scale, _sprite, _target = 0):
        super.__init__(_position, _orientation, _scale, _sprite, _target)
        self.health = _health
        self.blocksFromDir = _blocksFromDir
    def Death():
        pass

def DoDamage(base, other, damage):
    if(CannotBlockAttack(base, other)):
        base.health -= damage
    if(base.health <= 0): base.Death()
    
def CannotBlockAttack(base, other):
    vec = gObj.VecMult(gObj.NormalOfVec(gObj.VecSum(base.position, other.position)), -1)
    for blockDir in base.blocksFromDir:
        if(blockDir == vec): return False
    return True


