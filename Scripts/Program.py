import pygame
import GridSystem
import GameObjects

FPS = 60
SPEED = 5
SIZE = 800
gridDiameter = 50
Win = pygame.display.set_mode((SIZE, SIZE))
#No of nodes = size/diameter
GridSystem.Grid(SIZE, gridDiameter)
player = GameObjects.Player()
orientation = [0, -1]

def Main():
    #Game loop
    clock = pygame.time.Clock()
    player = pygame.Rect(SIZE/2, SIZE/2, gridDiameter, gridDiameter)
    run = True
    num = 0
    while(run):
        clock.tick(FPS)
        num+=1
        for event in pygame.event.get():
            if(event.type == pygame.QUIT):
                #Game is trying to close
                run = False
            if(event.type == pygame.KEYDOWN and num > FPS*0.1):
                num = 0
                player.Movement()

        #Main logic
        player.x += orientation[0] * SPEED
        player.y += orientation[1] * SPEED
        DrawWindow(player)
        pygame.display.update()

    pygame.quit()

def DrawWindow(player):
    Win.fill((0, 0, 0))
    for node in GridSystem.grid.nodes:
        rect = pygame.Rect(node["wXPos"], node["wYPos"], gridDiameter/1.01, gridDiameter/1.01)
        pygame.draw.rect(Win, (153, 150, 150), rect)
    pygame.draw.rect(Win, (0, 212, 219), player)
Main()