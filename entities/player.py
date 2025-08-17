import pygame
from others.tile_type import TileType
from enum import IntEnum
from others.controls_type import ControlsType

tileSize = 64

class Facing(IntEnum):
    LEFT = 0
    RIGHT = 1

class Player:
    def __init__(self, img: pygame.Surface, grid_pos, controls):
        self.image = img
        self.rect = pygame.Rect(grid_pos[0] * tileSize, grid_pos[1] * tileSize, tileSize, tileSize)
        self.facing = Facing.LEFT
        self.controls = controls

        self.speed = 200
        self.movingLeft  = False
        self.movingRight = False
        self.jumpPressed = False

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == self.controls[ControlsType.LEFT]:
                self.movingLeft = True
            elif event.key == self.controls[ControlsType.RIGHT]:
                self.movingRight = True
            elif event.key == self.controls[ControlsType.JUMP]:
                self.jumpPressed = True

        elif event.type == pygame.KEYUP:
            if event.key == self.controls[ControlsType.LEFT]:
                self.movingLeft = False
            elif event.key == self.controls[ControlsType.RIGHT]:
                self.movingRight = False

    def draw(self, screen):
        image = self.image
        if self.facing == Facing.RIGHT:
            image = pygame.transform.flip(self.image, True, False)
        screen.blit(image, self.rect.topleft)

    def update(self, dt):
        if self.movingLeft:
            self.rect.x -= self.speed * dt
            self.facing = Facing.LEFT
        elif self.movingRight:
            self.rect.x += self.speed * dt
            self.facing = Facing.RIGHT