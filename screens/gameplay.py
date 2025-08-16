import pygame

class GameScreen:
    def __init__(self, fontMain, fontSmall, assets):
        pass
    def update(self, dt):
        pass
    
    def handle_event(self, event):
        if event.type == pygame.KEYDOWN and event.key in (pygame.K_ESCAPE, pygame.K_BACKSPACE):
            return "levelSelect"
        return None
    
    def load_level(self, path: str):
        pass
    
    def draw(self, screen):
        pass