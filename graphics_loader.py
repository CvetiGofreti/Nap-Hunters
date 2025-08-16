import pygame
from tile_type import TileType
from floor_type import FloorType
from player_type import PlayerType

TILE = 64

class Assets:
    def __init__(self):

        self.floorVariants = {
            FloorType.MID: self._load64("graphics/levels/floor.png"),
            FloorType.LEFT: self._load64("graphics/levels/floor_left.png"),
            FloorType.RIGHT: self._load64("graphics/levels/floor_right.png"),
            FloorType.FLOOR_SINGLE: self._load64("graphics/levels/floor_both.png"),
        }

        self.playerImages = {
            PlayerType.BLUE: self._load64("graphics/players/playerBlue.png"),
            PlayerType.RED:  self._load64("graphics/players/playerRed.png"),
        }

        self.beds = {
            PlayerType.BLUE: self._load_2x1("graphics/players/bedBlue.png"),
            PlayerType.RED:  self._load_2x1("graphics/players/bedRed.png"),
        }

        self.wall = self._load_original("graphics/levels/wall.png")
        self.wall = pygame.transform.scale(self.wall, pygame.display.get_surface().get_size())

    def _load64(self, path):
        img = pygame.image.load(path).convert_alpha()
        return pygame.transform.scale(img, (TILE, TILE))

    def _load_2x1(self, path):
        img = pygame.image.load(path).convert_alpha()
        return pygame.transform.scale(img, (2*TILE, TILE))

    def _load_original(self, path):
        return pygame.image.load(path).convert()
    