import pygame
import os
from others.tile_type import TileType
from entities import Facing

tileSize = 64

class MovableBooks:
    def __init__(self, x, y, image):
        self.image = image
        self.rect = pygame.Rect(x * tileSize, y * tileSize, tileSize, tileSize)
        self.velocity = 0
        self.gravity = 900
        self.onGround = False
        self.screenWidth, self.screenHeight = pygame.display.get_surface().get_size()
        self.playerPushing = None

    def update(self, dt, grid, players):
        self.playerPushing = None

        if not self.onGround:
            self.velocity += self.gravity * dt
        self.rect.y += self.velocity * dt
        self.onGround = False
        for x, y in self.get_overlapping_tiles():
            if grid[y][x] == TileType.FLOOR:
                floorRect = pygame.Rect(x * tileSize, y * tileSize, tileSize, 15)
                if self.rect.colliderect(floorRect):
                    self.rect.bottom = floorRect.top
                    self.velocity = 0
                    self.onGround = True
            
        pushOffset = 16
        for player in players:
            if player.rect.colliderect(self.rect):
                if player.facing == Facing.RIGHT and player.rect.right <= self.rect.left + pushOffset:
                    self.rect.x += player.speed * dt
                    self.playerPushing = player
                elif player.facing == Facing.LEFT and player.rect.left >= self.rect.right - pushOffset:
                    self.rect.x -= player.speed * dt
                    self.playerPushing = player
        
        if self.rect.bottom > self.screenHeight:
            self.rect.bottom = self.screenHeight
            self.velocity = 0
            self.onGround = True

        if self.rect.left < 0:
            self.rect.left = 0
            if(self.playerPushing.facing == Facing.LEFT):
                self.playerPushing.movingLeft = False
        if self.rect.right > pygame.display.get_surface().get_width():
            self.rect.right = pygame.display.get_surface().get_width()
            if(self.playerPushing.facing == Facing.RIGHT):
                self.playerPushing.movingRight = False


    def get_overlapping_tiles(self):
        tiles = []
        left = self.rect.left // tileSize
        right = (self.rect.right - 1) // tileSize
        top = self.rect.top // tileSize
        bottom = (self.rect.bottom - 1) // tileSize

        for y in range(top, bottom + 1):
            for x in range(left, right + 1):
                if 0 <= x < 15 and 0 <= y < 15:
                    tiles.append((x, y))
        return tiles

    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)
        if os.getenv("DEBUG") == "1":
            pygame.draw.rect(screen, pygame.Color("red"), self.rect, 2)
