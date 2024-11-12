import pygame
import GridSystem

class Object:
    def __init__(self, _position, _orientation, _scale):
        self.position = _position
        self.orientation = _orientation
        self.scale = _scale


class Player:
    head = Object()
'''
    def Movement(event):
        if(event.key == pygame.K_UP and orientation[1] == 0):
                    orientation[1] = -1
                    orientation[0] = 0
                    GridSystem.SnapToGrid(player)
                elif(event.key == pygame.K_DOWN and orientation[1] == 0):
                    orientation[1] = 1
                    orientation[0] = 0
                    GridSystem.SnapToGrid(player)
                elif(event.key == pygame.K_LEFT and orientation[0] == 0):
                    orientation[0] = -1
                    orientation[1] = 0
                    GridSystem.SnapToGrid(player)
                elif(event.key == pygame.K_RIGHT and orientation[0] == 0):
                    orientation[0] = 1
                    orientation[1] = 0
                    GridSystem.SnapToGrid(player)
'''