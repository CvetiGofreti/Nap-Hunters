import pygame
from others.tile_type import TileType
from others.floor_type import FloorType

tileSize = 64

class Assets:
    def __init__(self):

        self.floorVariants = {
            FloorType.MID: self._load64("graphics/levels/floor.png"),
            FloorType.LEFT: self._load64("graphics/levels/floor_left.png"),
            FloorType.RIGHT: self._load64("graphics/levels/floor_right.png"),
            FloorType.FLOOR_SINGLE: self._load64("graphics/levels/floor_both.png"),
        }

        self.playerImages = {
            TileType.BLUE_PLAYER: self._load64("graphics/players/playerBlue.png"),
            TileType.RED_PLAYER:  self._load64("graphics/players/playerRed.png"),
        }

        self.beds = {
            TileType.BLUE_BED: self._load_2x1("graphics/players/bedBlue.png"),
            TileType.RED_BED:  self._load_2x1("graphics/players/bedRed.png"),
        }

        self.entities = {
            TileType.SNACK: self._load64("graphics/entities/snack.png"),
        }

        self.wall = self._load_original("graphics/levels/wall.png")
        self.wall = pygame.transform.scale(self.wall, pygame.display.get_surface().get_size())
        self.passedLevelImage = self._load64("graphics/levels/levelPassed.png")

    def _load64(self, path):
        img = pygame.image.load(path).convert_alpha()
        return pygame.transform.scale(img, (tileSize, tileSize))

    def _load_2x1(self, path):
        img = pygame.image.load(path).convert_alpha()
        return pygame.transform.scale(img, (2*tileSize, tileSize))

    def _load_original(self, path):
        return pygame.image.load(path).convert()
    