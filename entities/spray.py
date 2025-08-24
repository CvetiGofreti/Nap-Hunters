import os

import pygame

from others import SprayType

TILE_SIZE = 64

class Spray:
    def __init__(self, x, y, height, assets):
        self.base_x = x
        self.base_y = y
        self.height = height
        self.assets = assets
        self.active = True
        self.collide_rect = pygame.Rect(
            x * TILE_SIZE,
            (y - height + 1) * TILE_SIZE,
            TILE_SIZE, height * TILE_SIZE
        )

    def update(self, any_button_pressed, players):
        self.active = not any_button_pressed

        for player in players:
            if self.active and self.collide_rect.colliderect(player.rect):
                player.respawn()

    def draw(self, screen):
        if os.getenv("DEBUG") == "1":
            pygame.draw.rect(screen, pygame.Color("red"), self.collide_rect, 2)

        draw_position = (self.base_x * TILE_SIZE, self.base_y * TILE_SIZE)
        if not self.active:
            screen.blit(self.assets.sprays[SprayType.OFF], draw_position)
        elif self.height == 1:
            screen.blit(self.assets.sprays[SprayType.ON], draw_position)
        else:
            screen.blit(self.assets.sprays[SprayType.ON_BOTTOM], draw_position)
            for i in range(1, self.height - 1):
                draw_position = (self.base_x * TILE_SIZE, (self.base_y - i) * TILE_SIZE)
                screen.blit(self.assets.sprays[SprayType.ON_MIDDLE], draw_position)
            draw_position = (self.base_x * TILE_SIZE, (self.base_y - self.height + 1) * TILE_SIZE)
            screen.blit(self.assets.sprays[SprayType.ON_TOP], draw_position)
