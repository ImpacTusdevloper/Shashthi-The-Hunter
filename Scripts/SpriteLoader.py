import pygame
import GridSystem as grid

scale = grid.diameter



#!Testing
Test_120x120 = pygame.transform.scale(pygame.image.load("Sprites/Test_120x120.png"), (scale, scale))
Test_240x240 = pygame.transform.scale(pygame.image.load("Sprites/Test_240x240.png"), (scale, scale))
Test_50x50 = pygame.transform.scale(pygame.image.load("Sprites/Test_50x50.png"), (scale, scale))

#Main
test_Head = pygame.transform.scale(pygame.image.load("Sprites/test_Head.png"), (scale, scale))
test_Body_Solid = pygame.transform.scale(pygame.image.load("Sprites/test_Body_Solid.png"), (scale, scale))
test_Body_Dotted = pygame.transform.scale(pygame.image.load("Sprites/test_Body_Dotted.png"), (scale, scale))
test_Tail = pygame.transform.scale(pygame.image.load("Sprites/test_Tail.png"), (scale, scale))
test_Wall = pygame.transform.scale(pygame.image.load("Sprites/test_Wall.png"), (scale, scale))
test_Food = pygame.transform.scale(pygame.image.load("Sprites/test_Food.png"), (scale, scale))

#Squares
test = pygame.transform.scale(pygame.image.load("Sprites/test.png"), (scale, scale))
test01 = pygame.transform.scale(pygame.image.load("Sprites/test01.png"), (scale, scale))
test02 = pygame.transform.scale(pygame.image.load("Sprites/test02.png"), (scale, scale))
test03 = pygame.transform.scale(pygame.image.load("Sprites/test03.png"), (scale, scale))
test04 = pygame.transform.scale(pygame.image.load("Sprites/test04.png"), (scale, scale))
#Circles
testR = pygame.transform.scale(pygame.image.load("Sprites/testR.png"), (scale, scale))
testR01 = pygame.transform.scale(pygame.image.load("Sprites/testR01.png"), (scale, scale))
print()
