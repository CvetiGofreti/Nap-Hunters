import os

import pygame

TILE_SIZE = 64

class Snack:
    def __init__(self, x, y, image):
        self.x = x
        self.y = y
        self.image = image
        self.rect = pygame.Rect(
            x * TILE_SIZE,
            y * TILE_SIZE,
            TILE_SIZE,
            TILE_SIZE
        )

        collision_size = 32
        offset = (TILE_SIZE - collision_size) // 2
        self.collide_rect = pygame.Rect(
            self.rect.x + offset,
            self.rect.y,
            collision_size,
            collision_size
        )

    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)
        if os.getenv("DEBUG") == "1":
            pygame.draw.rect(screen, pygame.Color("red"), self.collide_rect, 2)

    def is_colliding_with(self, player_rect):
        return self.collide_rect.colliderect(player_rect)
