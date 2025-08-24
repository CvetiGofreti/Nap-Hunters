import pygame
import os
from others import SprayType

tileSize = 64

class Spray:
    def __init__(self, x, y, height, assets):
        self.baseX = x
        self.baseY = y
        self.height = height
        self.assets = assets
        self.active = True
        self.collideRect = pygame.Rect(x * tileSize, (y - height + 1) * tileSize, tileSize, height * tileSize)

    def update(self, anyButtonPressed, players):
        self.active = not anyButtonPressed

        for player in players:
            if self.active and self.collideRect.colliderect(player.rect):
                player.respawn()

    def draw(self, screen):
        if os.getenv("DEBUG") == "1":
            pygame.draw.rect(screen, pygame.Color("red"), self.collideRect, 2)

        if not self.active:
            screen.blit(self.assets.sprays[SprayType.OFF], (self.baseX * tileSize, self.baseY * tileSize))
        elif self.height == 1:
            screen.blit(self.assets.sprays[SprayType.ON], (self.baseX * tileSize, self.baseY * tileSize))
        else:
            screen.blit(self.assets.sprays[SprayType.ON_BOTTOM], (self.baseX * tileSize, self.baseY * tileSize))
            for i in range(1, self.height - 1):
                screen.blit(self.assets.sprays[SprayType.ON_MIDDLE], (self.baseX * tileSize, (self.baseY - i) * tileSize))
            screen.blit(self.assets.sprays[SprayType.ON_TOP], (self.baseX * tileSize, (self.baseY - self.height + 1) * tileSize))