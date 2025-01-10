import pygame, os
import GridSystem as grid
import UI as uIScript

# Initialize Pygame
pygame.init()
FPS = 60
SPEED = 5
infoObject = pygame.display.Info()
screenWidth = infoObject.current_w; screenHeight = infoObject.current_h
SIZE = min(screenWidth, screenHeight)
#17x17 grid(diameter = size/divisions)
gridDiameter = (SIZE-1/10**10)/17
inputDelay = 0.01
win = pygame.display.set_mode((SIZE,SIZE), pygame.FULLSCREEN)
pygame.display.set_caption("STH")
#No of nodes = size/diameter
grid.Initialize(SIZE, (screenWidth, screenHeight), gridDiameter)
#Creating GameObjects
import GameObjects as gObj
player = gObj.player = gObj.CreatePlayer()
gObj.CreateBoundaries()
uI = uIScript.UI(win, player)

def Main():
    #?Game loop
    clock = pygame.time.Clock()
    player.WaitForInput()
    run = True; num = 0; t = 0
    while(run):
        if(player.health <= 0): ResetGame() #?Game Over
        clock.tick(FPS)
        num+=1
        for event in pygame.event.get():
            if(event.type == pygame.QUIT): run = False #?Game is trying to close
            if(event.type == pygame.KEYDOWN and num > FPS*inputDelay):
                num = 0
                player.Input(event)
                
        #?SpawnEnemy
        if(len(gObj.enemies) < 3):
            t+=1
            if(t > FPS*2):
                gObj.SpawnEnemies.SpawnRandEnemy()
                t = 0
        #?Main logic
        player.Movement()
        #?Animation
        for animation in gObj.animations:
            animation.Update()
        #?Collision Delay
        if(player.damageDelay > 0):
            head = player.parts[0]
            player.damageDelay -= 1
            if(player.damageDelay <= 0 and head.position == head.target):
                player.Collision()
        if(player.enemyHitDelay > 0):
            head = player.parts[0]
            player.enemyHitDelay -= 1
            if(player.enemyHitDelay <= 0):
                for enemy in gObj.enemies:
                    if(grid.NodeFromPos(enemy.position).position == head.target):
                        enemy.DoDamage()

        #?Drawing
        DrawWindow()
        uI.draw()
        pygame.display.update()
    pygame.quit()

def DrawWindow():
    win.fill((0, 0, 0))
    shakeX, shakeY = gObj.apply_screen_shake()
    #Grid System
    for node in grid.nodes:
        rect = pygame.Rect(node.wPosition[0], node.wPosition[1], gridDiameter/1.01, gridDiameter/1.01)
        pygame.draw.rect(win, (150, 150, 150), rect)
    #Boundary
    for bound in gObj.boundaries:
        win.blit(bound.sprite, (bound.rect.x + shakeX, bound.rect.y + shakeY))
    #BlockedDir
    for enemy in gObj.enemies:
        for dir in enemy.blocksFromDir:
            if(dir == (0, 0)): continue
            rect = pygame.Rect(enemy.wPosition[0] + dir[0]*gridDiameter, enemy.wPosition[1] + dir[1]*gridDiameter, gridDiameter/2, gridDiameter/2)
            rect.center = grid.NodeFromPos(rect.center).position
            pygame.draw.rect(win, (235, 82, 52), rect)
    #Enemies
    for enemy in gObj.enemies:
        win.blit(enemy.animatedSprite.curSprite, (enemy.rect.x + shakeX, enemy.rect.y + shakeY))
    #Player
    for part in player.parts:
        win.blit(part.animatedSprite.curSprite, (part.rect.x + shakeX, part.rect.y + shakeY))
    #PlayerCollider
    #pygame.draw.rect(win, (135, 245, 179), player.collider)
    #Unwakable Nodes
    '''for node in grid.nodes:
        if(node.walkable == True): continue
        rect = pygame.Rect(node.wPosition[0], node.wPosition[1], gridDiameter/1.01, gridDiameter/1.01)
        pygame.draw.rect(win, (168, 50, 60), rect)'''

def ResetGame():
    global player, gObj, uI
    player = gObj.player = gObj.CreatePlayer()  # Reinitialize player
    uI = uIScript.UI(win, player)  # Reinitialize UI
    gObj.enemies.clear()
    Main()  # Restart the main game loop

Main()