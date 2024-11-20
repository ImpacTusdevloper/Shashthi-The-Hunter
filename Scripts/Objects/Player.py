import math
import GameObjects as gObj
import pygame
import Load as LoadSprite

grid = gObj.GridSystem
func = 0
minValue = 1/10**2

class Player:
    def __init__(self, _scale):
        self.scale = _scale
        self.parts = []
        bodyLength = 4
        #Init body
        orientation = [0, -1]
        sprite = LoadSprite.test

        #Make parts
        head = gObj.DynObj(grid.centerPos, orientation, self.scale, sprite)
        bodies = []
        bodies.append(gObj.DynObj(gObj.VecSum(head.position, (0, -1*self.scale)), orientation, self.scale, sprite, head.position))
        for i in range(1, bodyLength-2):
            bodies.append(gObj.DynObj(gObj.VecSum(bodies[i-1].position, (0, -1*self.scale)), orientation, self.scale, sprite, bodies[i-1].position))
        tail = gObj.DynObj(gObj.VecSum(bodies[len(bodies)-1].position, (0, -1*self.scale)), orientation, self.scale, sprite, bodies[len(bodies)-1].position)

        #Add parts
        self.SetTargetToForward(head)
        self.parts.append(head)
        for body in bodies:
            self.parts.append(body)
        self.parts.append(tail)


    def Movement(self):
        #func defines the fraction of movement
        global func
        if(self.parts[0].position == self.parts[0].target): return
        if(func == 0): func = minValue
        func = gObj.AddFunc(func, 0.2)
        #print(func)
        if(func > 1):
            #set the part at target position to resolve errors
            for part in self.parts: 
                part.UpdatePosition(part.target)
                part.refVec = 0
            self.SetTargets(); func = 0
            return
        for part in self.parts:
            if(part.refVec == 0): part.refVec = part.position
            targetVec = gObj.VecMult(
                gObj.VecSum(part.target, gObj.VecMult(part.position, -1)), 
                func)
            part.UpdatePosition(gObj.VecSum(targetVec, part.refVec))

    def Input(self, event):
        head = self.parts[0]
        orientation = head.orientation
        changedOrientation = False
        #Changing orientation if possible
        if(event.key == pygame.K_UP and orientation[1] == 0):
            orientation = (0, -1); changedOrientation = True
        elif(event.key == pygame.K_DOWN and orientation[1] == 0):
            orientation = (0, 1); changedOrientation = True
        elif(event.key == pygame.K_LEFT and orientation[0] == 0):
            orientation = (-1, 0); changedOrientation = True
        elif(event.key == pygame.K_RIGHT and orientation[0] == 0):
            orientation = (1, 0); changedOrientation = True

        if(changedOrientation):
            for part in self.parts:
                grid.SnapToGrid(part, part.target)
            self.SetTargets()
            head.orientation = orientation

    def SetTargets(self):
        #Set target for rest of the body parts
        for i in range(len(self.parts[1:]), 0, -1):
            self.parts[i].target = self.parts[i-1].target
        #Set target for head
        self.SetTargetToForward(self.parts[0])

    def SetTargetToForward(self, obj):
        obj.target = gObj.VecSum(gObj.VecMult(obj.orientation, obj.scale), obj.position)