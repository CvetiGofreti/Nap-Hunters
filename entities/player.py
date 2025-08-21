import pygame
import os
from others.tile_type import TileType
from enum import IntEnum
from others.controls_type import ControlsType

tileSize = 64

class Facing(IntEnum):
    LEFT = 0
    RIGHT = 1

class Player:
    def __init__(self, img: pygame.Surface, grid_pos, controls, bed):
        self.image = img
        self.rect = pygame.Rect(grid_pos[0] * tileSize, grid_pos[1] * tileSize, tileSize, tileSize)
        self.facing = Facing.LEFT
        self.controls = controls
        self.screenWidth, self.screenHeight = pygame.display.get_surface().get_size()
        self.correspondingBed = bed

        self.speed = 200
        self.movingLeft  = False
        self.movingRight = False
        self.jumpPressed = False

        self.isJumping = False
        self.jumpVelocity = -550
        self.gravity = 900
        self.velocity = 0

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == self.controls[ControlsType.LEFT]:
                self.movingLeft = True
            elif event.key == self.controls[ControlsType.RIGHT]:
                self.movingRight = True
            elif event.key == self.controls[ControlsType.JUMP] and not self.isJumping:
                self.jumpPressed = True

        elif event.type == pygame.KEYUP:
            if event.key == self.controls[ControlsType.LEFT]:
                self.movingLeft = False
            elif event.key == self.controls[ControlsType.RIGHT]:
                self.movingRight = False

    def draw(self, screen, grid):
        image = self.image
        drawPos = self.rect.topleft

        if self.is_near_bed(grid):
            image = pygame.transform.rotate(self.image, 270)
            for y in range(len(grid)):
                for x in range(len(grid[0]) - 1):
                    if grid[y][x] == self.correspondingBed and grid[y][x + 1] == self.correspondingBed:
                        bedX = x * tileSize
                        bedY = y * tileSize
                        bedCenterX = bedX + tileSize
                        bedCenterY = bedY + tileSize // 2
                        bedCenter = (bedCenterX, bedCenterY)
                        imageRect = image.get_rect(bedCenter)
                        drawPos = imageRect.topleft
                        break
                else:
                    continue
                break

        elif self.facing == Facing.RIGHT:
            image = pygame.transform.flip(self.image, True, False)
        
        screen.blit(image, drawPos)
 
        if os.getenv("DEBUG") == "1":
            for x, y in self.get_overlapping_tiles():
                if 0 <= y < len(grid) and 0 <= x < len(grid[0]):
                    tileRect = pygame.Rect(x * tileSize, y * tileSize, tileSize, tileSize)
                    pygame.draw.rect(screen, (255, 0, 0), tileRect, 2)
                    floorTop = pygame.Rect(x * tileSize, y * tileSize, tileSize, 15)
                    pygame.draw.rect(screen, (0, 255, 0), floorTop, 1)

    def on_level_complete(self):
        self.movingLeft  = False
        self.movingRight = False
        self.jumpPressed = False

    def _check_bottom(self):
        if self.rect.bottom > self.screenHeight:
            self.rect.bottom = self.screenHeight
            self.velocity = 0
            self.isJumping = False

    def _check_top(self):
        if self.rect.top < 0:
            self.rect.top = 0
            self.velocity = 0

    def update_jump(self, dt, grid):
        if self.jumpPressed and not self.isJumping:
            self.velocity = self.jumpVelocity
            self.isJumping = True
        self.jumpPressed = False

        self.velocity += self.gravity * dt
        self.rect.y += self.velocity * dt

        for x, y in self.get_overlapping_tiles():
            tile = grid[y][x]
            if tile != TileType.FLOOR:
                continue

            floorTop = pygame.Rect(x * tileSize, y * tileSize, tileSize, 15)
            if self.rect.colliderect(floorTop):
                if self.velocity > 0 and self.prevRect.bottom <= floorTop.top:
                    self.rect.bottom = floorTop.top
                    self.velocity = 0
                    self.isJumping = False
                elif self.velocity < 0 and self.prevRect.top >= floorTop.bottom:
                    self.rect.top = floorTop.bottom
                    self.velocity = 0

    def update_move(self, dt, grid):
        if self.movingLeft:
            self.rect.x -= self.speed * dt
            if self.rect.left < 0:
                self.rect.left = 0
            self.facing = Facing.LEFT
        elif self.movingRight:
            self.rect.x += self.speed * dt
            if self.rect.right > self.screenWidth:
                self.rect.right = self.screenWidth
            self.facing = Facing.RIGHT

        for x, y in self.get_overlapping_tiles():
            tile = grid[y][x]
            if tile != TileType.FLOOR:
                continue

            floorTop = pygame.Rect(x * tileSize, y * tileSize, tileSize, 15)
            if self.rect.colliderect(floorTop):
                if self.facing == Facing.RIGHT:
                    self.rect.right = floorTop.left
                elif self.facing == Facing.LEFT:
                    self.rect.left = floorTop.right

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
    
    def is_near_bed(self, grid):
        for x, y in self.get_overlapping_tiles():
            if 0 <= y < len(grid) and 0 <= x < len(grid[0]):
                tile = grid[y][x]
                if self.correspondingBed == tile:
                    return True
        return False

    def update(self, dt, grid):
        self.prevRect = self.rect.copy()
        self.update_move(dt, grid)
        self.update_jump(dt, grid)
        self._check_bottom()
        self._check_top()