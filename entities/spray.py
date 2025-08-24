import pygame
from others.tile_type import TileType
from others.spray_type import SprayType

tileSize = 64

class Spray:
    def __init__(self, x, y, height, assets):
        self.baseX = x
        self.baseY = y
        self.height = height
        self.assets = assets
        self.active = True

    def update(self, anyButtonPressed):
        self.active = not anyButtonPressed

    def draw(self, screen):
        if not self.active:
            screen.blit(self.assets.sprays[SprayType.OFF], (self.baseX * tileSize, self.baseY * tileSize))
        elif self.height == 1:
            screen.blit(self.assets.sprays[SprayType.ON], (self.baseX * tileSize, self.baseY * tileSize))
        else:
            screen.blit(self.assets.sprays[SprayType.ON_BOTTOM], (self.baseX * tileSize, self.baseY * tileSize))
            for i in range(1, self.height - 1):
                screen.blit(self.assets.sprays[SprayType.ON_MIDDLE], (self.baseX * tileSize, (self.baseY - i) * tileSize))
            screen.blit(self.assets.sprays[SprayType.ON_TOP], (self.baseX * tileSize, (self.baseY - self.height + 1) * tileSize))