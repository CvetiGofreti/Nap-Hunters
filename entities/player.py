import os
from enum import IntEnum

import pygame

from others import TileType
from others import ControlsType

TILE_SIZE = 64

class Facing(IntEnum):
    LEFT = 0
    RIGHT = 1

class Player:
    def __init__(self, img: pygame.Surface, grid_pos, controls, bed):
        self.image = img
        self.rect = pygame.Rect(
            grid_pos[0] * TILE_SIZE,
            grid_pos[1] * TILE_SIZE,
            TILE_SIZE,
            TILE_SIZE
        )
        self.initial_pos = (grid_pos[0] * TILE_SIZE, grid_pos[1] * TILE_SIZE)
        self.facing = Facing.LEFT
        self.controls = controls
        self.screen_width, self.screen_height = pygame.display.get_surface().get_size()
        self.corresponding_bed = bed
        self.points = 0

        self.speed = 200
        self.moving_left  = False
        self.moving_right = False
        self.jump_pressed = False

        self.is_jumping = False
        self.jump_velocity = -670
        self.gravity = 900
        self.velocity = 0
        self.prev_rect = None

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == self.controls[ControlsType.LEFT]:
                self.moving_left = True
            elif event.key == self.controls[ControlsType.RIGHT]:
                self.moving_right = True
            elif event.key == self.controls[ControlsType.JUMP] and not self.is_jumping:
                self.jump_pressed = True

        elif event.type == pygame.KEYUP:
            if event.key == self.controls[ControlsType.LEFT]:
                self.moving_left = False
            elif event.key == self.controls[ControlsType.RIGHT]:
                self.moving_right = False

    def draw(self, screen, grid):
        image = self.image
        draw_pos = self.rect.topleft

        if self.is_near_bed(grid):
            image = pygame.transform.rotate(self.image, 270)
            for y in range(len(grid)):
                for x in range(len(grid[0]) - 1):
                    if (
                        grid[y][x] == self.corresponding_bed
                        and grid[y][x + 1] == self.corresponding_bed
                    ):
                        bed_x = x * TILE_SIZE
                        bed_y = y * TILE_SIZE
                        bed_center_x = bed_x + TILE_SIZE
                        bed_center_y = bed_y + TILE_SIZE // 2
                        bed_center = (bed_center_x, bed_center_y)
                        image_rect = image.get_rect(center = bed_center)
                        draw_pos = image_rect.topleft
                        break
                else:
                    continue
                break

        elif self.facing == Facing.RIGHT:
            image = pygame.transform.flip(self.image, True, False)

        screen.blit(image, draw_pos)

        if os.getenv("DEBUG") == "1":
            for x, y in self.get_overlapping_tiles():
                if 0 <= y < len(grid) and 0 <= x < len(grid[0]):
                    tile_rect = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                    pygame.draw.rect(screen, (255, 0, 0), tile_rect, 2)
                    floor_top = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, 15)
                    pygame.draw.rect(screen, (0, 255, 0), floor_top, 1)

    def respawn(self):
        self.rect.topleft = self.initial_pos
        self.velocity = 0
        self.is_jumping = False
        self.moving_left  = False
        self.moving_right = False

    def on_level_complete(self):
        self.moving_left  = False
        self.moving_right = False
        self.jump_pressed = False

    def _check_bottom(self):
        if self.rect.bottom > self.screen_height:
            self.rect.bottom = self.screen_height
            self.velocity = 0
            self.is_jumping = False

    def _check_top(self):
        if self.rect.top < 0:
            self.rect.top = 0
            self.velocity = 0

    def update_jump(self, dt, grid, book_rects):
        if self.jump_pressed and not self.is_jumping:
            self.velocity = self.jump_velocity
            self.is_jumping = True
        self.jump_pressed = False

        self.velocity += self.gravity * dt
        self.rect.y += self.velocity * dt

        for x, y in self.get_overlapping_tiles():
            tile = grid[y][x]
            if tile == TileType.FLOOR:
                floor_top = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, 15)
                if self.rect.colliderect(floor_top):
                    if self.velocity > 0 and self.prev_rect.bottom <= floor_top.top:
                        self.rect.bottom = floor_top.top
                        self.velocity = 0
                        self.is_jumping = False
                    elif self.velocity < 0 and self.prev_rect.top >= floor_top.bottom:
                        self.rect.top = floor_top.bottom
                        self.velocity = 0

        for book_rect in book_rects:
            if self.rect.colliderect(book_rect):
                if self.velocity > 0 and self.prev_rect.bottom <= book_rect.top:
                    self.rect.bottom = book_rect.top
                    self.velocity = 0
                    self.is_jumping = False
                elif self.velocity < 0 and self.prev_rect.top >= book_rect.bottom:
                    self.rect.top = book_rect.bottom
                    self.velocity = 0

    def update_move(self, dt, grid):
        if self.moving_left:
            self.rect.x -= self.speed * dt
            self.rect.left = max(self.rect.left, 0)
            self.facing = Facing.LEFT
        elif self.moving_right:
            self.rect.x += self.speed * dt
            self.rect.right = min(self.rect.right, self.screen_width)
            self.facing = Facing.RIGHT

        for x, y in self.get_overlapping_tiles():
            tile = grid[y][x]
            if tile != TileType.FLOOR:
                continue

            floor_top = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, 15)
            if self.rect.colliderect(floor_top):
                if self.facing == Facing.RIGHT:
                    self.rect.right = floor_top.left
                elif self.facing == Facing.LEFT:
                    self.rect.left = floor_top.right

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

    def is_near_bed(self, grid):
        for x, y in self.get_overlapping_tiles():
            if 0 <= y < len(grid) and 0 <= x < len(grid[0]):
                tile = grid[y][x]
                if self.corresponding_bed == tile:
                    return True
        return False

    def update(self, dt, grid, book_rects):
        self.prev_rect = self.rect.copy()
        self.update_move(dt, grid)
        self.update_jump(dt, grid, book_rects)
        self._check_bottom()
        self._check_top()
