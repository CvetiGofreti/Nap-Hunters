import os
import json

import pygame

import others
from others import Button, Assets
from screens.interface import BaseScreen

LEVEL_BUTTON_HEIGHT = 56
LEVEL_BUTTON_PADDING = 20
LEVEL_BUTTON_VERTICAL_PADDING = 10
LEVEL_LIST_START_POS = 100


class LevelSelect(BaseScreen):
    def __init__(
        self,
        font_main: pygame.font.Font,
        font_small: pygame.font.Font,
        assets: Assets,
    ) -> None:
        self.font_main: pygame.font.Font = font_main
        self.font_small: pygame.font.Font = font_small
        self.assets: Assets = assets
        self.level_buttons: list[Button] = []
        self.next_screen: str | tuple | None = None
        self._scan_levels()

    def _scan_levels(self) -> None:
        self.level_buttons.clear()
        os.makedirs("levels", exist_ok=True)
        file_paths = sorted(
            [file for file in os.listdir("levels") if file.endswith(".json")]
        )
        y = LEVEL_LIST_START_POS
        passed_levels = self._load_passed_levels()

        for file_path in file_paths:
            full_path = os.path.join("levels", file_path)
            name = file_path
            try:
                with open(full_path, "r", encoding="utf-8") as file:
                    data = json.load(file)
                    name = data.get("name", file_path)
            except (OSError, json.JSONDecodeError) as exception:
                print(f"Failed to load {full_path}: {exception}")
            rect = pygame.Rect(
                LEVEL_BUTTON_PADDING,
                y,
                pygame.display.get_surface().get_width()
                - 2 * LEVEL_BUTTON_PADDING,
                LEVEL_BUTTON_HEIGHT,
            )

            was_passed = name in passed_levels
            button = Button(
                pos = (rect.x, rect.y),
                size = (rect.width, rect.height),
                label = name,
                on_click = lambda path = full_path: self._set_next(path),
                font = self.font_small,
                show_check = was_passed,
                check_image = self.assets.passed_level_image
            )
            self.level_buttons.append(button)
            y += LEVEL_BUTTON_HEIGHT + LEVEL_BUTTON_VERTICAL_PADDING

    def _load_passed_levels(self) -> set[str]:
        team_name = others.global_values.current_team_name
        try:
            with open("history.json", "r", encoding="utf-8") as file:
                data = json.load(file)
                return set(
                    data.get("teams", {})
                    .get(team_name, {})
                    .get("completed_levels", {})
                    .keys()
                )
        except (OSError, json.JSONDecodeError) as exception:
            print(f"Could not read history.json: {exception}")
            return set()

    def _set_next(self, level_path: str) -> None:
        self.next_screen = ("playLevel", level_path)

    def handle_event(
        self, event: pygame.event.Event
    ) -> str | tuple | None:
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            return "mainMenu"

        self.next_screen = None
        for button in self.level_buttons:
            button.handle_event(event)
        return self.next_screen

    def update(self, _dt: float) -> None:
        pass

    def draw(self, screen: pygame.Surface) -> None:
        screen_width = screen.get_width()
        title = self.font_main.render("Select Level", True, pygame.Color("royalblue3"))
        screen.blit(
            title,
            (
                (screen_width - title.get_width()) // 2,
                LEVEL_LIST_START_POS - title.get_height() - 10,
            ),
        )

        for button in self.level_buttons:
            button.draw(screen)
