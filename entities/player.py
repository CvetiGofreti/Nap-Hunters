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
        self.screenWidth, self.screenHeight = pygame.display.get_surface().get_size()

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

    def draw(self, screen):
        image = self.image
        if self.facing == Facing.RIGHT:
            image = pygame.transform.flip(self.image, True, False)
        screen.blit(image, self.rect.topleft)

    def update(self, dt):
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

        if self.jumpPressed and not self.isJumping:
            self.velocity = self.jumpVelocity
            self.isJumping = True
            self.jumpPressed = False

        self.velocity += self.gravity * dt
        self.rect.y += self.velocity * dt

        if self.rect.bottom >= self.screenHeight:
            self.rect.bottom = self.screenHeight
            self.velocity = 0
            self.isJumping = False