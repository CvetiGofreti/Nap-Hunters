import pygame

import others
from others import Button
from others import TextInputBox
from screens.interface import BaseScreen

BUTTON_HEIGHT = 70
BUTTON_WIDTH = 260
BUTTON_SPACING = 20
INPUT_WIDTH = 260
INPUT_HEIGHT = 50


class MainMenu(BaseScreen):
    """Main menu screen of the game.

    Displays buttons for navigating to other parts of the game such as
    level selection, level builder, and leaderboard. Also includes a text
    input box for entering the team name.
    """

    def __init__(self, font_main, font_small, assets):
        self.font_main = font_main
        self.font_small = font_small
        screen_width, screen_height = pygame.display.get_surface().get_size()
        self.next_screen = None

        total_height = 3 * BUTTON_HEIGHT + 2 * BUTTON_SPACING
        start_x = (screen_width - BUTTON_WIDTH) // 2
        start_y = (screen_height - total_height) // 2

        buttons_info = [
            ("Play", "levelSelect"),
            ("Build Level", "levelBuilder"),
            ("Leaderboard", "leaderboard")
        ]

        self.buttons = [
            Button(
                pos = (start_x, start_y + index * (BUTTON_HEIGHT + BUTTON_SPACING)),
                size = (BUTTON_WIDTH, BUTTON_HEIGHT),
                label = label,
                onClick = lambda name=screen: self._set_next(name),
                font = font_main
            )
            for index, (label, screen) in enumerate(buttons_info)
        ]

        input_x = screen_width // 2 - INPUT_WIDTH // 2
        self.team_name_box = TextInputBox(
            input_x, 20, INPUT_WIDTH, INPUT_HEIGHT, font_small, "Enter team name"
            )

        self.team_name_box.label = others.global_values.current_team_name

    def _set_next(self, screen_name):
        self.next_screen = screen_name

    def handle_event(self, event):
        self.team_name_box.handle_event(event)
        self.next_screen = None

        for button in self.buttons:
            button.handle_event(event)

        return self.next_screen

    def update(self, dt):
        self.team_name_box.update(dt)
        others.global_values.current_team_name = self.team_name_box.label.strip()

    def draw(self, screen):
        self.team_name_box.draw(screen)

        for button in self.buttons:
            button.draw(screen)
