import json
import pygame

import others
from others import TileType, FloorType, ControlsType, LevelHistoryManager
from entities import Player, Snack, MovableBooks, Button, Spray

TILE_SIZE = 64
POPUP_WIDTH = 400
POPUP_HEIGHT = 200

class GameScreen:
    def __init__(self, font_main, font_small, assets):
        self.font_main = font_main
        self.font_small = font_small
        self.assets = assets
        self.grid = []
        self.level_name = "Level"
        self.players = []
        self.has_error = False
        self.screen_width, self.screen_height = pygame.display.get_surface().get_size()
        self.tile_count_width = self.screen_width // TILE_SIZE
        self.tile_count_height = self.screen_height // TILE_SIZE
        self.level_path = ""
        self.level_complete = False
        self.level_start_time = 0
        self.snacks: list[Snack] = []
        self.movable_books: list[MovableBooks] = []
        self.buttons: list[Button] = []
        self.sprays: list[Spray] = []

    def _get_tyle_type_at(self, x: int, y: int) -> TileType:
        if 0 <= y < self.tile_count_height and 0 <= x < self.tile_count_width:
            return self.grid[y][x]
        return TileType.INVALID

    def load_level(self, level_path: str) -> None:
        self.level_path = level_path
        self.movable_books.clear()
        try:
            with open(level_path, "r", encoding="utf-8") as level:
                data = json.load(level)
        except (OSError, json.JSONDecodeError) as exception:
            print(f"Failed to load level {level_path}: {exception}")
            self.has_error = True
            return

        self.level_name = data.get("name", "Level")
        grid = data.get("grid", [])
        self.grid = [[TileType(value) for value in row] for row in grid]
        self.players.clear()
        self.snacks.clear()
        self.buttons.clear()
        self.sprays.clear()

        for y in range(self.tile_count_height):
            for x in range(self.tile_count_width):
                tile_type = self._get_tyle_type_at(x, y)
                match tile_type:
                    case TileType.BLUE_PLAYER:
                        controls = {
                            ControlsType.LEFT: pygame.K_a,
                            ControlsType.RIGHT: pygame.K_d,
                            ControlsType.JUMP: pygame.K_w,
                        }

                        self.players.append(
                            Player(
                                self.assets.playerImages[tile_type],
                                (x, y),
                                controls,
                                TileType.BLUE_BED
                            )
                        )

                    case TileType.RED_PLAYER:
                        controls = {
                            ControlsType.LEFT: pygame.K_LEFT,
                            ControlsType.RIGHT: pygame.K_RIGHT,
                            ControlsType.JUMP: pygame.K_UP,
                        }
                        self.players.append(
                            Player(
                               self.assets.playerImages[tile_type],
                                (x, y),
                                controls,
                                TileType.RED_BED
                            )
                        )
                    case TileType.SNACK:
                        self.snacks.append(
                            Snack(
                                x,
                                y,
                                self.assets.entities[tile_type]
                            )
                        )
                    case TileType.BOOKS:
                        self.movable_books.append(
                            MovableBooks(
                                x,
                                y,
                                self.assets.entities[tile_type]
                            )
                        )
                    case TileType.BUTTON:
                        self.buttons.append(Button(x, y, self.assets))
                    case TileType.SPRAY:
                        height = 1
                        while (
                            y - height >= 0
                            and self._get_tyle_type_at(x, y - height)
                            in (TileType.EMPTY, TileType.SNACK)
                        ):
                            height += 1
                        self.sprays.append(Spray(x, y, height, self.assets))

        self._validate_loaded_level()
        self.level_start_time = pygame.time.get_ticks() / 1000

    def _pick_floor_variant(self, grid: list[list[TileType]], x: int, y: int) -> FloorType:
        grid_width = len(grid[0])
        left = x > 0 and self._get_tyle_type_at(x - 1, y) == TileType.FLOOR
        right = x < grid_width - 1 and self._get_tyle_type_at(x + 1, y) == TileType.FLOOR
        if left and right:
            return FloorType.MID
        if not left and right:
            return FloorType.LEFT
        if left and not right:
            return FloorType.RIGHT
        return FloorType.FLOOR_SINGLE

    def _validate_loaded_level(self) -> None:
        if self.tile_count_width != len(self.grid[0]) or self.tile_count_height != len(self.grid):
            self.has_error = True

    def handle_event(self, event: pygame.event.Event) -> str | None:
        if self.level_complete:
            if event.type in (pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN):
                self.level_complete = False
                return "levelSelect"
            return None

        if event.type == pygame.KEYDOWN and event.key in (pygame.K_ESCAPE, pygame.K_BACKSPACE):
            return "levelSelect"

        if not self.has_error:
            for player in self.players:
                player.handle_event(event)

        return None

    def _on_level_complete(self) -> None:
        if not self.level_complete:
            elapsed = pygame.time.get_ticks() / 1000 - self.level_start_time
            total_points = sum(player.points for player in self.players)

            history_manager = LevelHistoryManager()
            history_manager.record_attempt(
                others.global_values.current_team_name,
                self.level_name,
                elapsed,
                total_points
            )
            for player in self.players:
                player.on_level_complete()

        self.level_complete = True

    def update(self, dt: float) -> None:
        if self.has_error:
            return

        book_rects = [book.rect for book in self.movable_books]

        for book in self.movable_books:
            book.update(dt, self.grid, self.players)

        any_pressed = any(button.is_pressed(self.players) for button in self.buttons)
        for spray in self.sprays:
            spray.update(any_pressed, self.players)

        for player in self.players:
            player.update(dt, self.grid, book_rects)
            for snack in self.snacks[:]:
                if snack.is_colliding_with(player.rect):
                    player.points += 1
                    self.snacks.remove(snack)

        if all(player.is_near_bed(self.grid) for player in self.players):
            self._on_level_complete()

    def draw_completion_popup(self, screen: pygame.Surface) -> None:
        popup = pygame.Rect(
            (self.screen_width - POPUP_WIDTH) // 2,
            (self.screen_height - POPUP_HEIGHT) // 2,
            POPUP_WIDTH,
            POPUP_HEIGHT
        )
        pygame.draw.rect(screen, pygame.Color("black"), popup)
        pygame.draw.rect(screen, pygame.Color("white"), popup, 4)
        message = self.font_main.render("Level Complete!", True, pygame.Color("white"))
        screen.blit(message, (popup.centerx - message.get_width() // 2, popup.y + 30))
        hint = self.font_small.render("Press any key to continue...", True, pygame.Color("gray"))
        screen.blit(hint, (popup.centerx - hint.get_width() // 2, popup.bottom - 50))

    def draw(self, screen: pygame.Surface) -> None:
        if self.has_error:
            msg = self.font_main.render("Error in level data", True, pygame.Color("red"))
            screen.blit(msg, msg.get_rect(center=screen.get_rect().center))
            return

        for y, row in enumerate(self.grid):
            for x, tile_type in enumerate(row):
                match tile_type:
                    case TileType.FLOOR:
                        variant = self._pick_floor_variant(self.grid, x, y)
                        screen.blit(
                            self.assets.floorVariants[variant],
                            (x * TILE_SIZE, y * TILE_SIZE)
                        )
                    case TileType.RED_BED | TileType.BLUE_BED:
                        if self._get_tyle_type_at(x + 1, y) == tile_type:
                            screen.blit(self.assets.beds[tile_type], (x * TILE_SIZE, y * TILE_SIZE))

        for player in self.players:
            player.draw(screen, self.grid)

        for entity_list in [self.sprays, self.movable_books, self.snacks]:
            for entity in entity_list:
                entity.draw(screen)

        for button in self.buttons:
            button.draw(screen, self.players)

        if self.level_complete:
            self.draw_completion_popup(screen)
