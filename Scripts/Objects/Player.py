import math
import GameObjects as gObj
import pygame

grid = gObj.grid
func = 0
minValue = 1/10**2

class Player:
    def __init__(self, _scale):
        self.scale = _scale
        self.parts = []
        self.InitBody()
        colScale = self.scale/2
        self.collider = pygame.Rect(0, 0, colScale, colScale)
        self.canMove = True
        self.health = 3

    def InitBody(self):
        #Init body
        bodyLength = 4
        orientation = (0, -1)
        sprite = gObj.sprites.test03

        #Make parts
        head = gObj.DynObj(grid.centerPos, orientation, self.scale, sprite)
        bodies = []
        bodies.append(gObj.DynObj(gObj.VecSum(head.position, (0, self.scale)), orientation, self.scale, sprite, head.position))
        for i in range(1, bodyLength-2):
            bodies.append(gObj.DynObj(gObj.VecSum(bodies[i-1].position, (0, self.scale)), orientation, self.scale, sprite, bodies[i-1].position))

        tail = gObj.DynObj(gObj.VecSum(bodies[-1].position, (0, self.scale)), orientation, self.scale, sprite, bodies[-1].position)

        #Add parts
        self.SetTargetToForward(head)
        self.parts.append(head)
        for body in bodies:
            self.parts.append(body)
        self.parts.append(tail)

        for part in self.parts:
            grid.NodeFromPos(part.position).walkable = False
        grid.NodeFromPos(self.parts[-1].position).walkable = True

    def Movement(self):
        if(not self.canMove or self.parts[0].position == self.parts[0].target): return
        #func defines the fraction of movement
        global func
        if(func == 0): func = minValue
        func = gObj.AddFunc(func, 0.15)
        #func += gObj.SmoothFunc(0.15)

        #Reset movement
        if(func > 1): self.WrapUpMovement(); return
        for part in self.parts:
            targetVec = gObj.VecMult(
                gObj.VecSum(part.target, gObj.VecMult(part.prePos, -1)), 
                func)
            part.UpdatePosition(gObj.VecSum(targetVec, part.prePos))

    def Input(self, event):
        head = self.parts[0]
        orientation = head.orientation
        changedOrientation = False
        #Changing orientation if possible
        if(orientation[0] == 0):
            if(event.key == pygame.K_LEFT):
                orientation = (-1, 0); changedOrientation = True
            elif(event.key == pygame.K_RIGHT):
                orientation = (1, 0); changedOrientation = True
        elif(orientation[1] == 0):
            if(event.key == pygame.K_UP):
                orientation = (0, -1); changedOrientation = True
            elif(event.key == pygame.K_DOWN):
                orientation = (0, 1); changedOrientation = True

        if(changedOrientation):
            self.Movement()
            head.orientation = orientation
    
    def SnapParts(self):
        for part in self.parts:
                grid.SnapToGrid(part, part.position)

    def SetTargets(self):
        #Set target for rest of the body parts
        for i in range(len(self.parts[1:]), 0, -1):
            self.parts[i].target = self.parts[i-1].target
        #Set target for head
        head = self.parts[0]
        self.SetTargetToForward(head)
        #Updating grid conditions
        grid.NodeFromPos(head.prePos).walkable = False
        grid.NodeFromPos(self.parts[-1].prePos).walkable = True

    def SetTargetToForward(self, obj):
        target = grid.NodeFromPos(gObj.VecSum(gObj.VecMult(obj.orientation, obj.scale), obj.position))
        #!Collided with unwalkable node
        if(target.walkable == False): target = obj; self.TakeDamage()
        obj.target = target.position
    def ExtendBody(self):
        func = 1
        self.Movement()
        tail = self.parts[-1]
        body = gObj.DynObj(tail.position, self.parts[-2].orientation, self.scale, tail.sprite, self.parts[-2].position)
        self.parts.insert(-2, body)
        tail.target = body.position

    def UpdateCollider(self):
        head = self.parts[0]
        pos = gObj.VecSum(head.position, gObj.VecMult(head.orientation, head.scale/3))
        self.collider.center = pos

    def WaitForInput(self, do = True):
        if(do): self.canMove = False
        elif(not do): self.canMove = True; self.WrapUpMovement()

    def WrapUpMovement(self):
        global func
        #set the part at target position to resolve errors
        for part in self.parts: 
            part.UpdatePosition(part.target)
            part.prePos = part.position
        self.SetTargets(); func = 0
    def TakeDamage(self):
        self.health -= 1
        self.WaitForInput()