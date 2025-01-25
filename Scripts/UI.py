import pygame
import pygame.font

class UI:
    def __init__(self, screen, _gObj):
        pygame.font.init()
        self.screen = screen
        self.gObj = _gObj
        self.player = self.gObj.player
        # Load the custom font
        font_path = self.gObj.sprites.resourcePath("Data/Font/SHUTTLE-X.ttf")
        self.font = pygame.font.Font(font_path, 25)

    def draw(self):
        if(self.gObj.zoom_factor>1.01): return
        self.DisplayHealth()
        self.DisplayScore()
        self.DisplayHighScore()
        self.DisplayInfo()

    def DisplayHealth(self):
        text = f"Health: {self.player.health}"
        surface = self.font.render(text, True, (255, 255, 255))
        self.screen.blit(surface, (10, 10))  # Position the health text

    def DisplayHighScore(self):
        text = f"HighScore: {self.gObj.highScore}"
        surface = self.font.render(text, True, (255, 255, 255))
        self.screen.blit(surface, (10, 50))  # Position the high score text

    def DisplayScore(self):
        text = f"Score: {self.gObj.score}"
        surface = self.font.render(text, True, (255, 255, 255))
        self.screen.blit(surface, (10, 90))  # Position the score text

    def DisplayInfo(self):
        info_text = "Hold 'H' for info"
        quit_text = "Press 'K' to quit"
        
        info_surface = self.font.render(info_text, True, (255, 255, 255))
        quit_surface = self.font.render(quit_text, True, (255, 255, 255))
        
        info_rect = info_surface.get_rect()
        quit_rect = quit_surface.get_rect()
        
        info_rect.bottomright = (self.screen.get_width() - 10, self.screen.get_height() - 30)
        quit_rect.bottomright = (self.screen.get_width() - 10, self.screen.get_height() - 10)
        
        self.screen.blit(info_surface, info_rect)
        self.screen.blit(quit_surface, quit_rect)
