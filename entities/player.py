import pygame
from others.tile_type import TileType

tileSize = 64

class Player:
    def __init__(self, img: pygame.Surface, grid_pos, controls):
        self.image = img
        self.rect = pygame.Rect(grid_pos[0] * tileSize, grid_pos[1] * tileSize, tileSize, tileSize)
        self.controls = controls

    def handle_event(self, event):
        pass
    
    def draw(self, screen):
        image = self.image
        screen.blit(image, self.rect.topleft)

    def update(self, dt):
        pass