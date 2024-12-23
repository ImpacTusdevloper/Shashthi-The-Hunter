import pygame
import GridSystem as grid

FPS = 60
SPEED = 5
SIZE = 800
#17x17 grid(diameter = size/divisions)
gridDiameter = 47.04
inputDelay = 0.08
win = pygame.display.set_mode((SIZE, SIZE))
pygame.display.set_caption("Shashthi The Hunter")
#No of nodes = size/diameter
grid.Initialize(SIZE, gridDiameter)
#Creating GameObjects
import GameObjects as gObj
player = gObj.player = gObj.CreatePlayer()
gObj.CreateBoundaries()

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
                if(not player.canMove):
                    player.WaitForInput(False)
                if(event.key == pygame.K_SPACE):
                    player.ExtendBody()

        #SpawnEnemy
        t+=1
        if(t > FPS*2):
            t = 0
            gObj.SpawnEnemies.LadyBug()
        #Main logic
        player.Movement()
        CollisionDetection()
        DrawWindow()
        pygame.display.update()
    pygame.quit()

def DrawWindow():
    win.fill((0, 0, 0))
    #Grid System
    for node in grid.nodes:
        rect = pygame.Rect(node.wPosition[0], node.wPosition[1], gridDiameter/1.01, gridDiameter/1.01)
        pygame.draw.rect(win, (150, 150, 150), rect)
    #Enemies
    for enemy in gObj.enemies:
        rect = pygame.Rect(enemy.wPosition[0], enemy.wPosition[1], enemy.scale, enemy.scale)
        win.blit(enemy.sprite, (rect.x, rect.y))
    #Player
    for part in player.parts:
        rect = pygame.Rect(part.wPosition[0], part.wPosition[1], part.scale, part.scale)
        win.blit(part.sprite, (rect.x, rect.y))
    #Boundary
    for bound in gObj.boundaries:
        win.blit(bound.sprite, (bound.rect.x, bound.rect.y))
    #PlayerCollider
    pygame.draw.rect(win, (135, 245, 179), player.collider)
    #Unwakable Nodes
    '''for node in grid.nodes:
        if(node.walkable == True): continue
        rect = pygame.Rect(node.wPosition[0], node.wPosition[1], gridDiameter/1.01, gridDiameter/1.01)
        pygame.draw.rect(win, (168, 50, 60), rect)'''
def CollisionDetection():
    player.UpdateCollider()
    #Boundary collision
    for bound in gObj.boundaries:
        if(player.collider.colliderect(bound.rect)):
            continue
    #Enemy collision
    for enemy in gObj.enemies:
        if(player.collider.colliderect(enemy.collider)):
            #player.DoDamage(enemy, 1)
            gObj.enemies.remove(enemy)
            grid.NodeFromPos(enemy.position).walkable = True
            player.ExtendBody()
Main()