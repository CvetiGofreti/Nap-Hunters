"""Main entry point the game."""

import pygame

from screens.main_menu import MainMenu
from screens.level_builder import LevelBuilder
from screens.level_selector import LevelSelect
from screens.leaderboard import Leaderboard
from screens.gameplay import GameScreen
from others.graphics_loader import Assets

def main():
    """Initializes and runs the game loop."""
    pygame.init()
    screen_width = 960
    screen_height = 960
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Nap Hunters")
    clock = pygame.time.Clock()
    font_main = pygame.font.Font(None, 48)
    font_small = pygame.font.Font(None, 24)
    assets = Assets()

    actions = {
        "mainMenu": lambda: MainMenu(font_main, font_small, assets),
        "levelBuilder": lambda: LevelBuilder(font_main, font_small, assets),
        "levelSelect": lambda: LevelSelect(font_main, font_small, assets),
        "leaderboard": lambda: Leaderboard(font_main, font_small, assets),
    }

    game_screen = GameScreen(font_main, font_small, assets)
    current_screen = actions["mainMenu"]()

    running = True
    while running:
        delta_time = clock.tick(60) / 1000.0

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
