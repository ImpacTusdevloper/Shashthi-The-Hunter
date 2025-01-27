import GameObjects as gObj
import pygame
import random

grid = gObj.grid
func = 0
baseSpeed = 9
 #!should be between 0 and 100

minValue = 1/10**2
timesDamaged = 0

class Player:
    #!Creating PlayerObj
    def __init__(self, _scale):
        self.scale = _scale
        self.parts = []
        self.canMove = True
        self.health = 9
        self.damageDelay = 0
        self.speed = baseSpeed
        self.defAnim = self.SetSprite("Head/Default")
        self.idleAnim = [self.SetSprite("Head/Blinking", 6), self.SetSprite("Head/LookAround", 4), self.SetSprite("Head/Yawn", 5)]
        self.InitBody()
        self.WrapUpMovement()
        #Init Idle Animations
        for anim in self.idleAnim:
            anim.loop = False
            anim.obj = self.parts[0]
            anim.exitToAnimation = self.defAnim

    def InitBody(self):
        #Init body
        bodyLength = 3
        orientation = (0, -1)

        #Make parts
        head = gObj.DynObj(grid.centerPos, orientation, self.scale*1.01, self.defAnim, grid.centerPos)
        bodies = []
        bodies.append(gObj.DynObj(gObj.VecSum(head.position, (0, self.scale)), orientation, self.scale, self.GetBodySprite(), head.position))
        for i in range(1, bodyLength-3):
            bodies.append(gObj.DynObj(gObj.VecSum(bodies[i-1].position, (0, self.scale)), orientation, self.scale, self.GetBodySprite(), bodies[i-1].position))
        #?Add Lower Body and tail
        bodies.append(gObj.DynObj(gObj.VecSum(bodies[-1].position, (0, self.scale)), orientation, self.scale, self.SetSprite("LBody"), bodies[-1].position))
        tail = gObj.DynObj(gObj.VecSum(bodies[-1].position, (0, self.scale)), orientation, self.scale, self.SetSprite("Tail", 5), bodies[-1].position)

        #Add parts
        self.GetForwardTarget(obj=head)
        self.parts.append(head)
        for body in bodies:
            self.parts.append(body)
        self.parts.append(tail)

    #!Logic
    def Movement(self):
        if(not self.canMove or self.parts[0].position == self.parts[0].target): return
        #func defines the fraction of movement
        global func; baseSpeed
        #?Calculating speed based on bodyLength and health
        self.speed = baseSpeed + len(self.parts)/5 + (9-self.health)/4
        #Rounding to 2 decimals
        self.speed = int(self.speed*100)/100
        if(func == 0): func = minValue
        func = gObj.AddFunc(func, self.speed/100)
        #Rounding to 2 decimals
        func = int(func*100)/100
        #Reset movement
        if(func >= 1): self.WrapUpMovement(); return
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
            if(head.position == head.target):
                self.SetTargets()

    def SnapParts(self):
        for part in self.parts:
                pos = part.position
                grid.SnapToGrid(part, pos)

    def SetTargets(self):
        head = self.parts[0]
        self.GetForwardTarget()
        #!Collided with unwalkable node
        if(head.position == head.target and self.damageDelay<=0): 
            self.damageDelay = 5
            return
        #!Collided with enemy
        for enemy in gObj.enemies:
            if(grid.NodeFromPos(enemy.position).position == head.target):
                enemy.TakeDamage()
        #?Set target for rest of the body parts
        for i in range(len(self.parts[1:]), 0, -1):
            self.parts[i].target = grid.NodeFromPos(self.parts[i-1].position).position
            self.parts[i].UpdateOrientation(self.parts[i-1].orientation)

    def GetForwardTarget(self, raw = False, obj = None):
        if(obj == None):
            head = self.parts[0]
        else: head = obj
        target = grid.NodeFromPos(gObj.VecSum(gObj.VecMult(head.orientation, head.scale), head.position))
        #get Raw targetPosition
        if(raw): return target
        selfCollision = False
        for part in self.parts[1:-1]:
            if(target == grid.NodeFromPos(part.position)):
                selfCollision = True
        if(target.walkable == False or selfCollision): target = head; 
        head.target = target.position

    def WaitForInput(self, do = True):
        if(do): self.canMove = False
        elif(not do):
            self.canMove = True
            #gObj.SmoothZoom(1.5, 1, 0.05)
            self.WrapUpMovement()

    def WrapUpMovement(self):
        global func
        #set the part at position to resolve errors
        self.SnapParts()
        for part in self.parts: 
            part.prePos = part.position
        self.SetTargets()
        func = 0

    def Collision(self):
        target = self.GetForwardTarget(True)
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

    def ExtendBody(self):
        func = 1
        tail = self.parts[-1]
        body = gObj.DynObj(self.parts[-3].position, self.parts[-3].orientation, self.scale, self.GetBodySprite(), self.parts[-3].position)
        self.parts.insert(-2, body)
        tail.UpdatePosition(self.parts[-2].prePos)
        tail.target = self.parts[-2].position
        gObj.score += 1
        gObj.update_high_score()
    
    def RemoveParts(self, index):
        partsToRemove = []
        for i in range(index-1, len(self.parts)-2):
            partsToRemove.append(self.parts[i])
        if(index in [0, 1]): return
        self.SetPartEqualTo(-2, index-1)
        self.SetPartEqualTo(-1, index)
        for part in partsToRemove:
            self.parts.remove(part)
    
    def SetPartEqualTo(self, ind1, ind2):
        self.parts[ind1].UpdatePosition(self.parts[ind2].position)
        self.parts[ind1].UpdateOrientation(self.parts[ind2].orientation)
        self.parts[ind1].target = self.parts[ind2].position
    
    #!Animation Logic
    def SetSprite(self, name, tickRate = 30, loop = True):
        return gObj.sprites.AnimatedSprite("Player/" + name + "/", tickRate, _loop = loop, _scale = (self.scale, self.scale))
    
    def SwitchToIdleAnim(self):
        head = self.parts[0]
        anim = random.choice(self.idleAnim)
        anim.pointer = 0
        gObj.animations.remove(head.animatedSprite)
        head.animatedSprite = anim
        gObj.animations.append(anim)
    
    def GetBodySprite(self):
        sprite = self.SetSprite("Body", 30)
        sprite.randomizeOnEnd = True
        sprite.SetRandomPointer()
        return sprite       