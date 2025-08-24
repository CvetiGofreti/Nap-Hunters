import pygame
import os

from others import TileType

tileSize = 64

class Button:
    def __init__(self, x, y, assets):
        self.image = assets.entities[TileType.BUTTON]
        self.imagePressed = assets.button_pressed
        self.rect = pygame.Rect(x * tileSize, y * tileSize, tileSize, tileSize)
        collideOffset = 32
        self.collideRect = pygame.Rect(x * tileSize + collideOffset // 2, y * tileSize + collideOffset, tileSize - collideOffset, tileSize - collideOffset)

    def is_pressed(self, players):
        for player in players:
            if self.collideRect.colliderect(player.rect):
                return True
        return False

    def draw(self, screen, players):
        if(self.is_pressed(players)):
            screen.blit(self.imagePressed, self.rect.topleft)
        else:
            screen.blit(self.image, self.rect.topleft)

        if os.getenv("DEBUG") == "1":
            pygame.draw.rect(screen, pygame.Color("red"), self.collideRect, 2)