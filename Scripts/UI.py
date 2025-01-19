import pygame, os
import pygame.font

class UI:
    def __init__(self, screen, _gObj):
        pygame.font.init()
        self.screen = screen
        self.gObj = _gObj
        self.player = self.gObj.player
        # Load the custom font
        font_path = self.gObj.sprites.resourcePath("Data/Font/batman_forever.ttf")
        self.font = pygame.font.Font(font_path, 25)

    def draw(self):
        self.DisplayHealth()
        self.DisplayScore()
        self.DisplayHighScore()

    def DisplayHealth(self):
        health_text = f"Health: {self.player.health}"
        health_surface = self.font.render(health_text, True, (255, 255, 255))
        self.screen.blit(health_surface, (10, 10))  # Position the health text
    def DisplayHighScore(self):
        text = f"HighScore: {self.gObj.highScore}"
        surface = self.font.render(text, True, (255, 255, 255))
        self.screen.blit(surface, (10, 50))  # Position the speed text

    def DisplayScore(self):
        text = f"Score: {self.gObj.score}"
        surface = self.font.render(text, True, (255, 255, 255))
        self.screen.blit(surface, (10, 90))