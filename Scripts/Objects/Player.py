import math
import GameObjects as gObj
import pygame

grid = gObj.grid
func = 0
speed = 15 #!should be between 0 and 100
minValue = 1/10**2
timesDamaged = 0

class Player:
    #!Creating PlayerObj
    def __init__(self, _scale):
        self.scale = _scale
        self.parts = []
        self.InitBody()
        colScale = self.scale/2
        self.canMove = True
        self.health = 9
        self.damageDelay = 0
        self.enemyHitDelay = 0

    def InitBody(self):
        #Init body
        bodyLength = 4
        orientation = (0, -1)

        #Make parts
        head = gObj.DynObj(grid.centerPos, orientation, self.scale, self.SetSprite("Head"), grid.centerPos)
        bodies = []
        bodies.append(gObj.DynObj(gObj.VecSum(head.position, (0, self.scale)), orientation, self.scale, self.SetSprite("Body"), head.position))
        for i in range(1, bodyLength-2):
            bodies.append(gObj.DynObj(gObj.VecSum(bodies[i-1].position, (0, self.scale)), orientation, self.scale, self.SetSprite("Body"), bodies[i-1].position))

        tail = gObj.DynObj(gObj.VecSum(bodies[-1].position, (0, self.scale)), orientation, self.scale, self.SetSprite("Tail"), bodies[-1].position)

        #Add parts
        self.GetForwardTarget(head)
        self.parts.append(head)
        for body in bodies:
            self.parts.append(body)
        self.parts.append(tail)

    #!Logic
    def Movement(self):
        if(not self.canMove or self.parts[0].position == self.parts[0].target): return
        #func defines the fraction of movement
        global func; speed
        if(func == 0): func = minValue
        func = gObj.AddFunc(func, speed/100)
        #func += gObj.SmoothFunc(0.15)

        #Reset movement
        if(func > 1): self.WrapUpMovement(); return
        for part in self.parts:
            targetVec = gObj.VecMult(
                gObj.VecSum(part.target, gObj.VecMult(part.prePos, -1)), 
                func)
            part.UpdatePosition(gObj.VecSum(targetVec, part.prePos))

    def Input(self, event):
        global timesDamaged
        head = self.parts[0]
        orientation = head.orientation
        changedOrientation = False
        #Changing orientation if possible
        key = event.key
        if key in [pygame.K_LEFT, pygame.K_a]:
            orientation = (-1, 0); changedOrientation = True
        elif key in [pygame.K_RIGHT, pygame.K_d]:
            orientation = (1, 0); changedOrientation = True
        elif key in [pygame.K_UP, pygame.K_w]:
            orientation = (0, -1); changedOrientation = True
        elif key in [pygame.K_DOWN, pygame.K_s]:
            orientation = (0, 1); changedOrientation = True
        #Check if the player is trying to move backwards
        if(self.parts[1].orientation == gObj.VecMult(orientation, -1)): return
        if(changedOrientation and head.orientation != orientation and timesDamaged >= 1):
            self.WaitForInput()
            timesDamaged = 0
        if(not self.canMove and changedOrientation): self.WaitForInput(False)

        if(changedOrientation):
            head.UpdateOrientation(orientation)
            self.Movement()
            if(head.position == head.target):
                self.SetTargets()

    def SnapParts(self):
        for part in self.parts:
                grid.SnapToGrid(part, part.position)

    def SetTargets(self):
        head = self.parts[0]
        self.GetForwardTarget(head)
        #!Collided with unwalkable node
        if(head.position == head.target and self.damageDelay<=0): 
            self.damageDelay = 5
            return
        #!Collided with enemy
        for enemy in gObj.enemies:
            if(grid.NodeFromPos(enemy.position).position == head.target):
                self.enemyHitDelay = 1
        #?Set target for rest of the body parts
        for i in range(len(self.parts[1:]), 0, -1):
            self.parts[i].target = grid.NodeFromPos(self.parts[i-1].position).position
            self.parts[i].UpdateOrientation(self.parts[i-1].orientation)

    def GetForwardTarget(self, obj, raw = False):
        target = grid.NodeFromPos(gObj.VecSum(gObj.VecMult(obj.orientation, obj.scale), obj.position))
        #get Raw targetPosition
        if(raw): return target
        selfCollision = False
        for part in self.parts[1:]:
            if(target == grid.NodeFromPos(part.position)):
                selfCollision = True
        if(target.walkable == False or selfCollision): target = obj; 
        obj.target = target.position

    def ExtendBody(self):
        self.Movement()
        func = 1
        tail = self.parts[-1]
        body = gObj.DynObj(tail.position, self.parts[-2].orientation, self.scale, self.SetSprite("Body"), self.parts[-2].position)
        self.parts.insert(-1, body)
        tail.target = body.position

    def WaitForInput(self, do = True):
        if(do): self.canMove = False
        elif(not do): self.canMove = True; self.WrapUpMovement()

    def WrapUpMovement(self):
        global func
        head = self.parts[0]
        #set the part at target position to resolve errors
        for part in self.parts: 
            part.UpdatePosition(grid.NodeFromPos(part.target).position) 
            part.prePos = part.position
        self.SetTargets()
        func = 0

    def Collision(self):
        target = self.GetForwardTarget(self.parts[0], True)
        for part in self.parts[1:]:
            if(grid.NodeFromPos(part.position) == target):
                self.RemoveParts(self.parts.index(part))
                break
        self.TakeDamage()
    
    def TakeDamage(self):
        global timesDamaged
        if(timesDamaged >= 1): return
        self.health -= 1
        self.WaitForInput()
        gObj.trigger_screen_shake(10)
        timesDamaged += 1
    
    def RemoveParts(self, index):
        partsToRemove = []

        self.parts[-1].UpdatePosition(self.parts[index-1].position)
        self.parts[-1].target = self.parts[index-1].position
        for i in range(index-1, len(self.parts)-1):
            partsToRemove.append(self.parts[i])
        for part in partsToRemove:
            self.parts.remove(part)
    
    def SetSprite(self, name, tickRate = 30):
        return gObj.sprites.AnimatedSprite("Player/" + name + "/", tickRate)