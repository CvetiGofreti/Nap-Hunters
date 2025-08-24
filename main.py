"""Main entry point for the game."""

import pygame
from pygame.surface import Surface
from pygame.font import Font

from screens import MainMenu, LevelBuilder, LevelSelect, Leaderboard, GameScreen
from others import Assets


def main() -> None:
    """Initializes and runs the game loop."""
    pygame.init()
    screen_width: int = 960
    screen_height: int = 960
    screen: Surface = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Nap Hunters")
    clock = pygame.time.Clock()
    font_main: Font = pygame.font.Font(None, 48)
    font_small: Font = pygame.font.Font(None, 24)
    assets: Assets = Assets()

    actions: dict[str, callable] = {
        "mainMenu": lambda: MainMenu(font_main, font_small, assets),
        "levelBuilder": lambda: LevelBuilder(font_main, font_small, assets),
        "levelSelect": lambda: LevelSelect(font_main, font_small, assets),
        "leaderboard": lambda: Leaderboard(font_main, font_small, assets),
    }

    game_screen: GameScreen = GameScreen(font_main, font_small, assets)
    current_screen = actions["mainMenu"]()

    running: bool = True
    while running:
        delta_time: float = clock.tick(60) / 1000.0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                continue

            action = current_screen.handle_event(event)

            if action == "quit":
                running = False
            elif action in actions:
                current_screen = actions[action]()
            elif isinstance(action, tuple) and action[0] == "playLevel":
                game_screen.load_level(action[1])
                current_screen = game_screen

        current_screen.update(delta_time)
        screen.blit(assets.wall, (0, 0))
        current_screen.draw(screen)
        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
