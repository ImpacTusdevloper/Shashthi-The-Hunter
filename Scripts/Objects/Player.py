import math
import GameObjects as gObj
import pygame

grid = gObj.grid
func = 0
speed = 20 #!should be between 0 and 100
minValue = 1/10**2

class Player:
    def __init__(self, _scale):
        self.scale = _scale
        self.parts = []
        self.InitBody()
        colScale = self.scale/2
        self.canMove = True
        self.health = 9
        self.collider = pygame.Rect(0, 0, colScale, colScale)

    def InitBody(self):
        #Init body
        bodyLength = 4
        orientation = (0, -1)
        sprites = gObj.sprites

        #Make parts
        head = gObj.DynObj(grid.centerPos, orientation, self.scale, sprites.test_Head)
        bodies = []
        bodies.append(gObj.DynObj(gObj.VecSum(head.position, (0, self.scale)), orientation, self.scale, sprites.test_Body_Dotted, head.position))
        for i in range(1, bodyLength-2):
            bodies.append(gObj.DynObj(gObj.VecSum(bodies[i-1].position, (0, self.scale)), orientation, self.scale, sprites.test_Body_Solid, bodies[i-1].position))

        tail = gObj.DynObj(gObj.VecSum(bodies[-1].position, (0, self.scale)), orientation, self.scale, sprites.test_Tail, bodies[-1].position)

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
        head = self.parts[0]
        orientation = head.orientation
        changedOrientation = False
        #Changing orientation if possible
        if(event.key == pygame.K_LEFT):
            orientation = (-1, 0); changedOrientation = True
        elif(event.key == pygame.K_RIGHT):
            orientation = (1, 0); changedOrientation = True
        if(event.key == pygame.K_UP):
            orientation = (0, -1); changedOrientation = True
        elif(event.key == pygame.K_DOWN):
            orientation = (0, 1); changedOrientation = True
        #Check if the player is trying to move backwards
        if(self.parts[1].orientation == gObj.VecMult(orientation, -1)): return

        if(changedOrientation):
            head.UpdateOrientation(orientation)
            self.Movement()

    
    def SnapParts(self):
        for part in self.parts:
                grid.SnapToGrid(part, part.position)

    def SetTargets(self):
        head = self.parts[0]
        self.SetTargetToForward(head)
        #!Collided with unwalkable node
        if(head.position == head.target): self.Collision(); return
        #Set target for rest of the body parts
        for i in range(len(self.parts[1:]), 0, -1):
            self.parts[i].target = grid.NodeFromPos(self.parts[i-1].position).position
            self.parts[i].UpdateOrientation(self.parts[i-1].orientation)
        #Updating grid conditions
        grid.NodeFromPos(head.prePos).walkable = False
        grid.NodeFromPos(self.parts[-1].prePos).walkable = True

    def SetTargetToForward(self, obj, raw = False):
        target = grid.NodeFromPos(gObj.VecSum(gObj.VecMult(obj.orientation, obj.scale), obj.position))
        #get Raw targetposition
        if(raw): return target
        if(target.walkable == False): target = obj; 
        obj.target = target.position

    def ExtendBody(self):
        self.Movement()
        func = 1
        tail = self.parts[-1]
        body = gObj.DynObj(tail.position, self.parts[-2].orientation, self.scale, gObj.sprites.test_Body_Solid, self.parts[-2].position)
        self.parts.insert(-1, body)
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
        head = self.parts[0]
        #set the part at target position to resolve errors
        for part in self.parts: 
            part.UpdatePosition(grid.NodeFromPos(part.target).position) 
            part.prePos = part.position
        self.SetTargets()
        func = 0

    def Collision(self):
        target = self.SetTargetToForward(self.parts[0], True)
        for part in self.parts[1:]:
            if(grid.NodeFromPos(part.position) == target):
                self.RemoveParts(self.parts.index(part))
                break
        self.TakeDamage()

    def TakeDamage(self):
        self.health -= 1
        self.WaitForInput()
        gObj.trigger_screen_shake(10)
    
    def RemoveParts(self, index):
        partsToRemove = []
        grid.NodeFromPos(self.parts[-1].position).walkable = True
        self.parts[-1].UpdatePosition(self.parts[index-1].position)
        self.parts[-1].target = self.parts[index-1].position
        for i in range(index-1, len(self.parts)-1):
            grid.NodeFromPos(self.parts[i].position).walkable = True
            partsToRemove.append(self.parts[i])
        for part in partsToRemove:
            self.parts.remove(part)