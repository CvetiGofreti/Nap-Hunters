import pygame
from screens.main_menu import MainMenu
from screens.level_builder import LevelBuilder
from screens.level_selector import LevelSelect
from screens.leaderboard import Leaderboard
from screens.gameplay import GameScreen
from others.graphics_loader import Assets

def main():
    pygame.init()
    screenWidth = 960
    screenHeight = 960
    screen = pygame.display.set_mode((screenWidth, screenHeight))
    pygame.display.set_caption("Nap Hunters")
    clock = pygame.time.Clock()
    fontMain = pygame.font.Font(None, 48)
    fontSmall = pygame.font.Font(None, 24)
    assets = Assets()

    actions = {
        "mainMenu": lambda: MainMenu(fontMain, fontSmall, assets),
        "levelBuilder": lambda: LevelBuilder(fontMain, fontSmall, assets),
        "levelSelect": lambda: LevelSelect(fontMain, fontSmall, assets),
        "leaderboard": lambda: Leaderboard(fontMain, fontSmall, assets),
    }

    gameScreen = GameScreen(fontMain, fontSmall, assets)
    currentScreen = actions["mainMenu"]()

    running = True
    while running:
        deltaTime = clock.tick(60) / 1000.0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                continue

            action = currentScreen.handle_event(event)

            if action == "quit":
                running = False
            elif action in actions:
                currentScreen = actions[action]()
            elif isinstance(action, tuple) and action[0] == "playLevel":
                gameScreen.load_level(action[1])
                currentScreen = gameScreen

        currentScreen.update(deltaTime)
        screen.blit(assets.wall, (0, 0))
        currentScreen.draw(screen)
        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()