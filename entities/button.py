import os

import pygame

from others import TileType

TILE_SIZE = 64

class Button:
    def __init__(self, x, y, assets):
        self.image = assets.entities[TileType.BUTTON]
        self.image_pressed = assets.button_pressed
        self.rect = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
        collide_offset = 32
        self.collide_rect = pygame.Rect(
            x * TILE_SIZE + collide_offset // 2,
            y * TILE_SIZE + collide_offset,
            TILE_SIZE - collide_offset,
            TILE_SIZE - collide_offset
        )

    def is_pressed(self, players):
        for player in players:
            if self.collide_rect.colliderect(player.rect):
                return True
        return False

    def draw(self, screen, players):
        if self.is_pressed(players):
            screen.blit(self.image_pressed, self.rect.topleft)
        else:
            screen.blit(self.image, self.rect.topleft)

        if os.getenv("DEBUG") == "1":
            pygame.draw.rect(screen, pygame.Color("red"), self.collide_rect, 2)
