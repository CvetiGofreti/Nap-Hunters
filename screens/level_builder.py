import os
import json
from datetime import datetime
from typing import Optional, TypedDict, List

import pygame
from pygame.surface import Surface

from screens.interface import BaseScreen
from others import (
    TileType,
    FloorType,
    TextInputBox,
    Button,
    SprayType,
    Assets,
)

TILE_SIZE: int = 64
PALETTE_WIDTH: int = 192


class _PaletteItem(TypedDict):
    type: TileType
    name: str
    rect: pygame.Rect
    asset: Surface


class LevelBuilder(BaseScreen):
    def __init__(
        self,
        font_main: pygame.font.Font,
        font_small: pygame.font.Font,
        assets: Assets,
    ) -> None:
        self.screen_width, self.screen_height = pygame.display.get_surface().get_size()
        pygame.display.set_mode((self.screen_width + PALETTE_WIDTH, self.screen_height))

        self.font_main: pygame.font.Font = font_main
        self.font_small: pygame.font.Font = font_small
        self.assets: Assets = assets

        self.tile_count_width: int = self.screen_width // TILE_SIZE
        self.tile_count_height: int = self.screen_height // TILE_SIZE
        self.grid: list[list[TileType]] = [
            [TileType.EMPTY for _ in range(self.tile_count_width)]
            for _ in range(self.tile_count_height)
        ]

        self.grid[self.tile_count_height - 1][0] = TileType.BLUE_PLAYER
        self.grid[self.tile_count_height - 1][1] = TileType.RED_PLAYER
        self.grid[1][self.tile_count_width - 2] = TileType.BLUE_BED
        self.grid[1][self.tile_count_width - 1] = TileType.BLUE_BED
        self.grid[1][self.tile_count_width - 5] = TileType.RED_BED
        self.grid[1][self.tile_count_width - 4] = TileType.RED_BED

        self.dragging: Optional[tuple[TileType, int, int]] = None
        self.left_down: bool = False
        self.right_down: bool = False

        self.palette_rect: pygame.Rect = pygame.Rect(
            self.screen_width, 0, PALETTE_WIDTH, self.screen_height
        )

        x0, y0 = self.screen_width + 16, 16
        self.items: List[_PaletteItem] = [
            {
                "type": TileType.FLOOR,
                "name": "Floor",
                "rect": pygame.Rect(x0, y0, TILE_SIZE, TILE_SIZE),
                "asset": assets.floorVariants[FloorType.MID],
            },
            {
                "type": TileType.SNACK,
                "name": "Snack",
                "rect": pygame.Rect(x0 + 64 + 16, y0, TILE_SIZE, TILE_SIZE),
                "asset": assets.entities[TileType.SNACK],
            },
            {
                "type": TileType.BOOKS,
                "name": "Books",
                "rect": pygame.Rect(x0, y0 + 64 + 32, TILE_SIZE, TILE_SIZE),
                "asset": assets.entities[TileType.BOOKS],
            },
            {
                "type": TileType.SPRAY,
                "name": "Water spray",
                "rect": pygame.Rect(x0 + 64 + 16, y0 + 64 + 32, TILE_SIZE, TILE_SIZE),
                "asset": assets.sprays[SprayType.OFF],
            },
            {
                "type": TileType.BUTTON,
                "name": "Button",
                "rect": pygame.Rect(
                    x0, y0 + 64 + 32 + 64 + 32, TILE_SIZE, TILE_SIZE
                ),
                "asset": assets.entities[TileType.BUTTON],
            },
        ]

        self.selected_item_type: TileType = TileType.FLOOR
        self.hover_cell: Optional[tuple[int, int]] = None

        save_button_height = 40
        save_button_margin = 16
        button_pos = (
            self.screen_width + 16,
            self.screen_height - save_button_height - save_button_margin,
        )
        button_size = (PALETTE_WIDTH - 32, save_button_height)

        self.save_button: Button = Button(
            pos = button_pos,
            size = button_size,
            label = "Save Level",
            onClick = self._save_level,
            font = self.font_small,
        )

        input_width = PALETTE_WIDTH - 32
        input_height = 32
        input_x = self.screen_width + 16
        input_y = self.save_button.rect.y - input_height - 8
        self.level_name_box: TextInputBox = TextInputBox(
            input_x,
            input_y,
            input_width,
            input_height,
            font_small,
            "Enter level name",
            pygame.Color("white"),
        )

    def _pick_floor_variant(self, x: int, y: int) -> FloorType:
        left = x > 0 and self._get_tyle_type_at(x - 1, y) == TileType.FLOOR
        right = (
            x < self.tile_count_width - 1
            and self._get_tyle_type_at(x + 1, y) == TileType.FLOOR
        )
        if left and right:
            return FloorType.MID
        if not left and right:
            return FloorType.LEFT
        if left and not right:
            return FloorType.RIGHT
        return FloorType.FLOOR_SINGLE

    def _is_bed_tile(self, x: int, y: int) -> bool:
        if 0 <= y < self.tile_count_height and 0 <= x < self.tile_count_width:
            t = self._get_tyle_type_at(x, y)
            return t in (TileType.BLUE_BED, TileType.RED_BED)
        return False

    def _is_player_tile(self, x: int, y: int) -> bool:
        if 0 <= y < self.tile_count_height and 0 <= x < self.tile_count_width:
            t = self._get_tyle_type_at(x, y)
            return t in (TileType.BLUE_PLAYER, TileType.RED_PLAYER)
        return False

    def _entity_at(self, x: int, y: int) -> Optional[TileType]:
        if self._is_bed_tile(x, y):
            return self._get_tyle_type_at(x, y)
        if self._is_player_tile(x, y):
            return self._get_tyle_type_at(x, y)
        return None

    def _get_tyle_type_at(self, x: int, y: int) -> TileType:
        if 0 <= y < self.tile_count_height and 0 <= x < self.tile_count_width:
            return self.grid[y][x]
        return TileType.INVALID

    def _save_level(self) -> None:
        os.makedirs("levels", exist_ok=True)
        filename = datetime.now().strftime("%Y%m%d_%H%M%S") + "_level.json"
        path = os.path.join("levels", filename)
        data = {
            "name": self.level_name_box.label,
            "grid": [[cell.value for cell in row] for row in self.grid],
        }
        with open(path, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=2)
        print(f"Level saved: {path}")

    def _handle_click_event(self, event: pygame.event.Event) -> None:
        mouse_x, mouse_y = event.pos
        if event.button == 1:
            self.left_down = True
        if event.button == 3:
            self.right_down = True

        if event.button == 2 and mouse_x < self.screen_width and mouse_y < self.screen_height:
            grid_x, grid_y = mouse_x // TILE_SIZE, mouse_y // TILE_SIZE
            entity_type = self._entity_at(grid_x, grid_y)
            if entity_type is not None:
                self.dragging = (entity_type, grid_x, grid_y)

        if self.palette_rect.collidepoint(mouse_x, mouse_y) and event.button == 1:
            for item in self.items:
                if item["rect"].collidepoint(mouse_x, mouse_y):
                    self.selected_item_type = item["type"]
                    return

        if mouse_x < self.screen_width and mouse_y < self.screen_height:
            grid_x, grid_y = mouse_x // TILE_SIZE, mouse_y // TILE_SIZE
            if self._entity_at(grid_x, grid_y) is None:
                if event.button == 1:
                    self.grid[grid_y][grid_x] = self.selected_item_type
                elif event.button == 3:
                    self.grid[grid_y][grid_x] = TileType.EMPTY

        self.save_button.handle_event(event)

    def _handle_unclick_event(self, event: pygame.event.Event) -> None:
        if event.button == 1:
            self.left_down = False
        if event.button == 3:
            self.right_down = False
        if event.button == 2:
            self.dragging = None

    def _handle_drag_event(self, event: pygame.event.Event) -> None:
        mouse_x, mouse_y = event.pos
        if mouse_x < self.screen_width and mouse_y < self.screen_height:
            grid_x, grid_y = mouse_x // TILE_SIZE, mouse_y // TILE_SIZE
            self.hover_cell = (grid_x, grid_y)
        else:
            self.hover_cell = None

        if mouse_x < self.screen_width and mouse_y < self.screen_height:
            grid_x, grid_y = mouse_x // TILE_SIZE, mouse_y // TILE_SIZE
            if self.left_down and self._entity_at(grid_x, grid_y) is None:
                self.grid[grid_y][grid_x] = self.selected_item_type
            elif self.right_down and self._entity_at(grid_x, grid_y) is None:
                self.grid[grid_y][grid_x] = TileType.EMPTY

        if self.dragging and mouse_x < self.screen_width and mouse_y < self.screen_height:
            grid_x, grid_y = mouse_x // TILE_SIZE, mouse_y // TILE_SIZE
            kind, old_x, old_y = self.dragging

            if kind in (TileType.BLUE_PLAYER, TileType.RED_PLAYER):
                grid_x = max(0, min(self.tile_count_width - 1, grid_x))
                grid_y = max(0, min(self.tile_count_height - 1, grid_y))

                if (
                    not self._is_bed_tile(grid_x, grid_y)
                    and self._get_tyle_type_at(grid_x, grid_y) == TileType.EMPTY
                ):
                    self.grid[old_y][old_x] = TileType.EMPTY
                    self.grid[grid_y][grid_x] = kind
                    self.dragging = (kind, grid_x, grid_y)

            elif kind in (TileType.BLUE_BED, TileType.RED_BED):
                grid_x = max(0, min(self.tile_count_width - 2, grid_x))
                grid_y = max(0, min(self.tile_count_height - 1, grid_y))

                if (
                    self._get_tyle_type_at(grid_x, grid_y) == TileType.EMPTY
                    and self._get_tyle_type_at(grid_x + 1, grid_y) == TileType.EMPTY
                ):
                    self.grid[old_y][old_x] = TileType.EMPTY
                    self.grid[old_y][old_x + 1] = TileType.EMPTY
                    self.grid[grid_y][grid_x] = kind
                    self.grid[grid_y][grid_x + 1] = kind
                    self.dragging = (kind, grid_x, grid_y)

    def handle_event(
        self, event: pygame.event.Event
    ) -> str | tuple | None:
        self.level_name_box.handle_event(event)

        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            pygame.display.set_mode((self.screen_width, self.screen_height))
            return "mainMenu"

        if event.type == pygame.MOUSEBUTTONDOWN:
            self._handle_click_event(event)
        elif event.type == pygame.MOUSEBUTTONUP:
            self._handle_unclick_event(event)
        elif event.type == pygame.MOUSEMOTION:
            self._handle_drag_event(event)

        return None

    def update(self, dt: float) -> None:
        self.level_name_box.update(dt)

    def _draw_grid(self, screen: Surface) -> None:
        grid_color = pygame.Color("dimgray")
        for x in range(self.tile_count_width + 1):
            pygame.draw.line(
                screen, grid_color, (x * TILE_SIZE, 0), (x * TILE_SIZE, self.screen_height)
            )
        for y in range(self.tile_count_height + 1):
            pygame.draw.line(
                screen, grid_color, (0, y * TILE_SIZE), (self.screen_width, y * TILE_SIZE)
            )

        if self.hover_cell:
            gx, gy = self.hover_cell
            pygame.draw.rect(
                screen,
                (255, 255, 255),
                pygame.Rect(gx * TILE_SIZE, gy * TILE_SIZE, TILE_SIZE, TILE_SIZE),
                2,
            )

    def _draw_items(self, screen: Surface) -> None:
        for y in range(self.tile_count_height):
            for x in range(self.tile_count_width):
                tile_type = self._get_tyle_type_at(x, y)
                item_position = (x * TILE_SIZE, y * TILE_SIZE)
                if tile_type == TileType.FLOOR:
                    variant = self._pick_floor_variant(x, y)
                    screen.blit(self.assets.floorVariants[variant], item_position)
                elif tile_type == TileType.SNACK:
                    screen.blit(self.assets.entities[TileType.SNACK], item_position)
                elif tile_type == TileType.BOOKS:
                    screen.blit(self.assets.entities[TileType.BOOKS], item_position)
                elif tile_type == TileType.SPRAY:
                    screen.blit(self.assets.sprays[SprayType.OFF], item_position)
                elif tile_type == TileType.BUTTON:
                    screen.blit(self.assets.entities[TileType.BUTTON], item_position)

    def _draw_players(self, screen: Surface) -> None:
        for y in range(self.tile_count_height):
            for x in range(self.tile_count_width):
                tile_type = self._get_tyle_type_at(x, y)
                if tile_type == TileType.RED_PLAYER:
                    screen.blit(
                        self.assets.playerImages[TileType.RED_PLAYER],
                        (x * TILE_SIZE, y * TILE_SIZE),
                    )
                elif tile_type == TileType.BLUE_PLAYER:
                    screen.blit(
                        self.assets.playerImages[TileType.BLUE_PLAYER],
                        (x * TILE_SIZE, y * TILE_SIZE),
                    )

    def _draw_beds(self, screen: Surface) -> None:
        for y in range(self.tile_count_height):
            for x in range(self.tile_count_width):
                tile_type = self._get_tyle_type_at(x, y)
                if (
                    tile_type == TileType.RED_BED
                    and self._get_tyle_type_at(x + 1, y) == TileType.RED_BED
                ):
                    screen.blit(self.assets.beds[TileType.RED_BED], (x * TILE_SIZE, y * TILE_SIZE))
                elif (
                    tile_type == TileType.BLUE_BED
                    and self._get_tyle_type_at(x + 1, y) == TileType.BLUE_BED
                ):
                    screen.blit(self.assets.beds[TileType.BLUE_BED], (x * TILE_SIZE, y * TILE_SIZE))

    def _draw_palette(self, screen: Surface) -> None:
        pygame.draw.rect(screen, pygame.Color("black"), self.palette_rect)
        for item in self.items:
            image = item["asset"]
            rect = item["rect"]
            if image:
                screen.blit(image, rect.topleft)

            label = self.font_small.render(item["name"], True, pygame.Color("white"))
            screen.blit(label, (rect.x, rect.bottom + 4))

            if item["type"] == self.selected_item_type:
                pygame.draw.rect(screen, pygame.Color("yellow"), rect, 3)
            else:
                pygame.draw.rect(screen, pygame.Color("white"), rect, 3)

        self.level_name_box.draw(screen)
        self.save_button.draw(screen)

    def draw(self, screen: Surface) -> None:
        self._draw_items(screen)
        self._draw_grid(screen)
        self._draw_players(screen)
        self._draw_beds(screen)
        self._draw_palette(screen)
