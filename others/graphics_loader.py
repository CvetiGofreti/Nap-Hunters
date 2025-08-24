import pygame
from pygame.surface import Surface

from others.tile_type import TileType
from others.floor_type import FloorType
from others.spray_type import SprayType

tileSize = 64

class Assets:
    def __init__(self) -> None:
        self.floor_variants: dict[FloorType, Surface] = {
            FloorType.MID: self._load64("graphics/levels/floor.png"),
            FloorType.LEFT: self._load64("graphics/levels/floor_left.png"),
            FloorType.RIGHT: self._load64("graphics/levels/floor_right.png"),
            FloorType.FLOOR_SINGLE: self._load64("graphics/levels/floor_both.png"),
        }

        self.player_images: dict[TileType, Surface] = {
            TileType.BLUE_PLAYER: self._load64("graphics/players/playerBlue.png"),
            TileType.RED_PLAYER:  self._load64("graphics/players/playerRed.png"),
        }

        self.beds: dict[TileType, Surface] = {
            TileType.BLUE_BED: self._load_2x1("graphics/players/bedBlue.png"),
            TileType.RED_BED:  self._load_2x1("graphics/players/bedRed.png"),
        }

        self.entities: dict[TileType, Surface] = {
            TileType.SNACK: self._load64("graphics/entities/snack.png"),
            TileType.BOOKS: self._load64("graphics/entities/books.png"),
            TileType.BUTTON: self._load64("graphics/spray/button.png"),
        }

        self.sprays: dict[SprayType, Surface] = {
            SprayType.OFF:       self._load64("graphics/spray/spray_off.png"),
            SprayType.ON:        self._load64("graphics/spray/spray_on.png"),
            SprayType.ON_BOTTOM: self._load64("graphics/spray/spray_on_bottom.png"),
            SprayType.ON_MIDDLE: self._load64("graphics/spray/spray_on_middle.png"),
            SprayType.ON_TOP:    self._load64("graphics/spray/spray_on_top.png")
        }

        self.button_pressed: Surface = self._load64("graphics/spray/button_pressed.png")
        self.wall: Surface = self._load_original("graphics/levels/wall.png")
        self.wall = pygame.transform.scale(self.wall, pygame.display.get_surface().get_size())
        self.passed_level_image: Surface = self._load64("graphics/levels/levelPassed.png")

    def _load64(self, path: str) -> Surface:
        img = pygame.image.load(path).convert_alpha()
        return pygame.transform.scale(img, (tileSize, tileSize))

    def _load_2x1(self, path: str) -> Surface:
        img = pygame.image.load(path).convert_alpha()
        return pygame.transform.scale(img, (2 * tileSize, tileSize))

    def _load_original(self, path: str) -> Surface:
        return pygame.image.load(path).convert()
