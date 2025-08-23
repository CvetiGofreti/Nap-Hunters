import pygame
import os

tileSize = 64

class Snack:
    def __init__(self, x, y, image):
        self.x = x 
        self.y = y
        self.image = image
        self.rect = pygame.Rect(
            x * tileSize,
            y * tileSize,
            tileSize,
            tileSize
        )

        collisionSize = 32
        offset = (tileSize - collisionSize) // 2
        self.collideRect = pygame.Rect(
            self.rect.x + offset,
            self.rect.y,
            collisionSize,
            collisionSize
        )

    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)
        if os.getenv("DEBUG") == "1":
            pygame.draw.rect(screen, pygame.Color("red"), self.collideRect, 2)

    def is_colliding_with(self, playerRect):
        return self.collideRect.colliderect(playerRect)
