import os
import json
import pygame
from others.tile_type import TileType
from others.floor_type import FloorType
from others.controls_type import ControlsType
from entities.player import Player

tileSize = 64

class GameScreen:
    def __init__(self, fontMain, fontSmall, assets):
        self.fontMain = fontMain
        self.fontSmall = fontSmall
        self.assets = assets
        self.grid = []
        self.levelName = "Level"
        self.players = []
        self.hasError = False
        self.screenWidth, self.screenHeight = pygame.display.get_surface().get_size()
        self.tileCountWidth = self.screenWidth // tileSize
        self.tileCountHeight = self.screenHeight // tileSize

    def _get_tyle_type_at(self, x, y):
        if 0 <= y < self.tileCountHeight and 0 <= x < self.tileCountWidth:
            return self.grid[y][x]
        return TileType.INVALID

    def load_level(self, levelPath):
        try:
            with open(levelPath, "r", encoding="utf-8") as level:
                data = json.load(level)
        except Exception as exeption:
            print(f"Failed to load level {levelPath}: {exeption}")
            self.hasError = True
            return

        self.levelName = data.get("name", "Level")
        grid = data.get("grid", [])
        self.grid = [[TileType(value) for value in row] for row in grid]
        self.players = []

        for y in range(self.tileCountHeight):
            for x in range(self.tileCountWidth):
                tileType = self._get_tyle_type_at(x, y)
                if tileType == TileType.BLUE_PLAYER:
                    image = self.assets.playerImages[tileType]
                    controls = {ControlsType.LEFT: pygame.K_a, ControlsType.RIGHT: pygame.K_d, ControlsType.JUMP: pygame.K_w}
                    self.players.append(Player(image, (x, y) , controls, TileType.BLUE_BED))
                if tileType == TileType.RED_PLAYER:
                    image = self.assets.playerImages[tileType]
                    controls = {ControlsType.LEFT: pygame.K_LEFT, ControlsType.RIGHT: pygame.K_RIGHT, ControlsType.JUMP: pygame.K_UP}
                    self.players.append(Player(image, (x, y) , controls, TileType.RED_BED))

        self._validate_loaded_level()

    def _pick_floor_variant(self, grid, x, y):
        gridWidth, gridHight = len(grid[0]), len(grid)
        left = (x > 0 and self._get_tyle_type_at(x - 1, y) == TileType.FLOOR)
        right = (x < gridWidth - 1 and self._get_tyle_type_at(x + 1, y) == TileType.FLOOR)
        if left and right: return FloorType.MID
        if not left and right: return FloorType.LEFT
        if left and not right: return FloorType.RIGHT
        return FloorType.FLOOR_SINGLE

    #todo - add more validations
    def _validate_loaded_level(self):
        tileCountHeight = len(self.grid)
        tileCountWidth = len(self.grid[0])
        if (self.tileCountWidth != tileCountWidth or self.tileCountHeight != tileCountHeight):
            self.hasError = True

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN and event.key in (pygame.K_ESCAPE, pygame.K_BACKSPACE):
            return "levelSelect"
        
        if not self.hasError:
            for player in self.players:
                player.handle_event(event)

        return None

    def update(self, dt):
        if not self.hasError:
            for player in self.players:
                player.update(dt, self.grid)

    def draw(self, screen):
        if self.hasError:
            text = self.fontMain.render("Error in level data", True, pygame.Color("red"))
            rect = text.get_rect(center=screen.get_rect().center)
            screen.blit(text, rect)
            return
        
        if self.grid:
            tileCountHeight = len(self.grid)
            tileCountWidth = len(self.grid[0])
            for y in range(tileCountHeight):
                for x in range(tileCountWidth):
                    if self._get_tyle_type_at(x, y) == TileType.FLOOR:
                        floorVariant = self._pick_floor_variant(self.grid, x, y)
                        screen.blit(self.assets.floorVariants[floorVariant], (x * tileSize, y * tileSize))
                    if self._get_tyle_type_at(x, y) == TileType.RED_BED and self._get_tyle_type_at(x + 1, y) == TileType.RED_BED:
                        bedImage = self.assets.beds[TileType.RED_BED]
                        screen.blit(bedImage, (x * tileSize, y * tileSize))
                    if self._get_tyle_type_at(x, y) == TileType.BLUE_BED and self._get_tyle_type_at(x + 1, y) == TileType.BLUE_BED:
                        bedImage = self.assets.beds[TileType.BLUE_BED]
                        screen.blit(bedImage, (x * tileSize, y * tileSize))
        
        for player in self.players:
            player.draw(screen, self.grid)
