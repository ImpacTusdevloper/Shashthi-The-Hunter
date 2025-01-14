import pygame
import pygame.font

class UI:
    def __init__(self, screen, _gObj):
        pygame.font.init()
        self.screen = screen
        self.gObj = _gObj
        self.player = self.gObj.player
        self.font = pygame.font.Font(None, 36)

    def draw(self):
        self.DisplayBodyLength()
        self.DisplayHealth()
        self.DisplayScore()
        self.DisplaySpeed()

    def DisplayHealth(self):
        health_text = f"Health: {self.player.health}"
        health_surface = self.font.render(health_text, True, (255, 255, 255))
        self.screen.blit(health_surface, (10, 10))  # Position the health text

    def DisplayBodyLength(self):
        body_length_text = f"Body Length: {len(self.player.parts)}"
        body_length_surface = self.font.render(body_length_text, True, (255, 255, 255))
        self.screen.blit(body_length_surface, (10, 50))  # Position the body length text
    def DisplayScore(self):
        text = f"Score: {self.gObj.score}"
        surface = self.font.render(text, True, (255, 255, 255))
        self.screen.blit(surface, (10, 110))
    def DisplaySpeed(self):
        speedText = f"Speed: {self.player.speed}"
        speedSurface = self.font.render(speedText, True, (255, 255, 255))
        self.screen.blit(speedSurface, (10, 150))  # Position the speed text