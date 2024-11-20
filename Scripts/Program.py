import pygame
import GridSystem as grid
import GameObjects as gObj

FPS = 60
SPEED = 5
SIZE = 800
#17x17 grid(diameter = size/divisions)
gridDiameter = 47.04
inputDelay = 0.08
win = pygame.display.set_mode((SIZE, SIZE))
#No of nodes = size/diameter
grid.Initialize(SIZE, gridDiameter)
player = gObj.CreatePlayer()

def Main():
    #Game loop
    clock = pygame.time.Clock()
    run = True; num = 0
    while(run):
        clock.tick(FPS)
        num+=1
        for event in pygame.event.get():
            if(event.type == pygame.QUIT): run = False #Game is trying to close
            if(event.type == pygame.KEYDOWN and num > FPS*inputDelay):
                num = 0
                player.Input(event)

        #Main logic
        player.Movement()
        DrawWindow(player)
        pygame.display.update()

    pygame.quit()

def DrawWindow(player):
    win.fill((0, 0, 0))
    for node in grid.nodes:
        rect = pygame.Rect(node.wPosition[0], node.wPosition[1], gridDiameter/1.01, gridDiameter/1.01)
        pygame.draw.rect(win, (150, 150, 150), rect)
    for part in player.parts:
        rect = pygame.Rect(part.wPosition[0], part.wPosition[1], part.scale, part.scale)
        win.blit(part.sprite, (rect.x, rect.y))
    rect = pygame.Rect(SIZE//2-gridDiameter/2, SIZE//2-gridDiameter/2, gridDiameter/1.01, gridDiameter/1.01)
    pygame.draw.rect(win, (55, 222, 100), rect)
Main()