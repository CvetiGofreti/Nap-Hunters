from enum import IntEnum

class TileType(IntEnum):
    EMPTY  = 0
    FLOOR  = 1
    RED_PLAYER = 2
    BLUE_PLAYER = 3
    RED_BED = 4
    BLUE_BED = 5
    INVALID = 6
    SNACK = 7