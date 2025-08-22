import pygame

class Leaderboard:
    def __init__(self, fontMain, fontSmall, assets):
        self.fontMain = fontMain
        self.fontSmall = fontSmall

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            return "mainMenu"

    def update(self, dt):
        pass

    def draw(self, screen):
        pass