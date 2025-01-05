import pygame
import GridSystem as grid
import UI as uIScript

# Initialize Pygame
pygame.init()
FPS = 60
SPEED = 5
infoObject = pygame.display.Info()
SIZE = min(infoObject.current_w, infoObject.current_h)
#17x17 grid(diameter = size/divisions)
gridDiameter = (SIZE-1/10**10)/17
inputDelay = 0.08
win = pygame.display.set_mode((SIZE,SIZE))
pygame.display.set_caption("Shashthi The Hunter")
#No of nodes = size/diameter
grid.Initialize(SIZE, gridDiameter)
#Creating GameObjects
import GameObjects as gObj
player = gObj.player = gObj.CreatePlayer()
gObj.CreateBoundaries()
uI = uIScript.UI(win, player)

def Main():
    #Game loop
    clock = pygame.time.Clock()
    player.WaitForInput()
    run = True; num = 0; t = 0
    while(run):
        if(player.health <= 0): run = False #?Game Over
        clock.tick(FPS)
        num+=1
        for event in pygame.event.get():
            if(event.type == pygame.QUIT): run = False #?Game is trying to close
            if(event.type == pygame.KEYDOWN and num > FPS*inputDelay):
                num = 0
                player.Input(event)
                
        #SpawnEnemy
        if(len(gObj.enemies) <= 1):
            t+=1
            if(t > FPS*2):
                t = 0
                gObj.SpawnEnemies.LadyBug()
        #Main logic
        player.Movement()
        CollisionDetection()
        #Animation
        for animation in gObj.animations:
            animation.Update()
        #Drawing
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
    #Boundary
    for bound in gObj.boundaries:
        win.blit(bound.sprite, (bound.rect.x + shakeX, bound.rect.y + shakeY))

    #PlayerCollider
    #pygame.draw.rect(win, (135, 245, 179), player.collider)
    #Unwakable Nodes
    '''for node in grid.nodes:
        if(node.walkable == True): continue
        rect = pygame.Rect(node.wPosition[0], node.wPosition[1], gridDiameter/1.01, gridDiameter/1.01)
        pygame.draw.rect(win, (168, 50, 60), rect)'''
def CollisionDetection():
    player.UpdateCollider()
    #Enemy collision
    for enemy in gObj.enemies:
        if(player.collider.colliderect(enemy.rect)):
            enemy.DoDamage()
Main()