import os

import pygame

from others import TileType
from entities import Facing

TILE_SIZE = 64

class MovableBooks:
    def __init__(self, x, y, image):
        self.image = image
        self.rect = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
        self.velocity = 0
        self.gravity = 900
        self.on_ground = False
        self.screen_width, self.screen_height = pygame.display.get_surface().get_size()
        self.player_pushing = None

    def update(self, dt, grid, players):
        self.player_pushing = None

        if not self.on_ground:
            self.velocity += self.gravity * dt
        self.rect.y += self.velocity * dt
        self.on_ground = False
        for x, y in self.get_overlapping_tiles():
            if grid[y][x] == TileType.FLOOR:
                floor_rect = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, 15)
                if self.rect.colliderect(floor_rect):
                    self.rect.bottom = floor_rect.top
                    self.velocity = 0
                    self.on_ground = True

        push_offset = 16
        for player in players:
            if player.rect.colliderect(self.rect):
                if (
                    player.facing == Facing.RIGHT
                    and player.rect.right <= self.rect.left + push_offset
                    ):
                    self.rect.x += player.speed * dt
                    self.player_pushing = player
                elif (
                    player.facing == Facing.LEFT
                    and player.rect.left >= self.rect.right - push_offset
                    ):
                    self.rect.x -= player.speed * dt
                    self.player_pushing = player

        if self.rect.bottom > self.screen_height:
            self.rect.bottom = self.screen_height
            self.velocity = 0
            self.on_ground = True

        if self.rect.left < 0:
            self.rect.left = 0
            if self.player_pushing.facing == Facing.LEFT:
                self.player_pushing.movingLeft = False
        if self.rect.right > pygame.display.get_surface().get_width():
            self.rect.right = pygame.display.get_surface().get_width()
            if self.player_pushing.facing == Facing.RIGHT:
                self.player_pushing.movingRight = False


    def get_overlapping_tiles(self):
        tiles = []
        left = self.rect.left // TILE_SIZE
        right = (self.rect.right - 1) // TILE_SIZE
        top = self.rect.top // TILE_SIZE
        bottom = (self.rect.bottom - 1) // TILE_SIZE

        for y in range(top, bottom + 1):
            for x in range(left, right + 1):
                if 0 <= x < 15 and 0 <= y < 15:
                    tiles.append((x, y))
        return tiles

    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)
        if os.getenv("DEBUG") == "1":
            pygame.draw.rect(screen, pygame.Color("red"), self.rect, 2)
